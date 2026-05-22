<script setup lang="ts">
import { computed, ref } from 'vue'
import { marked } from 'marked'
import katex from 'katex'
import 'katex/dist/katex.min.css'

const props = defineProps<{
  role: 'ai' | 'human' | 'fileupload'
  content: string
}>()

const collapsed = ref(props.role === 'fileupload')

const html = computed(() => {
  let text = props.content

  // 1. 提取块级公式 $$...$$ 用占位符替换，避免 marked 将其放入 <p> 中
  const blocks: string[] = []
  text = text.replace(/\$\$([\s\S]*?)\$\$/g, (_match, tex: string) => {
    const t = tex.trim()
    try {
      blocks.push(katex.renderToString(t, { displayMode: true, throwOnError: false }))
    } catch {
      blocks.push(`<pre>${t}</pre>`)
    }
    return `\n␀MATH${blocks.length - 1}␀\n`
  })

  // 2. marked 渲染
  let html = marked.parse(text) as string

  // 3. 还原块级公式
  html = html.replace(/<p>\s*␀MATH(\d+)␀\s*<\/p>/g, (_match, i: string) => blocks[parseInt(i)] ?? '')
  html = html.replace(/␀MATH(\d+)␀/g, (_match, i: string) => blocks[parseInt(i)] ?? '')

  // 4. 行内公式 $...$
  html = html.replace(/\$([^\$\n]+?)\$/g, (_match, tex: string) => {
    const t = tex.trim()
    try {
      return katex.renderToString(t, { displayMode: false, throwOnError: false })
    } catch {
      return `$${t}$`
    }
  })

  return html
})
</script>

<template>
  <!-- fileupload: 可折叠样式 -->
  <div v-if="role === 'fileupload'" class="msg-row fileupload">
    <div class="fu-bubble">
      <div class="fu-header" @click="collapsed = !collapsed">
        <span class="fu-toggle">{{ collapsed ? '&#9654;' : '&#9660;' }}</span>
        <span class="fu-label">文件记录</span>
      </div>
      <div v-if="!collapsed" class="fu-body" v-html="html" />
    </div>
  </div>

  <!-- AI / Human -->
  <div v-else class="msg-row" :class="role">
    <div class="msg-bubble" v-html="html" />
  </div>
</template>

<style scoped>
.msg-row {
  display: flex;
  padding: 10px 20px;
}

/* ---- AI ---- */
.msg-row.ai {
  justify-content: center;
}

.msg-row.ai .msg-bubble {
  width: 100%;
  max-width: 1100px;
  min-width: 200px;
  font-size: 15px;
  line-height: 1.75;
  color: #1a1a1a;
}

.msg-row.ai .msg-bubble :deep(p) {
  margin: 0 0 8px;
}

.msg-row.ai .msg-bubble :deep(p:last-child) {
  margin-bottom: 0;
}

.msg-row.ai .msg-bubble :deep(code) {
  background: #f0f0f0;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.9em;
  font-family: 'Consolas', 'Monaco', monospace;
}

.msg-row.ai .msg-bubble :deep(pre) {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 12px 16px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 8px 0;
}

.msg-row.ai .msg-bubble :deep(pre code) {
  background: none;
  padding: 0;
  border-radius: 0;
  font-size: 13px;
}

.msg-row.ai .msg-bubble :deep(ul),
.msg-row.ai .msg-bubble :deep(ol) {
  padding-left: 24px;
  margin: 4px 0 8px;
}

.msg-row.ai .msg-bubble :deep(li) {
  margin-bottom: 4px;
}

.msg-row.ai .msg-bubble :deep(h1),
.msg-row.ai .msg-bubble :deep(h2),
.msg-row.ai .msg-bubble :deep(h3),
.msg-row.ai .msg-bubble :deep(h4),
.msg-row.ai .msg-bubble :deep(h5),
.msg-row.ai .msg-bubble :deep(h6) {
  margin: 16px 0 8px;
  line-height: 1.4;
}

.msg-row.ai .msg-bubble :deep(h1) { font-size: 1.5em; }
.msg-row.ai .msg-bubble :deep(h2) { font-size: 1.35em; }
.msg-row.ai .msg-bubble :deep(h3) { font-size: 1.2em; }

.msg-row.ai .msg-bubble :deep(blockquote) {
  border-left: 3px solid #ddd;
  margin: 8px 0;
  padding: 4px 12px;
  color: #666;
}

.msg-row.ai .msg-bubble :deep(table) {
  border-collapse: collapse;
  margin: 8px 0;
  width: 100%;
}

.msg-row.ai .msg-bubble :deep(th),
.msg-row.ai .msg-bubble :deep(td) {
  border: 1px solid #ddd;
  padding: 6px 12px;
  text-align: left;
}

.msg-row.ai .msg-bubble :deep(th) {
  background: #f5f5f5;
  font-weight: 600;
}

.msg-row.ai .msg-bubble :deep(a) {
  color: #2563eb;
  text-decoration: none;
}

.msg-row.ai .msg-bubble :deep(a:hover) {
  text-decoration: underline;
}

.msg-row.ai .msg-bubble :deep(hr) {
  border: none;
  border-top: 1px solid #e0e0e0;
  margin: 12px 0;
}

.msg-row.ai .msg-bubble :deep(.katex-display) {
  margin: 12px 0;
}

.msg-row.ai .msg-bubble :deep(.katex) {
  font-size: 1.1em;
  line-height: 1.2;
}

/* ---- Human ---- */
.msg-row.human {
  justify-content: flex-end;
}

.msg-row.human .msg-bubble {
  max-width: 1100px;
  min-width: 80px;
  padding: 10px 16px;
  font-size: 14px;
  line-height: 1.6;
  color: #1a1a1a;
  background: #e8f0fe;
  border-radius: 12px;
}

/* ---- File Upload (可折叠) ---- */
.msg-row.fileupload {
  justify-content: center;
}

.fu-bubble {
  width: 100%;
  max-width: 1100px;
  min-width: 200px;
  background: #f0f7f4;
  border: 1px solid #c3e6d6;
  border-radius: 10px;
  padding: 10px 16px;
  font-size: 14px;
  line-height: 1.7;
  color: #2d4a3b;
}

.fu-header {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  user-select: none;
  font-weight: 500;
}

.fu-toggle {
  font-size: 10px;
  flex-shrink: 0;
  width: 14px;
  text-align: center;
}

.fu-label {
  font-size: 13px;
  color: #5a7a66;
}

.fu-body {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #c3e6d6;
}

.fu-body :deep(p) {
  margin: 0 0 6px;
}

.fu-body :deep(p:last-child) {
  margin-bottom: 0;
}

.fu-body :deep(code) {
  background: #e2ede7;
  padding: 1px 5px;
  border-radius: 3px;
  font-size: 0.9em;
  font-family: 'Consolas', 'Monaco', monospace;
}

.fu-body :deep(pre) {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 10px 14px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 6px 0;
  font-size: 13px;
}
</style>
