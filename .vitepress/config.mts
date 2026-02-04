import { defineConfig } from "vitepress";
import { teekConfig } from "./teekConfig";

export default defineConfig({
  extends: teekConfig, // 关键：继承 teek 的配置
  title: "Chuiyu Wiki",
  description: "要努力去发光,而不是被照亮",
  lang: "zh-CN",
  cleanUrls: false,
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
  }
});