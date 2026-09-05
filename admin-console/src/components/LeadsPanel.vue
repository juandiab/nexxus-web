<template>
  <div class="content-panel content-panel-padded leads-panel">
    <div class="panel-intro flex align-items-start justify-content-between gap-3 flex-wrap">
      <div>
        <h2 class="section-title">Leads</h2>
        <p class="section-copy">
          Track AI integration consulting leads from web forms and manual entry.
        </p>
      </div>
      <div class="panel-toolbar flex align-items-center gap-2 flex-wrap">
        <IconField icon-position="left" class="search-field">
          <InputIcon class="pi pi-search" />
          <InputText v-model="searchQuery" placeholder="Search company or email…" />
        </IconField>
        <Select
          v-model="filterStatus"
          :options="statusFilterOptions"
          option-label="label"
          option-value="value"
          placeholder="All statuses"
          show-clear
          class="filter-select"
        />
        <Select
          v-model="filterSource"
          :options="sourceFilterOptions"
          option-label="label"
          option-value="value"
          placeholder="All sources"
          show-clear
          class="filter-select"
        />
        <Select
          v-model="filterLocale"
          :options="localeFilterOptions"
          option-label="label"
          option-value="value"
          placeholder="All locales"
          show-clear
          class="filter-select"
        />
        <div class="flex align-items-center gap-2">
          <Checkbox v-model="includeArchived" input-id="includeArchived" binary />
          <label for="includeArchived" class="field-label mb-0">Show archived</label>
        </div>
        <Button
          label="Export CSV"
          icon="pi pi-download"
          size="small"
          severity="secondary"
          outlined
          :loading="exporting"
          @click="exportCsv"
        />
        <Button label="Add lead" icon="pi pi-plus" size="small" @click="openCreateDialog" />
      </div>
    </div>

    <DataTable
      class="leads-table mt-4"
      :value="filteredLeads"
      :loading="loading"
      striped-rows
      paginator
      :rows="15"
      empty-message="No leads found."
      scrollable
    >
      <Column field="company_name" header="Company" sortable style="min-width: 10rem" />
      <Column field="contact_name" header="Contact" sortable style="min-width: 9rem">
        <template #body="{ data }">
          {{ data.contact_name || '—' }}
        </template>
      </Column>
      <Column field="contact_email" header="Email" sortable style="min-width: 12rem">
        <template #body="{ data }">
          <a v-if="data.contact_email" :href="`mailto:${data.contact_email}`" class="lead-email">
            {{ data.contact_email }}
          </a>
          <span v-else>—</span>
        </template>
      </Column>
      <Column field="status" header="Status" sortable style="min-width: 9rem">
        <template #body="{ data }">
          <Tag :value="statusLabel(data.status)" :severity="statusSeverity(data.status)" />
        </template>
      </Column>
      <Column field="source" header="Source" sortable style="min-width: 8rem">
        <template #body="{ data }">
          {{ sourceLabel(data.source) }}
        </template>
      </Column>
      <Column field="locale" header="Locale" sortable style="min-width: 5rem">
        <template #body="{ data }">
          {{ data.locale?.toUpperCase() || '—' }}
        </template>
      </Column>
      <Column field="package_interest" header="Package" sortable style="min-width: 8rem">
        <template #body="{ data }">
          {{ packageLabel(data.package_interest) }}
        </template>
      </Column>
      <Column field="last_touch_at" header="Last touch" sortable style="min-width: 10rem">
        <template #body="{ data }">
          {{ formatDate(data.last_touch_at || data.updated_at) }}
        </template>
      </Column>
      <Column headerClass="actions-col" bodyClass="actions-col" style="min-width: 10rem">
        <template #header>
          <span class="actions-header">Actions</span>
        </template>
        <template #body="{ data }">
          <div class="actions-cell flex gap-1">
            <Button
              v-tooltip="'View details'"
              icon="pi pi-eye"
              text
              rounded
              size="small"
              @click="openDetailDialog(data)"
            />
            <Button
              v-tooltip="'Edit lead'"
              icon="pi pi-pencil"
              text
              rounded
              size="small"
              @click="openEditDialog(data)"
            />
            <Button
              v-if="!data.archived"
              v-tooltip="'Archive lead'"
              icon="pi pi-trash"
              text
              rounded
              size="small"
              severity="danger"
              @click="confirmArchive(data)"
            />
          </div>
        </template>
      </Column>
    </DataTable>

    <Dialog
      v-model:visible="formVisible"
      :header="isEditing ? 'Edit lead' : 'Add lead'"
      modal
      :style="{ width: 'min(36rem, 92vw)' }"
      :draggable="false"
    >
      <div class="form-grid">
        <div class="flex flex-column gap-2">
          <label for="company_name" class="field-label">Company name *</label>
          <InputText id="company_name" v-model="form.company_name" class="w-full" />
        </div>
        <div class="flex flex-column gap-2">
          <label for="website" class="field-label">Website</label>
          <InputText id="website" v-model="form.website" class="w-full" placeholder="https://…" />
        </div>
        <div class="flex flex-column gap-2">
          <label for="contact_name" class="field-label">Contact name</label>
          <InputText id="contact_name" v-model="form.contact_name" class="w-full" />
        </div>
        <div class="flex flex-column gap-2">
          <label for="contact_email" class="field-label">Contact email</label>
          <InputText id="contact_email" v-model="form.contact_email" type="email" class="w-full" />
        </div>
        <div class="flex flex-column gap-2">
          <label for="contact_phone" class="field-label">Contact phone</label>
          <InputText id="contact_phone" v-model="form.contact_phone" class="w-full" />
        </div>
        <div class="flex flex-column gap-2">
          <label for="country" class="field-label">Country</label>
          <InputText id="country" v-model="form.country" class="w-full" />
        </div>
        <div class="flex flex-column gap-2">
          <label for="locale" class="field-label">Locale</label>
          <Select id="locale" v-model="form.locale" :options="localeOptions" class="w-full" />
        </div>
        <div class="flex flex-column gap-2">
          <label for="source" class="field-label">Source</label>
          <Select id="source" v-model="form.source" :options="sourceOptions" class="w-full" />
        </div>
        <div class="flex flex-column gap-2">
          <label for="status" class="field-label">Status</label>
          <Select id="status" v-model="form.status" :options="statusOptions" class="w-full" />
        </div>
        <div class="flex flex-column gap-2">
          <label for="package_interest" class="field-label">Package interest</label>
          <Select
            id="package_interest"
            v-model="form.package_interest"
            :options="packageOptions"
            class="w-full"
          />
        </div>
        <div class="flex flex-column gap-2">
          <label for="proposal_status" class="field-label">Proposal status</label>
          <Select
            id="proposal_status"
            v-model="form.proposal_status"
            :options="proposalOptions"
            class="w-full"
          />
        </div>
        <div class="flex flex-column gap-2">
          <label for="owner" class="field-label">Owner</label>
          <InputText id="owner" v-model="form.owner" class="w-full" />
        </div>
        <div class="flex flex-column gap-2 span-2">
          <label for="research_summary" class="field-label">Research summary</label>
          <Textarea id="research_summary" v-model="form.research_summary" rows="3" class="w-full" />
        </div>
        <div class="flex flex-column gap-2 span-2">
          <label for="notes" class="field-label">Notes</label>
          <Textarea id="notes" v-model="form.notes" rows="4" class="w-full" />
        </div>
      </div>
      <template #footer>
        <Button label="Cancel" text @click="formVisible = false" />
        <Button :label="isEditing ? 'Save' : 'Create'" :loading="saving" @click="saveLead" />
      </template>
    </Dialog>

    <Dialog
      v-model:visible="detailVisible"
      :header="detailLead ? detailLead.company_name : 'Lead details'"
      modal
      :style="{ width: 'min(40rem, 92vw)' }"
      :draggable="false"
    >
      <div v-if="detailLead" class="detail-body flex flex-column gap-4">
        <div
          v-if="detailLead.last_api_sync_at"
          class="api-sync-banner flex align-items-center gap-2 flex-wrap"
        >
          <Tag value="API" severity="info" />
          <span class="api-sync-text">
            Last sync via <strong>{{ agentLabel(detailLead.last_api_agent) }}</strong>
            · {{ formatDate(detailLead.last_api_sync_at) }}
          </span>
        </div>

        <div class="detail-grid">
          <div><span class="detail-label">Status</span>{{ statusLabel(detailLead.status) }}</div>
          <div><span class="detail-label">Source</span>{{ sourceLabel(detailLead.source) }}</div>
          <div><span class="detail-label">Locale</span>{{ detailLead.locale?.toUpperCase() }}</div>
          <div>
            <span class="detail-label">Package</span>{{ packageLabel(detailLead.package_interest) }}
          </div>
          <div>
            <span class="detail-label">Proposal</span>{{ proposalLabel(detailLead.proposal_status) }}
          </div>
          <div><span class="detail-label">Owner</span>{{ detailLead.owner || '—' }}</div>
          <div v-if="detailLead.contact_email">
            <span class="detail-label">Email</span>
            <a :href="`mailto:${detailLead.contact_email}`">{{ detailLead.contact_email }}</a>
          </div>
          <div v-if="detailLead.website">
            <span class="detail-label">Website</span>{{ detailLead.website }}
          </div>
        </div>

        <div v-if="detailLead.research_summary">
          <h3 class="detail-heading">Research summary</h3>
          <p class="detail-text">{{ detailLead.research_summary }}</p>
        </div>

        <div v-if="detailLead.notes">
          <h3 class="detail-heading">Notes</h3>
          <pre class="detail-notes">{{ detailLead.notes }}</pre>
        </div>

        <div>
          <h3 class="detail-heading">Propuestas</h3>
          <DataTable
            v-if="detailLead.proposals?.length"
            :value="detailLead.proposals"
            size="small"
            striped-rows
            class="proposals-table"
          >
            <Column field="kind" header="Kind" style="min-width: 6rem">
              <template #body="{ data }">
                <Tag
                  :value="proposalKindLabel(data.kind)"
                  :severity="data.kind === 'final' ? 'success' : 'secondary'"
                />
              </template>
            </Column>
            <Column header="Date" style="min-width: 9rem">
              <template #body="{ data }">
                {{ formatDate(data.uploaded_at || data.created_at || data.date) }}
              </template>
            </Column>
            <Column field="language" header="Language" style="min-width: 5rem">
              <template #body="{ data }">
                {{ (data.language || data.locale || '—').toUpperCase() }}
              </template>
            </Column>
            <Column header="" style="min-width: 6rem">
              <template #body="{ data }">
                <Button
                  label="Download"
                  icon="pi pi-download"
                  size="small"
                  text
                  :loading="downloadingProposalId === data.id"
                  @click="downloadProposal(data)"
                />
              </template>
            </Column>
          </DataTable>
          <p v-else class="detail-text">No proposals uploaded yet.</p>
        </div>

        <div>
          <h3 class="detail-heading">Timeline</h3>
          <ul v-if="detailLead.timeline?.length" class="timeline-list">
            <li v-for="(event, index) in detailLead.timeline" :key="index">
              <span class="timeline-time">{{ formatDate(event.at) }}</span>
              <Tag :value="timelineLabel(event.type)" severity="secondary" />
              <span class="timeline-detail">{{ event.detail }}</span>
              <span v-if="event.by" class="timeline-by">— {{ event.by }}</span>
            </li>
          </ul>
          <p v-else class="detail-text">No timeline events yet.</p>
        </div>

        <div class="flex flex-column gap-2">
          <label for="newNote" class="field-label">Add note</label>
          <Textarea id="newNote" v-model="newNote" rows="3" class="w-full" />
          <Button
            label="Add note"
            icon="pi pi-comment"
            size="small"
            :loading="addingNote"
            :disabled="!newNote.trim()"
            @click="submitNote"
          />
        </div>
      </div>
      <template #footer>
        <Button label="Close" text @click="detailVisible = false" />
        <Button
          v-if="detailLead"
          label="Edit"
          icon="pi pi-pencil"
          @click="openEditFromDetail"
        />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import Button from 'primevue/button'
