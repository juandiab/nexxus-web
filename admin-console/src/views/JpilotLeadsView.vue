<template>
  <AdminLayout
    title="JPilot"
    subtitle="People who requested JPilot install access from the public products page."
  >
    <JpilotLeadsPanel />
  </AdminLayout>
</template>

<script setup>
import AdminLayout from '@/layouts/AdminLayout.vue'
import JpilotLeadsPanel from '@/components/JpilotLeadsPanel.vue'
</script>
