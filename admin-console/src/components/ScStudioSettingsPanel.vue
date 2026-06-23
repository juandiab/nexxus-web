<template>
  <div class="content-panel content-panel-padded scstudio-settings">
    <div class="panel-intro flex align-items-start justify-content-between gap-3 flex-wrap">
      <div>
        <h2 class="section-title">SC Studio servers</h2>
        <p class="section-copy">
          Each approved server has one API key for license database sync. Approve pending
          registrations, then view or copy the linked key for the SC Studio operator.
        </p>
      </div>
      <Button
        label="Refresh"
        icon="pi pi-refresh"
        size="small"
        severity="secondary"
        outlined
        :loading="serversLoading"
        @click="loadServers"
      />
    </div>

    <DataTable
      class="scstudio-table mt-4"
      :value="servers"
      :loading="serversLoading"
      striped-rows
      paginator
      :rows="10"
      empty-message="No server registrations yet."
    >
      <Column field="serverName" header="Server" sortable style="min-width: 11rem">
        <template #body="{ data }">
          <div class="cell-stack">
            <span class="cell-primary">{{ data.serverName }}</span>
            <span class="cell-meta">
              <span class="cell-label">Public</span>{{ data.publicIpAddress || '—' }}
            </span>
            <span class="cell-meta">
              <span class="cell-label">Local</span>{{ data.ipAddress || '—' }}
            </span>
          </div>
        </template>
      </Column>
      <Column header="Identity" style="min-width: 12rem">
        <template #body="{ data }">
          <div class="cell-stack">
            <span class="cell-meta mono-line" :title="data.serverId">
              <span class="cell-label">ID</span>{{ data.serverId || '—' }}
            </span>
            <span class="cell-meta mono-line" :title="data.serverFingerprint">
              <span class="cell-label">FP</span>{{ data.serverFingerprint || '—' }}
            </span>
          </div>
        </template>
      </Column>
      <Column field="status" header="Status" sortable style="min-width: 7rem">
        <template #body="{ data }">
          <div class="cell-stack">
            <Tag :value="data.status" :severity="statusSeverity(data.status)" class="cell-tag" />
            <Tag
              v-if="data.status === 'approved' && data.apiKeyId"
              :value="data.apiKeyActive ? 'Key active' : 'Key disabled'"
              :severity="data.apiKeyActive ? 'success' : 'warn'"
              class="cell-tag"
            />
            <span v-else-if="data.status === 'approved'" class="cell-secondary">No key</span>
          </div>
        </template>
      </Column>
      <Column header="API key" style="min-width: 9rem">
        <template #body="{ data }">
          <div v-if="data.keyPrefix" class="cell-stack">
            <span class="cell-primary mono">{{ data.keyPrefix }}…</span>
            <span class="cell-meta">
              <span class="cell-label">Used</span>{{ formatDate(data.apiKeyLastUsedAt) }}
            </span>
          </div>
          <span v-else class="muted">—</span>
        </template>
      </Column>
      <Column field="lastSyncAt" header="Sync" sortable style="min-width: 8rem">
        <template #body="{ data }">
          <div class="cell-stack">
            <span class="cell-meta">
              <span class="cell-label">Last</span>{{ formatDate(data.lastSyncAt) }}
            </span>
          </div>
        </template>
      </Column>
      <Column headerClass="actions-col" bodyClass="actions-col" style="min-width: 13rem">
        <template #header>
          <span class="actions-header">Actions</span>
        </template>
        <template #body="{ data }">
          <div class="actions-cell flex gap-1 flex-wrap">
            <template v-if="data.status === 'pending'">
              <Button
                v-tooltip="'Approve server'"
                icon="pi pi-check"
                text
                rounded
                size="small"
                severity="success"
                @click="confirmApprove(data)"
              />
              <Button
                v-tooltip="'Reject server'"
                icon="pi pi-times"
                text
                rounded
                size="small"
                severity="danger"
                @click="confirmReject(data)"
              />
            </template>
            <template v-else-if="data.status === 'approved'">
              <Button
                v-tooltip="data.apiKeyRetrievable ? 'View API key' : 'Regenerate key to view'"
                icon="pi pi-eye"
                text
                rounded
                size="small"
                :disabled="!data.apiKeyId || !data.apiKeyRetrievable"
                @click="viewApiKey(data)"
              />
              <Button
                v-tooltip="data.apiKeyRetrievable ? 'Copy API key' : 'Regenerate key to copy'"
                icon="pi pi-copy"
                text
                rounded
                size="small"
                :disabled="!data.apiKeyId || !data.apiKeyRetrievable"
                @click="copyApiKey(data)"
              />
              <Button
                v-if="data.apiKeyId"
                v-tooltip="data.apiKeyActive ? 'Disable key' : 'Enable key'"
                :icon="data.apiKeyActive ? 'pi pi-ban' : 'pi pi-check-circle'"
                text
                rounded
                size="small"
                :severity="data.apiKeyActive ? 'warn' : 'success'"
                @click="confirmToggleKey(data)"
              />
              <Button
                v-tooltip="'Regenerate API key'"
                icon="pi pi-refresh"
                text
                rounded
                size="small"
                severity="secondary"
                @click="confirmRegenerateKey(data)"
              />
            </template>
            <Button
              v-tooltip="'Delete server'"
              icon="pi pi-trash"
              text
              rounded
              size="small"
              severity="danger"
              @click="confirmDeleteServer(data)"
            />
          </div>
        </template>
      </Column>
    </DataTable>

    <Dialog
      v-model:visible="approvalDialogVisible"
      header="Server approved"
      modal
      :style="{ width: 'min(32rem, 92vw)' }"
      :draggable="false"
    >
      <p class="section-copy">
        Copy the server ID and API key below. Provide the API key to the SC Studio operator to paste into their platform.
      </p>
      <div class="flex flex-column gap-3 mt-3">
        <div class="field-block">
          <label class="field-label">Server ID</label>
          <div class="copy-row flex gap-2 align-items-center">
            <InputText :model-value="approvalResult.serverId" readonly class="w-full mono" />
            <Button icon="pi pi-copy" severity="secondary" outlined @click="copyText(approvalResult.serverId)" />
          </div>
        </div>
        <div class="field-block">
          <label class="field-label">API key</label>
          <div class="copy-row flex gap-2 align-items-center">
            <InputText :model-value="approvalResult.apiKey" readonly class="w-full mono" />
            <Button icon="pi pi-copy" severity="secondary" outlined @click="copyText(approvalResult.apiKey)" />
          </div>
        </div>
      </div>
      <template #footer>
        <Button label="Done" @click="approvalDialogVisible = false" />
      </template>
    </Dialog>

    <Dialog
      v-model:visible="keyDialogVisible"
      header="API key regenerated"
      modal
      :style="{ width: 'min(32rem, 92vw)' }"
      :draggable="false"
    >
      <p class="section-copy">Copy the new API key for the SC Studio operator. The previous key no longer works.</p>
      <div class="field-block mt-3">
        <label class="field-label">API key</label>
        <div class="copy-row flex gap-2 align-items-center">
          <InputText :model-value="regeneratedKey.apiKey" readonly class="w-full mono" />
          <Button icon="pi pi-copy" severity="secondary" outlined @click="copyText(regeneratedKey.apiKey)" />
        </div>
      </div>
      <template #footer>
        <Button label="Done" @click="keyDialogVisible = false" />
      </template>
    </Dialog>

    <Dialog
      v-model:visible="viewKeyDialogVisible"
      header="API key"
      modal
      :style="{ width: 'min(32rem, 92vw)' }"
      :draggable="false"
    >
      <div v-if="viewKeyLoading" class="loading-row">
        <ProgressSpinner style="width: 2rem; height: 2rem" stroke-width="4" />
      </div>
      <template v-else>
        <p v-if="viewKeyResult.serverName" class="section-copy">
          Key for <strong>{{ viewKeyResult.serverName }}</strong> ({{ viewKeyResult.keyPrefix }}…)
        </p>
        <div class="field-block mt-3">
          <label class="field-label">API key</label>
          <div class="copy-row flex gap-2 align-items-center">
            <InputText :model-value="viewKeyResult.apiKey" readonly class="w-full mono" />
            <Button icon="pi pi-copy" severity="secondary" outlined @click="copyText(viewKeyResult.apiKey)" />
          </div>
        </div>
      </template>
      <template #footer>
        <Button label="Close" @click="viewKeyDialogVisible = false" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useConfirm } from 'primevue/useconfirm'
