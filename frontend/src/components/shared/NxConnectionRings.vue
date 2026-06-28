<template>
  <div
    class="ld-nexus"
    :class="`ld-nexus--${size}`"
    aria-hidden="true"
  >
    <i></i><i></i><i></i>
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
  --ink: currentColor;
  --ring-width: 1px;
  position: relative;
  width: 56px;
  height: 56px;
  color: var(--nt-primary-l);
}

.ld-nexus::before {
  content: "";
  position: absolute;
  inset: 22px;
  border-radius: 50%;
  background: var(--ink);
  box-shadow:
    0 -18px 0 -3px var(--ink),
    15px 10px 0 -3px var(--ink),
    -15px 10px 0 -3px var(--ink);
}

.ld-nexus i {
  position: absolute;
  inset: 4px;
  border: var(--ring-width) solid transparent;
  border-top-color: var(--ink);
  border-right-color: var(--ink);
  border-radius: 50%;
  opacity: .85;
}

.ld-nexus i:nth-child(1) {
  animation: nexus-spin 1.4s linear infinite;
}

.ld-nexus i:nth-child(2) {
  inset: 10px;
  animation: nexus-spin 1.1s linear infinite reverse;
  opacity: .6;
}

.ld-nexus i:nth-child(3) {
  inset: 16px;
  animation: nexus-pulse .9s ease-in-out infinite;
  opacity: .35;
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

@keyframes nexus-spin {
  to { transform: rotate(360deg); }
}

@keyframes nexus-pulse {
  0%, 100% { transform: scale(.92); opacity: .25; }
  50% { transform: scale(1); opacity: .55; }
}

@media (prefers-reduced-motion: reduce) {
  .ld-nexus i {
    animation: none !important;
  }
}
</style>
