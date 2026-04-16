import { defineConfig } from "vitepress";
import { teekConfig } from "./teekConfig";
import { generateRSS } from "./rss";

export default defineConfig({
  extends: teekConfig, // 关键：继承 teek 的配置
  buildEnd: generateRSS,
  title: "Chuiyu Wiki",
  description: "要努力去发光,而不是被照亮",
  lang: "zh-CN",
  cleanUrls: false,
  head: [
    ['link', { rel: 'alternate', type: 'application/rss+xml', title: 'Chuiyu Wiki RSS', href: 'https://chuiyu.wiki/rss.xml' }],
  ],
  themeConfig: {
    logo: "/logo.jpg",
    // 导航栏配置
    nav: [
      { text: '🏠 首页', link: '/' },
      { text: '✍️ 博客文章', link: '/blog/' },
      { text: '📚 学习笔记', link: '/guide/' },
      { text: '🛠️ 项目记录', link: '/projects/' },
    ],
    socialLinks: [{ icon: "github", link: "https://github.com/ana52070/chuiyu_Wiki" }],

    search: {
      provider: 'local',
      options: {
        locales: {
          root: {
            translations: {
              button: {
                buttonText: '搜索文档',
                buttonAriaLabel: '搜索文档'
              },
              modal: {
                noResultsText: '无法找到相关结果',
                resetButtonTitle: '清除查询条件',
                footer: {
                  selectText: '选择',
                  navigateText: '切换',
                  closeText: '关闭'
                }
              }
            }
          }
        }
      }
    }


  }
});