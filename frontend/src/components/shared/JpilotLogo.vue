<template>
  <div
    class="jpilot-wordmark"
    :class="[`jpilot-wordmark--${variant}`]"
    role="img"
    :aria-label="alt"
  >
    <JpilotMark
      :size="markSize"
      class="jpilot-wordmark__mark"
      aria-hidden="true"
      aria-label=""
    />
    <div class="jpilot-wordmark__stack">
      <component :is="titleTag" class="jpilot-wordmark__title ld-cursor">
        <span class="jpilot-wordmark__jp">JP</span><span class="jpilot-wordmark__ilot">ilot</span>
      </component>
      <span v-if="tagline" class="jpilot-wordmark__tagline">{{ tagline }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import JpilotMark from './JpilotMark.vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'hero',
    validator: (value) => ['hero', 'compact'].includes(value),
  },
  tagline: {
    type: String,
    default: '',
  },
  titleTag: {
    type: String,
    default: 'h1',
  },
  alt: {
    type: String,
    default: 'JPilot',
  },
})

const isMobile = ref(false)
let mobileQuery

onMounted(() => {
  mobileQuery = window.matchMedia('(max-width: 767px)')
  isMobile.value = mobileQuery.matches
  mobileQuery.addEventListener('change', onMobileChange)
})

onUnmounted(() => {
  mobileQuery?.removeEventListener('change', onMobileChange)
})

function onMobileChange(event) {
  isMobile.value = event.matches
}

const markSize = computed(() => {
  if (props.variant === 'compact') return 40
  return isMobile.value ? 72 : 88
})
</script>

<style scoped>
.jpilot-wordmark {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  text-align: center;
  color: var(--nt-primary-l);
}

.jpilot-wordmark__mark {
  filter: drop-shadow(0 4px 16px rgba(0, 168, 224, 0.25));
}

.jpilot-wordmark__stack {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  min-width: 0;
}

.jpilot-wordmark__title {
  margin: 0;
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-weight: 600;
  line-height: 1;
  white-space: nowrap;
  letter-spacing: 0.1em;
  position: relative;
  display: inline-block;
  padding-right: 0.55em;
  color: var(--ink, currentColor);
}

.jpilot-wordmark__title.ld-cursor::after {
  position: absolute;
  right: 0;
  bottom: 0;
  margin-left: 0;
  color: var(--nt-primary-l);
  font-size: 1.05em;
}

.jpilot-wordmark__jp {
  color: var(--nt-primary-l);
}

.jpilot-wordmark__ilot {
  color: var(--nt-white);
}

.jpilot-wordmark__tagline {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: clamp(0.72rem, 2vw, 0.9rem);
  font-weight: 400;
  line-height: 1.35;
  letter-spacing: 0.04em;
  word-spacing: -0.05em;
  color: rgba(255, 255, 255, 0.62);
  white-space: nowrap;
}

.jpilot-wordmark--hero {
  width: 100%;
}

.jpilot-wordmark--hero .jpilot-wordmark__title {
  font-size: clamp(2.25rem, 5.5vw, 3.25rem);
}

.jpilot-wordmark--hero .jpilot-wordmark__tagline {
  font-size: clamp(0.78rem, 2.2vw, 1rem);
}

.jpilot-wordmark--compact {
  gap: 8px;
}

.jpilot-wordmark--compact .jpilot-wordmark__title {
  font-size: clamp(0.95rem, 2.4vw, 1.15rem);
}

.jpilot-wordmark--compact .jpilot-wordmark__tagline {
  font-size: 0.62rem;
}

@media (max-width: 767px) {
  .jpilot-wordmark--hero {
    gap: 12px;
  }

  .jpilot-wordmark--hero .jpilot-wordmark__title {
    font-size: clamp(1.85rem, 9vw, 2.5rem);
  }

  .jpilot-wordmark--hero .jpilot-wordmark__tagline {
    font-size: clamp(0.7rem, 3.2vw, 0.88rem);
  }
}
</style>
