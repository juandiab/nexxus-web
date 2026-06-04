<template>
  <AdminLayout :title="sectionTitle" :subtitle="sectionSubtitle">
    <div class="content-panel content-panel-padded in-progress-panel">
      <div class="in-progress-body">
        <span class="in-progress-icon" aria-hidden="true">
          <i class="pi pi-wrench" />
        </span>
        <h2 class="section-title">{{ sectionTitle }}</h2>
        <p class="section-copy">
          This section is in progress. Check back soon for updates.
        </p>
        <Tag value="In progress" severity="warn" />
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Tag from 'primevue/tag'
import AdminLayout from '@/layouts/AdminLayout.vue'

const route = useRoute()

const sectionTitle = computed(() => route.meta.sectionTitle || route.meta.title || 'Section')
const sectionSubtitle = computed(() => route.meta.sectionSubtitle || '')
</script>

<style scoped>
.in-progress-panel {
  min-height: 16rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.in-progress-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.75rem;
  max-width: 28rem;
  padding: 1rem 0;
}

.in-progress-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 3rem;
  height: 3rem;
  border-radius: 999px;
  background: color-mix(in srgb, var(--p-primary-color) 12%, transparent);
  color: var(--p-primary-color);
  font-size: 1.25rem;
}

.in-progress-body .section-title {
  margin-top: 0.25rem;
}

.in-progress-body .section-copy {
  margin: 0;
}
</style>
