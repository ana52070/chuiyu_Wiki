<template></template>

<script setup lang="ts">
import { nextTick, onMounted, watch } from "vue";
import { useData } from "vitepress";

const VIDEO_WRAP_CLASS = "home-banner-video-wrap";

const injectBannerVideo = () => {
  const bgImage = document.querySelector<HTMLElement>(".tk-banner-bg-image");
  if (!bgImage) return;
  if (bgImage.querySelector(`.${VIDEO_WRAP_CLASS}`)) return;

  const wrap = document.createElement("div");
  wrap.className = VIDEO_WRAP_CLASS;
  wrap.setAttribute("aria-hidden", "true");

  const video = document.createElement("video");
  video.className = "home-banner-video";
  video.autoplay = true;
  video.muted = true;
  video.loop = true;
  video.playsInline = true;
  video.preload = "metadata";
  video.poster = "/background2.jpg";

  const source = document.createElement("source");
  source.src = "/background.mp4";
  source.type = "video/mp4";

  video.appendChild(source);
  wrap.appendChild(video);
  bgImage.prepend(wrap);
};

const ensureBannerVideo = () => {
  nextTick(() => {
    injectBannerVideo();
    setTimeout(injectBannerVideo, 0);
  });
};

const { page } = useData();

onMounted(() => {
  ensureBannerVideo();
});

watch(
  () => page.value.relativePath,
  () => {
    ensureBannerVideo();
  }
);
</script>
