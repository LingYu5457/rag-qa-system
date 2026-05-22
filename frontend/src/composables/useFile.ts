import { ref } from 'vue'
import { useStatusStore } from '@/stores/statusStore'
import { useConversationStore } from '@/stores/conversationStore'
import { getFileHistory } from '@/api/file'
import { ApiError } from '@/api/client'

export function useFile() {
  const { userId } = useStatusStore()
  const { addFile } = useConversationStore()

  const loading = ref(false)
  const error = ref('')

  async function loadFiles() {
    if (!userId.value) return

    loading.value = true
    error.value = ''

    try {
      const res = await getFileHistory(userId.value)
      for (const f of res.data) {
        addFile(
          String(f.file_id),
          f.file_name,
          f.session_id != null ? String(f.session_id) : '',
          f.created_at,
        )
      }
    } catch (e) {
      error.value = e instanceof ApiError ? e.message : '加载文件列表失败'
    } finally {
      loading.value = false
    }
  }

  return { loading, error, loadFiles }
}
