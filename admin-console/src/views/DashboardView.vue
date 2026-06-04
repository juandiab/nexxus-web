<template>
  <AdminLayout
    title="Dashboard"
    :subtitle="`Signed in as ${username} (${user?.role || ''})`"
  >
    <div class="content-panel content-panel-padded">
      <h2 class="section-title">Dashboard</h2>
      <p class="section-copy">Admin console modules will be added here based on your role.</p>
      <ul class="role-list">
        <li><Tag value="admin" severity="warn" /> — full access, user management</li>
        <li><Tag value="blog" severity="secondary" /> — blog content (coming soon)</li>
        <li><Tag value="licensing" severity="secondary" /> — license management (coming soon)</li>
        <li><Tag value="user" severity="secondary" /> — limited access (coming soon)</li>
      </ul>
    </div>
  </AdminLayout>
</template>

<script setup>
import Tag from 'primevue/tag'
import AdminLayout from '@/layouts/AdminLayout.vue'
import { useAdminAuth } from '@/composables/useAdminAuth'

const { username, user } = useAdminAuth()
</script>

<style scoped>
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
