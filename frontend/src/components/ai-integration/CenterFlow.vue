<template>
  <div
    ref="containerRef"
    class="center-flow"
    :class="className"
    role="img"
    :aria-label="ariaLabel"
  >
    <svg
      class="center-flow__svg"
      :width="dimensions.width"
      :height="dimensions.height"
      aria-hidden="true"
    >
      <defs>
        <filter
          :id="`${uid}-pulse-glow`"
          x="-100%"
          y="-100%"
          width="300%"
          height="300%"
        >
          <feGaussianBlur stdDeviation="3" result="blur" />
          <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
        <linearGradient
          v-for="segment in pulseSegments"
          :key="`grad-${segment.id}`"
          :id="`${uid}-pulse-grad-${segment.id}`"
          :x1="segment.startPoint.x"
          :y1="segment.startPoint.y"
          :x2="segment.endPoint.x"
          :y2="segment.endPoint.y"
          gradientUnits="userSpaceOnUse"
        >
          <stop offset="0%" :stop-color="pulseColor" stop-opacity="0" />
          <stop
            :offset="`${tailStop}%`"
            :stop-color="pulseColor"
            stop-opacity="1"
          />
          <stop
            :offset="`${headStop}%`"
            :stop-color="pulseColor"
            stop-opacity="1"
          />
          <stop offset="100%" :stop-color="pulseColor" stop-opacity="0" />
        </linearGradient>
      </defs>

      <path
        v-for="(node, i) in nodePositions"
        :key="`line-${i}`"
        :d="generatePathD(node, center)"
        fill="none"
        :stroke="lineColor"
        :stroke-width="lineWidth"
        stroke-linecap="round"
      />

      <g v-for="segment in pulseSegments" :key="segment.id">
        <path
          :d="segment.d"
          fill="none"
          :stroke="`url(#${uid}-pulse-grad-${segment.id})`"
          :stroke-width="pulseWidth * 3"
          stroke-linecap="round"
          :opacity="segment.opacity * 0.4"
          :filter="`url(#${uid}-pulse-glow)`"
        />
        <path
          :d="segment.d"
          fill="none"
          :stroke="`url(#${uid}-pulse-grad-${segment.id})`"
          :stroke-width="pulseWidth"
          stroke-linecap="round"
          :opacity="segment.opacity"
        />
      </g>
    </svg>

    <div
      v-for="(node, i) in nodePositions"
      :key="`node-${i}`"
      class="center-flow__node"
      :style="nodeWrapperStyle(node)"
    >
      <div class="center-flow__node-box" :style="nodeBoxStyle">
        <slot :name="`node-${i}`" :item="visibleNodeItems[i]" :index="i">
          <slot name="node" :item="visibleNodeItems[i]" :index="i">
            <span class="center-flow__node-dot" />
          </slot>
        </slot>
      </div>
      <span
        v-if="visibleNodeItems[i]?.label"
        class="center-flow__node-caption"
      >
        {{ visibleNodeItems[i].label }}
      </span>
    </div>

    <div
      ref="glowRef"
      class="center-flow__center"
      :style="centerBoxStyle"
    >
      <div class="center-flow__center-inner">
        <slot name="center">
          <slot>
            <svg
              class="center-flow__layers-icon"
              viewBox="0 0 24 24"
              fill="none"
              aria-hidden="true"
            >
              <path
                d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"
                stroke="currentColor"
                stroke-width="1.5"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </slot>
        </slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  computed,
  onBeforeUnmount,
  onMounted,
  ref,
  useId,
  watch,
} from 'vue'

const BASE_GLOW = 40
const FADE_THRESHOLD = 0.15

