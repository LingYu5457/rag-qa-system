<script setup lang="ts">
import { useChatInput, CHAT_INPUT_MIN_HEIGHT, CHAT_INPUT_MAX_HEIGHT } from '@/composables/useChat'
import type { FileEntry } from '@/composables/useChat'

const props = defineProps<{
  uploadedFiles: FileEntry[]
  isUploading: boolean
}>()

const emit = defineEmits<{
  send: [text: string]
  upload: [file: File]
  removeFile: [id: string]
}>()

const {
  text,
  textareaRef,
  fileInputRef,
  canSend,
  autoResize,
  send,
  uploadClick,
  fileChange,
  onKeydown,
} = useChatInput(
  (t) => emit('send', t),
  (f) => emit('upload', f),
  () => props.isUploading,
)
</script>

<template>
  <div class="chat-input">
    <!-- 文件标签行 -->
    <div v-if="uploadedFiles.length > 0" class="file-tags">
      <span
        v-for="f in uploadedFiles"
        :key="f.id"
        class="file-tag"
        :class="f.status"
      >
        <span class="tag-icon">
          <template v-if="f.status === 'uploading'">
            <span class="spinner" />
          </template>
          <template v-else-if="f.status === 'done'">
            &#10003;
          </template>
          <template v-else>
            &#10007;
          </template>
        </span>
        <span class="tag-name">{{ f.fileName }}</span>
        <button
          v-if="f.status === 'done' || f.status === 'error'"
          class="tag-close"
          title="移除"
          @click="emit('removeFile', f.id)"
        >
          &times;
        </button>
      </span>
    </div>

    <!-- 输入框行 -->
    <div class="input-row">
      <textarea
        ref="textareaRef"
        v-model="text"
        class="editor"
        placeholder="输入消息，Enter 发送，Shift+Enter 换行"
        :style="{ minHeight: CHAT_INPUT_MIN_HEIGHT + 'px', maxHeight: CHAT_INPUT_MAX_HEIGHT + 'px' }"
        @input="autoResize"
        @keydown="onKeydown"
      />
    </div>

    <!-- 底部按钮行 -->
    <div class="btn-row">
      <input
        ref="fileInputRef"
        type="file"
        class="file-input"
        @change="fileChange"
      />

      <button class="btn btn-upload" title="上传文件" @click="uploadClick">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
          <polyline points="17 8 12 3 7 8" />
          <line x1="12" y1="3" x2="12" y2="15" />
        </svg>
      </button>

      <div class="spacer" />

      <button class="btn btn-send" :disabled="!canSend" title="发送" @click="send">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
          <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
        </svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
.chat-input {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 10px 16px;
  border-top: 1px solid #e5e5e5;
  background: #fff;
}

/* ---- 文件标签 ---- */
.file-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.file-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 12px;
  line-height: 1.4;
}

.file-tag.uploading {
  background: #fef3c7;
  color: #92400e;
  border: 1px solid #fcd34d;
}

.file-tag.done {
  background: #d1fae5;
  color: #065f46;
  border: 1px solid #6ee7b7;
}

.file-tag.error {
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #fca5a5;
}

.tag-icon {
  flex-shrink: 0;
  font-size: 11px;
  line-height: 1;
}

.spinner {
  display: inline-block;
  width: 10px;
  height: 10px;
  border: 2px solid #92400e;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin-anim 0.8s linear infinite;
}

@keyframes spin-anim {
  to { transform: rotate(360deg); }
}

.tag-name {
  max-width: 160px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.tag-close {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  margin-left: 2px;
  padding: 0;
  border: none;
  border-radius: 50%;
  background: transparent;
  color: inherit;
  font-size: 14px;
  line-height: 1;
  cursor: pointer;
  opacity: 0.6;
}

.tag-close:hover {
  opacity: 1;
}

/* ---- 输入框 ---- */
.input-row {
  display: flex;
  align-items: flex-end;
}

.editor {
  display: block;
  width: 100%;
  padding: 10px 14px;
  font-size: 14px;
  line-height: 1.55;
  color: #1a1a1a;
  background: #f5f5f5;
  border: 1px solid transparent;
  border-radius: 12px;
  outline: none;
  resize: none;
  box-sizing: border-box;
  transition: border-color 0.2s, background 0.2s;
  font-family: inherit;
}

.editor:focus {
  background: #fff;
  border-color: #4a90d9;
}

/* ---- 按钮行 ---- */
.btn-row {
  display: flex;
  align-items: center;
  gap: 6px;
}

.spacer {
  flex: 1;
}

.file-input {
  display: none;
}

.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  background: #f0f0f0;
  color: #555;
  transition: background 0.2s, color 0.2s;
}

.btn:hover {
  background: #e0e0e0;
  color: #333;
}

.btn-upload {
  color: #666;
}

.btn-send {
  color: #fff;
  background: #4a90d9;
}

.btn-send:hover {
  background: #357abd;
}

.btn-send:disabled {
  background: #b0cef0;
  cursor: not-allowed;
}
</style>
