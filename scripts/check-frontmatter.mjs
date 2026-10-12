#!/usr/bin/env node
/**
 * 校验 Markdown frontmatter，防止「能提交、构建时才炸」的问题。
 *
 * 起因：guide/claude-code/daily/2026-04-08.md 的 title 写成未加引号的
 * `2026-04-08`，YAML 把它解析成 Date 对象而不是字符串，主题里
 * `post.title.includes(...)` 直接抛 TypeError，VitePress 渲染阶段失败。
 * 这类错误 build 能过「解析」但在渲染时才炸，且容易被别的部署报错盖过去，
 * 所以单独做一次静态检查，几秒内给出精确到行的报错。
 *
 * 用法：
 *   node scripts/check-frontmatter.mjs          # 检查全部
 *   node scripts/check-frontmatter.mjs a.md b.md  # 只检查指定文件
 */
import { readFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import matter from "gray-matter";

// 这些字段在主题 / VitePress 里会被当字符串用（.includes / .length / 拼接）。
// YAML 会把 2026-04-08、true、123 解析成 Date / boolean / number，必须引号包起来。
const STRING_FIELDS = ["title", "description", "author", "permalink", "layout"];
// 首页（layout: home）这类纯布局页没有文章标题，不强制要求 title。
const TITLE_EXEMPT_LAYOUTS = new Set(["home", "page", "false"]);

function trackedMarkdown() {
  const out = execFileSync("git", ["ls-files", "-z", "*.md"], {
    maxBuffer: 1 << 28,
  });
  return out.toString("utf8").split("\0").filter(Boolean);
}

function check(file) {
  const errors = [];
  const raw = readFileSync(file, "utf8");

  if (!raw.startsWith("---")) {
    errors.push("缺少 frontmatter（文件开头应为 ---）");
    return errors;
  }

  let parsed;
  try {
    parsed = matter(raw);
  } catch (err) {
    errors.push(`YAML 解析失败：${err.message}`);
    return errors;
  }

  const data = parsed.data ?? {};

  const layout = typeof data.layout === "string" ? data.layout : "";
  const titleExempt = TITLE_EXEMPT_LAYOUTS.has(layout) || data.home === true;

  if (
    !titleExempt &&
    (data.title === undefined || data.title === null || data.title === "")
  ) {
    errors.push("缺少必填字段 title（纯布局页请设置 layout: home / page）");
  }

  for (const field of STRING_FIELDS) {
    const value = data[field];
    if (value === undefined || value === null) continue;
    if (typeof value !== "string") {
      const kind = value instanceof Date ? "Date 对象" : typeof value;
      // 报错里回显源码里的原始写法，比 Date 的 toString 好认。
      const literal = raw.match(
        new RegExp(`^${field}:[ \\t]*(.*)$`, "m")
      )?.[1];
      const hint = literal
        ? `${field}: "${literal.trim()}"`
        : `${field}: "..."`;
      errors.push(
        `${field} 被解析成 ${kind}（值：${JSON.stringify(value)}），` +
          `请加引号写成 ${hint}`
      );
    }
  }

  // tags 写成 null / 字符串都容易在主题里出问题，统一成数组。
  if (data.tags !== undefined && !Array.isArray(data.tags)) {
    errors.push(`tags 应为数组，当前是 ${typeof data.tags}`);
  }

  return errors;
}

const files = process.argv.slice(2).length
  ? process.argv.slice(2)
  : trackedMarkdown();

let failed = 0;
for (const file of files) {
  let errors;
  try {
    errors = check(file);
  } catch (err) {
    errors = [`读取失败：${err.message}`];
  }
  if (errors.length) {
    failed++;
    console.error(`\n✗ ${file}`);
    for (const e of errors) console.error(`    ${e}`);
  }
}

if (failed) {
  console.error(`\n共 ${failed}/${files.length} 个文件有问题。`);
  process.exit(1);
}
console.log(`✓ frontmatter 检查通过（${files.length} 个文件）`);
