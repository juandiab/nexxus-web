<template>
  <button
    type="button"
    class="feature-zoom-trigger"
    :aria-label="`View larger: ${alt}`"
    @click="open = true"
  >
    <img
      :src="src"
      :alt="alt"
      class="feature-zoom-image"
      :width="width"
      :height="height"
    />
  </button>

  <Teleport to="body">
    <Transition name="feature-lightbox">
      <div
        v-if="open"
        class="feature-lightbox"
        role="dialog"
        aria-modal="true"
        :aria-label="alt"
        @click.self="close"
      >
        <button
          type="button"
          class="feature-lightbox-close"
          aria-label="Close image"
          @click="close"
        >
          <i class="pi pi-times"></i>
        </button>
        <img :src="src" :alt="alt" class="feature-lightbox-image" />
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { onUnmounted, ref, watch } from 'vue'

defineProps({
  src: { type: String, required: true },
  alt: { type: String, required: true },
  width: { type: [Number, String], default: 720 },
  height: { type: [Number, String], default: 480 },
})

const open = ref(false)

function close() {
  open.value = false
}

function onKeydown(event) {
  if (event.key === 'Escape') close()
}

watch(open, (isOpen) => {
  if (isOpen) {
    document.addEventListener('keydown', onKeydown)
    document.body.style.overflow = 'hidden'
  } else {
    document.removeEventListener('keydown', onKeydown)
    document.body.style.overflow = ''
  }
})

onUnmounted(() => {
  document.removeEventListener('keydown', onKeydown)
  document.body.style.overflow = ''
})
</script>

<style scoped>
.feature-zoom-trigger {
  display: block;
  width: 100%;
  height: 100%;
  min-height: 100%;
  padding: 0;
  border: none;
  background: transparent;
  cursor: zoom-in;
  border-radius: var(--nt-radius);
  overflow: hidden;
}

.feature-zoom-trigger:hover .feature-zoom-image,
.feature-zoom-trigger:focus-visible .feature-zoom-image {
  filter: brightness(1.08);
  transform: scale(1.015);
}

.feature-zoom-trigger:focus-visible {
  outline: 2px solid var(--nt-primary-l);
  outline-offset: 3px;
}

.feature-zoom-image {
  width: 100%;
  height: 100%;
  min-height: 100%;
  object-fit: cover;
  object-position: center;
  border-radius: var(--nt-radius);
  display: block;
  background: #05070c;
  transition: filter 0.2s ease, transform 0.2s ease;
}

.feature-lightbox {
  position: fixed;
  inset: 0;
  z-index: 10050;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 28px 48px;
  background: rgba(5, 8, 18, 0.88);
  backdrop-filter: blur(8px);
  cursor: zoom-out;
}

.feature-lightbox-image {
  max-width: min(1280px, 100%);
  max-height: min(88dvh, 100%);
  width: auto;
  height: auto;
  object-fit: contain;
  border-radius: 12px;
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.5);
  cursor: default;
}

.feature-lightbox-close {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.08);
  color: #e2e8f0;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.feature-lightbox-close:hover,
.feature-lightbox-close:focus-visible {
  background: rgba(255, 255, 255, 0.14);
  color: #fff;
}

.feature-lightbox-enter-active,
.feature-lightbox-leave-active {
  transition: opacity 0.2s ease;
}

.feature-lightbox-enter-from,
.feature-lightbox-leave-to {
  opacity: 0;
}

@media (max-width: 900px) {
  .feature-zoom-image {
    height: 240px;
    min-height: 240px;
  }

  .feature-lightbox {
    padding: 56px 16px 16px;
  }
}
</style>
