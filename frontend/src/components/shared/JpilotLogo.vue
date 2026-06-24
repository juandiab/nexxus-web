<template>
  <img
    :src="logoSrc"
    :alt="alt"
    :class="imgClass"
    :width="width"
    :height="height"
    :loading="loading"
    decoding="async"
  />
</template>

<script setup>
import { computed } from 'vue'
import { JPILOT_LOGOS } from '@/data/products.js'

const props = defineProps({
  /** `dark` = dark UI backgrounds; `light` = light/white section backgrounds */
  theme: {
    type: String,
    default: 'dark',
    validator: (v) => ['dark', 'light'].includes(v),
  },
  alt: {
    type: String,
    default: 'JPilot',
  },
  imgClass: {
    type: String,
    default: '',
  },
  width: {
    type: [Number, String],
    default: undefined,
  },
  height: {
    type: [Number, String],
    default: undefined,
  },
  loading: {
    type: String,
    default: 'lazy',
  },
})

const logoSrc = computed(() =>
  props.theme === 'light' ? JPILOT_LOGOS.light : JPILOT_LOGOS.dark
)
</script>
