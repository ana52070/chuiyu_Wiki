#!/usr/bin/env node
/**
 * 校验 Markdown frontmatter，防止「能提交、构建时才炸」的问题。
 *
 * 起因：guide/claude-code/daily/2026-04-08.md 的 title 写成未加引号的
 * `2026-04-08`，YAML 把它解析成 Date 对象而不是字符串，主题里
 * `post.title.includes(...)` 直接抛 TypeError，VitePress 渲染阶段失败。
 * 这类错误 build 不会以非零码退出，只在渲染日志里，容易被别的部署报错
 * 盖过去，所以单独做一次静态检查。
 *
 * 分两档：
 *   error   —— 会让渲染真的出错，退出码 1，CI 直接红
 *   warn    —— 内容规范问题（缺 frontmatter、空列表项），只提示不拦
 *
 * 用法：
 *   node scripts/check-frontmatter.mjs              # 检查全部
 *   node scripts/check-frontmatter.mjs a.md b.md    # 只检查指定文件
 */
import { readFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import matter from "gray-matter";

// 这些字段在主题 / VitePress 里会被当字符串用（.includes / .length / 拼接）。
// YAML 会把 2026-04-08、true、123 解析成 Date / boolean / number，必须引号包起来。
const STRING_FIELDS = ["title", "description", "author", "permalink", "layout"];
// 列表字段会被主题直接 renderList 后做字符串处理。
const LIST_FIELDS = ["tags", "categories"];
// 首页（layout: home）这类纯布局页没有文章标题，不要求 title。
const TITLE_EXEMPT_LAYOUTS = new Set(["home", "page", "false"]);

function trackedMarkdown() {
  const out = execFileSync("git", ["ls-files", "-z", "*.md"], {
    maxBuffer: 1 << 28,
  });
  return out.toString("utf8").split("\0").filter(Boolean);
}

/** 返回 { errors: string[], warnings: string[] } */
function check(file) {
  const errors = [];
  const warnings = [];
  const raw = readFileSync(file, "utf8").replace(/^﻿/, "");

  if (!raw.startsWith("---")) {
    warnings.push("没有 frontmatter（文件开头不是 ---），页面会缺少标题等信息");
    return { errors, warnings };
  }

  let parsed;
  try {
    parsed = matter(raw);
  } catch (err) {
    errors.push(`YAML 解析失败：${err.message}`);
    return { errors, warnings };
  }

  const data = parsed.data ?? {};

  const layout = typeof data.layout === "string" ? data.layout : "";
  const titleExempt = TITLE_EXEMPT_LAYOUTS.has(layout) || data.home === true;

  if (
    !titleExempt &&
    (data.title === undefined || data.title === null || data.title === "")
  ) {
    warnings.push("没有 title");
  }

  for (const field of STRING_FIELDS) {
    const value = data[field];
    if (value === undefined || value === null) continue;
    if (typeof value !== "string") {
      const kind = value instanceof Date ? "Date 对象" : typeof value;
      // 报错里回显源码里的原始写法，比 Date 的 toString 好认。
      const literal = raw.match(new RegExp(`^${field}:[ \\t]*(.*)$`, "m"))?.[1];
      const hint = literal ? `${field}: "${literal.trim()}"` : `${field}: "..."`;
      errors.push(
        `${field} 被解析成 ${kind}（值：${JSON.stringify(value)}），` +
          `主题会当字符串用，请加引号写成 ${hint}`
      );
    }
  }

  for (const field of LIST_FIELDS) {
    const value = data[field];
    if (value === undefined || value === null) continue;
    if (!Array.isArray(value)) {
      errors.push(`${field} 应为数组，当前是 ${typeof value}`);
      continue;
    }
    value.forEach((item, i) => {
      if (typeof item !== "string" || item.trim() === "") {
        warnings.push(
          `${field}[${i}] 是空项（${JSON.stringify(item)}），` +
            `会在页面上渲染成空标签，建议删掉这一行`
        );
      }
    });
  }

  return { errors, warnings };
}

const files = process.argv.slice(2).length
  ? process.argv.slice(2)
  : trackedMarkdown();

let failed = 0;
let warned = 0;

for (const file of files) {
  let result;
  try {
    result = check(file);
  } catch (err) {
    result = { errors: [`读取失败：${err.message}`], warnings: [] };
  }
  if (result.errors.length) {
    failed++;
    console.error(`\n✗ ${file}`);
    for (const e of result.errors) console.error(`    [error] ${e}`);
  }
  if (result.warnings.length) {
    warned++;
    console.log(`\n! ${file}`);
    for (const w of result.warnings) console.log(`    [warn]  ${w}`);
  }
}

if (failed) {
  console.error(
    `\n${failed}/${files.length} 个文件有 error，构建会失败，请修复后重试。`
  );
  process.exit(1);
}

console.log(
  `\n✓ frontmatter 检查通过（${files.length} 个文件` +
    (warned ? `，其中 ${warned} 个有 warning）` : "）")
);
