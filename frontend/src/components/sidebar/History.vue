<script setup lang="ts">
import { useStatusStore } from '@/stores/statusStore'
import { useConversationStore } from '@/stores/conversationStore'
import { useConversation } from '@/composables/useConversation'
import { useFile } from '@/composables/useFile'
import { deleteSession } from '@/api/session'
import { deleteFile } from '@/api/file'
import HistoryList from './HistoryList.vue'

function formatDate(iso: string): string {
  return iso.slice(0, 10)
}

const { sidebarMode, setSidebarMode, currentConversationId, setCurrentConversation, setMessages } =
  useStatusStore()
const { conversationList, files, isMessagesLoaded, getConversation, removeConversation, removeFile } =
  useConversationStore()
const { loadMessages } = useConversation()
const { loadFiles } = useFile()

async function onConversationClick(id: string, title: string) {
  setCurrentConversation(id, title)
  if (!isMessagesLoaded(id)) {
    await loadMessages(id)
  } else {
    const cached = getConversation(id)
    if (cached) setMessages(cached.messages)
  }
}

async function onDeleteSession(id: string) {
  if (!window.confirm('确定要删除该会话吗？关联的所有文件和消息也将被删除。')) return
  try { await deleteSession(id) } catch { /* ignore */ }
  removeConversation(id)
  if (currentConversationId.value === id) {
    setCurrentConversation('', '')
    setMessages([])
  }
  // 清除属于该会话的本地文件缓存，重新拉取文件列表
  for (const fileId of Object.keys(files)) {
    if (files[fileId]?.conversation_id === id) delete files[fileId]
  }
  await loadFiles()
}

async function onDeleteFile(id: string) {
  if (!window.confirm('确定要删除该文件吗？')) return
  try { await deleteFile(id) } catch { /* ignore */ }
  removeFile(id)
}

function onFileClick(fileId: string) {
  const file = files[fileId]
  if (!file) return
  // TODO: load/create conversation for this file's RAG
}

const isActive = (id: string) => currentConversationId.value === id
</script>

<template>
  <div class="history">
    <div class="tabs">
      <button
        class="tab"
        :class="{ active: sidebarMode === 'conversations' }"
        @click="setSidebarMode('conversations')"
      >
        会话
      </button>
      <button
        class="tab"
        :class="{ active: sidebarMode === 'files' }"
        @click="setSidebarMode('files')"
      >
        文件
      </button>
    </div>

    <div class="list">
      <!-- 会话列表 -->
      <template v-if="sidebarMode === 'conversations'">
        <HistoryList
          v-for="item in conversationList"
          :key="item.conversation_id"
          :title="item.title"
          :subtitle="formatDate(item.created_at)"
          :active="isActive(item.conversation_id)"
          @click="onConversationClick(item.conversation_id, item.title)"
          @delete="onDeleteSession(item.conversation_id)"
        />
        <p v-if="conversationList.length === 0" class="empty">暂无会话</p>
      </template>

      <!-- 文件列表 -->
      <template v-else>
        <HistoryList
          v-for="(file, id) in files"
          :key="id"
          :title="file.filename"
          :subtitle="formatDate(file.created_at)"
          @click="onFileClick(id)"
          @delete="onDeleteFile(id)"
        />
        <p v-if="Object.keys(files).length === 0" class="empty">暂无文件</p>
      </template>
    </div>
  </div>
</template>

<style scoped>
.history {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}

.tabs {
  display: flex;
  gap: 0;
  padding: 6px 12px 0;
  border-bottom: 1px solid #e5e5e5;
}

.tab {
  flex: 1;
  padding: 8px 0 10px;
  font-size: 13px;
  font-family: inherit;
  color: #888;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  transition: color 0.15s, border-color 0.15s;
}

.tab:hover {
  color: #555;
}

.tab.active {
  color: #4a90d9;
  border-bottom-color: #4a90d9;
}

.list {
  flex: 1;
  overflow-y: auto;
  padding: 6px 8px;
}

.empty {
  margin: 32px 0 0;
  text-align: center;
  font-size: 13px;
  color: #bbb;
  user-select: none;
}
</style>
