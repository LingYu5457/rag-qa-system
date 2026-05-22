import { ref } from 'vue'
import { useStatusStore } from '@/stores/statusStore'
import { useConversationStore } from '@/stores/conversationStore'
import { getSessionHistory, getSessionDetail } from '@/api/session'
import { ApiError } from '@/api/client'
import type { ChatMessage } from '@/types/chat'

export function useConversation() {
  const { userId, setMessages } = useStatusStore()
  const { addConversation, setConversationMessages } = useConversationStore()

  const loading = ref(false)
  const error = ref('')

  async function loadSessions() {
    if (!userId.value) return

    loading.value = true
    error.value = ''

    try {
      const res = await getSessionHistory(userId.value)
      for (const s of res.data) {
        addConversation(String(s.session_id), s.session_title, s.created_at)
      }
    } catch (e) {
      error.value = e instanceof ApiError ? e.message : '加载会话列表失败'
    } finally {
      loading.value = false
    }
  }

  async function loadMessages(sessionId: number | string) {
    loading.value = true
    error.value = ''

    try {
      const res = await getSessionDetail(sessionId)
      const messages: ChatMessage[] = res.data.chats
        .filter((c) => c.role === 'assistant' || c.role === 'user' || c.role === 'fileupload')
        .map((c) => ({
          id: c.role === 'fileupload' ? `fu-${c.chat_id}` : String(c.chat_id),
          role: c.role === 'user' ? 'human' : c.role === 'fileupload' ? 'fileupload' : 'ai',
          content: c.chat_message,
        }))

      setConversationMessages(String(sessionId), messages)
      setMessages(messages)
    } catch (e) {
      error.value = e instanceof ApiError ? e.message : '加载消息失败'
    } finally {
      loading.value = false
    }
  }

  return { loading, error, loadSessions, loadMessages }
}