const props = defineProps({
  nodeItems: {
    type: Array,
    default: () => Array(8).fill({}),
  },
  centerSize: {
    type: Number,
    default: 120,
  },
  nodeSize: {
    type: Number,
    default: 60,
  },
  pulseDuration: {
    type: Number,
    default: 5,
  },
  pulseInterval: {
    type: Number,
    default: 10,
  },
  pulseLength: {
    type: Number,
    default: 0.4,
  },
  lineWidth: {
    type: Number,
    default: 2,
  },
  pulseWidth: {
    type: Number,
    default: 1,
  },
  pulseSoftness: {
    type: Number,
    default: 10,
  },
  lineColor: {
    type: String,
    default: 'rgba(0, 168, 224, 0.14)',
  },
  pulseColor: {
    type: String,
    default: '#00A8E0',
  },
  glowColor: {
    type: String,
    default: '#00A8E0',
  },
  maxGlowIntensity: {
    type: Number,
    default: 25,
  },
  glowDecay: {
    type: Number,
    default: 0.95,
  },
  borderRadius: {
    type: Number,
    default: 35,
  },
  nodeDistance: {
    type: Number,
    default: 0.7,
  },
  disableBlinking: {
    type: Boolean,
    default: false,
  },
  className: {
    type: String,
    default: '',
  },
  ariaLabel: {
    type: String,
    default: 'AI agents connected to a central core',
  },
})

const uid = useId().replace(/:/g, '')

const containerRef = ref(null)
const glowRef = ref(null)
const glowIntensityRef = ref(0)
const pathCache = new Map()
const dimensions = ref({ width: 800, height: 600 })
const pulses = ref([])
const pulseSegments = ref([])

let resizeObserver = null
let glowFrameId = null
let pulseCleanupFrameId = null
let segmentFrameId = null
let spawnTimeouts = []
let mounted = false
let reducedMotion = false

const nodeCount = computed(() => {
  const total = props.nodeItems.length
  const w = dimensions.value.width
  const max = w < 480 ? 4 : total
  return Math.max(2, Math.min(14, max))
})

const visibleNodeItems = computed(() =>
  props.nodeItems.slice(0, nodeCount.value),
)

const layoutScale = computed(() => {
  const w = dimensions.value.width
  if (w < 360) return 0.58
  if (w < 480) return 0.68
  if (w < 640) return 0.78
  if (w < 900) return 0.88
  return 1
})

const effectiveCenterSize = computed(() => props.centerSize * layoutScale.value)
const effectiveNodeSize = computed(() => props.nodeSize * layoutScale.value)
const effectiveNodeDistance = computed(() =>
  props.nodeDistance * (layoutScale.value < 0.8 ? 0.88 : 1),
)
const effectiveBorderRadius = computed(() => props.borderRadius * layoutScale.value)

const softness = computed(() => props.pulseSoftness / 10)
const tailStop = computed(() => softness.value * 30)
const headStop = computed(() => 100 - softness.value * 20)

const normalizedNodes = computed(() =>
  generateNodePositions(nodeCount.value, effectiveNodeDistance.value),
)

const center = computed(() => ({
  x: dimensions.value.width / 2,
  y: dimensions.value.height / 2,
}))

const nodePositions = computed(() =>
  normalizedNodes.value.map((node) => ({
    x: (node.x / 100) * dimensions.value.width,
    y: (node.y / 100) * dimensions.value.height,
  })),
)

const centerBoxStyle = computed(() => ({
  left: `${center.value.x}px`,
  top: `${center.value.y}px`,
  width: `${effectiveCenterSize.value}px`,
  height: `${effectiveCenterSize.value}px`,
  borderRadius: `${effectiveBorderRadius.value}px`,
}))

function generateNodePositions(count, distance) {
  const clampedCount = Math.max(2, Math.min(14, count))
  const nodes = new Array(clampedCount)
  const angleStep = (Math.PI * 2) / clampedCount
  const radius = distance * 45

  for (let i = 0; i < clampedCount; i++) {
    const angle = i * angleStep - Math.PI / 2
    nodes[i] = {
      x: 50 + Math.cos(angle) * radius,
      y: 50 + Math.sin(angle) * radius,
    }
  }
  return nodes
}

function generatePathD(from, to) {
  const dx = to.x - from.x
  const dy = to.y - from.y
  return `M ${from.x} ${from.y} C ${from.x + dx * 0.4} ${from.y + dy * 0.1}, ${from.x + dx * 0.6} ${to.y - dy * 0.1}, ${to.x} ${to.y}`
}

function nodeWrapperStyle(node) {
  return {
    left: `${node.x}px`,
    top: `${node.y}px`,
  }
}

function nodeBoxStyle() {
  const r = effectiveBorderRadius.value * 0.6
  const size = effectiveNodeSize.value * 0.72
  return {
    width: `${size}px`,
    height: `${size}px`,
    borderRadius: `${r}px`,
  }
}

