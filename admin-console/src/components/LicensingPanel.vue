<template>
  <div class="content-panel content-panel-padded licensing-panel">
    <div class="panel-intro flex align-items-start justify-content-between gap-3 flex-wrap">
      <div>
        <h2 class="section-title">Licenses</h2>
        <p class="section-copy">Manage issued licenses and activation links.</p>
      </div>
      <Button
        label="Open activation page"
        icon="pi pi-external-link"
        size="small"
        outlined
        @click="openActivatePage"
      />
    </div>

    <DataTable
      class="licenses-table mt-4"
      :value="licenses"
      :loading="loading"
      striped-rows
      paginator
      :rows="10"
      empty-message="No licenses yet."
    >
      <Column field="name" header="Contact" sortable style="min-width: 10rem">
        <template #body="{ data }">
          <div class="cell-stack">
            <span class="cell-primary">{{ data.name || '—' }}</span>
            <span class="cell-secondary">{{ data.email || '—' }}</span>
          </div>
        </template>
      </Column>
      <Column field="company" header="Organization" sortable style="min-width: 9rem">
        <template #body="{ data }">
          <div class="cell-stack">
            <span class="cell-primary">{{ data.company || '—' }}</span>
            <span class="cell-secondary">{{ formatUsageType(data.usageType) }}</span>
          </div>
        </template>
      </Column>
      <Column field="application" header="License" sortable style="min-width: 9rem">
        <template #body="{ data }">
          <div class="cell-stack">
            <span class="cell-primary">{{ data.application || '—' }}</span>
            <Tag :value="formatLicenseType(data.licenseType)" severity="secondary" class="cell-tag" />
          </div>
        </template>
      </Column>
      <Column header="Status" sortable sort-field="expirationDate" style="min-width: 7rem">
        <template #body="{ data }">
          <Tag :value="licenseStatus(data).label" :severity="licenseStatus(data).severity" />
        </template>
      </Column>
      <Column field="expirationDate" header="Validity" sortable style="min-width: 10rem">
        <template #body="{ data }">
          <div class="cell-stack">
            <span class="cell-meta">
              <span class="cell-label">Reg</span>{{ formatDateShort(data.registrationDate) }}
            </span>
            <span class="cell-meta">
              <span class="cell-label">Exp</span>{{ formatDateShort(data.expirationDate) }}
            </span>
          </div>
        </template>
      </Column>
      <Column headerClass="actions-col" bodyClass="actions-col" style="min-width: 13rem">
        <template #header>
          <span class="actions-header">Actions</span>
        </template>
        <template #body="{ data }">
          <div class="actions-cell flex gap-1">
            <Button
              v-tooltip="tooltip('View license code')"
              icon="pi pi-key"
              text
              rounded
              size="small"
              :disabled="!data.hasLicenseCode"
              @click="openCodeDialog(data)"
            />
            <Button
              v-tooltip="tooltip('Force expire (blocks auto-renew)')"
              icon="pi pi-clock"
              text
              rounded
              size="small"
              severity="warn"
              @click="confirmExpire(data)"
            />
            <Button
              v-tooltip="tooltip(data.active === false ? 'Reactivate license' : 'Deactivate license')"
              :icon="data.active === false ? 'pi pi-check-circle' : 'pi pi-ban'"
              text
              rounded
              size="small"
              :severity="data.active === false ? 'success' : 'warn'"
              @click="confirmToggleActive(data)"
            />
            <Button
              v-tooltip="tooltip('Extend validity')"
              icon="pi pi-calendar-plus"
              text
              rounded
              size="small"
              @click="openExtendDialog(data)"
            />
            <Button
              v-tooltip="tooltip('Change license type')"
              icon="pi pi-tags"
              text
              rounded
              size="small"
              @click="openTypeDialog(data)"
            />
            <Button
              v-tooltip="tooltip('Delete license')"
              icon="pi pi-trash"
              text
              rounded
              size="small"
              severity="danger"
              @click="openDeleteDialog(data)"
            />
          </div>
        </template>
      </Column>
    </DataTable>

    <Dialog
      v-model:visible="codeVisible"
      header="License code"
      modal
      :style="{ width: 'min(28rem, 92vw)' }"
      :draggable="false"
    >
      <div v-if="selectedLicense" class="flex flex-column gap-3">
        <p class="dialog-copy m-0">
          License for <strong>{{ selectedLicense.email }}</strong> — {{ selectedLicense.application }}
        </p>
        <div v-if="codeLoading" class="py-3 text-center">Loading…</div>
        <div v-else-if="displayedCode" class="license-code-block">
          <code class="license-code-value">{{ displayedCode }}</code>
        </div>
        <Message v-else severity="warn" :closable="false">
          No license code is stored for this record.
        </Message>
      </div>
      <template #footer>
        <Button label="Close" text @click="codeVisible = false" />
        <Button
          label="Copy code"
          icon="pi pi-copy"
          :disabled="!displayedCode || codeLoading"
          @click="copyLicenseCode"
        />
      </template>
    </Dialog>

    <Dialog
      v-model:visible="extendVisible"
      header="Extend license"
      modal
      :style="{ width: 'min(24rem, 92vw)' }"
      :draggable="false"
    >
      <div v-if="selectedLicense" class="flex flex-column gap-3">
        <p class="dialog-copy m-0">
          Extend <strong>{{ selectedLicense.email }}</strong> — {{ selectedLicense.application }}
        </p>
        <div class="flex flex-column gap-2">
          <label for="extendDays" class="field-label">Additional days</label>
          <InputNumber id="extendDays" v-model="extendDays" :min="1" :max="3650" class="w-full" />
        </div>
      </div>
      <template #footer>
        <Button label="Cancel" text @click="extendVisible = false" />
        <Button label="Extend" icon="pi pi-calendar-plus" :loading="actionLoading" @click="submitExtend" />
      </template>
    </Dialog>

    <Dialog
      v-model:visible="typeVisible"
      header="Change license type"
      modal
      :style="{ width: 'min(24rem, 92vw)' }"
      :draggable="false"
    >
      <div v-if="selectedLicense" class="flex flex-column gap-3">
        <p class="dialog-copy m-0">
          Update type for <strong>{{ selectedLicense.email }}</strong>
        </p>
        <div class="flex flex-column gap-2">
          <label for="licenseType" class="field-label">License type</label>
          <Select
            id="licenseType"
            v-model="typeForm.licenseType"
            :options="licenseTypes"
            option-label="label"
            option-value="value"
            class="w-full"
          />
        </div>
        <div class="flex align-items-center gap-2">
          <Checkbox v-model="typeForm.recalculateValidity" input-id="recalculateValidity" binary />
          <label for="recalculateValidity" class="checkbox-label">
            Recalculate expiration from registration date
          </label>
        </div>
      </div>
      <template #footer>
        <Button label="Cancel" text @click="typeVisible = false" />
        <Button label="Save type" icon="pi pi-check" :loading="actionLoading" @click="submitTypeChange" />
      </template>
    </Dialog>

    <Dialog
      v-model:visible="deleteVisible"
      header="Delete license"
      modal
      :style="{ width: 'min(28rem, 92vw)' }"
      :draggable="false"
    >
      <div v-if="selectedLicense" class="flex flex-column gap-3">
        <Message severity="warn" :closable="false">
          This permanently removes the license. The deployment will need to activate again.
        </Message>
        <p class="dialog-copy m-0">
          You are about to delete the license for
          <strong>{{ selectedLicense.name }}</strong> ({{ selectedLicense.email }}).
        </p>
        <div class="flex flex-column gap-2">
          <label for="deleteConfirm" class="field-label">
            Type <strong>DELETE</strong> to confirm
          </label>
          <InputText
            id="deleteConfirm"
            v-model="deleteConfirmText"
            class="w-full"
            autocomplete="off"
            placeholder="DELETE"
          />
        </div>
      </div>
      <template #footer>
        <Button label="Cancel" text @click="closeDeleteDialog" />
        <Button
          label="Delete license"
          icon="pi pi-trash"
          severity="danger"
          :loading="actionLoading"
          :disabled="deleteConfirmText !== 'DELETE'"
          @click="submitDelete"
        />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useConfirm } from 'primevue/useconfirm'
