<template>
  <div class="content-panel content-panel-padded jpilot-leads-panel">
    <div class="panel-intro flex align-items-start justify-content-between gap-3 flex-wrap">
      <div>
        <h2 class="section-title">Product leads</h2>
        <p class="section-copy">Registrations from the JPilot interest form, newest first.</p>
      </div>
      <IconField icon-position="left" class="search-field">
        <InputIcon class="pi pi-search" />
        <InputText v-model="searchQuery" placeholder="Search leads…" />
      </IconField>
    </div>

    <DataTable
      class="leads-table mt-4"
      :value="filteredLeads"
      :loading="loading"
      striped-rows
      paginator
      :rows="15"
      empty-message="No JPilot registrations yet."
      scrollable
      scroll-height="flex"
    >
      <Column field="name" header="Name" sortable style="min-width: 9rem" />
      <Column field="email" header="Email" sortable style="min-width: 14rem">
        <template #body="{ data }">
          <a :href="`mailto:${data.email}`" class="lead-email">{{ data.email }}</a>
        </template>
      </Column>
      <Column field="useType" header="Use type" sortable style="min-width: 8rem">
        <template #body="{ data }">
          {{ useTypeLabel(data.useType) }}
        </template>
      </Column>
      <Column field="country" header="Country" sortable style="min-width: 8rem" />
      <Column field="company" header="Company" sortable style="min-width: 9rem">
        <template #body="{ data }">
          {{ data.company || '—' }}
        </template>
      </Column>
      <Column field="companySize" header="Company size" sortable style="min-width: 8rem">
        <template #body="{ data }">
          {{ data.companySize || '—' }}
        </template>
      </Column>
      <Column field="createdAt" header="Created" sortable style="min-width: 10rem">
        <template #body="{ data }">
          {{ formatDate(data.createdAt) }}
        </template>
      </Column>
      <Column field="lastSeenAt" header="Last seen" sortable style="min-width: 10rem">
        <template #body="{ data }">
          {{ formatDate(data.lastSeenAt || data.updatedAt) }}
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import { useToast } from 'primevue/usetoast'
import { listJpilotLeads } from '@/api/client'

const USE_TYPE_LABELS = {
  company: 'Company',
  consultant: 'Consultant',
  personal: 'Personal use',
}

const toast = useToast()
const leads = ref([])
const loading = ref(false)
const searchQuery = ref('')

const filteredLeads = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return leads.value
  return leads.value.filter((lead) =>
    [
      lead.name,
      lead.email,
      USE_TYPE_LABELS[lead.useType] || lead.useType,
      lead.country,
      lead.company,
      lead.companySize,
    ].some((value) => String(value || '').toLowerCase().includes(q))
  )
})

function useTypeLabel(value) {
  return USE_TYPE_LABELS[value] || value || '—'
}

function formatDate(value) {
  if (!value) return '—'
  return new Date(value).toLocaleString()
}

async function loadLeads() {
  loading.value = true
  try {
    leads.value = await listJpilotLeads()
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Failed to load JPilot leads',
      detail: error.message,
      life: 5000,
    })
  } finally {
    loading.value = false
  }
}

onMounted(loadLeads)
</script>

<style scoped>
.search-field {
  min-width: 12rem;
}

.lead-email {
  color: var(--p-primary-color);
  text-decoration: none;
}

.lead-email:hover {
  text-decoration: underline;
}

.leads-table {
  overflow-x: auto;
}
</style>