function updateDimensions() {
  if (!containerRef.value) return
  const { width, height } = containerRef.value.getBoundingClientRect()
  if (width > 0 && height > 0) {
    dimensions.value = { width, height }
  }
}

function onPulseArrive() {
  if (props.disableBlinking || reducedMotion) return
  glowIntensityRef.value = Math.min(
    glowIntensityRef.value + props.maxGlowIntensity * 0.6,
    props.maxGlowIntensity,
  )
}

function clearSpawnTimeouts() {
  spawnTimeouts.forEach(clearTimeout)
  spawnTimeouts = []
}

function startPulseSpawning() {
  clearSpawnTimeouts()
  if (reducedMotion) return

  const spawnPulseForPath = (pathIndex) => {
    if (!mounted) return
    pulses.value = [
      ...pulses.value,
      {
        id: `${pathIndex}-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`,
        pathIndex,
        startTime: Date.now(),
      },
    ]
    const timeout = setTimeout(
      () => spawnPulseForPath(pathIndex),
      props.pulseInterval * 1000 * (0.7 + Math.random() * 0.6),
    )
    spawnTimeouts.push(timeout)
  }

  nodePositions.value.forEach((_, pathIndex) => {
    const timeout = setTimeout(
      () => spawnPulseForPath(pathIndex),
      Math.random() * props.pulseInterval * 1000,
    )
    spawnTimeouts.push(timeout)
  })
}

function startGlowLoop() {
  const updateGlow = () => {
    if (!mounted) return
    if (glowRef.value) {
      const dynamicIntensity = glowIntensityRef.value
      const totalIntensity = BASE_GLOW + dynamicIntensity
      const spread = totalIntensity * 0.8
      const blur = totalIntensity * 1.5
      const alpha = Math.min(255, Math.floor(totalIntensity * 4))
        .toString(16)
        .padStart(2, '0')

      glowRef.value.style.boxShadow = `0 0 ${blur}px ${spread}px ${props.glowColor}40, 0 0 ${blur * 2}px ${spread * 1.5}px ${props.glowColor}20, inset 0 0 ${blur * 0.5}px ${props.glowColor}30`
      glowRef.value.style.borderColor = `${props.glowColor}${alpha}`

      glowIntensityRef.value =
        dynamicIntensity > 0.5 ? dynamicIntensity * props.glowDecay : 0
    }
    glowFrameId = requestAnimationFrame(updateGlow)
  }
  glowFrameId = requestAnimationFrame(updateGlow)
}

function startPulseCleanupLoop() {
  const duration = props.pulseDuration * 1000

  const animate = () => {
    if (!mounted) return
    const now = Date.now()
    const next = pulses.value.filter((pulse) => {
      if ((now - pulse.startTime) / duration >= 1) {
        onPulseArrive()
        return false
      }
      return true
    })
    if (next.length !== pulses.value.length) {
      pulses.value = next
    }
    pulseCleanupFrameId = requestAnimationFrame(animate)
  }
  pulseCleanupFrameId = requestAnimationFrame(animate)
}

function startSegmentLoop() {
  const duration = props.pulseDuration * 1000

  const calculateSegments = () => {
    if (!mounted) return
    const now = Date.now()
    const segments = []
    const centerPt = center.value

    for (const pulse of pulses.value) {
      const from = nodePositions.value[pulse.pathIndex]
      if (!from) continue

      let path = pathCache.get(pulse.pathIndex)
      if (!path) {
        path = document.createElementNS('http://www.w3.org/2000/svg', 'path')
        path.setAttribute('d', generatePathD(from, centerPt))
        pathCache.set(pulse.pathIndex, path)
      }

      const progress = Math.min((now - pulse.startTime) / duration, 1)
      if (progress <= 0 || progress >= 1) continue

      const length = path.getTotalLength()
      const headPos = progress
      const tailPos = Math.max(0, progress - props.pulseLength)

      const points = []
      for (let i = 0; i <= 8; i++) {
        const point = path.getPointAtLength(
          length * (tailPos + (headPos - tailPos) * (i / 8)),
        )
        points.push({ x: point.x, y: point.y })
      }

      if (points.length < 2) continue

      const opacity =
        Math.min(1, progress / FADE_THRESHOLD) *
        Math.min(1, (1 - progress) / FADE_THRESHOLD)

      segments.push({
        id: pulse.id,
        d:
          `M ${points[0].x} ${points[0].y}` +
          points
            .slice(1)
            .map((p) => ` L ${p.x} ${p.y}`)
            .join(''),
        opacity,
        startPoint: points[0],
        endPoint: points[points.length - 1],
      })
    }

    pulseSegments.value = segments
    segmentFrameId = requestAnimationFrame(calculateSegments)
  }

  segmentFrameId = requestAnimationFrame(calculateSegments)
}

