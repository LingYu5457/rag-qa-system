import { reactive, computed } from 'vue'
import type { ChatMessage } from '@/types/conversation'

/* ---- 类型 ---- */

export interface ConversationCache {
  title: string
  created_at: string
  messages: ChatMessage[]
}

export interface FileRecord {
  filename: string
  conversation_id: string
  created_at: string
}

/* ---- 模块级单例状态 ---- */

const conversations = reactive<Record<string, ConversationCache>>({})
const files = reactive<Record<string, FileRecord>>({})

/* ---- 派生 ---- */

const conversationList = computed(() =>
  Object.entries(conversations)
    .map(([id, c]) => ({ conversation_id: id, ...c }))
    .sort((a, b) => b.created_at.localeCompare(a.created_at)),
)

/* ---- 操作函数 ---- */

function hasConversation(id: string): boolean {
  return id in conversations
}

function getConversation(id: string): ConversationCache | undefined {
  return conversations[id]
}

function addConversation(id: string, title: string, created_at: string) {
  if (!conversations[id]) {
    conversations[id] = { title, created_at, messages: [] }
  }
}

function removeConversation(id: string) {
  delete conversations[id]
}

function setConversationMessages(id: string, msgs: ChatMessage[]) {
  const c = conversations[id]
  if (c) c.messages = [...msgs]
}

function nowISO(): string {
  const d = new Date()
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
}

function updateConversationTime(id: string) {
  const c = conversations[id]
  if (c) {
    conversations[id] = { title: c.title, created_at: nowISO(), messages: c.messages }
  }
}

function addConversationMessage(id: string, msg: ChatMessage) {
  const c = conversations[id]
  if (c) c.messages.push(msg)
}

function isMessagesLoaded(id: string): boolean {
  const c = conversations[id]
  return !!c && c.messages.length > 0
}

function addFile(file_id: string, filename: string, conversation_id: string, created_at: string) {
  files[file_id] = { filename, conversation_id, created_at }
}

function removeFile(file_id: string) {
  delete files[file_id]
}

function getFilesByConversation(conversation_id: string): FileRecord[] {
  return Object.values(files).filter((f) => f.conversation_id === conversation_id)
}

export function useConversationStore() {
  return {
    conversations,
    files,
    conversationList,
    hasConversation,
    getConversation,
    addConversation,
    removeConversation,
    setConversationMessages,
    nowISO,
    updateConversationTime,
    addConversationMessage,
    isMessagesLoaded,
    addFile,
    removeFile,
    getFilesByConversation,
  }
}
