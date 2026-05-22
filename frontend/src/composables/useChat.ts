import { ref, computed } from 'vue'
import { useStatusStore } from '@/stores/statusStore'
import { useConversationStore } from '@/stores/conversationStore'
import { createSession } from '@/api/session'
import { streamChat } from '@/api/chat'
import { uploadFile, deleteFile } from '@/api/file'
import { getSessionDetail } from '@/api/session'
import type { ChatMessage } from '@/types/chat'

export const CHAT_INPUT_MIN_HEIGHT = 44
export const CHAT_INPUT_MAX_HEIGHT = 180

export interface FileEntry {
  id: string
  fileId: number | null
  status: 'uploading' | 'done' | 'error'
  fileName: string
  summary: string
  errorMsg: string
}

let nextId = 1
function genMsgId() {
  return `msg-${Date.now()}-${nextId++}`
}

let fileIdSeq = 0
function genFileId() {
  return `file-${Date.now()}-${++fileIdSeq}`
}

/* ---- 对话发送 ---- */

export function useChat() {
  const { userId, currentConversationId, messages, setCurrentConversation, addMessage } =
    useStatusStore()
  const { addConversation, nowISO, updateConversationTime, addConversationMessage } =
    useConversationStore()

  const sending = ref(false)
  const error = ref('')

  async function loadFileuploadMessages(sid: string) {
    const existing = new Set(messages.value.map((m) => m.id))
    const res = await getSessionDetail(sid)
    for (const c of res.data.chats) {
      if (c.role === 'fileupload') {
        const id = `fu-${c.chat_id}`
        if (!existing.has(id)) {
          addMessage({ id, role: 'fileupload', content: c.chat_message })
        }
      }
    }
  }

  async function send(text: string, onPreSend?: () => Promise<void>) {
    if (!userId.value || sending.value) return

    sending.value = true
    error.value = ''

    if (onPreSend) {
      try { await onPreSend() } catch { /* ignore pre-send errors */ }
    }

    const userMsg: ChatMessage = {
      id: genMsgId(),
      role: 'human',
      content: text,
    }
    addMessage(userMsg)

    let sid = currentConversationId.value

    // 新对话：先创建会话
    if (!sid) {
      try {
        const res = await createSession(userId.value, text)
        sid = String(res.data.session_id)
        setCurrentConversation(sid, res.data.session_title)
        addConversation(sid, res.data.session_title, nowISO())
        addConversationMessage(sid, userMsg)
      } catch (e: unknown) {
        error.value = (e as Error).message || '创建会话失败'
        sending.value = false
        return
      }
    } else {
      addConversationMessage(sid, userMsg)
    }

    // AI 消息占位
    addMessage({ id: genMsgId(), role: 'ai', content: '' })
    const aiMsg = messages.value[messages.value.length - 1]!

    try {
      for await (const chunk of streamChat(sid, text)) {
        if (chunk.type === 'chunk') {
          aiMsg.content += chunk.content
        } else if (chunk.type === 'error') {
          error.value = chunk.message
        }
      }
    } catch (e: unknown) {
      error.value = (e as Error).message || '对话请求失败'
    }

    if (aiMsg.content) {
      addConversationMessage(sid, { id: aiMsg.id, role: aiMsg.role, content: aiMsg.content })
      updateConversationTime(sid)
    }

    sending.value = false
  }

  return { sending, error, send, loadFileuploadMessages }
}

/* ---- 文件上传管理 ---- */

export function useFileUpload() {
  const { userId, currentConversationId } = useStatusStore()

  const uploadedFiles = ref<FileEntry[]>([])

  const isUploading = computed(() =>
    uploadedFiles.value.some((f) => f.status === 'uploading'),
  )

  const hasPendingFiles = computed(() =>
    uploadedFiles.value.some((f) => f.status === 'done'),
  )

  async function startUpload(file: File) {
    if (!userId.value || isUploading.value) return

    const entry: FileEntry = {
      id: genFileId(),
      fileId: null,
      status: 'uploading',
      fileName: file.name,
      summary: '',
      errorMsg: '',
    }
    uploadedFiles.value = [...uploadedFiles.value, entry]

    try {
      const res = await uploadFile(
        userId.value,
        file,
        currentConversationId.value || undefined,
      )
      uploadedFiles.value = uploadedFiles.value.map((f) =>
        f.id === entry.id
          ? { ...f, status: 'done', fileId: res.data.file_id, summary: res.data.summary ?? '' }
          : f,
      )
    } catch (e: unknown) {
      uploadedFiles.value = uploadedFiles.value.map((f) =>
        f.id === entry.id
          ? { ...f, status: 'error', errorMsg: (e as Error).message || '上传失败' }
          : f,
      )
    }
  }

  async function removeFile(id: string) {
    const target = uploadedFiles.value.find((f) => f.id === id)
    if (target?.fileId) {
      try { await deleteFile(target.fileId) } catch { /* ignore */ }
    }
    uploadedFiles.value = uploadedFiles.value.filter((f) => f.id !== id)
  }

  function clearUploaded() {
    uploadedFiles.value = uploadedFiles.value.filter(
      (f) => f.status !== 'done' && f.status !== 'error',
    )
  }

  return { uploadedFiles, isUploading, hasPendingFiles, startUpload, removeFile, clearUploaded }
}

/* ---- 输入框 ---- */

export function useChatInput(
  onSend: (text: string) => void,
  onUpload: (file: File) => void,
  isUploading?: () => boolean,
) {
  const text = ref('')
  const textareaRef = ref<HTMLTextAreaElement | null>(null)
  const fileInputRef = ref<HTMLInputElement | null>(null)

  const canSend = computed(() => {
    if (isUploading?.()) return false
    return text.value.trim().length > 0
  })

  function autoResize() {
    const el = textareaRef.value
    if (!el) return
    el.style.height = '0'
    el.style.height =
      Math.min(Math.max(el.scrollHeight, CHAT_INPUT_MIN_HEIGHT), CHAT_INPUT_MAX_HEIGHT) + 'px'
  }

  function send() {
    const trimmed = text.value.trim()
    if (!trimmed) return
    onSend(trimmed)
    text.value = ''
    const el = textareaRef.value
    if (el) el.style.height = CHAT_INPUT_MIN_HEIGHT + 'px'
  }

  function uploadClick() {
    fileInputRef.value?.click()
  }

  function fileChange(e: Event) {
    const input = e.target as HTMLInputElement
    const file = input.files?.[0]
    if (file) onUpload(file)
    input.value = ''
  }

  function onKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      send()
    }
  }

  return {
    text,
    textareaRef,
    fileInputRef,
    canSend,
    autoResize,
    send,
    uploadClick,
    fileChange,
    onKeydown,
  }
}
