<template>
  <AdminLayout
    title="SC Studio"
    subtitle="Approve SC Studio servers and manage their linked license sync API keys."
  >
    <ScStudioSettingsPanel />
  </AdminLayout>
</template>

<script setup>
import AdminLayout from '@/layouts/AdminLayout.vue'
import ScStudioSettingsPanel from '@/components/ScStudioSettingsPanel.vue'
</script>
