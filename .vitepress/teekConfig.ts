// 引入在线主题包的配置函数和版本号
import { defineTeekConfig } from "vitepress-theme-teek/config";
import { version } from "vitepress-theme-teek/es/version";

export const teekConfig = defineTeekConfig({
  teekTheme: true,   // 开启 Teek 主题
  teekHome: true,    // 开启博客首页风格
  sidebarTrigger: true,

  // 博主信息（左侧第一个卡片）
  blogger: {
    name: "Chuiyu",
    slogan: "要努力去发光,而不是被照亮",
    avatar: "/logo.jpg", // 确保 public 文件夹有这个图
    shape: "circle-rotate",
    color: "#000000ff",
    circleSize: 120,
  },

  // 首页顶部的 Banner 配置（解决你那个黑大块的问题）
  banner: {
    enabled: true,
    name: "Chuiyu Wiki",
    bgStyle: "fullImg", // 暂时设为纯色 pure 或全屏图 fullImg
    imgSrc:"/background2.jpg",
    description: [
      "要努力去发光,而不是被照亮",
      "光而不耀"
    ],
    descStyle: "types", // 开启打字机效果
  },

  footerInfo: {
    theme: { name: `Theme By Teek@${version}` },
    copyright: { createYear: 2026, suffix: "Chuiyu Wiki" },
  },

  // 核心插件配置（自动生成分类和侧边栏）
  vitePlugins: {
    sidebar: true,
    autoFrontmatter: true,
    autoFrontmatterOption: {
      categories: true,
    },
    docAnalysis: true,
    fileContentLoaderIgnore: ['**/tags.md', '**/categories.md', '**/archives.md', '**/assets/**'],
    sidebarOption: {
      ignoreList: ['**/assets/**', 'assets']
    },
    catalogueOption: {
      path: './',
      ignoreList: ['assets', 'public', '.vitepress', 'node_modules']
    }
  },


  topArticle: {
    enabled: true,
    title: "🔥 精选文章",
    limit: 5, // 最多显示 5 篇
  },

  friendLink: {
  enabled: true,
  title: "🤝 友情链接",
  list: [
        {
        name: "Github个人主页",
        desc: "全球最大的开源社区",
        avatar: "https://th.bing.com/th/id/ODF.bYAvaN8MCaSZfP0o7q_Z_w?w=32&h=32&qlt=90&pcl=fffffc&o=6&pid=1.2",
        link: "https://github.com/ana52070",
        },
        {
        name: "B站个人主页",
        desc: "bilibili- ( ゜- ゜)つロ 乾杯~",
        avatar: "https://th.bing.com/th/id/ODF.HcIfqnk4n-lbffGcaqDC2w?w=32&h=32&qlt=90&pcl=fffffc&o=6&pid=1.2", 
        link: "https://space.bilibili.com/166842001",
        },
        {
        name: "CSDN个人主页",
        desc: "很一般的开发者社区",
        avatar: "https://th.bing.com/th/id/ODF.XgN2n5Bhof8syOMYSfYpGg?w=32&h=32&qlt=90&pcl=fffffc&o=6&pid=1.2", 
        link: "https://blog.csdn.net/chui_yu666",
        },
    ],
  },



});