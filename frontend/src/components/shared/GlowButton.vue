<template>
  <BorderGlow
    class="glow-button"
    :class="[`glow-button--${variant}`, className, { 'is-active': active }]"
    v-bind="glowProps"
  >
    <slot />
  </BorderGlow>
</template>

<script setup>
import { computed } from 'vue'
import BorderGlow from '@/components/shared/BorderGlow.vue'

const BRAND_COLORS = ['#00A8E0', '#007BA7', '#4DB8E0']

const VARIANTS = {
  nav: {
    borderRadius: 8,
    glowRadius: 20,
    glowIntensity: 1,
    edgeSensitivity: 30,
    coneSpread: 26,
    fillOpacity: 0.42,
    glowColor: '192 85 62',
    backgroundColor: 'rgba(255, 255, 255, 0.03)',
    activeBackgroundColor: 'rgba(0, 123, 167, 0.16)',
  },
  primary: {
    borderRadius: 8,
    glowRadius: 28,
    glowIntensity: 1.15,
    edgeSensitivity: 28,
    coneSpread: 28,
    fillOpacity: 0.48,
    glowColor: '192 90 68',
    backgroundColor: 'rgba(0, 123, 167, 0.92)',
    activeBackgroundColor: 'rgba(0, 168, 224, 0.92)',
  },
  secondary: {
    borderRadius: 8,
    glowRadius: 24,
    glowIntensity: 1.05,
    edgeSensitivity: 30,
    coneSpread: 26,
    fillOpacity: 0.4,
    glowColor: '192 80 62',
    backgroundColor: 'rgba(0, 0, 0, 0.18)',
    activeBackgroundColor: 'rgba(0, 123, 167, 0.12)',
  },
  outline: {
    borderRadius: 8,
    glowRadius: 22,
    glowIntensity: 1,
    edgeSensitivity: 32,
    coneSpread: 24,
    fillOpacity: 0.38,
    glowColor: '192 75 58',
    backgroundColor: 'rgba(255, 255, 255, 0.04)',
    activeBackgroundColor: 'rgba(0, 123, 167, 0.1)',
  },
}

const props = defineProps({
  variant: {
    type: String,
    default: 'nav',
    validator: (value) => ['nav', 'primary', 'secondary', 'outline'].includes(value),
  },
  active: {
    type: Boolean,
    default: false,
  },
  className: {
    type: String,
    default: '',
  },
})

const glowProps = computed(() => {
  const preset = VARIANTS[props.variant] ?? VARIANTS.nav
  return {
    colors: BRAND_COLORS,
    borderRadius: preset.borderRadius,
    glowRadius: preset.glowRadius,
    glowIntensity: preset.glowIntensity,
    edgeSensitivity: preset.edgeSensitivity,
    coneSpread: preset.coneSpread,
    fillOpacity: preset.fillOpacity,
    glowColor: preset.glowColor,
    backgroundColor: props.active ? preset.activeBackgroundColor : preset.backgroundColor,
  }
})
</script>

<style scoped>
.glow-button {
  box-shadow: none;
}

.glow-button :deep(.border-glow-inner) {
  overflow: visible;
}

.glow-button :deep(.nav-link),
.glow-button :deep(.btn),
.glow-button :deep(a) {
  width: 100%;
  border: none !important;
  background: transparent !important;
  box-shadow: none !important;
  transform: none !important;
}

.glow-button--primary.is-active,
.glow-button--primary:hover {
  border-color: rgba(0, 168, 224, 0.45);
}

.glow-button--secondary {
  border-color: rgba(77, 184, 224, 0.35);
}

.glow-button--outline {
  border-color: rgba(255, 255, 255, 0.18);
}

.glow-button--nav.is-active {
  border-color: rgba(0, 168, 224, 0.32);
}
</style>
