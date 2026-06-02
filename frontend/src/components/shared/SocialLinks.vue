<template>
  <component
    :is="variant === 'icons' ? 'div' : 'div'"
    :class="variant === 'icons' ? 'social-icons' : 'social-labels'"
  >
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
      <SocialIconX v-if="link.icon === 'x'" :class="{ 'social-icon-x': variant === 'labels' }" />
      <i v-else :class="`pi pi-${link.icon}`"></i>
      <span v-if="variant === 'labels'">{{ link.label }}</span>
    </a>
  </component>
</template>

<script setup>
import { socialLinks } from '@/config/socialLinks.js'
import SocialIconX from '@/components/shared/SocialIconX.vue'

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

.social-icon-x {
  width: 0.95rem;
  height: 0.95rem;
  flex-shrink: 0;
}
</style>
