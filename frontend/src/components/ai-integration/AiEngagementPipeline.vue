<template>
  <div
    class="engagement-pipeline"
    role="img"
    :aria-label="caption"
  >
    <p v-if="caption" class="pipeline-caption">{{ caption }}</p>

    <div class="pipeline-track">
      <!-- brand ring backdrop -->
      <div class="pipeline-rings" aria-hidden="true">
        <MagicRings
          color="#00A8E0"
          color-two="#007BA7"
          :ring-count="5"
          :speed="0.5"
          :attenuation="13"
          :line-thickness="1.4"
          :base-radius="0.3"
          :radius-step="0.08"
          :scale-rate="0.07"
          :opacity="0.2"
          :noise-amount="0.04"
          :ring-gap="1.4"
          :fade-in="0.75"
          :fade-out="0.55"
        />
      </div>

      <svg
        class="pipeline-svg"
        viewBox="0 0 800 130"
        preserveAspectRatio="xMidYMid meet"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="pipe-edge" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#007BA7" stop-opacity="0.3" />
            <stop offset="50%" stop-color="#00A8E0" stop-opacity="0.85" />
            <stop offset="100%" stop-color="#007BA7" stop-opacity="0.3" />
          </linearGradient>
          <radialGradient id="pipe-node-glow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#00A8E0" stop-opacity="0.85" />
            <stop offset="100%" stop-color="#007BA7" stop-opacity="0" />
          </radialGradient>
          <filter id="pipe-glow-filter" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        <line x1="80" y1="65" x2="720" y2="65" class="pipe-line-base" />
        <line x1="80" y1="65" :x2="progressX" y2="65" class="pipe-line-active" />

        <!-- traveling ring pulse -->
        <circle class="pipe-pulse" :cx="pulseX" cy="65" r="5" />
        <circle class="pipe-pulse-ring" :cx="pulseX" cy="65" r="12" />

        <!-- hex ring nodes (NxConnectionRings language) -->
        <g
          v-for="(step, i) in steps"
          :key="step.name"
          class="pipe-node-group"
          :class="{ active: activeIndex === i, passed: activeIndex > i }"
          :transform="`translate(${nodeX(i)}, 65)`"
        >
          <circle class="pipe-node-halo" r="26" />
          <polygon
            class="pipe-node-hex"
            points="0,-16 13.9,-8 13.9,8 0,16 -13.9,8 -13.9,-8"
          />
          <polygon
            class="pipe-node-hex-inner"
            points="0,-10 8.7,-5 8.7,5 0,10 -8.7,5 -8.7,-5"
          />
          <circle class="pipe-node-core" r="4" />
          <text class="pipe-node-num" y="4" text-anchor="middle">{{ i + 1 }}</text>
        </g>
      </svg>

      <div class="pipeline-labels">
        <button
          v-for="(step, i) in steps"
          :key="step.name"
          type="button"
          class="pipeline-label"
          :class="{ active: activeIndex === i }"
          :aria-pressed="activeIndex === i"
          @click="selectStep(i)"
          @mouseenter="pauseCycle"
          @mouseleave="resumeCycle"
        >
          <span class="label-name">{{ step.name }}</span>
          <span class="label-desc">{{ step.desc }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import MagicRings from '@/components/shared/MagicRings.vue'

const props = defineProps({
  steps: {
    type: Array,
    required: true,
  },
  caption: {
    type: String,
    default: '',
  },
  cycleMs: {
    type: Number,
    default: 4500,
  },
})

const NODE_POSITIONS = [80, 293, 507, 720]
const activeIndex = ref(0)
let cycleTimer = null
let paused = false
let prefersReducedMotion = false

const progressX = computed(() => {
  const idx = activeIndex.value
  if (idx <= 0) return NODE_POSITIONS[0]
  const start = NODE_POSITIONS[idx - 1]
  const end = NODE_POSITIONS[idx]
  return start + (end - start) * 0.85
})

const pulseX = computed(() => NODE_POSITIONS[activeIndex.value])

function nodeX(i) {
  return NODE_POSITIONS[i] ?? 80
}

function selectStep(i) {
  activeIndex.value = i
  resetCycle()
}

function pauseCycle() {
  paused = true
}

function resumeCycle() {
  paused = false
}

function resetCycle() {
  if (prefersReducedMotion) return
  clearInterval(cycleTimer)
  cycleTimer = setInterval(tick, props.cycleMs)
}

function tick() {
  if (paused) return
  activeIndex.value = (activeIndex.value + 1) % props.steps.length
}

onMounted(() => {
  prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (!prefersReducedMotion) {
    cycleTimer = setInterval(tick, props.cycleMs)
  }
})

onBeforeUnmount(() => {
  clearInterval(cycleTimer)
})
</script>

<style scoped>
.engagement-pipeline {
  width: 100%;
}

.pipeline-caption {
  text-align: center;
  font-size: 0.9rem;
  color: var(--nt-text-muted);
  margin: 0 0 28px;
  max-width: 520px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.6;
}

.pipeline-track {
  position: relative;
  padding: 28px 16px 0;
  background: linear-gradient(180deg, rgba(0, 123, 167, 0.06) 0%, transparent 100%);
  border: 1px solid var(--nt-border);
  border-radius: var(--nt-radius-lg);
  overflow: hidden;
}

.pipeline-rings {
  position: absolute;
  inset: 0;
  opacity: 0.5;
  pointer-events: none;
}

.pipeline-track::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 50% 0%, rgba(0, 168, 224, 0.07) 0%, transparent 55%);
  pointer-events: none;
  z-index: 0;
}