function stopAnimationLoops() {
  if (glowFrameId != null) {
    cancelAnimationFrame(glowFrameId)
    glowFrameId = null
  }
  if (pulseCleanupFrameId != null) {
    cancelAnimationFrame(pulseCleanupFrameId)
    pulseCleanupFrameId = null
  }
  if (segmentFrameId != null) {
    cancelAnimationFrame(segmentFrameId)
    segmentFrameId = null
  }
  clearSpawnTimeouts()
}

function startAnimations() {
  stopAnimationLoops()
  pathCache.clear()
  pulses.value = []
  pulseSegments.value = []
  startGlowLoop()
  if (!reducedMotion) {
    startPulseSpawning()
    startPulseCleanupLoop()
    startSegmentLoop()
  }
}

onMounted(() => {
  mounted = true
  reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  updateDimensions()

  if (containerRef.value && typeof ResizeObserver !== 'undefined') {
    resizeObserver = new ResizeObserver(updateDimensions)
    resizeObserver.observe(containerRef.value)
  } else {
    window.addEventListener('resize', updateDimensions)
  }

  startAnimations()
})

onBeforeUnmount(() => {
  mounted = false
  stopAnimationLoops()
  resizeObserver?.disconnect()
  window.removeEventListener('resize', updateDimensions)
})

watch(
  () => [nodePositions.value, center.value, props.pulseInterval],
  () => {
    pathCache.clear()
    if (mounted) startPulseSpawning()
  },
  { deep: true },
)

watch(
  () => props.pulseDuration,
  () => {
    if (!mounted) return
    if (pulseCleanupFrameId != null) cancelAnimationFrame(pulseCleanupFrameId)
    if (segmentFrameId != null) cancelAnimationFrame(segmentFrameId)
    if (!reducedMotion) {
      startPulseCleanupLoop()
      startSegmentLoop()
    }
  },
)
</script>

<style scoped>
.center-flow {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 280px;
  overflow: visible;
  background: transparent;
}

.center-flow__svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: visible;
}

.center-flow__node {
  position: absolute;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  z-index: 1;
  overflow: visible;
  pointer-events: none;
}

.center-flow__node-box {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: rgba(28, 28, 30, 0.92);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(0, 168, 224, 0.18);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.35);
}

.center-flow__node-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(0, 168, 224, 0.55);
  box-shadow: 0 0 8px rgba(0, 168, 224, 0.45);
}

.center-flow__node-caption {
  font-family: var(--font-heading);
  font-size: clamp(0.58rem, 1.6vw, 0.72rem);
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--nt-text-light);
  text-align: center;
  line-height: 1.25;
  max-width: 5.5rem;
  white-space: normal;
  overflow: visible;
  word-break: break-word;
}

.center-flow__center {
  position: absolute;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(28, 28, 30, 0.95);
  backdrop-filter: blur(12px);
  border: 2px solid rgba(0, 168, 224, 0.15);
  box-shadow: 0 0 20px 5px rgba(0, 168, 224, 0.08);
  z-index: 2;
  transition: border-color 0.3s ease;
}

.center-flow__center-inner {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 82%;
  height: auto;
  min-width: 0;
  padding: 0 4px;
  color: var(--nt-primary-l);
}
.center-flow__center-inner :slotted(*) {
  white-space: nowrap;
}

.center-flow__layers-icon {
  width: 100%;
  height: 100%;
}

@media (prefers-reduced-motion: reduce) {
  .center-flow__center {
    box-shadow: 0 0 24px 8px rgba(0, 168, 224, 0.2);
    border-color: rgba(0, 168, 224, 0.35);
  }
}
</style>
