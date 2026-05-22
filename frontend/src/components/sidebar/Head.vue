<script setup lang="ts">
import { ref, inject } from 'vue'

const emit = defineEmits<{
  'new-conversation': []
  'upload-rag': [file: File]
}>()

const toggleSidebar = inject<() => void>('toggleSidebar', () => {})

const fileInputRef = ref<HTMLInputElement | null>(null)

function onUploadClick() {
  fileInputRef.value?.click()
}

function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (file) emit('upload-rag', file)
  input.value = ''
}
</script>

<template>
  <div class="sidebar-head">
    <input
      ref="fileInputRef"
      type="file"
      class="file-input-hidden"
      @change="onFileChange"
    />

    <button class="head-btn" title="新对话" @click="emit('new-conversation')">
      <svg
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
      >
        <line x1="12" y1="5" x2="12" y2="19" />
        <line x1="5" y1="12" x2="19" y2="12" />
      </svg>
      <span>新对话</span>
    </button>

    <button class="head-btn" title="上传文件构建知识库" @click="onUploadClick">
      <svg
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
        <polyline points="17 8 12 3 7 8" />
        <line x1="12" y1="3" x2="12" y2="15" />
      </svg>
      <span>上传</span>
    </button>

    <span class="spacer" />

    <button class="head-btn collapse-btn" title="收起侧栏" @click="toggleSidebar">
      <svg
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <polyline points="15 18 9 12 15 6" />
      </svg>
    </button>
  </div>
</template>

<style scoped>
.sidebar-head {
  display: flex;
  align-items: center;
  gap: 2px;
  height: 52px;
  padding: 0 12px;
  border-bottom: 1px solid #e5e5e5;
}

.head-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  height: 34px;
  padding: 0 10px;
  font-size: 13px;
  color: #555;
  background: transparent;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.15s, color 0.15s;
  font-family: inherit;
}

.head-btn:hover {
  background: #f0f0f0;
  color: #1a1a1a;
}

.collapse-btn {
  padding: 0;
  width: 34px;
  justify-content: center;
  flex-shrink: 0;
}

.spacer {
  flex: 1;
}

.file-input-hidden {
  display: none;
}
</style>
