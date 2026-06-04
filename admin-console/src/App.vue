<template>
  <Toast />
  <ConfirmDialog />
  <RouterView />
</template>

<script setup>
import { RouterView } from 'vue-router'
import ConfirmDialog from 'primevue/confirmdialog'
import Toast from 'primevue/toast'
</script>
