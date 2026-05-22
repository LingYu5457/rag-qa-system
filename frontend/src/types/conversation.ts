import type { ChatMessage } from './chat'

export type { ChatMessage }

export interface Conversation {
  conversation_id: string
  title: string
  messages: ChatMessage[]
}