import { useToast } from 'primevue/usetoast'
import Button from 'primevue/button'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import ProgressSpinner from 'primevue/progressspinner'
import Tag from 'primevue/tag'
import {
  approveScStudioServer,
  deleteScStudioServer,
  fetchScStudioApiKeySecret,
  fetchScStudioServers,
  regenerateScStudioApiKey,
  rejectScStudioServer,
  updateScStudioApiKey,
} from '@/api/client'

const confirm = useConfirm()
const toast = useToast()

const servers = ref([])
const serversLoading = ref(true)

const approvalDialogVisible = ref(false)
const approvalResult = ref({ serverId: '', apiKey: '' })

const keyDialogVisible = ref(false)
const regeneratedKey = ref({ apiKey: '' })

const viewKeyDialogVisible = ref(false)
const viewKeyLoading = ref(false)
const viewKeyResult = ref({ apiKey: '', serverName: '', keyPrefix: '' })

function statusSeverity(status) {
  if (status === 'approved') return 'success'
  if (status === 'rejected') return 'danger'
  return 'warn'
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

async function loadServers() {
  serversLoading.value = true
  try {
    servers.value = await fetchScStudioServers()
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Failed to load servers',
      detail: error.message,
      life: 5000,
    })
  } finally {
    serversLoading.value = false
  }
}

