<template>
  <AdminLayout
    title="Dashboard"
    :subtitle="`Signed in as ${username} (${user?.role || ''})`"
  >
    <div class="content-panel content-panel-padded">
      <h2 class="section-title">Dashboard</h2>
      <p class="section-copy">Admin console modules available for your account.</p>

      <div v-if="quickLinks.length" class="quick-links">
        <RouterLink
          v-for="link in quickLinks"
          :key="link.to"
          :to="link.to"
          class="quick-link-card"
        >
          <span class="quick-link-label">{{ link.label }}</span>
          <span class="quick-link-copy">{{ link.copy }}</span>
        </RouterLink>
      </div>

      <ul class="role-list">
        <li><Tag value="admin" severity="warn" /> — full access, user management</li>
        <li><Tag value="blog" severity="secondary" /> — blog content management</li>
        <li><Tag value="licensing" severity="secondary" /> — license management</li>
        <li><Tag value="user" severity="secondary" /> — limited access (coming soon)</li>
      </ul>
    </div>
  </AdminLayout>
</template>

<script setup>
import { computed } from 'vue'
import Tag from 'primevue/tag'
import AdminLayout from '@/layouts/AdminLayout.vue'
import { useAdminAuth } from '@/composables/useAdminAuth'

const { username, user, isAdmin, canAccessLicensing, canAccessBlog, canAccessSettings } = useAdminAuth()

const quickLinks = computed(() => {
  const links = []
  if (isAdmin.value) {
    links.push({ to: '/users', label: 'Users', copy: 'Manage admin accounts and roles.' })
  }
  if (canAccessLicensing.value) {
    links.push({ to: '/licensing', label: 'Licensing', copy: 'View and manage product licenses.' })
  }
  if (canAccessBlog.value) {
    links.push({ to: '/blogs', label: 'Blogs', copy: 'Create, edit, and delete blog posts.' })
  }
  if (canAccessSettings.value) {
    links.push({
      to: '/scstudio',
      label: 'SC Studio',
      copy: 'Approve servers and manage license sync API keys.',
    })
    links.push({ to: '/settings', label: 'Settings', copy: 'Configure JPbot LLM provider and API key.' })
  }
  return links
})
</script>

<style scoped>
.quick-links {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(14rem, 1fr));
  gap: 0.75rem;
  margin: 1rem 0 1.5rem;
}

.quick-link-card {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.9rem 1rem;
  border-radius: 0.65rem;
  border: 1px solid var(--p-content-border-color);
  background: var(--p-surface-0);
  text-decoration: none;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.quick-link-card:hover {
  border-color: var(--p-primary-color);
  box-shadow: 0 2px 8px color-mix(in srgb, var(--p-primary-color) 12%, transparent);
}

.quick-link-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--p-text-color);
}

.quick-link-copy {
  font-size: 0.82rem;
  color: var(--p-text-muted-color);
  line-height: 1.4;
}

.role-list {
  list-style: none;
  margin: 1.25rem 0 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  color: var(--p-text-color);
  font-size: 0.9375rem;
}

.role-list li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
</style>
