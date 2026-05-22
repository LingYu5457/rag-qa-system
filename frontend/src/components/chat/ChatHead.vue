<script setup lang="ts">
import { inject, ref, type Ref } from 'vue'
import { useStatusStore } from '@/stores/statusStore'

const props = withDefaults(
  defineProps<{
    title?: string
  }>(),
  { title: '新对话' },
)

const { setCurrentConversation } = useStatusStore()

const toggleSidebar = inject<() => void>('toggleSidebar', () => {})
const sidebarOpen = inject<Ref<boolean>>('sidebarOpen', ref(true))

function onNewConversation() {
  setCurrentConversation('', '')
}
</script>

<template>
  <header class="chat-head">
    <button v-if="!sidebarOpen" class="menu-btn" title="展开侧栏" @click="toggleSidebar">
      <svg
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
      >
        <line x1="3" y1="6" x2="21" y2="6" />
        <line x1="3" y1="12" x2="21" y2="12" />
        <line x1="3" y1="18" x2="21" y2="18" />
      </svg>
    </button>

    <h1 class="title">{{ props.title }}</h1>
    <span class="spacer" />

    <button
      v-if="!sidebarOpen"
      class="new-btn"
      title="新对话"
      @click="onNewConversation"
    >
      <svg
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
      >
        <line x1="12" y1="5" x2="12" y2="19" />
        <line x1="5" y1="12" x2="19" y2="12" />
      </svg>
    </button>
  </header>
</template>

<style scoped>
.chat-head {
  display: flex;
  align-items: center;
  height: 52px;
  padding: 0 16px;
  border-bottom: 1px solid #e5e5e5;
  background: #fff;
}

.menu-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: #555;
  cursor: pointer;
  flex-shrink: 0;
  transition: background 0.15s, color 0.15s;
}

.menu-btn:hover {
  background: #f0f0f0;
  color: #333;
}

.title {
  margin: 0 0 0 12px;
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.spacer {
  flex: 1;
}

.new-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: #555;
  cursor: pointer;
  flex-shrink: 0;
  transition: background 0.15s, color 0.15s;
}

.new-btn:hover {
  background: #f0f0f0;
  color: #333;
}
</style>