import Checkbox from 'primevue/checkbox'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import Tag from 'primevue/tag'
import Textarea from 'primevue/textarea'
import { useConfirm } from 'primevue/useconfirm'
import { useToast } from 'primevue/usetoast'
import {
  addLeadNote,
  archiveLead,
  createLead,
  downloadLeadProposalFile,
  exportLeadsCsv,
  getLead,
  listLeads,
  updateLead,
} from '@/api/client'

const STATUS_LABELS = {
  new: 'New',
  researching: 'Researching',
  proposal_draft: 'Proposal draft',
  proposal_sent: 'Proposal sent',
  negotiation: 'Negotiation',
  won: 'Won',
  lost: 'Lost',
  nurture: 'Nurture',
}

const SOURCE_LABELS = {
  web_form: 'Web form',
  referral: 'Referral',
  manual: 'Manual',
  linkedin: 'LinkedIn',
  other: 'Other',
}

const PACKAGE_LABELS = {
  diagnostic: 'Diagnostic',
  pilot: 'Pilot',
  system: 'System',
  retainer: 'Retainer',
  unknown: 'Unknown',
}

const PROPOSAL_LABELS = {
  none: 'None',
  draft: 'Draft',
  sent: 'Sent',
  accepted: 'Accepted',
  rejected: 'Rejected',
}

