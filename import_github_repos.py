import base64
import datetime as dt
import os
import posixpath
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import requests
from requests.exceptions import RequestException


GITHUB_USER = "ana52070"
TARGET_DIR = Path("projects")
DEFAULT_CATEGORY = "软件项目"
DEFAULT_TAG = "GitHub"
ENV_FILE = Path(".env")
DEFAULT_PROXY_URL = "http://127.0.0.1:7897"
FORCE_PROXY_7897 = True
HTTP_TIMEOUT = 20
MAX_RETRIES = 4

GITHUB_REPO_PATTERN = re.compile(
    r"github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git)?(?:[/?#)\]\s]|$)",
    re.IGNORECASE,
)
MD_LINK_PATTERN = re.compile(r"(!?\[[^\]]*\])\(([^)]+)\)")
HTML_SRC_HREF_PATTERN = re.compile(r"(src|href)=([\"'])(.+?)\2", re.IGNORECASE)


def load_env_from_file(env_path: Path) -> None:
    """轻量加载 .env（不依赖 python-dotenv）。"""
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def build_headers() -> Dict[str, str]:
    token = os.getenv("GITHUB_TOKEN", "").strip()
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "wiki-github-importer",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def build_proxies() -> Dict[str, str]:
    # 按需求固定走 Clash 7897 代理
    if FORCE_PROXY_7897:
        return {"http": DEFAULT_PROXY_URL, "https": DEFAULT_PROXY_URL}

    # 非固定模式下：优先使用环境变量代理；否则默认走 Clash 7897
    env_http = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
    env_https = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")
    proxy = (env_https or env_http or DEFAULT_PROXY_URL).strip()
    return {"http": proxy, "https": proxy}


def request_get(url: str, headers: Dict[str, str], params: Optional[dict] = None) -> requests.Response:
    proxies = build_proxies()
    last_exc: Optional[Exception] = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return requests.get(
                url,
                headers=headers,
                params=params,
                timeout=HTTP_TIMEOUT,
                proxies=proxies,
            )
        except RequestException as exc:
            last_exc = exc
            if attempt < MAX_RETRIES:
                wait_s = attempt * 1.2
                print(f"网络波动，重试 {attempt}/{MAX_RETRIES - 1}：{url}")
                time.sleep(wait_s)

    raise RuntimeError(f"网络请求失败：{url} -> {last_exc}")


def github_get_json(url: str, headers: Dict[str, str], params: Optional[dict] = None) -> dict:
    resp = request_get(url, headers=headers, params=params)
    if resp.status_code != 200:
        raise RuntimeError(f"GitHub API 请求失败: {resp.status_code} {resp.text}")
    return resp.json()


def fetch_owned_repos(username: str, headers: Dict[str, str]) -> List[dict]:
    repos: List[dict] = []
    page = 1

    while True:
        url = f"https://api.github.com/users/{username}/repos"
        params = {
            "type": "owner",
            "sort": "updated",
            "per_page": 100,
            "page": page,
        }
        batch = github_get_json(url, headers, params=params)

        if not batch:
            break

        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    return [r for r in repos if not r.get("fork", False)]


def extract_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    if end == -1:
        return ""
    return text[3:end]


def parse_repo_field(frontmatter: str) -> str:
    for line in frontmatter.splitlines():
        m = re.match(r"^\s*repo\s*:\s*(.+?)\s*$", line)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    return ""


def parse_title_field(frontmatter: str) -> str:
    for line in frontmatter.splitlines():
        m = re.match(r"^\s*title\s*:\s*(.+?)\s*$", line)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    return ""


