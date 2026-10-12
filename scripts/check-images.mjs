#!/usr/bin/env node
/**
 * 检查 Markdown 里的本地图片引用是否都能找到文件。
 *
 * 起因：blog/yolo/RK3588从数据集到训练到部署YoloV8.md 里有一行
 *   ![![](./assets/Pasted image ...png)(https://i-blog.csdnimg.cn/...)
 * 括号错位，VitePress 把它渲染成一串纯文本，图片直接不显示，
 * 但构建既不报错也不警告——只能靠人肉发现。
 *
 * 用法：
 *   node scripts/check-images.mjs
 */
import { readFileSync, existsSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { dirname, join, normalize, resolve } from "node:path";

const ROOT = process.cwd();

function trackedMarkdown() {
  const out = execFileSync("git", ["ls-files", "-z", "*.md"], {
    maxBuffer: 1 << 28,
  });
  return out.toString("utf8").split("\0").filter(Boolean);
}

const IMAGE_RE = /!\[[^\]]*\]\(([^)]+)\)/g;
const REMOTE = /^(https?:)?\/\/|^data:|^#/;

const problems = [];
let checked = 0;

for (const file of trackedMarkdown()) {
  const text = readFileSync(file, "utf8");
  const lines = text.split(/\r?\n/);

  lines.forEach((line, i) => {
    for (const m of line.matchAll(IMAGE_RE)) {
      let ref = m[1].trim();
      if (ref.startsWith("<") && ref.endsWith(">")) ref = ref.slice(1, -1);
      ref = ref.replace(/\s+["'].*$/, "").trim();
      if (!ref || REMOTE.test(ref)) continue;

      checked++;
      const target = ref.startsWith("/")
        ? join(ROOT, decodeURIComponent(ref.replace(/^\//, "")))
        : resolve(ROOT, dirname(file), decodeURIComponent(ref));

      if (!existsSync(normalize(target))) {
        problems.push({
          file,
          line: i + 1,
          ref,
          why: "找不到文件",
        });
      }
    }
  });
}

for (const p of problems) {
  console.error(`\n✗ ${p.file}:${p.line}\n    ${p.why}：${p.ref}`);
}

if (problems.length) {
  console.error(`\n共 ${problems.length} 处问题（已检查 ${checked} 个本地图片引用）。`);
  process.exit(1);
}
console.log(`✓ 图片引用检查通过（${checked} 个本地引用）`);
