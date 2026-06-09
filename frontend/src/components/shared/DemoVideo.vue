<template>
  <div ref="root" class="demo-video" :class="{ 'demo-video--hero': variant === 'hero' }">
    <video
      v-if="state === 'present'"
      v-bind="videoAttrs"
      class="demo-video__player"
    >
      <source :src="`/videos/${name}.webm`" type="video/webm" />
      <source :src="`/videos/${name}.mp4`" type="video/mp4" />
    </video>

    <div v-else class="demo-video__skeleton">
      <div class="card">
        <div class="skeleton-panel">
          <div class="flex mb-4">
            <Skeleton shape="circle" size="4rem" class="mr-2" />
            <div>
              <Skeleton width="10rem" class="mb-2" />
              <Skeleton width="5rem" class="mb-2" />
              <Skeleton height=".5rem" />
            </div>
          </div>
          <Skeleton width="100%" class="skeleton-video-body" />
          <div class="flex justify-between mt-4">
            <Skeleton width="4rem" height="2rem" />
            <Skeleton width="4rem" height="2rem" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import Skeleton from 'primevue/skeleton'

const props = defineProps({
  name: {
    type: String,
    required: true,
  },
  variant: {
    type: String,
    default: 'section',
    validator: (v) => ['section', 'hero'].includes(v),
  },
  lazy: {
    type: Boolean,
    default: true,
  },
  poster: {
    type: String,
    default: '',
  },
})

const root = ref(null)
const state = ref('idle')
let observer = null

const videoAttrs = computed(() => {
  if (props.variant === 'hero') {
    return {
      controls: true,
      preload: 'metadata',
      poster: props.poster || `/videos/${props.name}-poster.jpg`,
    }
  }
  return {
    autoplay: true,
    loop: true,
    muted: true,
    playsinline: true,
    preload: 'metadata',
  }
})

async function checkVideoExists() {
  if (state.value === 'checking' || state.value === 'present') return
  state.value = 'checking'
  try {
    const res = await fetch(`/videos/${props.name}.webm`, { method: 'HEAD' })
    state.value = res.ok ? 'present' : 'missing'
  } catch {
    state.value = 'missing'
  }
}

function startCheck() {
  if (state.value === 'idle') {
    checkVideoExists()
  }
}

onMounted(() => {
  if (!props.lazy) {
    startCheck()
    return
  }

  observer = new IntersectionObserver(
    (entries) => {
      if (entries.some((e) => e.isIntersecting)) {
        startCheck()
        observer?.disconnect()
      }
    },
    { rootMargin: '200px 0px' },
  )

  if (root.value) {
    observer.observe(root.value)
  }
})

onUnmounted(() => {
  observer?.disconnect()
})
</script>

<style scoped>
.demo-video {
  width: 100%;
  max-width: 720px;
  margin: 0 auto;
  aspect-ratio: 16 / 9;
}

.demo-video__player {
  width: 100%;
  height: 100%;
  border-radius: var(--nt-radius);
  display: block;
  object-fit: cover;
  background: var(--nt-dark-3);
}

.demo-video__skeleton {
  width: 100%;
  height: 100%;
}

.demo-video__skeleton .card {
  height: 100%;
  padding: 0;
  overflow: hidden;
  display: flex;
  min-height: 0;
}

.skeleton-panel {
  width: 100%;
  height: 100%;
  padding: 0.875rem;
  border-radius: var(--nt-radius);
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: var(--nt-dark-2);
  display: flex;
  flex-direction: column;
  min-height: 0;
  box-sizing: border-box;
}

.section-light .skeleton-panel {
  background: #ffffff;
  border-color: #e2e8f0;
}

.flex {
  display: flex;
}

.mb-4 {
  margin-bottom: 1rem;
}

.mb-2 {
  margin-bottom: 0.5rem;
}

.mt-4 {
  margin-top: 1rem;
}

.mr-2 {
  margin-right: 0.5rem;
}

.justify-between {
  justify-content: space-between;
}

.skeleton-video-body {
  flex: 1;
  min-height: 0;
}

.demo-video--hero .demo-video__player {
  object-fit: contain;
}
</style>
