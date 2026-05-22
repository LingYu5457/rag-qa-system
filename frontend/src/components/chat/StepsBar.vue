<script setup lang="ts">
import { ref, watch } from 'vue'
import { getStep } from '@/api/chat'

const props = defineProps<{
  sessionId: string
  refreshTrigger: number
}>()

const collapsed = ref(true)
const steps = ref<string[]>([])
const loading = ref(false)

async function fetchSteps() {
  if (!props.sessionId) return
  loading.value = true
  try {
    steps.value = await getStep(props.sessionId)
  } catch {
    steps.value = []
  } finally {
    loading.value = false
  }
}

watch(
  () => props.refreshTrigger,
  () => {
    if (props.sessionId) fetchSteps()
  },
)

watch(
  () => props.sessionId,
  (id) => {
    if (!id) {
      steps.value = []
      collapsed.value = true
    }
  },
)

function toggle() {
  collapsed.value = !collapsed.value
}
</script>

<template>
  <div v-if="sessionId" class="steps-bar" :class="{ collapsed }">
    <div class="steps-header" @click="toggle">
      <span class="toggle-arrow" :class="{ open: !collapsed }">&#9654;</span>
      <span class="steps-title">
        对话步骤
        <span v-if="steps.length" class="steps-count">({{ steps.length }})</span>
        <span v-if="loading" class="loading-dot" />
      </span>
    </div>
    <div v-if="!collapsed" class="steps-body">
      <div v-if="steps.length === 0 && !loading" class="steps-empty">暂无步骤记录</div>
      <ol v-else class="steps-list">
        <li v-for="(step, i) in steps" :key="i" class="step-item">
          <span class="step-index">{{ i + 1 }}</span>
          <span class="step-text">{{ step }}</span>
        </li>
      </ol>
    </div>
  </div>
</template>

<style scoped>
.steps-bar {
  border-top: 1px solid #e5e5e5;
  background: #fff;
  font-size: 13px;
}

.steps-header {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  cursor: pointer;
  user-select: none;
  color: #888;
  transition: color 0.15s;
}

.steps-header:hover {
  color: #555;
}

.toggle-arrow {
  font-size: 10px;
  transition: transform 0.2s;
  display: inline-block;
}

.toggle-arrow.open {
  transform: rotate(90deg);
}

.steps-title {
  display: flex;
  align-items: center;
  gap: 4px;
}

.steps-count {
  font-size: 12px;
  color: #aaa;
}

.loading-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #4a90d9;
  animation: pulse 1s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}

.steps-body {
  padding: 0 16px 10px 16px;
  max-height: 260px;
  overflow-y: auto;
}

.steps-empty {
  color: #bbb;
  font-size: 12px;
  padding: 4px 0 4px 20px;
}

.steps-list {
  margin: 0;
  padding: 0;
  list-style: none;
  counter-reset: step-counter;
}

.step-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 3px 0;
  color: #666;
  font-size: 12px;
  line-height: 1.5;
}

.step-index {
  flex-shrink: 0;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #e8f0fe;
  color: #4a90d9;
  font-size: 11px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 1px;
}

.step-text {
  word-break: break-word;
}
</style>
