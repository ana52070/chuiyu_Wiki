import { defineConfig } from 'vitepress'
import { generateSidebar } from 'vitepress-sidebar'; // <--- 引入插件

export default defineConfig({
  title: "Chuiyu Wiki",
  description: "我的个人技术知识库",
  ignoreDeadLinks: true,

  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      // 这里的 link 指向分类文件夹即可，插件会自动处理
      { text: '博客文章', link: '/blog/' }, 
      { text: '学习笔记', link: '/guide/' },
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
      },
      // 2. 自动生成 'guide' 文件夹的侧边栏
      {
        documentRootPath: '/',
        scanStartPath: 'guide',
        resolvePath: '/guide/',
        useTitleFromFileHeading: true,
        collapsed: false, 
      },
      // 3. 自动生成 'projects' 文件夹的侧边栏
      {
        documentRootPath: '/',
        scanStartPath: 'projects',
        resolvePath: '/projects/',
        useTitleFromFileHeading: true,
        collapsed: false,
      }
    ]),

    socialLinks: [
      { icon: 'github', link: 'https://github.com/ana52070/chuiyu_Wiki' }
    ],
    
    search: {
      provider: 'local'
    }
  }
})