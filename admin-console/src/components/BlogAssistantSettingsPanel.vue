<template>
  <div class="content-panel content-panel-padded blog-assistant-settings mt-4">
    <div class="panel-intro">
      <h2 class="section-title">Blog assistant</h2>
      <p class="section-copy">
        LLM used to extract title, slug, excerpt, tags, and other metadata when authors paste a draft in Blogs.
        Stored encrypted in MongoDB (separate from JPbot).
      </p>
    </div>

    <div v-if="loading" class="loading-row">
      <ProgressSpinner style="width: 2rem; height: 2rem" stroke-width="4" />
    </div>

    <form v-else class="settings-form flex flex-column gap-4 mt-4" @submit.prevent="saveSettings">
      <div class="field-grid">
        <div class="field-block">
          <label for="blogProvider" class="field-label">Provider</label>
          <Select
            id="blogProvider"
            v-model="form.provider"
            :options="providerOptions"
            option-label="label"
            option-value="id"
            class="w-full"
            @change="onProviderChange"
          />
        </div>
        <div class="field-block">
          <label for="blogModel" class="field-label">Model</label>
          <Select
            id="blogModel"
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
        <label for="blogApiKey" class="field-label">API key</label>
        <Password
          id="blogApiKey"
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
          <Checkbox v-model="form.enabled" input-id="blogAssistantEnabled" binary />
          <label for="blogAssistantEnabled" class="checkbox-label">Enable blog assistant</label>
        </div>
      </div>

      <div class="actions-row">
        <Button type="submit" label="Save blog assistant" icon="pi pi-check" :loading="saving" />
      </div>
    </form>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import Button from 'primevue/button'
import Checkbox from 'primevue/checkbox'
import Password from 'primevue/password'
import ProgressSpinner from 'primevue/progressspinner'
import Select from 'primevue/select'
import {
  getBlogAssistantModels,
  getBlogAssistantSettings,
  saveBlogAssistantSettings,
} from '@/api/client'

const toast = useToast()

const loading = ref(true)
const saving = ref(false)
const modelsLoading = ref(false)
const providerOptions = ref([])
const modelOptions = ref([])
const apiKeyMasked = ref('')
const configured = ref(false)

const form = ref({
  provider: 'openai',
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
    const data = await getBlogAssistantModels(provider, currentModel)
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

async function loadSettings() {
  loading.value = true
  try {
    const data = await getBlogAssistantSettings()
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
      summary: 'Failed to load blog assistant settings',
      detail: error.message,
      life: 5000,
    })
  } finally {
    loading.value = false
  }
}

async function saveSettings() {
  saving.value = true
  try {
    const data = await saveBlogAssistantSettings({
      provider: form.value.provider,
      model: form.value.model.trim() || selectedProviderDefault.value,
      enabled: form.value.enabled,
      apiKey: form.value.apiKey.trim(),
    })
    form.value.apiKey = ''
    apiKeyMasked.value = data.apiKeyMasked || ''
    configured.value = data.configured
    modelOptions.value = data.models || modelOptions.value
    toast.add({ severity: 'success', summary: 'Blog assistant settings saved', life: 3000 })
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

@media (max-width: 720px) {
  .field-grid {
    grid-template-columns: 1fr;
  }
}
</style>
