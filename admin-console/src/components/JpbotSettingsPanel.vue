<template>
  <div class="content-panel content-panel-padded jpbot-settings">
    <div class="panel-intro">
      <h2 class="section-title">JP Chat (JPbot)</h2>
      <p class="section-copy">
        Choose the LLM provider and model used for site chat discovery and enquiry summaries.
        API keys are stored encrypted in MongoDB.
      </p>
    </div>

    <div v-if="loading" class="loading-row">
      <ProgressSpinner style="width: 2rem; height: 2rem" stroke-width="4" />
    </div>

    <form v-else class="settings-form flex flex-column gap-4 mt-4" @submit.prevent="saveSettings">
      <div class="field-grid">
        <div class="field-block">
          <label for="provider" class="field-label">Provider</label>
          <Select
            id="provider"
            v-model="form.provider"
            :options="providerOptions"
            option-label="label"
            option-value="id"
            class="w-full"
            @change="onProviderChange"
          />
        </div>
        <div class="field-block">
          <label for="model" class="field-label">Model</label>
          <Select
            id="model"
            v-model="form.model"
            :options="modelOptions"
            option-label="label"
            option-value="id"
            class="w-full"
            :loading="modelsLoading"
            filter
            placeholder="Select a model"
          />
        </div>
      </div>

      <div class="field-block">
        <label for="apiKey" class="field-label">API key</label>
        <Password
          id="apiKey"
          v-model="form.apiKey"
          class="w-full"
          :feedback="false"
          toggle-mask
          :placeholder="configured ? 'Leave blank to keep current key' : 'Required'"
          autocomplete="off"
        />
        <small v-if="apiKeyMasked" class="field-hint">Current key: {{ apiKeyMasked }}</small>
      </div>

      <div class="field-block">
        <div class="flex align-items-center gap-2">
          <Checkbox v-model="form.enabled" input-id="jpbotEnabled" binary />
          <label for="jpbotEnabled" class="checkbox-label">Enable JPbot LLM responses</label>
        </div>
      </div>

      <Message v-if="testResult" :severity="testResult.success ? 'success' : 'error'" :closable="false">
        {{ testResult.message }}
        <span v-if="testResult.replyPreview"> — {{ testResult.replyPreview }}</span>
      </Message>

      <div class="actions-row flex gap-2 flex-wrap">
        <Button
          type="button"
          label="Test connection"
          icon="pi pi-bolt"
          severity="secondary"
          outlined
          :loading="testing"
          @click="runTest"
        />
        <Button
          type="submit"
          label="Save settings"
          icon="pi pi-check"
          :loading="saving"
        />
      </div>
    </form>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import Button from 'primevue/button'
import Checkbox from 'primevue/checkbox'
import Message from 'primevue/message'
import Password from 'primevue/password'
import ProgressSpinner from 'primevue/progressspinner'
import Select from 'primevue/select'
import {
  getJpbotModels,
  getJpbotSettings,
  saveJpbotSettings,
  testJpbotSettings,
} from '@/api/client'

const toast = useToast()

const loading = ref(true)
const saving = ref(false)
const testing = ref(false)
const modelsLoading = ref(false)
const providerOptions = ref([])
const modelOptions = ref([])
const apiKeyMasked = ref('')
const configured = ref(false)
const testResult = ref(null)

const form = ref({
  provider: 'deepseek',
  model: '',
  apiKey: '',
  enabled: true,
})

const selectedProviderDefault = computed(() => {
  const match = providerOptions.value.find((item) => item.id === form.value.provider)
  return match?.defaultModel || ''
})

async function loadModelsForProvider(provider, currentModel = form.value.model) {
  modelsLoading.value = true
  try {
    const data = await getJpbotModels(provider, currentModel)
    modelOptions.value = data.models || []
    const ids = modelOptions.value.map((item) => item.id)
    if (!form.value.model || !ids.includes(form.value.model)) {
      form.value.model = data.defaultModel || selectedProviderDefault.value
    }
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Failed to load models',
      detail: error.message,
      life: 5000,
    })
  } finally {
    modelsLoading.value = false
  }
}

async function onProviderChange() {
  await loadModelsForProvider(form.value.provider)
}

function buildPayload() {
  return {
    provider: form.value.provider,
    model: form.value.model.trim() || selectedProviderDefault.value,
    enabled: form.value.enabled,
    apiKey: form.value.apiKey.trim(),
  }
}

async function loadSettings() {
  loading.value = true
  testResult.value = null
  try {
    const data = await getJpbotSettings()
    providerOptions.value = data.providers || []
    form.value.provider = data.provider
    form.value.model = data.model
    form.value.enabled = data.enabled
    form.value.apiKey = ''
    apiKeyMasked.value = data.apiKeyMasked || ''
    configured.value = data.configured
    modelOptions.value = data.models || []
    if (!modelOptions.value.length) {
      await loadModelsForProvider(form.value.provider, form.value.model)
    }
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Failed to load settings',
      detail: error.message,
      life: 5000,
    })
  } finally {
    loading.value = false
  }
}

async function saveSettings() {
  saving.value = true
  testResult.value = null
  try {
    const data = await saveJpbotSettings(buildPayload())
    form.value.apiKey = ''
    apiKeyMasked.value = data.apiKeyMasked || ''
    configured.value = data.configured
    modelOptions.value = data.models || modelOptions.value
    toast.add({ severity: 'success', summary: 'JPbot settings saved', life: 3000 })
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

async function runTest() {
  testing.value = true
  testResult.value = null
  try {
    testResult.value = await testJpbotSettings(buildPayload())
  } catch (error) {
    testResult.value = { success: false, message: error.message, replyPreview: '' }
  } finally {
    testing.value = false
  }
}

onMounted(loadSettings)
</script>

<style scoped>
.loading-row {
  display: flex;
  justify-content: center;
  padding: 2rem 0;
}

.field-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.field-block {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.field-label {
  font-size: 0.82rem;
  font-weight: 600;
}

.field-hint {
  font-size: 0.78rem;
  color: var(--p-text-muted-color);
}

.checkbox-label {
  font-size: 0.88rem;
  cursor: pointer;
}

.actions-row {
  padding-top: 0.25rem;
}

@media (max-width: 720px) {
  .field-grid {
    grid-template-columns: 1fr;
  }
}
</style>
