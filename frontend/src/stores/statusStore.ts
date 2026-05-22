import { ref, computed } from 'vue'
import type { ChatMessage } from '@/types/conversation'

/* ---- 模块级单例状态 ---- */

const userId = ref<number | string>('')
const userName = ref('')
const userAccount = ref('')
const isLoggedIn = ref(false)

const currentConversationId = ref('')
const currentConversationTitle = ref('')
const messages = ref<ChatMessage[]>([])

const sidebarMode = ref<'conversations' | 'files'>('conversations')

/* ---- 派生 ---- */

const isInConversation = computed(() => currentConversationId.value !== '')

/* ---- 操作函数 ---- */

function setSidebarMode(mode: 'conversations' | 'files') {
  sidebarMode.value = mode
}

function setUser(user: { user_id: number | string; user_name: string; user_account?: string }) {
  userId.value = user.user_id
  userName.value = user.user_name
  userAccount.value = user.user_account ?? ''
  isLoggedIn.value = true
}

function logout() {
  userId.value = ''
  userName.value = ''
  userAccount.value = ''
  isLoggedIn.value = false
  clearConversation()
}

function setCurrentConversation(id: string, title: string) {
  currentConversationId.value = id
  currentConversationTitle.value = title
}

function clearConversation() {
  currentConversationId.value = ''
  currentConversationTitle.value = ''
  messages.value = []
}

function setMessages(msgs: ChatMessage[]) {
  messages.value = [...msgs]
}

function addMessage(msg: ChatMessage) {
  messages.value.push(msg)
}

export function useStatusStore() {
  return {
    userId,
    userName,
    userAccount,
    isLoggedIn,
    currentConversationId,
    currentConversationTitle,
    messages,
    isInConversation,
    sidebarMode,
    setSidebarMode,
    setUser,
    logout,
    setCurrentConversation,
    clearConversation,
    setMessages,
    addMessage,
  }
}
