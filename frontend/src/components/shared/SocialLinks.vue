<template>
  <div :class="variant === 'icons' ? 'social-icons' : 'social-labels'">
    <a
      v-for="link in socialLinks"
      :key="link.id"
      :href="link.href"
      class="social-btn"
      :aria-label="link.label"
      :title="link.label"
      target="_blank"
      rel="noopener noreferrer"
    >
      <svg
        v-if="link.icon === 'x'"
        class="icon-x"
        :class="variant === 'icons' ? 'icon-x--footer' : 'icon-x--inline'"
        viewBox="0 0 24 24"
        aria-hidden="true"
        fill="currentColor"
      >
        <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
      </svg>
      <i v-else :class="`pi pi-${link.icon}`"></i>
      <span v-if="variant === 'labels'">{{ link.label }}</span>
    </a>
  </div>
</template>

<script setup>
import { socialLinks } from '@/config/socialLinks.js'

defineProps({
  variant: {
    type: String,
    default: 'icons',
    validator: (v) => ['icons', 'labels'].includes(v),
  },
})
</script>

<style scoped>
.social-icons {
  display: flex;
  gap: 10px;
}

.social-labels {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.social-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 6px;
  color: var(--nt-text-muted);
  font-size: 0.8rem;
  font-weight: 600;
  text-decoration: none;
  transition: var(--nt-transition);
}

.social-icons .social-btn {
  width: 40px;
  height: 40px;
  padding: 0;
  justify-content: center;
  border-radius: 8px;
  font-size: 1rem;
}

.social-btn:hover {
  background: rgba(0, 123, 167, 0.15);
  border-color: var(--nt-primary);
  color: var(--nt-primary-l);
  transform: translateY(-2px);
}

.icon-x {
  display: block;
  flex-shrink: 0;
}

.icon-x--footer {
  width: 18px;
  height: 18px;
}

.icon-x--inline {
  width: 15px;
  height: 15px;
}
</style>
