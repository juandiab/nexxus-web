<template>
  <div
    class="ld-trio"
    :style="trioStyle"
    role="img"
    :aria-label="ariaLabel"
  >
    <i></i><i></i><i></i>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import './TriArcLoader.css'

const props = defineProps({
  ink: { type: String, default: '' },
  size: { type: [Number, String], default: 56 },
  ariaLabel: { type: String, default: 'JPilot' },
})

const trioStyle = computed(() => {
  const px = typeof props.size === 'number' ? `${props.size}px` : props.size
  return {
    width: px,
    height: px,
    ...(props.ink ? { '--ink': props.ink } : {}),
  }
})
</script>