.pipeline-svg {
  display: block;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  height: auto;
  min-height: 90px;
  position: relative;
  z-index: 1;
}

.pipe-line-base {
  stroke: rgba(0, 168, 224, 0.12);
  stroke-width: 1.5;
  stroke-linecap: round;
}

.pipe-line-active {
  stroke: url(#pipe-edge);
  stroke-width: 2;
  stroke-linecap: round;
  filter: url(#pipe-glow-filter);
  transition: x2 0.7s cubic-bezier(0.4, 0, 0.2, 1);
}

.pipe-pulse {
  fill: #7EDFFF;
  filter: drop-shadow(0 0 5px #00A8E0);
  transition: cx 0.7s cubic-bezier(0.4, 0, 0.2, 1);
  animation: pipe-pulse-beat 2s ease-in-out infinite;
}

.pipe-pulse-ring {
  fill: none;
  stroke: rgba(0, 168, 224, 0.35);
  stroke-width: 1;
  transition: cx 0.7s cubic-bezier(0.4, 0, 0.2, 1);
  animation: pipe-ring-expand 2s ease-out infinite;
}

@keyframes pipe-pulse-beat {
  0%, 100% { opacity: 0.75; }
  50% { opacity: 1; }
}

@keyframes pipe-ring-expand {
  0% { r: 8; opacity: 0.6; }
  100% { r: 20; opacity: 0; }
}

.pipe-node-halo {
  fill: url(#pipe-node-glow);
  opacity: 0;
  transition: opacity 0.5s ease;
}

.pipe-node-hex {
  fill: none;
  stroke: rgba(0, 168, 224, 0.3);
  stroke-width: 1.4;
  vector-effect: non-scaling-stroke;
  transition: stroke 0.4s ease;
}

.pipe-node-hex-inner {
  fill: none;
  stroke: rgba(0, 123, 167, 0.2);
  stroke-width: 0.8;
  stroke-dasharray: 2 4;
  transform-origin: center;
  transition: stroke 0.4s ease;
}

.pipe-node-core {
  fill: var(--nt-dark-3);
  stroke: rgba(0, 168, 224, 0.45);
  stroke-width: 1.2;
  transition: fill 0.4s ease, stroke 0.4s ease;
}

.pipe-node-num {
  font-family: var(--font-heading);
  font-size: 10px;
  font-weight: 800;
  fill: rgba(255, 255, 255, 0.45);
  pointer-events: none;
  transition: fill 0.4s ease;
}

.pipe-node-group.active .pipe-node-halo {
  opacity: 0.9;
  animation: node-halo-pulse 2.5s ease-in-out infinite;
}

.pipe-node-group.active .pipe-node-hex {
  stroke: #00A8E0;
  stroke-width: 1.8;
  filter: drop-shadow(0 0 4px rgba(0, 168, 224, 0.5));
}

.pipe-node-group.active .pipe-node-hex-inner {
  stroke: rgba(126, 223, 255, 0.45);
  animation: hex-inner-spin 10s linear infinite;
}

.pipe-node-group.active .pipe-node-core {
  fill: #007BA7;
  stroke: #7EDFFF;
}

.pipe-node-group.active .pipe-node-num {
  fill: white;
}

.pipe-node-group.passed .pipe-node-hex {
  stroke: rgba(0, 168, 224, 0.55);
}

.pipe-node-group.passed .pipe-node-core {
  fill: rgba(0, 123, 167, 0.55);
  stroke: rgba(0, 168, 224, 0.65);
}

.pipe-node-group.passed .pipe-node-num {
  fill: rgba(255, 255, 255, 0.85);
}

@keyframes node-halo-pulse {
  0%, 100% { transform: scale(1); opacity: 0.65; }
  50% { transform: scale(1.12); opacity: 1; }
}

@keyframes hex-inner-spin {
  to { transform: rotate(360deg); }
}

.pipeline-labels {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  padding: 20px 8px 24px;
  position: relative;
  z-index: 1;
}

.pipeline-label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 14px 12px;
  border: 1px solid transparent;
  border-radius: 10px;
  background: transparent;
  cursor: pointer;
  text-align: center;
  transition: background 0.3s ease, border-color 0.3s ease;
  font-family: inherit;
}

.pipeline-label:hover {
  background: rgba(0, 123, 167, 0.08);
  border-color: rgba(0, 168, 224, 0.15);
}

.pipeline-label.active {
  background: rgba(0, 123, 167, 0.14);
  border-color: rgba(0, 168, 224, 0.35);
}

.label-name {
  font-family: var(--font-heading);
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--nt-white);
  letter-spacing: 0.02em;
}

.label-desc {
  font-size: 0.75rem;
  color: var(--nt-text-muted);
  line-height: 1.45;
}

@media (max-width: 768px) {
  .pipeline-labels {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .pipeline-labels {
    grid-template-columns: 1fr;
  }
}

@media (prefers-reduced-motion: reduce) {
  .pipe-pulse,
  .pipe-pulse-ring,
  .pipe-node-group.active .pipe-node-halo,
  .pipe-node-group.active .pipe-node-hex-inner {
    animation: none !important;
  }

  .pipe-node-group.active .pipe-node-halo {
    opacity: 0.7;
  }
}
</style>
