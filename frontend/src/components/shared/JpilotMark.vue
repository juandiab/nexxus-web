<template>
  <TriArcLoader :size="size" class="jpilot-logo-mark" v-bind="$attrs" />
</template>

<script setup>
import TriArcLoader from './TriArcLoader.vue'

defineProps({
  size: { type: [Number, String], default: 52 },
})

defineOptions({ inheritAttrs: false })
</script>

<style scoped>
.jpilot-logo-mark {
  color: var(--p-primary-color, var(--nt-primary-l));
}
</style>