const TIMELINE_LABELS = {
  created: 'Created',
  status_changed: 'Status change',
  proposal_sent: 'Proposal sent',
  note_added: 'Note',
}

const API_AGENT_LABELS = {
  leads: 'Leads bot',
  'chief-of-staff': 'Chief of Staff',
}

const PROPOSAL_KIND_LABELS = {
  draft: 'Draft',
  final: 'Final',
}

const DEFAULT_OWNER = 'JP / business@nexxus-tech.com'

const statusOptions = Object.entries(STATUS_LABELS).map(([value, label]) => ({ value, label }))
const sourceOptions = Object.entries(SOURCE_LABELS).map(([value, label]) => ({ value, label }))
const packageOptions = Object.entries(PACKAGE_LABELS).map(([value, label]) => ({ value, label }))
const proposalOptions = Object.entries(PROPOSAL_LABELS).map(([value, label]) => ({ value, label }))
const localeOptions = [
  { value: 'en', label: 'English (EN)' },
  { value: 'es', label: 'Spanish (ES)' },
]

const statusFilterOptions = [{ value: null, label: 'All statuses' }, ...statusOptions]
const sourceFilterOptions = [{ value: null, label: 'All sources' }, ...sourceOptions]
const localeFilterOptions = [{ value: null, label: 'All locales' }, ...localeOptions]

