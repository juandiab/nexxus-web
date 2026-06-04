<template>
  <div class="content-panel content-panel-padded users-panel">
    <div class="panel-intro flex align-items-start justify-content-between gap-3 flex-wrap">
      <div>
        <h2 class="section-title">Users</h2>
        <p class="section-copy">Manage platform accounts and passkeys.</p>
      </div>
      <div class="panel-toolbar flex align-items-center gap-2 flex-wrap">
        <IconField icon-position="left" class="search-field">
          <InputIcon class="pi pi-search" />
          <InputText v-model="searchQuery" placeholder="Search users…" />
        </IconField>
        <Button label="Add user" icon="pi pi-user-plus" size="small" @click="openCreateDialog" />
      </div>
    </div>

    <DataTable
      class="users-table mt-4"
      :value="filteredUsers"
      :loading="loading"
      striped-rows
      paginator
      :rows="10"
      empty-message="No users found."
    >
      <Column field="username" header="Username" sortable />
      <Column field="displayName" header="Display name" sortable />
      <Column field="email" header="Email" sortable>
        <template #body="{ data }">
          {{ data.email || '—' }}
        </template>
      </Column>
      <Column field="role" header="Role" sortable>
        <template #body="{ data }">
          <Tag :value="data.role" :severity="roleSeverity(data.role)" />
        </template>
      </Column>
      <Column field="active" header="Status" sortable>
        <template #body="{ data }">
          <Tag
            :value="data.active !== false ? 'Active' : 'Inactive'"
            :severity="data.active !== false ? 'success' : 'danger'"
          />
        </template>
      </Column>
      <Column header="Passkeys">
        <template #body="{ data }">
          <Tag
            :value="data.passkeyCount ? `${data.passkeyCount} registered` : 'Not set up'"
            :severity="data.passkeyCount ? 'success' : 'danger'"
          />
        </template>
      </Column>
      <Column headerClass="actions-col" bodyClass="actions-col" style="min-width: 14rem">
        <template #header>
          <span class="actions-header">Actions</span>
        </template>
        <template #body="{ data }">
          <div class="actions-cell flex gap-1">
            <Button
              v-tooltip="tooltip('Send password reset email')"
              icon="pi pi-envelope"
              text
              rounded
              size="small"
              :disabled="!data.email || data.active === false"
              @click="confirmResetPassword(data)"
            />
            <Button
              v-tooltip="tooltip(data.active !== false ? 'Deactivate user' : 'Activate user')"
              :icon="data.active !== false ? 'pi pi-ban' : 'pi pi-check-circle'"
              text
              rounded
              size="small"
              :severity="data.active !== false ? 'warn' : 'success'"
              :disabled="data.username === currentUsername"
              @click="confirmToggleActive(data)"
            />
            <Button
              v-tooltip="tooltip('View passkeys')"
              icon="pi pi-key"
              text
              rounded
              size="small"
              @click="openPasskeysDialog(data)"
            />
            <Button
              v-tooltip="tooltip('Edit user')"
              icon="pi pi-pencil"
              text
              rounded
              size="small"
              @click="openEditDialog(data)"
            />
            <Button
              v-tooltip="tooltip('Delete user')"
              icon="pi pi-trash"
              text
              rounded
              size="small"
              severity="danger"
              :disabled="data.username === currentUsername"
              @click="confirmDelete(data)"
            />
          </div>
        </template>
      </Column>
    </DataTable>

    <Dialog
      v-model:visible="dialogVisible"
      :header="isEditing ? 'Edit user' : 'Add user'"
      modal
      :style="{ width: 'min(28rem, 92vw)' }"
      :draggable="false"
    >
      <div class="flex flex-column gap-3">
        <div v-if="!isEditing" class="flex flex-column gap-2">
          <label for="username" class="field-label">Username</label>
          <InputText id="username" v-model="form.username" class="w-full" autocomplete="off" />
          <small class="field-hint">Letters, numbers, dots, dashes, and underscores only.</small>
        </div>
        <div class="flex flex-column gap-2">
          <label for="displayName" class="field-label">Display name</label>
          <InputText id="displayName" v-model="form.displayName" class="w-full" />
        </div>
        <div class="flex flex-column gap-2">
          <label for="email" class="field-label">Email</label>
          <InputText id="email" v-model="form.email" type="email" class="w-full" autocomplete="off" />
          <small class="field-hint">A temporary password will be emailed to this address.</small>
        </div>
        <div class="flex flex-column gap-2">
          <label for="role" class="field-label">Role</label>
          <Select id="role" v-model="form.role" :options="roles" class="w-full" />
        </div>
        <Message v-if="!isEditing" severity="info" :closable="false">
          The user signs in with the emailed password, sets a new password, then registers a passkey.
          After that, only passkey sign-in is allowed.
        </Message>
      </div>
      <template #footer>
        <Button label="Cancel" text @click="dialogVisible = false" />
        <Button :label="isEditing ? 'Save' : 'Create'" :loading="saving" @click="saveUser" />
      </template>
    </Dialog>

    <Dialog
      v-model:visible="passkeysVisible"
      :header="passkeysUser ? `Passkeys — ${passkeysUser.username}` : 'Passkeys'"
      modal
      :style="{ width: 'min(32rem, 92vw)' }"
      :draggable="false"
    >
      <div v-if="passkeysLoading" class="py-4 text-center">Loading…</div>
      <div v-else-if="!passkeys.length" class="py-2">
        <Message severity="warn" :closable="false">
          No passkey registered yet. The user can add one after signing in and completing account setup.
        </Message>
      </div>
      <DataTable v-else :value="passkeys" size="small">
        <Column field="label" header="Label" />
        <Column field="createdAt" header="Added">
          <template #body="{ data }">
            {{ formatDate(data.createdAt) }}
          </template>
        </Column>
        <Column field="lastUsedAt" header="Last used">
          <template #body="{ data }">
            {{ data.lastUsedAt ? formatDate(data.lastUsedAt) : '—' }}
          </template>
        </Column>
        <Column header="">
          <template #body="{ data }">
            <Button
              icon="pi pi-trash"
              text
              rounded
              size="small"
              severity="danger"
              @click="confirmDeletePasskey(data)"
            />
          </template>
        </Column>
      </DataTable>
    </Dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useConfirm } from 'primevue/useconfirm'