def normalize_name(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def extract_repo_refs_from_text(content: str, username: str) -> Set[str]:
    refs: Set[str] = set()
    for owner, repo in GITHUB_REPO_PATTERN.findall(content):
        if owner.lower() == username.lower():
            refs.add(f"{owner}/{repo}".lower())
    return refs


def scan_existing_signals(base_dir: Path, username: str) -> Tuple[Set[str], Set[str], Set[str]]:
    existing_repo_full_names: Set[str] = set()
    existing_title_keys: Set[str] = set()
    existing_file_keys: Set[str] = set()
    if not base_dir.exists():
        return existing_repo_full_names, existing_title_keys, existing_file_keys

    for md in base_dir.rglob("*.md"):
        existing_file_keys.add(normalize_name(md.stem))
        try:
            content = md.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        fm = extract_frontmatter(content)
        if fm:
            repo = parse_repo_field(fm)
            if repo:
                existing_repo_full_names.add(repo.lower())

            title = parse_title_field(fm)
            if title:
                existing_title_keys.add(normalize_name(title))

        existing_repo_full_names.update(extract_repo_refs_from_text(content, username))

    return existing_repo_full_names, existing_title_keys, existing_file_keys


def safe_filename(name: str) -> str:
    name = re.sub(r"[<>:\"/\\|?*]", "-", name).strip()
    name = re.sub(r"\s+", " ", name)
    return name or "repo"


def slugify(text: str) -> str:
    slug = text.lower().strip()
    slug = re.sub(r"[^a-z0-9\-]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "repo"


def now_str() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def to_text(value) -> str:
    if value is None:
        return ""
    return str(value).replace("\n", " ").strip()


def yaml_quote(value: str) -> str:
    escaped = value.replace("'", "''")
    return f"'{escaped}'"


def parse_selection(text: str, max_index: int) -> List[int]:
    raw = text.strip().lower()
    if raw in {"all", "a"}:
        return list(range(1, max_index + 1))

    indices: Set[int] = set()
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    if not parts:
        raise ValueError("输入为空")

    for part in parts:
        if "-" in part:
            s, e = part.split("-", 1)
            start = int(s)
            end = int(e)
            if start > end:
                start, end = end, start
            for i in range(start, end + 1):
                if 1 <= i <= max_index:
                    indices.add(i)
        else:
            i = int(part)
            if 1 <= i <= max_index:
                indices.add(i)

    if not indices:
        raise ValueError("没有有效序号")

    return sorted(indices)


def choose_repos(repos: List[dict]) -> List[dict]:
    if not repos:
        return []

    print("\n可导入的新仓库：")
    for idx, repo in enumerate(repos, start=1):
        name = to_text(repo.get("name"))
        lang = to_text(repo.get("language")) or "未知"
        stars = int(repo.get("stargazers_count") or 0)
        desc = to_text(repo.get("description")) or "暂无描述"
        if len(desc) > 60:
            desc = desc[:57] + "..."
        print(f"{idx:>3}. {name}  [★{stars}] [{lang}]  {desc}")

    print("\n输入说明：")
    print("- 单选：3")
    print("- 多选：1,3,5")
    print("- 区间：2-6")
    print("- 全选：all")
    print("- 退出：q")

    while True:
        user_input = input("\n请输入要导入的序号: ").strip()
        if user_input.lower() in {"q", "quit", "exit"}:
            return []
        try:
            selected = parse_selection(user_input, len(repos))
            return [repos[i - 1] for i in selected]
        except Exception as exc:
            print(f"输入无效：{exc}，请重试。")


def fetch_readme(owner: str, repo_name: str, headers: Dict[str, str]) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """返回 (readme_content, readme_path, branch)。"""
    url = f"https://api.github.com/repos/{owner}/{repo_name}/readme"
    resp = request_get(url, headers=headers)

    if resp.status_code == 404:
        return None, None, None
    if resp.status_code != 200:
        raise RuntimeError(f"获取 README 失败: {resp.status_code} {resp.text}")

    data = resp.json()
    encoded = data.get("content", "")
    readme_path = data.get("path", "README.md")

    if not encoded:
        return None, readme_path, None

    readme_text = base64.b64decode(encoded).decode("utf-8", errors="replace")

    # 从 download_url 推断分支，取不到就用 default_branch 再兜底
    download_url = to_text(data.get("download_url"))
    branch = None
    marker = f"https://raw.githubusercontent.com/{owner}/{repo_name}/"
    if download_url.startswith(marker):
        rest = download_url[len(marker):]
        parts = rest.split("/", 1)
        if parts and parts[0]:
            branch = parts[0]

    return readme_text, readme_path, branch


def fetch_repo_detail(owner: str, repo_name: str, headers: Dict[str, str]) -> dict:
    url = f"https://api.github.com/repos/{owner}/{repo_name}"
    return github_get_json(url, headers)


def fetch_latest_commit_message(owner: str, repo_name: str, headers: Dict[str, str]) -> str:
    url = f"https://api.github.com/repos/{owner}/{repo_name}/commits"
    try:
        data = github_get_json(url, headers, params={"per_page": 1})
    except Exception:
        return ""
    if not data:
        return ""
    commit = data[0].get("commit", {})
    return to_text(commit.get("message"))


def split_link_target(target: str) -> Tuple[str, str, str]:
    base = target
    fragment = ""
    query = ""

    if "#" in base:
        base, fragment = base.split("#", 1)
        fragment = f"#{fragment}"
    if "?" in base:
        base, query = base.split("?", 1)
        query = f"?{query}"

    return base, query, fragment


def should_skip_link(link: str) -> bool:
    lower = link.lower().strip()
    return (
        not lower
        or lower.startswith("http://")
        or lower.startswith("https://")
        or lower.startswith("mailto:")
        or lower.startswith("#")
        or lower.startswith("data:")
        or lower.startswith("javascript:")
    )


def resolve_repo_path(link: str, readme_path: str) -> str:
    link_base, query, fragment = split_link_target(link)

    readme_dir = posixpath.dirname(readme_path or "README.md")
    if link_base.startswith("/"):
        raw_path = link_base.lstrip("/")
    else:
        raw_path = posixpath.normpath(posixpath.join(readme_dir, link_base))

    while raw_path.startswith("../"):
        raw_path = raw_path[3:]
    if raw_path == ".":
        raw_path = ""

    return raw_path + query + fragment


def convert_relative_links(markdown: str, owner: str, repo_name: str, branch: str, readme_path: str) -> str:
    raw_prefix = f"https://raw.githubusercontent.com/{owner}/{repo_name}/{branch}/"
    blob_prefix = f"https://github.com/{owner}/{repo_name}/blob/{branch}/"

    def replace_md(match: re.Match) -> str:
        whole = match.group(0)
        label = match.group(1)
        target = match.group(2).strip()

        if should_skip_link(target):
            return whole

        resolved = resolve_repo_path(target, readme_path)
        is_image = label.startswith("!")
        if is_image:
            return f"{label}({raw_prefix}{resolved})"
        return f"{label}({blob_prefix}{resolved})"

    converted = MD_LINK_PATTERN.sub(replace_md, markdown)

    def replace_html_attr(match: re.Match) -> str:
        attr = match.group(1)
        quote = match.group(2)
        target = match.group(3).strip()

        if should_skip_link(target):
            return match.group(0)

        resolved = resolve_repo_path(target, readme_path)
        attr_lower = attr.lower()
        if attr_lower == "src":
            new_target = f"{raw_prefix}{resolved}"
        else:
            new_target = f"{blob_prefix}{resolved}"

        return f"{attr}={quote}{new_target}{quote}"

    return HTML_SRC_HREF_PATTERN.sub(replace_html_attr, converted)


def render_frontmatter(repo: dict, detail: dict) -> str:
    name = to_text(repo.get("name"))
    full_name = to_text(repo.get("full_name"))
    description = to_text(repo.get("description")) or "暂无描述"
    homepage = to_text(repo.get("homepage"))
    stars = int(repo.get("stargazers_count") or 0)
    language = to_text(repo.get("language")) or "未知"
    permalink = f"/projects/{slugify(name)}"

    license_name = ""
    license_obj = detail.get("license") or {}
    if isinstance(license_obj, dict):
        license_name = to_text(license_obj.get("spdx_id") or license_obj.get("name"))

    topics = detail.get("topics") or []
    if not isinstance(topics, list):
        topics = []

    created_at = to_text(repo.get("created_at"))
    updated_at = to_text(repo.get("updated_at"))

    lines = [
        "---",
        f"title: {yaml_quote(name)}",
        f"date: {yaml_quote(now_str())}",
        "categories:",
        f"  - {yaml_quote(DEFAULT_CATEGORY)}",
        "tags:",
        f"  - {yaml_quote(DEFAULT_TAG)}",
        f"permalink: {yaml_quote(permalink)}",
        f"repo: {yaml_quote(full_name)}",
        f"description: {yaml_quote(description)}",
        f"homepage: {yaml_quote(homepage)}",
        f"stars: {stars}",
        f"language: {yaml_quote(language)}",
        f"license: {yaml_quote(license_name)}",
        f"created_at: {yaml_quote(created_at)}",
        f"updated_at: {yaml_quote(updated_at)}",
        "topics:",
    ]

    if topics:
        for t in topics:
            lines.append(f"  - {yaml_quote(to_text(t))}")
    else:
        lines.append("  - '暂无'")

    lines.append("---")
    return "\n".join(lines)


def render_fallback_body(repo: dict, detail: dict, latest_commit: str) -> str:
    name = to_text(repo.get("name"))
    html_url = to_text(repo.get("html_url"))
    homepage = to_text(repo.get("homepage"))
    description = to_text(repo.get("description")) or "暂无描述"
    stars = int(repo.get("stargazers_count") or 0)
    language = to_text(repo.get("language")) or "未知"

    topics = detail.get("topics") or []
    topic_text = "、".join([to_text(t) for t in topics if to_text(t)]) or "暂无"

    lines = [
        f"# {name}",
        "",
        f"- 仓库：[{html_url}]({html_url})",
        f"- Star：{stars}",
        f"- 主语言：{language}",
    ]

    if homepage:
        lines.append(f"- 首页：[{homepage}]({homepage})")

    lines.extend(
        [
            f"- Topics：{topic_text}",
            "",
            "## 项目简介",
            description,
            "",
            "## 最近提交",
            latest_commit or "暂无提交信息",
            "",
            "## 备注",
            "- 未检测到 README，当前页面由仓库元数据自动生成。",
        ]
    )

    return "\n".join(lines) + "\n"


def render_readme_body(
    repo: dict, owner: str, readme_md: str, branch: str, readme_path: str
) -> str:
    name = to_text(repo.get("name"))
    html_url = to_text(repo.get("html_url"))
    stars = int(repo.get("stargazers_count") or 0)
    language = to_text(repo.get("language")) or "未知"

    converted = convert_relative_links(
        markdown=readme_md,
        owner=owner,
        repo_name=name,
        branch=branch,
        readme_path=readme_path,
    )

    lines = [
        f"# {name}",
        "",
        f"- 仓库：[{html_url}]({html_url})",
        f"- Star：{stars}",
        f"- 主语言：{language}",
        f"- README 来源：`{readme_path}` (分支：`{branch}`)",
        "",
        "---",
        "",
        converted.strip(),
        "",
    ]
    return "\n".join(lines)


def build_page_content(repo: dict, headers: Dict[str, str]) -> str:
    owner = to_text(repo.get("owner", {}).get("login")) or GITHUB_USER
    repo_name = to_text(repo.get("name"))
    default_branch = to_text(repo.get("default_branch")) or "main"

    detail = fetch_repo_detail(owner, repo_name, headers)
    frontmatter = render_frontmatter(repo, detail)

    readme_md, readme_path, branch_from_readme = fetch_readme(owner, repo_name, headers)
    if readme_md:
        branch = branch_from_readme or default_branch
        body = render_readme_body(
            repo, owner, readme_md, branch, readme_path or "README.md"
        )
    else:
        latest_commit = fetch_latest_commit_message(owner, repo_name, headers)
        body = render_fallback_body(repo, detail, latest_commit)

    return frontmatter + "\n\n" + body


def write_repo_page(target_dir: Path, repo: dict, headers: Dict[str, str]) -> Tuple[str, Optional[Path]]:
    target_dir.mkdir(parents=True, exist_ok=True)
    filename = safe_filename(to_text(repo.get("name"))) + ".md"
    file_path = target_dir / filename

    if file_path.exists():
        return "skip", file_path

    content = build_page_content(repo, headers)
    file_path.write_text(content, encoding="utf-8")
    return "written", file_path


def main() -> int:
    load_env_from_file(ENV_FILE)
    headers = build_headers()
    proxies = build_proxies()

    print(f"当前代理：{proxies.get('https', '')}")
    print(f"正在拉取 GitHub 用户 {GITHUB_USER} 的个人仓库列表...")
    try:
        all_repos = fetch_owned_repos(GITHUB_USER, headers)
    except Exception as exc:
        print(f"错误：{exc}")
        print("请检查网络，或在 .env 中配置 GITHUB_TOKEN 后重试。")
        return 1

    if not all_repos:
        print("未获取到仓库。")
        return 0

    existing_repo_set, existing_title_keys, existing_file_keys = scan_existing_signals(
        TARGET_DIR, GITHUB_USER
    )

    new_repos: List[dict] = []
    existed_count = 0
    for repo in all_repos:
        full_name = to_text(repo.get("full_name")).lower()
        repo_name_key = normalize_name(to_text(repo.get("name")))
        is_existing = (
            (full_name and full_name in existing_repo_set)
            or (repo_name_key and repo_name_key in existing_title_keys)
            or (repo_name_key and repo_name_key in existing_file_keys)
        )

        if is_existing:
            existed_count += 1
        else:
            new_repos.append(repo)

    print(f"总仓库数：{len(all_repos)}")
    print(f"已存在（多信号判重）：{existed_count}")
    print(f"可导入的新仓库：{len(new_repos)}")

    if not new_repos:
        print("没有可导入的新仓库。")
        return 0

    selected_repos = choose_repos(new_repos)
    if not selected_repos:
        print("未选择任何仓库，已退出。")
        return 0

    print("\n开始写入 Markdown 文件...")
    written: List[Tuple[str, Path]] = []
    skipped: List[Tuple[str, Path]] = []

    for repo in selected_repos:
        repo_full = to_text(repo.get("full_name"))
        try:
            status, path = write_repo_page(TARGET_DIR, repo, headers)
        except Exception as exc:
            print(f"- 导入失败：{repo_full} -> {exc}")
            continue

        if status == "skip" and path is not None:
            skipped.append((repo_full, path))
            print(f"- 跳过已存在文件：{repo_full} -> {path}")
        elif status == "written" and path is not None:
            written.append((repo_full, path))
            print(f"- 已导入：{repo_full} -> {path}")

    print(f"\n导入完成，新增 {len(written)} 个，跳过 {len(skipped)} 个。")
    print("按你的要求：未自动触发索引更新。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
