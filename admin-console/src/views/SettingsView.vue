<template>
  <AdminLayout
    title="Settings"
    subtitle="Configure JPbot, blog assistant, and admin console preferences."
  >
    <JpbotSettingsPanel />
    <BlogAssistantSettingsPanel />
  </AdminLayout>
</template>

<script setup>
import AdminLayout from '@/layouts/AdminLayout.vue'
import BlogAssistantSettingsPanel from '@/components/BlogAssistantSettingsPanel.vue'
import JpbotSettingsPanel from '@/components/JpbotSettingsPanel.vue'
</script>