const toast = useToast()
const confirm = useConfirm()

const leads = ref([])
const loading = ref(false)
const saving = ref(false)
const exporting = ref(false)
const addingNote = ref(false)
const searchQuery = ref('')
const filterStatus = ref(null)
const filterSource = ref(null)
const filterLocale = ref(null)
const includeArchived = ref(false)

const formVisible = ref(false)
const detailVisible = ref(false)
const isEditing = ref(false)
const editingId = ref(null)
const detailLead = ref(null)
const newNote = ref('')
const downloadingProposalId = ref(null)

const emptyForm = () => ({
  company_name: '',
  website: '',
  contact_name: '',
  contact_email: '',
  contact_phone: '',
  country: '',
  locale: 'en',
  source: 'manual',
  status: 'new',
  package_interest: 'unknown',
  proposal_status: 'none',
  owner: DEFAULT_OWNER,
  research_summary: '',
  notes: '',
})

const form = ref(emptyForm())

const filteredLeads = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return leads.value
  return leads.value.filter((lead) =>
    [lead.company_name, lead.contact_name, lead.contact_email]
      .some((value) => String(value || '').toLowerCase().includes(q))
  )
})

function statusLabel(value) {
  return STATUS_LABELS[value] || value || '—'
}

function sourceLabel(value) {
  return SOURCE_LABELS[value] || value || '—'
}

