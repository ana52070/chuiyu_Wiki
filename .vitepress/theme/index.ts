import Teek from "vitepress-theme-teek";

// 尝试这种更通用的路径引入方式
import "vitepress-theme-teek/index.css"; 
import "vitepress-theme-teek/vp-plus/code-block-mobile.scss";
import "vitepress-theme-teek/vp-plus/sidebar.scss";
import "vitepress-theme-teek/vp-plus/nav.scss";
import "vitepress-theme-teek/vp-plus/aside.scss";
import "vitepress-theme-teek/vp-plus/doc-h1-gradient.scss";
import "vitepress-theme-teek/vp-plus/table.scss";
import "vitepress-theme-teek/vp-plus/mark.scss";
import "vitepress-theme-teek/vp-plus/blockquote.scss";
import "vitepress-theme-teek/vp-plus/index-rainbow.scss";
import "vitepress-theme-teek/tk-plus/banner-desc-gradient.scss";
import "vitepress-theme-teek/tk-plus/home-card-hover.scss";
import "vitepress-theme-teek/tk-plus/fade-up-animation.scss";



export default {
  extends: Teek,
  Layout: Teek.Layout,
  enhanceApp({ app, router, siteData }) {
    Teek.enhanceApp({ app, router, siteData });
  }
};