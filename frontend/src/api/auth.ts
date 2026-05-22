import { request } from './client'
import type { ApiResponse } from './client'

export interface LoginRequest {
  user_account: string
  user_password: string
}

export interface RegisterRequest {
  user_name: string
  user_account: string
  user_password: string
}

export interface UserInfo {
  user_id: number
  user_name: string
  user_account: string
  created_at: string
}

export function login(data: LoginRequest): Promise<ApiResponse<UserInfo>> {
  return request<UserInfo>('/user/login', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function register(data: RegisterRequest): Promise<ApiResponse<UserInfo>> {
  return request<UserInfo>('/user/register', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}
