<template>
  <div
    class="ld-nexus"
    :class="`ld-nexus--${size}`"
    aria-hidden="true"
  >
    <svg
      class="ld-nexus__svg"
      viewBox="0 0 56 56"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <linearGradient id="ldnx-edge" x1="8" y1="6" x2="48" y2="50" gradientUnits="userSpaceOnUse">
          <stop offset="0" stop-color="var(--ldnx-cyan-300)" />
          <stop offset="1" stop-color="var(--ldnx-blue-500)" />
        </linearGradient>
        <radialGradient id="ldnx-node-glow" cx="0.5" cy="0.5" r="0.5">
          <stop offset="0" stop-color="var(--ldnx-cyan-300)" stop-opacity="0.9" />
          <stop offset="1" stop-color="var(--ldnx-cyan-300)" stop-opacity="0" />
        </radialGradient>
      </defs>

      <!-- outer static hex frame (always visible, incl. reduced-motion) -->
      <polygon
        class="ld-nexus__hex-base"
        points="28,4 48,16 48,40 28,52 8,40 8,16"
      />

      <!-- slow inner rotation group (paused under reduced-motion) -->
      <g class="ld-nexus__spin">
        <polygon
          class="ld-nexus__hex-inner"
          points="28,10 42,18 42,38 28,46 14,38 14,18"
        />
      </g>

      <!-- traveling light pulse along the outer edge -->
      <polygon
        class="ld-nexus__pulse"
        points="28,4 48,16 48,40 28,52 8,40 8,16"
      />

      <!-- N letterform in negative space -->
      <g class="ld-nexus__letter">
        <path d="M 22 17 L 22 39" />
        <path d="M 34 17 L 34 39" />
        <path d="M 22 18 L 34 38" />
      </g>

      <!-- vertex nodes, sequenced pulse -->
      <circle class="ld-nexus__node-glow n1" cx="28" cy="4" r="6" />
      <circle class="ld-nexus__node-glow n2" cx="48" cy="16" r="6" />
      <circle class="ld-nexus__node-glow n3" cx="48" cy="40" r="6" />
      <circle class="ld-nexus__node-glow n4" cx="28" cy="52" r="6" />
      <circle class="ld-nexus__node-glow n5" cx="8" cy="40" r="6" />
      <circle class="ld-nexus__node-glow n6" cx="8" cy="16" r="6" />

      <circle class="ld-nexus__node n1" cx="28" cy="4" r="2.1" />
      <circle class="ld-nexus__node n2" cx="48" cy="16" r="2.1" />
      <circle class="ld-nexus__node n3" cx="48" cy="40" r="2.1" />
      <circle class="ld-nexus__node n4" cx="28" cy="52" r="2.1" />
      <circle class="ld-nexus__node n5" cx="8" cy="40" r="2.1" />
      <circle class="ld-nexus__node n6" cx="8" cy="16" r="2.1" />

      <!-- hover radar ping (dormant until :hover/:focus-visible) -->
      <polygon
        class="ld-nexus__ping"
        points="28,4 48,16 48,40 28,52 8,40 8,16"
      />
    </svg>
  </div>
</template>

<script setup>
defineProps({
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['nav', 'md', 'lg'].includes(v),
  },
})
</script>

