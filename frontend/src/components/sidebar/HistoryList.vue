<script setup lang="ts">
defineProps<{
  title: string
  subtitle?: string
  active?: boolean
}>()

const emit = defineEmits<{
  click: []
  delete: []
}>()
</script>

<template>
  <div class="history-item" :class="{ active }">
    <button class="item-main" @click="emit('click')">
      <span class="item-title">{{ title }}</span>
      <span v-if="subtitle" class="item-sub">{{ subtitle }}</span>
    </button>
    <button class="item-delete" title="删除" @click.stop="emit('delete')">&times;</button>
  </div>
</template>

<style scoped>
.history-item {
  display: flex;
  align-items: center;
  gap: 4px;
  width: 100%;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s;
}

.history-item:hover {
  background: #f0f0f0;
}

.history-item.active {
  background: #e8f0fe;
}

.history-item.active:hover {
  background: #dce8f8;
}

.item-main {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
  min-width: 0;
  padding: 8px 0 8px 12px;
  font-family: inherit;
  text-align: left;
  background: transparent;
  border: none;
  cursor: pointer;
}

.item-title {
  font-size: 13px;
  color: #1a1a1a;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-sub {
  font-size: 11px;
  color: #999;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-delete {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  margin-right: 6px;
  padding: 0;
  font-size: 16px;
  line-height: 24px;
  color: #bbb;
  background: transparent;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: color 0.15s, background 0.15s;
}

.item-delete:hover {
  color: #e55;
  background: #fee;
}
</style>
