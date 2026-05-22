<script setup lang="ts">
import { ref } from 'vue'
import { useStatusStore } from '@/stores/statusStore'
import ChatHead from './ChatHead.vue'
import ChatIput from './ChatIput.vue'
import MessageList from './MessageList.vue'
import StepsBar from './StepsBar.vue'
import { useChat, useFileUpload } from '@/composables/useChat'

const { isInConversation, currentConversationTitle, currentConversationId } = useStatusStore()
const { send, loadFileuploadMessages } = useChat()
const { uploadedFiles, isUploading, hasPendingFiles, startUpload, removeFile, clearUploaded } =
  useFileUpload()

const stepsRefreshTrigger = ref(0)

async function onSend(text: string) {
  await send(text, async () => {
    if (hasPendingFiles.value && currentConversationId.value) {
      await loadFileuploadMessages(currentConversationId.value)
      clearUploaded()
    }
  })
  stepsRefreshTrigger.value++
}

function onUpload(file: File) {
  startUpload(file)
}
</script>

<template>
  <div class="chat-area">
    <ChatHead :title="currentConversationTitle" />

    <!-- 新对话：输入框居中 + 提示语 -->
    <div v-if="!isInConversation" class="body welcome">
      <p class="hint">开始新对话，输入你的问题</p>
      <div class="input-centered">
        <ChatIput
          :uploaded-files="uploadedFiles"
          :is-uploading="isUploading"
          @send="onSend"
          @upload="onUpload"
          @remove-file="removeFile"
        />
      </div>
    </div>

    <!-- 已有对话：消息列表 + 底部输入框 -->
    <div v-else class="body conversation">
      <div class="messages-wrap">
        <MessageList />
      </div>
      <div class="steps-wrap">
        <StepsBar
          :session-id="currentConversationId"
          :refresh-trigger="stepsRefreshTrigger"
        />
      </div>
      <div class="input-bottom">
        <ChatIput
          :uploaded-files="uploadedFiles"
          :is-uploading="isUploading"
          @send="onSend"
          @upload="onUpload"
          @remove-file="removeFile"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-area {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #fafafa;
}

.body {
  flex: 1;
  min-height: 0;
}

/* ---- 新对话：居中 ---- */
.welcome {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding-bottom: 60px;
}

.hint {
  margin: 0;
  font-size: 15px;
  color: #999;
  user-select: none;
}

.input-centered {
  width: 100%;
  max-width: 1100px;
}

/* ---- 已有对话：列表 + 底部 ---- */
.conversation {
  display: flex;
  flex-direction: column;
}

.messages-wrap {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
}

.steps-wrap {
  flex-shrink: 0;
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
}

.input-bottom {
  flex-shrink: 0;
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
}
</style>
