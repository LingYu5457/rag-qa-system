<script setup lang="ts">
import { useSidebarLayout, SIDEBAR_WIDTH } from '@/composables/useSidebarLayout'
import SideBar from './sidebar/SideBar.vue'
import ChatArea from './chat/ChatArea.vue'

const CHAT_MIN_WIDTH = 400

const { isOpen, isFloating, toggleSidebar } = useSidebarLayout()
</script>

<template>
  <div class="app-layout">
    <aside
      class="sidebar"
      :class="{
        collapsed: !isOpen,
        floating: isFloating,
      }"
      :style="{ '--sidebar-width': SIDEBAR_WIDTH + 'px' }"
    >
      <div class="sidebar-inner">
        <SideBar />
      </div>
    </aside>

    <div v-if="isFloating && isOpen" class="overlay" @click="toggleSidebar" />

    <main class="chat-area" :style="{ 'min-width': CHAT_MIN_WIDTH + 'px' }">
      <ChatArea />
    </main>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
  position: relative;
}

.sidebar {
  width: var(--sidebar-width);
  min-width: var(--sidebar-width);
  height: 100%;
  position: relative;
  overflow: hidden;
  transition:
    margin-left 0.3s ease,
    transform 0.3s ease,
    box-shadow 0.3s ease;
  z-index: 1;
}

.sidebar:not(.floating).collapsed {
  margin-left: calc(-1 * var(--sidebar-width));
}

.sidebar.floating {
  position: fixed;
  left: 0;
  top: 0;
  z-index: 20;
  background: var(--bg-sidebar, #fff);
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.12);
  transform: translateX(0);
}

.sidebar.floating.collapsed {
  transform: translateX(-100%);
  box-shadow: none;
}

.sidebar-inner {
  width: var(--sidebar-width);
  height: 100%;
}

.overlay {
  position: fixed;
  inset: 0;
  z-index: 15;
  background: rgba(0, 0, 0, 0.3);
}

.chat-area {
  flex: 1;
  min-width: v-bind('CHAT_MIN_WIDTH + "px"');
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
</style>
