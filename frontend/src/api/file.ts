const BASE_URL = '/api'

import { request, ApiError } from './client'
import type { ApiResponse } from './client'

export interface FileBrief {
  file_id: number
  file_name: string
  session_id: number | null
  created_at: string
}

export interface UploadResult {
  file_id: number
  file_name: string
  source: string
  summary?: string
  vector_count?: number
  text_count?: number
}

export function getFileHistory(userId: number | string): Promise<ApiResponse<FileBrief[]>> {
  return request<FileBrief[]>(`/file/history/${userId}`)
}

export function deleteFile(fileId: number | string): Promise<ApiResponse<null>> {
  return request<null>(`/file/${fileId}`, { method: 'DELETE' })
}

export async function uploadFile(
  userId: number | string,
  file: File,
  sessionId?: number | string,
): Promise<ApiResponse<UploadResult>> {
  const form = new FormData()
  form.append('user_id', String(userId))
  form.append('file', file)
  if (sessionId) {
    form.append('session_id', String(sessionId))
  }

  const endpoint = sessionId ? `${BASE_URL}/file/upload` : `${BASE_URL}/file/upload_rag`

  const res = await fetch(endpoint, {
    method: 'POST',
    body: form,
  })

  const body: ApiResponse<UploadResult> = await res.json()

  if (!res.ok) {
    throw new ApiError(body.message || '上传失败', body.code || res.status)
  }

  return body
}
