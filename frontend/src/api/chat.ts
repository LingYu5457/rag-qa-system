const BASE_URL = '/api'

export type ChatChunk =
  | { type: 'chunk'; content: string }
  | { type: 'done' }
  | { type: 'error'; message: string }

export async function getStep(sessionId: number | string): Promise<string[]> {
  const res = await fetch(`${BASE_URL}/chat/step/${sessionId}`)
  if (!res.ok) return []
  const body = await res.json()
  return body?.data?.steps ?? []
}

export async function* streamChat(
  sessionId: number | string,
  query: string,
): AsyncGenerator<ChatChunk> {
  const res = await fetch(`${BASE_URL}/chat/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, query }),
  })

  if (!res.ok) {
    const body = await res.json().catch(() => null)
    throw new Error(body?.message || '请求失败')
  }

  const reader = res.body?.getReader()
  if (!reader) throw new Error('不支持流式响应')

  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split('\n')
    buffer = lines.pop() || ''

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = line.slice(6)
        try {
          yield JSON.parse(data) as ChatChunk
        } catch {
          // skip unparseable lines
        }
      }
    }
  }

  // drain remaining buffer
  if (buffer.startsWith('data: ')) {
    try {
      yield JSON.parse(buffer.slice(6)) as ChatChunk
    } catch {
      // skip
    }
  }
}
