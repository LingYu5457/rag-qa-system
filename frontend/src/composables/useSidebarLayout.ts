import { ref, provide, onMounted, onUnmounted } from 'vue'

export const SIDEBAR_WIDTH = 280
const BREAKPOINT = 900

export function useSidebarLayout() {
  const isOpen = ref(true)
  const isFloating = ref(false)
  const lastAction = ref<'manual' | 'auto' | null>(null)

  function toggleSidebar() {
    if (isOpen.value) {
      isOpen.value = false
      lastAction.value = 'manual'
      isFloating.value = false
      return
    }

    isOpen.value = true
    lastAction.value = 'manual'
    isFloating.value = lastAction.value === null ? false : window.innerWidth < BREAKPOINT
  }

  function handleResize() {
    const width = window.innerWidth

    if (width < BREAKPOINT) {
      if (isOpen.value && lastAction.value !== 'manual') {
        isOpen.value = false
        lastAction.value = 'auto'
      }
      return
    }

    if (!isOpen.value && lastAction.value === 'auto') {
      isOpen.value = true
      isFloating.value = false
      lastAction.value = null
    } else if (isFloating.value) {
      isFloating.value = false
      lastAction.value = null
    }
  }

  provide('sidebarOpen', isOpen)
  provide('sidebarFloating', isFloating)
  provide('toggleSidebar', toggleSidebar)

  onMounted(() => {
    window.addEventListener('resize', handleResize)
    handleResize()
  })

  onUnmounted(() => window.removeEventListener('resize', handleResize))

  return { isOpen, isFloating, toggleSidebar }
}