import { useToast } from 'primevue/usetoast'
import Button from 'primevue/button'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import Message from 'primevue/message'
import Select from 'primevue/select'
import Tag from 'primevue/tag'
import {
  createUser,
  deletePasskey,
  deleteUser,
  getUser,
  listUsers,
  resetUserPassword,
  setUserActive,
  updateUser,
} from '@/api/client'
import { useAdminAuth } from '@/composables/useAdminAuth'

const confirm = useConfirm()
const toast = useToast()
const { username: currentUsername } = useAdminAuth()

const users = ref([])
const loading = ref(false)
const saving = ref(false)
const searchQuery = ref('')
const dialogVisible = ref(false)
const isEditing = ref(false)
const editingId = ref(null)
const passkeysVisible = ref(false)
const passkeysLoading = ref(false)
const passkeysUser = ref(null)
const passkeys = ref([])

const roles = ['admin', 'blog', 'licensing', 'user']

const form = ref({
  username: '',
  displayName: '',
  email: '',
  role: 'user',
})

function tooltip(value) {
  return { value, appendTo: 'body', position: 'bottom' }
}

function roleSeverity(role) {
  if (role === 'admin') return 'warn'
  return 'secondary'
}

const filteredUsers = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return users.value
  return users.value.filter((user) =>
    [user.username, user.displayName, user.email, user.role].some((value) =>
      String(value || '').toLowerCase().includes(q)
    )
  )
})

function formatDate(value) {
  if (!value) return '—'
  return new Date(value).toLocaleString()
}

async function loadUsers() {
  loading.value = true
  try {
    users.value = await listUsers()
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Failed to load users',
      detail: error.message,
      life: 5000,
    })
  } finally {
    loading.value = false
  }
}

function resetForm() {
  form.value = { username: '', displayName: '', email: '', role: 'user' }
}

function openCreateDialog() {
  isEditing.value = false
  editingId.value = null
  resetForm()
  dialogVisible.value = true
}

function openEditDialog(user) {
  isEditing.value = true
  editingId.value = user.id
  form.value = {
    username: user.username,
    displayName: user.displayName,
    email: user.email || '',
    role: user.role,
  }
  dialogVisible.value = true
}