function confirmApprove(server) {
  confirm.require({
    message: `Approve "${server.serverName}" and create its API key?`,
    header: 'Approve server',
    icon: 'pi pi-check-circle',
    acceptClass: 'p-button-success',
    accept: async () => {
      try {
        const result = await approveScStudioServer(server.id)
        approvalResult.value = {
          serverId: result.serverId,
          apiKey: result.apiKey,
        }
        approvalDialogVisible.value = true
        toast.add({ severity: 'success', summary: 'Server approved', life: 3000 })
        await loadServers()
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Approval failed',
          detail: error.message,
          life: 5000,
        })
      }
    },
  })
}

function confirmReject(server) {
  confirm.require({
    message: `Reject registration for "${server.serverName}"?`,
    header: 'Reject server',
    icon: 'pi pi-exclamation-triangle',
    acceptClass: 'p-button-danger',
    accept: async () => {
      try {
        await rejectScStudioServer(server.id)
        toast.add({ severity: 'success', summary: 'Server rejected', life: 3000 })
        await loadServers()
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Rejection failed',
          detail: error.message,
          life: 5000,
        })
      }
    },
  })
}

async function fetchKeySecret(server) {
  if (!server.apiKeyId) {
    throw new Error('No API key linked to this server.')
  }
  return fetchScStudioApiKeySecret(server.apiKeyId)
}

async function viewApiKey(server) {
  viewKeyDialogVisible.value = true
  viewKeyLoading.value = true
  viewKeyResult.value = { apiKey: '', serverName: server.serverName, keyPrefix: server.keyPrefix || '' }
  try {
    const result = await fetchKeySecret(server)
    viewKeyResult.value = {
      apiKey: result.apiKey,
      serverName: result.serverName,
      keyPrefix: result.keyPrefix,
    }
  } catch (error) {
    viewKeyDialogVisible.value = false
    toast.add({
      severity: 'error',
      summary: 'Unable to load API key',
      detail: error.message,
      life: 5000,
    })
  } finally {
    viewKeyLoading.value = false
  }
}

async function copyApiKey(server) {
  try {
    const result = await fetchKeySecret(server)
    await copyText(result.apiKey)
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Unable to copy API key',
      detail: error.message,
      life: 5000,
    })
  }
}

function confirmToggleKey(server) {
  const enabling = !server.apiKeyActive
  confirm.require({
    message: enabling ? 'Enable this API key?' : 'Disable this API key?',
    header: enabling ? 'Enable key' : 'Disable key',
    icon: 'pi pi-key',
    accept: async () => {
      try {
        await updateScStudioApiKey(server.apiKeyId, { active: enabling })
        toast.add({
          severity: 'success',
          summary: enabling ? 'Key enabled' : 'Key disabled',
          life: 3000,
        })
        await loadServers()
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Update failed',
          detail: error.message,
          life: 5000,
        })
      }
    },
  })
}

function confirmRegenerateKey(server) {
  confirm.require({
    message: `Regenerate the API key for "${server.serverName}"? The current key will stop working immediately.`,
    header: 'Regenerate API key',
    icon: 'pi pi-refresh',
    acceptClass: 'p-button-warn',
    accept: async () => {
      try {
        const result = await regenerateScStudioApiKey(server.id)
        regeneratedKey.value = { apiKey: result.apiKey }
        keyDialogVisible.value = true
        toast.add({ severity: 'success', summary: 'API key regenerated', life: 3000 })
        await loadServers()
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Regeneration failed',
          detail: error.message,
          life: 5000,
        })
      }
    },
  })
}

function confirmDeleteServer(server) {
  const detail =
    server.status === 'approved'
      ? 'This removes the registration and its API key. SC Studio will lose sync access.'
      : 'This permanently removes the registration.'
  confirm.require({
    message: `Delete "${server.serverName}"? ${detail}`,
    header: 'Delete server',
    icon: 'pi pi-trash',
    acceptClass: 'p-button-danger',
    accept: async () => {
      try {
        await deleteScStudioServer(server.id)
        toast.add({ severity: 'success', summary: 'Server deleted', life: 3000 })
        await loadServers()
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Delete failed',
          detail: error.message,
          life: 5000,
        })
      }
    },
  })
}

onMounted(() => {
  loadServers()
})
</script>

<style scoped>
.scstudio-table :deep(.p-datatable-table) {
  min-width: 48rem;
}

.cell-stack {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  line-height: 1.35;
}

.cell-primary {
  font-size: 0.88rem;
  font-weight: 600;
}

.cell-secondary,
.cell-meta {
  font-size: 0.8rem;
  color: var(--p-text-muted-color);
}

.cell-label {
  display: inline-block;
  min-width: 2.5rem;
  margin-right: 0.25rem;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--p-text-muted-color);
  opacity: 0.85;
}

.cell-tag {
  align-self: flex-start;
  font-size: 0.72rem;
}

.mono,
.mono-line {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.8rem;
}

.mono-line {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 14rem;
}

.muted {
  color: var(--p-text-muted-color);
}

.loading-row {
  display: flex;
  justify-content: center;
  padding: 1.5rem 0;
}
</style>
