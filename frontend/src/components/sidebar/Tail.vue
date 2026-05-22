<script setup lang="ts">
import { computed } from 'vue'
import { useStatusStore } from '@/stores/statusStore'

const emit = defineEmits<{
  refresh: []
}>()

const { userName, sidebarMode, setSidebarMode } = useStatusStore()

const isFilesMode = computed(() => sidebarMode.value === 'files')

function toggleFilesView() {
  setSidebarMode(isFilesMode.value ? 'conversations' : 'files')
}
</script>

<template>
  <div class="sidebar-tail">
    <div class="user-info">
      <span class="name">{{ userName || '未登录' }}</span>
    </div>

    <div class="actions">
      <button
        class="tail-btn"
        :class="{ on: isFilesMode }"
        title="切换文件历史"
        @click="toggleFilesView"
      >
        <svg
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z" />
          <polyline points="13 2 13 9 20 9" />
        </svg>
      </button>

      <button class="tail-btn" title="刷新历史记录" @click="emit('refresh')">
        <svg
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <polyline points="23 4 23 10 17 10" />
          <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10" />
        </svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
.sidebar-tail {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  border-top: 1px solid #e5e5e5;
  background: #fff;
}

.user-info {
  min-width: 0;
}

.name {
  font-size: 13px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.actions {
  display: flex;
  gap: 2px;
  flex-shrink: 0;
}

.tail-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  color: #999;
  background: transparent;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}

.tail-btn:hover {
  background: #f0f0f0;
  color: #555;
}

.tail-btn.on {
  color: #4a90d9;
  background: #e8f0fe;
}
</style>