async function saveUser() {
  if (!form.value.email.trim()) {
    toast.add({
      severity: 'warn',
      summary: 'Email required',
      detail: 'Each user needs an email address.',
      life: 4000,
    })
    return
  }

  saving.value = true
  try {
    if (isEditing.value) {
      await updateUser(editingId.value, {
        displayName: form.value.displayName.trim(),
        email: form.value.email.trim().toLowerCase(),
        role: form.value.role,
      })
      toast.add({ severity: 'success', summary: 'User updated', life: 3000 })
    } else {
      await createUser({
        username: form.value.username.trim().toLowerCase(),
        displayName: form.value.displayName.trim(),
        email: form.value.email.trim().toLowerCase(),
        role: form.value.role,
      })
      toast.add({
        severity: 'success',
        summary: 'User created',
        detail: 'A temporary password was sent by email.',
        life: 5000,
      })
    }
    dialogVisible.value = false
    await loadUsers()
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Save failed',
      detail: error.message,
      life: 5000,
    })
  } finally {
    saving.value = false
  }
}

function confirmDelete(user) {
  confirm.require({
    message: `Delete user "${user.username}"?`,
    header: 'Delete user',
    icon: 'pi pi-exclamation-triangle',
    acceptClass: 'p-button-danger',
    accept: async () => {
      try {
        await deleteUser(user.id)
        toast.add({ severity: 'success', summary: 'User deleted', life: 3000 })
        await loadUsers()
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

function confirmResetPassword(user) {
  confirm.require({
    message: `Send a password reset email to ${user.email}? Existing passkeys will be removed.`,
    header: 'Reset password',
    icon: 'pi pi-envelope',
    accept: async () => {
      try {
        await resetUserPassword(user.id)
        toast.add({
          severity: 'success',
          summary: 'Password reset sent',
          detail: `A temporary password was emailed to ${user.email}.`,
          life: 5000,
        })
        await loadUsers()
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Reset failed',
          detail: error.message,
          life: 5000,
        })
      }
    },
  })
}

function confirmToggleActive(user) {
  const activating = user.active === false
  confirm.require({
    message: activating
      ? `Activate user "${user.username}"? They will be able to sign in again.`
      : `Deactivate user "${user.username}"? They will no longer be able to sign in.`,
    header: activating ? 'Activate user' : 'Deactivate user',
    icon: activating ? 'pi pi-check-circle' : 'pi pi-ban',
    acceptClass: activating ? '' : 'p-button-danger',
    accept: async () => {
      try {
        await setUserActive(user.id, activating)
        toast.add({
          severity: 'success',
          summary: activating ? 'User activated' : 'User deactivated',
          life: 3000,
        })
        await loadUsers()
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

async function openPasskeysDialog(user) {
  passkeysUser.value = user
  passkeysVisible.value = true
  passkeysLoading.value = true
  try {
    const data = await getUser(user.id)
    passkeys.value = data.passkeys || []
  } catch (error) {
    passkeys.value = []
    toast.add({
      severity: 'error',
      summary: 'Failed to load passkeys',
      detail: error.message,
      life: 5000,
    })
  } finally {
    passkeysLoading.value = false
  }
}

function confirmDeletePasskey(passkey) {
  confirm.require({
    message: `Remove passkey "${passkey.label}"?`,
    header: 'Remove passkey',
    icon: 'pi pi-exclamation-triangle',
    acceptClass: 'p-button-danger',
    accept: async () => {
      try {
        await deletePasskey(passkeysUser.value.id, passkey.id)
        toast.add({ severity: 'success', summary: 'Passkey removed', life: 3000 })
        await openPasskeysDialog(passkeysUser.value)
        await loadUsers()
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Remove failed',
          detail: error.message,
          life: 5000,
        })
      }
    },
  })
}

onMounted(loadUsers)
</script>

<style scoped>
.panel-toolbar .search-field {
  min-width: 12rem;
}

.field-label {
  font-size: 0.8125rem;
  font-weight: 500;
}

.field-hint {
  color: var(--p-text-muted-color);
  font-size: 0.75rem;
}

.users-table :deep(.actions-col) {
  width: 14rem;
  min-width: 14rem;
}

.users-table :deep(thead .actions-col) {
  pointer-events: none;
}

.users-table :deep(tbody .actions-col) {
  position: relative;
  z-index: 1;
}

.actions-cell {
  min-height: 2rem;
  align-items: center;
}
</style>