import { useToast } from 'primevue/usetoast'
import Button from 'primevue/button'
import Checkbox from 'primevue/checkbox'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog'
import InputNumber from 'primevue/inputnumber'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Select from 'primevue/select'
import Tag from 'primevue/tag'
import {
  changeLicenseType,
  deactivateLicense,
  deleteLicense,
  expireLicense,
  extendLicense,
  getLicenseCode,
  listLicenses,
  reactivateLicense,
} from '@/api/client'

const confirm = useConfirm()
const toast = useToast()

const licenses = ref([])
const loading = ref(false)
const actionLoading = ref(false)
const selectedLicense = ref(null)
const extendVisible = ref(false)
const typeVisible = ref(false)
const deleteVisible = ref(false)
const codeVisible = ref(false)
const codeLoading = ref(false)
const displayedCode = ref('')
const extendDays = ref(30)
const deleteConfirmText = ref('')
const typeForm = ref({
  licenseType: 'free',
  recalculateValidity: true,
})

const licenseTypes = [
  { label: 'Free', value: 'free' },
  { label: 'Trial', value: 'trial' },
  { label: 'Enterprise', value: 'enterprise' },
  { label: 'Enterprise Pro', value: 'enterprise_pro' },
]

function tooltip(text) {
  return { value: text, showDelay: 400 }
}

