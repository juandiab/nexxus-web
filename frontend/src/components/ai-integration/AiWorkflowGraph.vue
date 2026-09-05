<template>
  <div class="workflow-graph" role="img" :aria-label="caption">
    <p v-if="caption" class="workflow-caption">{{ caption }}</p>

    <div class="workflow-panel">
      <!-- subtle ring backdrop -->
      <div class="workflow-rings" aria-hidden="true">
        <MagicRings
          color="#00A8E0"
          color-two="#007BA7"
          :ring-count="4"
          :speed="0.4"
          :attenuation="14"
          :line-thickness="1.2"
          :base-radius="0.28"
          :radius-step="0.07"
          :scale-rate="0.06"
          :opacity="0.22"
          :noise-amount="0.04"
          :ring-gap="1.3"
          :fade-in="0.8"
          :fade-out="0.6"
        />
      </div>

      <svg
        class="workflow-svg"
        viewBox="0 0 440 200"
        preserveAspectRatio="xMidYMid meet"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="wf-edge" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#007BA7" stop-opacity="0.4" />
            <stop offset="50%" stop-color="#00A8E0" />
            <stop offset="100%" stop-color="#007BA7" stop-opacity="0.4" />
          </linearGradient>
          <radialGradient id="wf-node-glow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#7EDFFF" stop-opacity="0.7" />
            <stop offset="100%" stop-color="#00A8E0" stop-opacity="0" />
          </radialGradient>
          <filter id="wf-glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="2" result="b" />
            <feMerge>
              <feMergeNode in="b" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        <!-- input feeds (abstract data lines, not agents) -->
        <path class="wf-feed f1" d="M 90 36 L 90 72" />
        <path class="wf-feed f2" d="M 220 164 L 220 128" />
        <path class="wf-feed f3" d="M 350 36 L 350 72" />

        <!-- main process spine -->
        <path class="wf-spine-base" d="M 50 100 L 390 100" />
        <path class="wf-spine-active" d="M 50 100 L 390 100" />

        <!-- traveling signals -->
        <circle class="wf-signal s1" cx="50" cy="100" r="3" />
        <circle class="wf-signal s2" cx="50" cy="100" r="2.5" />

        <!-- stage nodes: hex ring + vertex dots (NxConnectionRings language) -->
        <g
          v-for="(node, i) in nodes"
          :key="node.id"
          class="wf-stage"
          :class="[`wf-stage--${node.id}`, { 'wf-stage--human': node.id === 'human' }]"
          :transform="`translate(${nodeX(i)}, 100)`"
        >
          <circle class="wf-stage-halo" r="28" />
          <polygon
            class="wf-stage-hex"
            points="0,-18 15.6,-9 15.6,9 0,18 -15.6,9 -15.6,-9"
          />
          <polygon
            class="wf-stage-hex-inner"
            points="0,-12 10.4,-6 10.4,6 0,12 -10.4,6 -10.4,-6"
          />
          <!-- vertex nodes -->
          <circle class="wf-vertex v1" cx="0" cy="-18" r="2" />
          <circle class="wf-vertex v2" cx="15.6" cy="-9" r="2" />
          <circle class="wf-vertex v3" cx="15.6" cy="9" r="2" />
          <circle class="wf-vertex v4" cx="0" cy="18" r="2" />
          <circle class="wf-vertex v5" cx="-15.6" cy="9" r="2" />
          <circle class="wf-vertex v6" cx="-15.6" cy="-9" r="2" />
          <!-- center pulse -->
          <circle class="wf-stage-core" r="4" />
        </g>
      </svg>

      <div class="workflow-labels">
        <span
          v-for="(node, i) in nodes"
          :key="node.id"
          class="workflow-label"
          :class="{ 'is-human': node.id === 'human' }"
          :style="{ left: `${labelLeft(i)}%` }"
        >
          {{ node.label }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import MagicRings from '@/components/shared/MagicRings.vue'

defineProps({
  nodes: {
    type: Array,
    required: true,
  },
  caption: {
    type: String,
    default: '',
  },
})

const NODE_X = [90, 170, 270, 350]

function nodeX(i) {
  return NODE_X[i] ?? 90
}

function labelLeft(i) {
  const positions = [20.5, 38.6, 61.4, 79.5]
  return positions[i] ?? 20.5
}
</script>

<style scoped>
.workflow-graph {
  width: 100%;
}

.workflow-caption {
  font-size: 0.85rem;
  color: var(--nt-text-muted);
  margin: 0 0 16px;
  line-height: 1.5;
}

.workflow-panel {
  position: relative;
  padding: 32px 16px 44px;
  background: var(--nt-dark-3);
  border: 1px solid var(--nt-border);
  border-radius: var(--nt-radius-lg);
  overflow: hidden;
}

.workflow-rings {
  position: absolute;
  inset: 0;
  opacity: 0.55;
  pointer-events: none;
}

.workflow-svg {
  display: block;
  width: 100%;
  height: auto;
  position: relative;
  z-index: 1;
}

.wf-feed {
  fill: none;
  stroke: rgba(0, 168, 224, 0.18);
  stroke-width: 1;
  stroke-dasharray: 3 5;
}

.wf-feed.f1 { animation: wf-feed-pulse 5s ease-in-out infinite; }
.wf-feed.f2 { animation: wf-feed-pulse 5s ease-in-out infinite -1.6s; }
.wf-feed.f3 { animation: wf-feed-pulse 5s ease-in-out infinite -3.2s; }

@keyframes wf-feed-pulse {
  0%, 100% { stroke-opacity: 0.25; }
  50% { stroke-opacity: 0.7; }
}

.wf-spine-base {
  fill: none;
  stroke: rgba(0, 168, 224, 0.1);
  stroke-width: 1.5;
  stroke-linecap: round;
}

.wf-spine-active {
  fill: none;
  stroke: url(#wf-edge);
  stroke-width: 1.5;
  stroke-linecap: round;
  stroke-dasharray: 6 320;
  filter: url(#wf-glow);
  animation: wf-spine-flow 7s linear infinite;
}

@keyframes wf-spine-flow {
  0% { stroke-dashoffset: 0; }
  100% { stroke-dashoffset: -326; }
}

.wf-signal {
  fill: #7EDFFF;
  filter: drop-shadow(0 0 3px #00A8E0);
}

.wf-signal.s1 { animation: wf-signal-travel 5s linear infinite; }
.wf-signal.s2 { animation: wf-signal-travel 5s linear infinite -2.5s; opacity: 0.55; }

@keyframes wf-signal-travel {
  0% { cx: 50; opacity: 0; }
  6% { opacity: 1; }
  94% { opacity: 1; }
  100% { cx: 390; opacity: 0; }
}

.wf-stage-halo {
  fill: url(#wf-node-glow);
  opacity: 0;
  transition: opacity 0.4s ease;
}

.wf-stage-hex {
  fill: none;
  stroke: rgba(0, 168, 224, 0.35);
  stroke-width: 1.2;
  vector-effect: non-scaling-stroke;
}

.wf-stage-hex-inner {
  fill: none;
  stroke: rgba(0, 123, 167, 0.25);
  stroke-width: 0.8;
  stroke-dasharray: 2 3;
  transform-origin: center;
  animation: wf-hex-spin 12s linear infinite;
}

.wf-stage--human .wf-stage-hex {
  stroke: rgba(126, 223, 255, 0.5);
  stroke-dasharray: 5 3;
}

.wf-stage--human .wf-stage-hex-inner {
  animation: none;
  stroke-dasharray: none;
}

@keyframes wf-hex-spin {
  to { transform: rotate(360deg); }
}

.wf-vertex {
  fill: #7EDFFF;
  opacity: 0.45;
  animation: wf-vertex-seq 6s ease-in-out infinite;
}

.wf-stage .v1 { animation-delay: 0s; }
.wf-stage .v2 { animation-delay: -1s; }
.wf-stage .v3 { animation-delay: -2s; }
.wf-stage .v4 { animation-delay: -3s; }
.wf-stage .v5 { animation-delay: -4s; }
.wf-stage .v6 { animation-delay: -5s; }

@keyframes wf-vertex-seq {
  0%, 80%, 100% { opacity: 0.35; }
  10% { opacity: 1; }
  20% { opacity: 0.35; }
}

.wf-stage-core {
  fill: var(--nt-primary);
  stroke: #7EDFFF;
  stroke-width: 1;
  filter: drop-shadow(0 0 4px rgba(0, 168, 224, 0.5));
}

.wf-stage--human .wf-stage-core {
  fill: rgba(0, 123, 167, 0.5);
  stroke-dasharray: 2 2;
}

.wf-stage:nth-child(n) .wf-stage-halo {
  opacity: 0.35;
}

.workflow-labels {
  position: relative;
  height: 22px;
  margin-top: 8px;
  z-index: 1;
}

.workflow-label {
  position: absolute;
  transform: translateX(-50%);
  font-family: var(--font-heading);
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  color: var(--nt-text-muted);
  white-space: nowrap;
}

.workflow-label.is-human {
  color: #7EDFFF;
}

@media (max-width: 480px) {
  .workflow-label {
    font-size: 0.58rem;
    letter-spacing: 0.03em;
  }
}

@media (prefers-reduced-motion: reduce) {
  .wf-spine-active,
  .wf-signal,
  .wf-vertex,
  .wf-stage-hex-inner,
  .wf-feed {
    animation: none !important;
  }

  .wf-spine-active {
    stroke-dasharray: none;
    opacity: 0.65;
  }

  .wf-signal {
    cx: 220;
    opacity: 0.75;
  }

  .wf-stage-halo {
    opacity: 0.4 !important;
  }
}
</style>
