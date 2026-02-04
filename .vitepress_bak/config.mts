import { defineConfig } from 'vitepress'
import { generateSidebar } from 'vitepress-sidebar'; // <--- 引入插件

export default defineConfig({
  title: "Chuiyu Wiki",
  description: "我的个人技术知识库",
  ignoreDeadLinks: true,

  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }],
    ['meta', { name: 'referrer', content: 'no-referrer' }]
  ],



  themeConfig: {
    logo: '/logo.jpg',
    nav: [
      { text: '首页', link: '/' },
      // 这里的 link 指向分类文件夹即可，插件会自动处理
      { text: '博客文章', link: '/blog/' }, 
      { text: '学习笔记', link: '/guide/' },
      { text: '项目记录', link: '/projects/' }
    ],

    // 🚀 这里原来的 sidebar: { ... } 删掉，换成下面这个：
    sidebar: generateSidebar([
      // 1. 自动生成 'blog' 文件夹的侧边栏
      {
        documentRootPath: '/',
        scanStartPath: 'blog',
        resolvePath: '/blog/',
        useTitleFromFileHeading: true, // 读取 md 文件里的 # 标题作为侧边栏名称
        collapsed: false, // 是否默认折叠

          // ✅ 新增：开启按 Frontmatter 中的 date 排序
        sortMenusByFrontmatterDate: true,
        
        // ✅ 新增：排序方向 'desc' (降序: 新的在前) 或 'asc' (升序: 旧的在前)
        sortMenusOrderByDescending: true
      },
      // 2. 自动生成 'guide' 文件夹的侧边栏
      {
        documentRootPath: '/',
        scanStartPath: 'guide',
        resolvePath: '/guide/',
        useTitleFromFileHeading: true,
        collapsed: false, 

          // ✅ 新增：开启按 Frontmatter 中的 date 排序
        sortMenusByFrontmatterDate: true,
        
        // ✅ 新增：排序方向 'desc' (降序: 新的在前) 或 'asc' (升序: 旧的在前)
        sortMenusOrderByDescending: true
      },
      // 3. 自动生成 'projects' 文件夹的侧边栏
      {
        documentRootPath: '/',
        scanStartPath: 'projects',
        resolvePath: '/projects/',
        useTitleFromFileHeading: true,
        collapsed: false,

          // ✅ 新增：开启按 Frontmatter 中的 date 排序
        sortMenusByFrontmatterDate: true,
        
        // ✅ 新增：排序方向 'desc' (降序: 新的在前) 或 'asc' (升序: 旧的在前)
        sortMenusOrderByDescending: true
      }
    ]),

    socialLinks: [
      { icon: 'github', link: 'https://github.com/ana52070/chuiyu_Wiki' }
    ],

    // 👇 在这里加上这段代码：
    outline: {
      level: [1, 2], // 显示 h1 和 h2 级标题
      label: '页面导航' // 这里可以改标题，比如改成 "目录" 或 "本页内容"
    },
    
    search: {
      provider: 'local'
    }
  }
})