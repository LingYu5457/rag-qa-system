<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import { useStatusStore } from '@/stores/statusStore'
import ChatMessage from './ChatMessage.vue'

const { messages } = useStatusStore()

const listRef = ref<HTMLElement | null>(null)

function scrollToBottom() {
  nextTick(() => {
    requestAnimationFrame(() => {
      const el = listRef.value
      if (el) {
        el.scrollTop = el.scrollHeight
      }
    })
  })
}

watch(
  () => messages.value.length,
  () => scrollToBottom(),
)

watch(
  () => {
    const msgs = messages.value
    if (msgs.length === 0) return ''
    return msgs[msgs.length - 1]!.content
  },
  () => scrollToBottom(),
)
</script>

<template>
  <div ref="listRef" class="message-list">
    <ChatMessage
      v-for="msg in messages"
      :key="msg.id"
      :role="msg.role"
      :content="msg.content"
    />
  </div>
</template>

<style scoped>
.message-list {
  padding: 16px 0;
}
</style>