<style scoped>
.ld-nexus {
  --ldnx-blue-500: var(--nx-blue-500, #3D8BFD);
  --ldnx-cyan-400: var(--nx-cyan-400, #38C6F4);
  --ldnx-cyan-300: var(--nx-cyan-300, #7EDFFF);
  position: relative;
  width: 56px;
  height: 56px;
  color: var(--ldnx-cyan-400);
}

.ld-nexus__svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  overflow: visible;
}

.ld-nexus--nav {
  transform: scale(0.92);
  transform-origin: center center;
}

.ld-nexus--lg {
  transform: scale(2.4);
}

.ld-nexus--md {
  transform: scale(1.6);
}

/* ---------- static hex frame ---------- */
.ld-nexus__hex-base {
  stroke: currentColor;
  stroke-width: 1.4;
  opacity: 0.4;
  vector-effect: non-scaling-stroke;
}

.ld-nexus__hex-inner {
  stroke: var(--ldnx-blue-500);
  stroke-width: 1;
  stroke-dasharray: 2 4;
  opacity: 0.35;
  vector-effect: non-scaling-stroke;
}

/* ---------- slow inner rotation (transform/opacity only) ---------- */
.ld-nexus__spin {
  transform-origin: 28px 28px;
  animation: ldnx-spin 10s linear infinite;
}

@keyframes ldnx-spin {
  to { transform: rotate(360deg); }
}

/* ---------- traveling edge pulse ---------- */
.ld-nexus__pulse {
  stroke: url(#ldnx-edge);
  stroke-width: 2.2;
  stroke-linecap: round;
  fill: none;
  vector-effect: non-scaling-stroke;
  /* perimeter of the hex points (~124px), dash = short bright segment travelling around */
  stroke-dasharray: 14 220;
  stroke-dashoffset: 0;
  opacity: 0.9;
  animation: ldnx-travel 7s linear infinite;
  filter: drop-shadow(0 0 3px var(--ldnx-cyan-300));
}

@keyframes ldnx-travel {
  0% { stroke-dashoffset: 0; }
  100% { stroke-dashoffset: -234; }
}

/* ---------- N letterform ---------- */
.ld-nexus__letter {
  stroke: currentColor;
  stroke-width: 2.6;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
  opacity: 0.85;
}

/* ---------- vertex nodes ---------- */
.ld-nexus__node {
  fill: var(--ldnx-cyan-300);
  animation: ldnx-node-pulse 8s ease-in-out infinite;
}

.ld-nexus__node-glow {
  fill: url(#ldnx-node-glow);
  animation: ldnx-node-glow 8s ease-in-out infinite;
  transform-origin: center;
  transform-box: fill-box;
}

/* stagger sequence around the six vertices, ~1.3s apart across an 8s loop */
.n1 { animation-delay: 0s; }
.n2 { animation-delay: -1.33s; }
.n3 { animation-delay: -2.66s; }
.n4 { animation-delay: -4s; }
.n5 { animation-delay: -5.33s; }
.n6 { animation-delay: -6.66s; }

@keyframes ldnx-node-pulse {
  0%, 84%, 100% { opacity: 0.75; }
  8% { opacity: 1; }
  16% { opacity: 0.75; }
}

@keyframes ldnx-node-glow {
  0%, 84%, 100% { opacity: 0.25; transform: scale(0.85); }
  8% { opacity: 0.85; transform: scale(1.35); }
  16% { opacity: 0.25; transform: scale(0.85); }
}

/* ---------- hover / focus: quick radar ping ---------- */
.ld-nexus__ping {
  stroke: var(--ldnx-cyan-300);
  stroke-width: 1.6;
  fill: none;
  opacity: 0;
  transform-origin: 28px 28px;
  vector-effect: non-scaling-stroke;
}

.ld-nexus:hover .ld-nexus__ping,
.ld-nexus:focus-visible .ld-nexus__ping {
  animation: ldnx-ping 0.9s cubic-bezier(0.2, 0.7, 0.3, 1);
}

.ld-nexus:hover .ld-nexus__pulse,
.ld-nexus:focus-visible .ld-nexus__pulse {
  animation-duration: 2.2s;
  filter: drop-shadow(0 0 5px var(--ldnx-cyan-300));
}

@keyframes ldnx-ping {
  0% { transform: scale(0.75); opacity: 0.9; }
  100% { transform: scale(1.35); opacity: 0; }
}

/* ---------- reduced motion: static, finished-looking hexagon ---------- */
@media (prefers-reduced-motion: reduce) {
  .ld-nexus__spin {
    animation: none !important;
  }

  .ld-nexus__pulse {
    animation: none !important;
    stroke-dasharray: none;
    stroke: url(#ldnx-edge);
    opacity: 0.7;
  }

  .ld-nexus__node,
  .ld-nexus__node-glow {
    animation: none !important;
    opacity: 0.85;
  }

  .ld-nexus__node-glow {
    opacity: 0.35;
    transform: scale(1);
  }

  .ld-nexus:hover .ld-nexus__ping,
  .ld-nexus:focus-visible .ld-nexus__ping {
    animation: none !important;
    opacity: 0;
  }

  .ld-nexus:hover .ld-nexus__pulse,
  .ld-nexus:focus-visible .ld-nexus__pulse {
    filter: none;
  }
}
</style>