function formatLicenseType(value) {
  if (value === 'enterprise_pro') return 'Enterprise Pro'
  if (value === 'enterprise') return 'Enterprise'
  if (value === 'trial') return 'Trial'
  return 'Free'
}

function formatUsageType(value) {
  if (value === 'onprem') return 'On-premises'
  if (value === 'cloud') return 'Cloud'
  if (value === 'consulting') return 'Consulting'
  if (value === 'personal') return 'Personal'
  return value || '—'
}

function formatDateShort(value) {
  if (!value) return '—'
  return new Date(value).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

function parseUtcDate(value) {
  if (!value) return NaN
  const text = String(value).trim()
  if (!text) return NaN
  if (/[zZ]$/.test(text) || /[+-]\d{2}:\d{2}$/.test(text)) {
    return Date.parse(text)
  }
  return Date.parse(`${text}Z`)
}

function isExpired(license) {
  if (license.renewalBlocked) return true
  if (!license.expirationDate) return false
  const expiresAt = parseUtcDate(license.expirationDate)
  if (Number.isNaN(expiresAt)) return false
  return expiresAt <= Date.now()
}

const STATUS_DISPLAY = {
  active: { label: 'Active', severity: 'success' },
  expired: { label: 'Expired', severity: 'warn' },
  expired_blocked: { label: 'Expired (blocked)', severity: 'warn' },
  deactivated: { label: 'Deactivated', severity: 'danger' },
}

function licenseStatus(license) {
  if (license.status && STATUS_DISPLAY[license.status]) {
    return STATUS_DISPLAY[license.status]
  }
  if (license.active === false) {
    return STATUS_DISPLAY.deactivated
  }
  if (license.renewalBlocked || isExpired(license)) {
    return license.renewalBlocked ? STATUS_DISPLAY.expired_blocked : STATUS_DISPLAY.expired
  }
  return STATUS_DISPLAY.active
}

function openActivatePage() {
  window.open('/licensing/activate', '_blank', 'noopener')
}

async function loadLicenses() {
  loading.value = true
  try {
    licenses.value = await listLicenses()
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Failed to load licenses',
      detail: error.message,
      life: 5000,
    })
  } finally {
    loading.value = false
  }
}

async function runAction(action, successSummary) {
  actionLoading.value = true
  try {
    await action()
    toast.add({ severity: 'success', summary: successSummary, life: 3000 })
    await loadLicenses()
    return true
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Action failed',
      detail: error.message,
      life: 5000,
    })
    return false
  } finally {
    actionLoading.value = false
  }
}