function packageLabel(value) {
  return PACKAGE_LABELS[value] || value || '—'
}

function proposalLabel(value) {
  return PROPOSAL_LABELS[value] || value || '—'
}

function timelineLabel(value) {
  return TIMELINE_LABELS[value] || value || 'Event'
}

function agentLabel(value) {
  return API_AGENT_LABELS[value] || value || 'API agent'
}

function proposalKindLabel(value) {
  return PROPOSAL_KIND_LABELS[value] || value || '—'
}

function statusSeverity(status) {
  if (status === 'won') return 'success'
  if (status === 'lost') return 'danger'
  if (status === 'proposal_sent' || status === 'negotiation') return 'info'
  if (status === 'nurture') return 'secondary'
  return 'warn'
}

function formatDate(value) {
  if (!value) return '—'
  return new Date(value).toLocaleString()
}

function buildListParams() {
  const params = {}
  if (filterStatus.value) params.status = filterStatus.value
  if (filterSource.value) params.source = filterSource.value
  if (filterLocale.value) params.locale = filterLocale.value
  if (includeArchived.value) params.include_archived = 'true'
  if (searchQuery.value.trim()) params.q = searchQuery.value.trim()
  return params
}

async function loadLeads() {
  loading.value = true
  try {
    leads.value = await listLeads(buildListParams())
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Failed to load leads',
      detail: error.message,
      life: 5000,
    })
  } finally {
    loading.value = false
  }
}

function openCreateDialog() {
  isEditing.value = false
  editingId.value = null
  form.value = emptyForm()
  formVisible.value = true
}

function openEditDialog(lead) {
  isEditing.value = true
  editingId.value = lead.id
  form.value = {
    company_name: lead.company_name || '',
    website: lead.website || '',
    contact_name: lead.contact_name || '',
    contact_email: lead.contact_email || '',
    contact_phone: lead.contact_phone || '',
    country: lead.country || '',
    locale: lead.locale || 'en',
    source: lead.source || 'manual',
    status: lead.status || 'new',
    package_interest: lead.package_interest || 'unknown',
    proposal_status: lead.proposal_status || 'none',
    owner: lead.owner || DEFAULT_OWNER,
    research_summary: lead.research_summary || '',
    notes: lead.notes || '',
  }
  formVisible.value = true
}

async function openDetailDialog(lead) {
  try {
    detailLead.value = await getLead(lead.id)
    newNote.value = ''
    detailVisible.value = true
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Failed to load lead',
      detail: error.message,
      life: 5000,
    })
  }
}

function openEditFromDetail() {
  if (!detailLead.value) return
  detailVisible.value = false
  openEditDialog(detailLead.value)
}

async function saveLead() {
  if (!form.value.company_name.trim()) {
    toast.add({
      severity: 'warn',
      summary: 'Company name required',
      life: 4000,
    })
    return
  }

  saving.value = true
  const payload = {
    ...form.value,
    company_name: form.value.company_name.trim(),
    contact_email: form.value.contact_email.trim() || null,
  }

  try {
    if (isEditing.value && editingId.value) {
      await updateLead(editingId.value, payload)
      toast.add({ severity: 'success', summary: 'Lead updated', life: 3000 })
    } else {
      await createLead(payload)
      toast.add({ severity: 'success', summary: 'Lead created', life: 3000 })
    }
    formVisible.value = false
    await loadLeads()
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Failed to save lead',
      detail: error.message,
      life: 5000,
    })
  } finally {
    saving.value = false
  }
}

