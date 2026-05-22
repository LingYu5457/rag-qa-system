<script setup lang="ts">
import { ref } from 'vue'
import { useStatusStore } from '@/stores/statusStore'
import { useConversation } from '@/composables/useConversation'
import { useFile } from '@/composables/useFile'
import { uploadFile } from '@/api/file'
import Head from './Head.vue'
import History from './History.vue'
import Tail from './Tail.vue'

const { userId, sidebarMode, clearConversation } = useStatusStore()
const { loadSessions } = useConversation()
const { loadFiles } = useFile()

const ragUploading = ref(false)

function onNewConversation() {
  clearConversation()
}

async function onUploadRag(file: File) {
  if (!userId.value || ragUploading.value) return
  ragUploading.value = true
  try {
    const res = await uploadFile(userId.value, file)
    await loadFiles()
    alert(`「${res.data.file_name}」上传成功，已入库 ${res.data.vector_count ?? 0} 条向量、${res.data.text_count ?? 0} 条文本`)
  } catch (e: unknown) {
    alert((e as Error).message || '上传失败')
  } finally {
    ragUploading.value = false
  }
}

function onRefresh() {
  if (sidebarMode.value === 'files') {
    loadFiles()
  } else {
    loadSessions()
  }
}
</script>

<template>
  <div class="sidebar">
    <Head @new-conversation="onNewConversation" @upload-rag="onUploadRag" />
    <History />
    <Tail @refresh="onRefresh" />
  </div>
</template>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #fff;
}
</style>