function confirmExpire(license) {
  confirm.require({
    message: `Expire the license for ${license.email}? Auto-renew will be blocked and the user must request a new license or contact support.`,
    header: 'Expire license',
    icon: 'pi pi-clock',
    acceptClass: 'p-button-warning',
    accept: async () => {
      await runAction(() => expireLicense(license.id), 'License expired')
    },
  })
}

function confirmToggleActive(license) {
  const reactivating = license.active === false
  confirm.require({
    message: reactivating
      ? `Reactivate the license for ${license.email}? Sync will work again if not expired.`
      : `Deactivate the license for ${license.email}? The application will be blocked immediately on sync.`,
    header: reactivating ? 'Reactivate license' : 'Deactivate license',
    icon: reactivating ? 'pi pi-check-circle' : 'pi pi-ban',
    acceptClass: reactivating ? '' : 'p-button-danger',
    accept: async () => {
      const action = reactivating
        ? () => reactivateLicense(license.id)
        : () => deactivateLicense(license.id)
      await runAction(action, reactivating ? 'License reactivated' : 'License deactivated')
    },
  })
}

function openExtendDialog(license) {
  selectedLicense.value = license
  extendDays.value = 30
  extendVisible.value = true
}

async function openCodeDialog(license) {
  selectedLicense.value = license
  displayedCode.value = ''
  codeVisible.value = true
  codeLoading.value = true
  try {
    const data = await getLicenseCode(license.id)
    displayedCode.value = data.licenseCode || ''
  } catch (error) {
    codeVisible.value = false
    toast.add({
      severity: 'error',
      summary: 'Failed to load license code',
      detail: error.message,
      life: 5000,
    })
  } finally {
    codeLoading.value = false
  }
}

async function copyLicenseCode() {
  if (!displayedCode.value) return
  try {
    await navigator.clipboard.writeText(displayedCode.value)
    toast.add({ severity: 'success', summary: 'License code copied', life: 2500 })
  } catch {
    toast.add({
      severity: 'warn',
      summary: 'Copy failed',
      detail: 'Select and copy the code manually.',
      life: 4000,
    })
  }
}

async function submitExtend() {
  if (!selectedLicense.value) return
  const ok = await runAction(
    () => extendLicense(selectedLicense.value.id, extendDays.value),
    'License extended',
  )
  if (ok) extendVisible.value = false
}

function openTypeDialog(license) {
  selectedLicense.value = license
  typeForm.value = {
    licenseType: license.licenseType || 'free',
    recalculateValidity: true,
  }
  typeVisible.value = true
}

async function submitTypeChange() {
  if (!selectedLicense.value) return
  const ok = await runAction(
    () =>
      changeLicenseType(
        selectedLicense.value.id,
        typeForm.value.licenseType,
        typeForm.value.recalculateValidity,
      ),
    'License type updated',
  )
  if (ok) typeVisible.value = false
}

function openDeleteDialog(license) {
  selectedLicense.value = license
  deleteConfirmText.value = ''
  deleteVisible.value = true
}

function closeDeleteDialog() {
  deleteVisible.value = false
  deleteConfirmText.value = ''
}

async function submitDelete() {
  if (!selectedLicense.value || deleteConfirmText.value !== 'DELETE') return
  const ok = await runAction(() => deleteLicense(selectedLicense.value.id), 'License deleted')
  if (ok) closeDeleteDialog()
}

onMounted(loadLicenses)
</script>

<style scoped>
.licenses-table :deep(.p-datatable-table) {
  min-width: 40rem;
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
  min-width: 1.75rem;
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

.dialog-copy {
  color: var(--p-text-muted-color);
  font-size: 0.92rem;
  line-height: 1.5;
}

.field-label {
  font-size: 0.82rem;
  font-weight: 600;
}

.checkbox-label {
  font-size: 0.88rem;
  cursor: pointer;
}

.actions-col {
  white-space: nowrap;
}

.license-code-block {
  padding: 14px 16px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.license-code-value {
  display: block;
  font-family: Consolas, 'Courier New', monospace;
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  word-break: break-all;
  color: var(--p-text-color);
}
</style>
