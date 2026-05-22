const BASE_URL = '/api'

export interface ApiResponse<T = unknown> {
  code: number
  message: string
  data: T
}

export async function request<T>(
  path: string,
  options?: RequestInit,
): Promise<ApiResponse<T>> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })

  const body: ApiResponse<T> = await res.json()

  if (!res.ok) {
    throw new ApiError(body.message || '请求失败', body.code || res.status)
  }

  return body
}

export class ApiError extends Error {
  code: number

  constructor(message: string, code: number) {
    super(message)
    this.name = 'ApiError'
    this.code = code
  }
}
