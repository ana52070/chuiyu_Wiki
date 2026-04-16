import path from 'path'
import { writeFileSync } from 'fs'
import { Feed } from 'feed'
import { createContentLoader, type SiteConfig } from 'vitepress'

const baseUrl = 'https://chuiyu.wiki'

export async function generateRSS(config: SiteConfig) {
  const feed = new Feed({
    title: 'Chuiyu Wiki',
    description: '要努力去发光,而不是被照亮',
    id: `${baseUrl}/`,
    link: `${baseUrl}/`,
    language: 'zh-CN',
    image: `${baseUrl}/logo.jpg`,
    favicon: `${baseUrl}/logo.jpg`,
    copyright: `Copyright © ${new Date().getFullYear()} Chuiyu`,
    feedLinks: {
      rss2: `${baseUrl}/rss.xml`,
    },
  })

  // 加载所有文档（博客、学习笔记、项目记录）
  const posts = await createContentLoader(
    ['blog/**/*.md', 'guide/**/*.md', 'projects/**/*.md'],
    { excerpt: true }
  ).load()

  posts
    .filter(p => p.frontmatter.title && p.frontmatter.date)
    .sort((a, b) => +new Date(b.frontmatter.date) - +new Date(a.frontmatter.date))
    .slice(0, 30)  // 最多保留最新 30 篇
    .forEach(post => {
      // 优先用 frontmatter.description，其次用 excerpt（<!-- more --> 前的内容）
      // 所有字段必须是字符串，防止 xml-js 序列化报错
      const rawExcerpt = typeof post.excerpt === 'string'
        ? post.excerpt.replace(/<[^>]*>/g, '').trim()
        : ''
      const summary = String(post.frontmatter.description || rawExcerpt || '')

      const url = `${baseUrl}${post.url}`
      const title = String(post.frontmatter.title || 'Untitled')
      const author = String(post.frontmatter.author || 'Chuiyu')
      const tags: string[] = Array.isArray(post.frontmatter.tags)
        ? post.frontmatter.tags.filter((t: unknown) => typeof t === 'string')
        : []

      feed.addItem({
        title,
        id: url,
        link: url,
        description: summary,
        content: summary,
        author: [{ name: author }],
        date: new Date(post.frontmatter.date),
        category: tags.map(t => ({ name: t })),
      })
    })

  writeFileSync(path.join(config.outDir, 'rss.xml'), feed.rss2())
  console.log(`✅ RSS feed generated: ${config.outDir}/rss.xml (${feed.items.length} items)`)
}
