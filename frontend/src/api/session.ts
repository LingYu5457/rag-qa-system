import { request } from './client'
import type { ApiResponse } from './client'

export interface SessionBrief {
  session_id: number
  session_title: string
  created_at: string
}

export interface ChatRecord {
  chat_id: number
  role: string
  chat_message: string
  created_at: string
}

export interface SessionDetail {
  session_id: number
  session_title: string
  created_at: string
  chats: ChatRecord[]
}

export interface CreateSessionData {
  session_id: number
  session_title: string
}

export function createSession(userId: number | string, query: string): Promise<ApiResponse<CreateSessionData>> {
  return request<CreateSessionData>('/session/create', {
    method: 'POST',
    body: JSON.stringify({ user_id: userId, query }),
  })
}

export function getSessionHistory(userId: number | string): Promise<ApiResponse<SessionBrief[]>> {
  return request<SessionBrief[]>(`/session/history/${userId}`)
}

export function getSessionDetail(sessionId: number | string): Promise<ApiResponse<SessionDetail>> {
  return request<SessionDetail>(`/session/${sessionId}`)
}

export function deleteSession(sessionId: number | string): Promise<ApiResponse<null>> {
  return request<null>(`/session/${sessionId}`, { method: 'DELETE' })
}
