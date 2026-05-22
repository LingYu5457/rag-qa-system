<script setup lang="ts">
import { useStatusStore } from './stores/statusStore'
import AppLayout from './components/AppLayout.vue'
import LoginLayout from './components/login/LoginLayout.vue'

const { isLoggedIn } = useStatusStore()
</script>

<template>
  <AppLayout v-if="isLoggedIn" />
  <LoginLayout v-else />
</template>

<style>
/* 全局：去掉 body 默认 margin，消除 100vh 溢出滚动条 */
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  overflow: hidden;
}

*,
*::before,
*::after {
  box-sizing: border-box;
}
</style>