async function submitNote() {
  if (!detailLead.value || !newNote.value.trim()) return
  addingNote.value = true
  try {
    detailLead.value = await addLeadNote(detailLead.value.id, { note: newNote.value.trim() })
    newNote.value = ''
    toast.add({ severity: 'success', summary: 'Note added', life: 3000 })
    await loadLeads()
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Failed to add note',
      detail: error.message,
      life: 5000,
    })
  } finally {
    addingNote.value = false
  }
}

async function downloadProposal(proposal) {
  if (!detailLead.value || !proposal?.id) return
  downloadingProposalId.value = proposal.id
  const kind = proposal.kind || 'proposal'
  const lang = proposal.language || proposal.locale || 'pdf'
  const filename = `${detailLead.value.company_name || 'lead'}-${kind}-${lang}.pdf`
    .replace(/[^\w.-]+/g, '-')
    .toLowerCase()
  try {
    await downloadLeadProposalFile(detailLead.value.id, proposal.id, filename)
    toast.add({ severity: 'success', summary: 'PDF downloaded', life: 3000 })
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Download failed',
      detail: error.message,
      life: 5000,
    })
  } finally {
    downloadingProposalId.value = null
  }
}

function confirmArchive(lead) {
  confirm.require({
    message: `Archive lead for ${lead.company_name}?`,
    header: 'Archive lead',
    icon: 'pi pi-exclamation-triangle',
    rejectLabel: 'Cancel',
    acceptLabel: 'Archive',
    acceptClass: 'p-button-danger',
    accept: async () => {
      try {
        await archiveLead(lead.id)
        toast.add({ severity: 'success', summary: 'Lead archived', life: 3000 })
        await loadLeads()
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Failed to archive lead',
          detail: error.message,
          life: 5000,
        })
      }
    },
  })
}

async function exportCsv() {
  exporting.value = true
  try {
    await exportLeadsCsv(buildListParams())
    toast.add({ severity: 'success', summary: 'CSV exported', life: 3000 })
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Export failed',
      detail: error.message,
      life: 5000,
    })
  } finally {
    exporting.value = false
  }
}

watch([filterStatus, filterSource, filterLocale, includeArchived], () => {
  loadLeads()
})

onMounted(loadLeads)
</script>

<style scoped>
.search-field {
  min-width: 12rem;
}

.filter-select {
  min-width: 10rem;
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

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-grid .span-2 {
  grid-column: span 2;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem 1.5rem;
}

.detail-label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--p-text-muted-color);
  margin-bottom: 0.15rem;
}

.detail-heading {
  margin: 0 0 0.5rem;
  font-size: 0.95rem;
}

.detail-text {
  margin: 0;
  white-space: pre-wrap;
}

.detail-notes {
  margin: 0;
  padding: 0.75rem;
  background: var(--p-surface-100);
  border-radius: 6px;
  white-space: pre-wrap;
  font-family: inherit;
  font-size: 0.875rem;
}

.timeline-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.timeline-list li {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem;
}

.timeline-time {
  font-size: 0.8rem;
  color: var(--p-text-muted-color);
  min-width: 9rem;
}

.timeline-detail {
  flex: 1;
  min-width: 8rem;
}

.timeline-by {
  font-size: 0.8rem;
  color: var(--p-text-muted-color);
}

.api-sync-banner {
  padding: 0.65rem 0.85rem;
  border-radius: 0.5rem;
  background: color-mix(in srgb, var(--p-blue-500) 8%, var(--p-content-background));
  border: 1px solid color-mix(in srgb, var(--p-blue-500) 20%, transparent);
}

.api-sync-text {
  font-size: 0.875rem;
  color: var(--p-text-color);
}

.proposals-table {
  margin-top: 0.35rem;
}

@media (max-width: 640px) {
  .form-grid,
  .detail-grid {
    grid-template-columns: 1fr;
  }

  .form-grid .span-2 {
    grid-column: span 1;
  }
}
</style>
