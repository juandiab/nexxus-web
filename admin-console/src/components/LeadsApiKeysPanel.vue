<template>
  <div class="content-panel content-panel-padded leads-api-keys-panel">
    <div class="panel-intro flex align-items-start justify-content-between gap-3 flex-wrap">
      <div>
        <h2 class="section-title">Leads API keys</h2>
        <p class="section-copy">
          Create keys for the Leads bot and Chief of Staff agent. Each raw key is shown once at
          creation or rotation — copy it before closing the dialog.
        </p>
      </div>
      <div class="panel-toolbar flex align-items-center gap-2 flex-wrap">
        <Button
          label="Refresh"
          icon="pi pi-refresh"
          size="small"
          severity="secondary"
          outlined
          :loading="loading"
          @click="loadKeys"
        />
        <Button label="Create key" icon="pi pi-plus" size="small" @click="openCreateDialog" />
      </div>
    </div>

    <DataTable
      class="keys-table mt-4"
      :value="keys"
      :loading="loading"
      striped-rows
      paginator
      :rows="15"
      empty-message="No API keys yet."
      scrollable
    >
      <Column field="name" header="Name" sortable style="min-width: 10rem" />
      <Column field="key_prefix" header="Prefix" sortable style="min-width: 8rem">
        <template #body="{ data }">
          <span class="mono">{{ data.key_prefix }}…</span>
        </template>
      </Column>
      <Column field="agent" header="Agent" sortable style="min-width: 9rem">
        <template #body="{ data }">
          <Tag :value="agentLabel(data.agent)" severity="info" />
        </template>
      </Column>
      <Column field="created_at" header="Created" sortable style="min-width: 10rem">
        <template #body="{ data }">
          {{ formatDate(data.created_at) }}
        </template>
      </Column>
      <Column field="last_used_at" header="Last used" sortable style="min-width: 10rem">
        <template #body="{ data }">
          {{ formatDate(data.last_used_at) }}
        </template>
      </Column>
      <Column field="revoked_at" header="Status" sortable style="min-width: 8rem">
        <template #body="{ data }">
          <Tag
            v-if="data.revoked_at"
            value="Revoked"
            severity="danger"
          />
          <Tag v-else value="Active" severity="success" />
        </template>
      </Column>
      <Column headerClass="actions-col" bodyClass="actions-col" style="min-width: 10rem">
        <template #header>
          <span class="actions-header">Actions</span>
        </template>
        <template #body="{ data }">
          <div v-if="!data.revoked_at" class="actions-cell flex gap-1">
            <Button
              v-if="rotateSupported"
              v-tooltip="'Rotate key'"
              icon="pi pi-refresh"
              text
              rounded
              size="small"
              severity="secondary"
              :loading="rotatingId === data.id"
              @click="confirmRotate(data)"
            />
            <Button
              v-tooltip="'Revoke key'"
              icon="pi pi-ban"
              text
              rounded
              size="small"
              severity="danger"
              :loading="revokingId === data.id"
              @click="confirmRevoke(data)"
            />
          </div>
          <span v-else class="muted">—</span>
        </template>
      </Column>
    </DataTable>

    <Dialog
      v-model:visible="createVisible"
      header="Create API key"
      modal
      :style="{ width: 'min(32rem, 92vw)' }"
      :draggable="false"
    >
      <div class="flex flex-column gap-3">
        <div class="flex flex-column gap-2">
          <label for="keyName" class="field-label">Name *</label>
          <InputText
            id="keyName"
            v-model="createForm.name"
            class="w-full"
            placeholder="e.g. Leads bot production"
          />
        </div>
        <div class="flex flex-column gap-2">
          <label for="keyAgent" class="field-label">Agent *</label>
          <Select
            id="keyAgent"
            v-model="createForm.agent"
            :options="agentOptions"
            option-label="label"
            option-value="value"
            class="w-full"
          />
        </div>
      </div>
      <template #footer>
        <Button label="Cancel" text @click="createVisible = false" />
        <Button label="Create" :loading="creating" @click="submitCreate" />
      </template>
    </Dialog>

    <Dialog
      v-model:visible="rawKeyVisible"
      :header="rawKeyDialogTitle"
      modal
      :style="{ width: 'min(36rem, 92vw)' }"
      :draggable="false"
      :closable="false"
    >
      <Message severity="warn" :closable="false" class="mb-3">
        Copy this key now. It will not be shown again.
      </Message>
      <p class="section-copy">
        Use header <code class="inline-code">X-Nexxus-Leads-Key</code> when calling the Leads
        ingestion API.
      </p>
      <div class="field-block mt-3">
        <label class="field-label">Raw API key</label>
        <div class="copy-row flex gap-2 align-items-center">
          <InputText :model-value="rawKeyValue" readonly class="w-full mono" />
          <Button icon="pi pi-copy" severity="secondary" outlined @click="copyText(rawKeyValue)" />
        </div>
      </div>
      <template #footer>
        <Button label="I have copied the key" @click="closeRawKeyDialog" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import Button from 'primevue/button'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Select from 'primevue/select'
