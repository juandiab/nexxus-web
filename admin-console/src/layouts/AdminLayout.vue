<template>
  <div class="admin-layout">
    <header class="admin-header">
      <div class="brand">
        <img src="@/assets/nexxus-tech-logo-full-large.svg" alt="Nexxus Tech" class="brand-logo" />
        <span class="brand-badge">Admin</span>
      </div>
      <nav class="admin-nav">
        <RouterLink
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="nav-link"
        >
          {{ item.label }}
          <span v-if="item.inProgress" class="nav-badge">In progress</span>
        </RouterLink>
      </nav>
      <div class="header-actions">
        <span class="user-label">{{ username }}</span>
        <Button label="Sign out" text severity="secondary" class="sign-out-btn" @click="onLogout" />
      </div>
    </header>

    <main class="admin-main">
      <div v-if="!bare && (title || subtitle)" class="page-header">
        <h1 v-if="title">{{ title }}</h1>
        <p v-if="subtitle">{{ subtitle }}</p>
      </div>
      <slot />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import Button from 'primevue/button'
import { useAdminAuth } from '@/composables/useAdminAuth'

defineProps({
  title: { type: String, default: '' },
  subtitle: { type: String, default: '' },
  bare: { type: Boolean, default: false },
})

const router = useRouter()
const { username, isAdmin, canAccessLicensing, canAccessBlog, canAccessSettings, logout } =
  useAdminAuth()

const navItems = computed(() => {
  const items = [{ to: '/dashboard', label: 'Dashboard' }]
  if (isAdmin.value) items.push({ to: '/users', label: 'Users' })
  if (canAccessLicensing.value) {
    items.push({ to: '/licensing', label: 'Licensing' })
  }
  if (canAccessBlog.value) {
    items.push({ to: '/blogs', label: 'Blogs', inProgress: true })
  }
  if (canAccessSettings.value) {
    items.push({ to: '/settings', label: 'Settings', inProgress: true })
  }
  return items
})

function onLogout() {
  logout()
  router.push({ name: 'login' })
}
</script>

<style scoped>
.admin-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--p-surface-50);
}

.admin-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
  padding: 0.875rem 1.5rem;
  background: var(--p-surface-900);
  color: var(--p-surface-0);
  border-bottom: 1px solid var(--p-surface-700);
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.brand-logo {
  height: 2.5rem;
  width: auto;
  display: block;
}

.brand-name {
  font-weight: 600;
  font-size: 0.95rem;
}

.brand-badge {
  font-size: 0.6875rem;
  padding: 0.15rem 0.45rem;
  border-radius: 0.25rem;
  background: color-mix(in srgb, var(--p-surface-0) 12%, transparent);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.admin-nav {
  display: flex;
  gap: 0.25rem;
  flex: 1;
}

.nav-link {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  color: var(--p-surface-400);
  text-decoration: none;
  padding: 0.45rem 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  transition: color 0.15s ease, background 0.15s ease;
}

.nav-badge {
  font-size: 0.625rem;
  font-weight: 600;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  padding: 0.1rem 0.35rem;
  border-radius: 0.25rem;
  background: color-mix(in srgb, var(--p-yellow-500) 22%, transparent);
  color: var(--p-yellow-300);
}

.nav-link.router-link-active {
  background: color-mix(in srgb, var(--p-surface-0) 10%, transparent);
  color: var(--p-surface-0);
}

.nav-link:hover {
  color: var(--p-surface-0);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-left: auto;
}

.user-label {
  font-size: 0.875rem;
  color: var(--p-surface-400);
}

.sign-out-btn :deep(.p-button-label) {
  color: var(--p-surface-300);
}

.admin-main {
  flex: 1;
  padding: 1.5rem;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 1.25rem;
}

.page-header h1 {
  font-size: 1.375rem;
  font-weight: 600;
  margin: 0 0 0.25rem;
  color: var(--p-text-color);
}

.page-header p {
  margin: 0;
  color: var(--p-text-muted-color);
  font-size: 0.9375rem;
}
</style>
