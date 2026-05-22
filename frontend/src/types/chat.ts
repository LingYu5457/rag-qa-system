export interface ChatMessage {
  id: string
  role: 'ai' | 'human' | 'fileupload'
  content: string
  timestamp?: number
}