import Tag from 'primevue/tag'
import { useConfirm } from 'primevue/useconfirm'
import { useToast } from 'primevue/usetoast'
import {
  createLeadsApiKey,
  listLeadsApiKeys,
  revokeLeadsApiKey,
  rotateLeadsApiKey,
} from '@/api/client'

const AGENT_LABELS = {
  leads: 'Leads bot',
  'chief-of-staff': 'Chief of Staff',
}

const agentOptions = Object.entries(AGENT_LABELS).map(([value, label]) => ({ value, label }))

const toast = useToast()
const confirm = useConfirm()

const keys = ref([])
const loading = ref(false)
const creating = ref(false)
const revokingId = ref(null)
const rotatingId = ref(null)
const rotateSupported = ref(true)

const createVisible = ref(false)
const createForm = ref({ name: '', agent: 'leads' })

const rawKeyVisible = ref(false)
const rawKeyValue = ref('')
const rawKeyDialogTitle = ref('API key created')

function agentLabel(value) {
  return AGENT_LABELS[value] || value || '—'
}

function formatDate(value) {
  if (!value) return '—'
  return new Date(value).toLocaleString()
}

async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text)
    toast.add({ severity: 'success', summary: 'Copied', life: 2000 })
  } catch {
    toast.add({ severity: 'error', summary: 'Copy failed', life: 3000 })
  }
}

function openCreateDialog() {
  createForm.value = { name: '', agent: 'leads' }
  createVisible.value = true
}

function extractRawKey(result) {
  return result?.api_key || result?.raw_key || result?.key || ''
}

function showRawKey(rawKey, title = 'API key created') {
  rawKeyValue.value = rawKey
  rawKeyDialogTitle.value = title
  rawKeyVisible.value = true
}

function closeRawKeyDialog() {
  rawKeyVisible.value = false
  rawKeyValue.value = ''
}

async function loadKeys() {
  loading.value = true
  try {
    keys.value = await listLeadsApiKeys()
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Failed to load API keys',
      detail: error.message,
      life: 5000,
    })
  } finally {
    loading.value = false
  }
}

async function submitCreate() {
  const name = createForm.value.name.trim()
  if (!name) {
    toast.add({ severity: 'warn', summary: 'Name is required', life: 4000 })
    return
  }

  creating.value = true
  try {
    const result = await createLeadsApiKey({
      name,
      agent: createForm.value.agent,
    })
    createVisible.value = false
    showRawKey(extractRawKey(result), 'API key created')
    toast.add({ severity: 'success', summary: 'API key created', life: 3000 })
    await loadKeys()
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Failed to create key',
      detail: error.message,
      life: 5000,
    })
  } finally {
    creating.value = false
  }
}

function confirmRevoke(key) {
  confirm.require({
    message: `Revoke "${key.name}"? The Leads bot will stop authenticating with this key immediately.`,
    header: 'Revoke API key',
    icon: 'pi pi-exclamation-triangle',
    rejectLabel: 'Cancel',
    acceptLabel: 'Revoke',
    acceptClass: 'p-button-danger',
    accept: async () => {
      revokingId.value = key.id
      try {
        await revokeLeadsApiKey(key.id)
        toast.add({ severity: 'success', summary: 'Key revoked', life: 3000 })
        await loadKeys()
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Revoke failed',
          detail: error.message,
          life: 5000,
        })
      } finally {
        revokingId.value = null
      }
    },
  })
}

function confirmRotate(key) {
  confirm.require({
    message: `Rotate "${key.name}"? The current key stops working immediately. A new raw key will be shown once.`,
    header: 'Rotate API key',
    icon: 'pi pi-refresh',
    acceptClass: 'p-button-warn',
    accept: async () => {
      rotatingId.value = key.id
      try {
        const result = await rotateLeadsApiKey(key.id)
        showRawKey(extractRawKey(result), 'API key rotated')
        toast.add({ severity: 'success', summary: 'Key rotated', life: 3000 })
        await loadKeys()
      } catch (error) {
        if (error.status === 404) {
          rotateSupported.value = false
          toast.add({
            severity: 'warn',
            summary: 'Rotate unavailable',
            detail: 'Revoke this key and create a new one instead.',
            life: 6000,
          })
        } else {
          toast.add({
            severity: 'error',
            summary: 'Rotate failed',
            detail: error.message,
            life: 5000,
          })
        }
      } finally {
        rotatingId.value = null
      }
    },
  })
}

onMounted(loadKeys)
</script>

<style scoped>
.keys-table {
  overflow-x: auto;
}

.mono {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.85rem;
}

.muted {
  color: var(--p-text-muted-color);
}

.field-block {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.field-label {
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--p-text-muted-color);
}

.inline-code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.85em;
  padding: 0.1rem 0.35rem;
  border-radius: 0.25rem;
  background: var(--p-surface-100);
}
</style>
