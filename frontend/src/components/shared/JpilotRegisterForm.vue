<template>
  <form class="jpilot-register" @submit.prevent="handleSubmit" novalidate>
    <div class="form-row">
      <div class="form-group">
        <label for="jpilot-name">Name *</label>
        <input
          id="jpilot-name"
          v-model="form.name"
          type="text"
          placeholder="Jane Smith"
          autocomplete="name"
          :class="{ error: errors.name }"
          required
        />
        <span v-if="errors.name" class="error-msg">{{ errors.name }}</span>
      </div>
      <div class="form-group">
        <label for="jpilot-email">Email *</label>
        <input
          id="jpilot-email"
          v-model="form.email"
          type="email"
          placeholder="jane@company.com"
          autocomplete="email"
          :class="{ error: errors.email }"
          required
        />
        <span v-if="errors.email" class="error-msg">{{ errors.email }}</span>
      </div>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="jpilot-use-type">Use type *</label>
        <select
          id="jpilot-use-type"
          v-model="form.use_type"
          :class="{ error: errors.use_type }"
          required
        >
          <option value="" disabled>Select use type…</option>
          <option value="company">Company</option>
          <option value="consultant">Consultant</option>
          <option value="personal">Personal use</option>
        </select>
        <span v-if="errors.use_type" class="error-msg">{{ errors.use_type }}</span>
      </div>
      <div class="form-group">
        <label for="jpilot-country">Country *</label>
        <select
          id="jpilot-country"
          v-model="form.country"
          :class="{ error: errors.country }"
          required
        >
          <option value="" disabled>Select country…</option>
          <option v-for="country in countries" :key="country.code" :value="country.name">
            {{ country.name }}
          </option>
        </select>
        <span v-if="errors.country" class="error-msg">{{ errors.country }}</span>
      </div>
    </div>

    <div v-if="showCompany" class="form-row">
      <div class="form-group">
        <label for="jpilot-company">{{ companyLabel }}</label>
        <input
          id="jpilot-company"
          v-model="form.company"
          type="text"
          :placeholder="companyPlaceholder"
          autocomplete="organization"
          :class="{ error: errors.company }"
          :required="companyRequired"
        />
        <span v-if="errors.company" class="error-msg">{{ errors.company }}</span>
      </div>
      <div v-if="showCompanySize" class="form-group">
        <label for="jpilot-company-size">Company size *</label>
        <select
          id="jpilot-company-size"
          v-model="form.company_size"
          :class="{ error: errors.company_size }"
          required
        >
          <option value="" disabled>Select company size…</option>
          <option v-for="size in companySizes" :key="size" :value="size">{{ size }}</option>
        </select>
        <span v-if="errors.company_size" class="error-msg">{{ errors.company_size }}</span>
      </div>
    </div>

    <div v-if="submitStatus === 'error'" class="alert alert-error" role="alert" aria-live="assertive">
      <i class="pi pi-times-circle"></i>
      {{ errorMessage }}
    </div>

    <button type="submit" class="btn btn-primary submit-btn" :disabled="submitting">
      <i :class="submitting ? 'pi pi-spin pi-spinner' : 'pi pi-arrow-right'"></i>
      {{ submitting ? 'Registering…' : 'Register and continue' }}
    </button>
  </form>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import axios from 'axios'
import countries from '@/data/countries.json'

const emit = defineEmits(['registered'])
const companySizes = ['1–10', '11–50', '51–200', '201–1000', '1000+']

const form = reactive({
  name: '',
  email: '',
  use_type: '',
  country: '',
  company: '',
  company_size: '',
})
const errors = reactive({
  name: '',
  email: '',
  use_type: '',
  country: '',
  company: '',
  company_size: '',
})
const submitting = ref(false)
const submitStatus = ref('')
const errorMessage = ref('')

const showCompany = computed(() => form.use_type === 'company' || form.use_type === 'consultant')
const showCompanySize = computed(() => form.use_type === 'company')
const companyRequired = computed(() => form.use_type === 'company')
const companyLabel = computed(() =>
  form.use_type === 'consultant' ? 'Company / organization' : 'Company *',
)
const companyPlaceholder = computed(() =>
  form.use_type === 'consultant' ? 'Optional' : 'Acme Corp',
)

watch(
  () => form.use_type,
  (value) => {
    if (value === 'personal') {
      form.company = ''
      form.company_size = ''
      errors.company = ''
      errors.company_size = ''
    } else if (value === 'consultant') {
      form.company_size = ''
      errors.company_size = ''
    }
  },
)

const validate = () => {
  let valid = true
  errors.name = errors.email = errors.use_type = errors.country = ''
  errors.company = errors.company_size = ''

  if (!form.name.trim()) {
    errors.name = 'Name is required'
    valid = false
  }
  if (!form.email.trim() || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(form.email)) {
    errors.email = 'Valid email is required'
    valid = false
  }
  if (!form.use_type) {
    errors.use_type = 'Use type is required'
    valid = false
  }
  if (!form.country) {
    errors.country = 'Country is required'
    valid = false
  }
  if (form.use_type === 'company' && !form.company.trim()) {
    errors.company = 'Company is required'
    valid = false
  }
  if (form.use_type === 'company' && !form.company_size) {
    errors.company_size = 'Company size is required'
    valid = false
  }
  return valid
}

const handleSubmit = async () => {
  if (!validate()) return
  submitting.value = true
  submitStatus.value = ''
  try {
    const payload = {
      name: form.name.trim(),
      email: form.email.trim(),
      use_type: form.use_type,
      country: form.country,
      company: form.use_type === 'personal' ? '' : form.company.trim(),
      company_size: form.use_type === 'company' ? form.company_size : '',
    }
    await axios.post('/api/jpilot-interest', payload)
    emit('registered', payload.email)
  } catch (err) {
    submitStatus.value = 'error'
    const detail = err.response?.data?.detail
    errorMessage.value =
      typeof detail === 'string'
        ? detail
        : 'Something went wrong. Please try emailing us directly.'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.jpilot-register {
  display: flex;
  flex-direction: column;
  gap: 18px;
  text-align: left;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 0.78rem;
  font-weight: 700;
  font-family: var(--font-heading);
  letter-spacing: 0.06em;
  color: var(--nt-text-muted);
  text-transform: uppercase;
}

input,
select {
  background: var(--nt-dark-3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 12px 16px;
  color: var(--nt-text);
  font-size: 0.9rem;
  font-family: var(--font-body);
  outline: none;
  width: 100%;
}

input::placeholder {
  color: rgba(255, 255, 255, 0.25);
}

input:focus,
select:focus {
  border-color: var(--nt-primary);
  box-shadow: 0 0 0 3px rgba(0, 168, 224, 0.15);
}

input.error,
select.error {
  border-color: #ef4444;
}

select {
  appearance: none;
  cursor: pointer;
}

select option {
  background: var(--nt-dark-3);
  color: var(--nt-text);
}

.error-msg {
  font-size: 0.78rem;
  color: #ef4444;
}

.alert {
  padding: 14px 18px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.9rem;
}

.alert-error {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
}

.submit-btn {
  align-self: flex-start;
  padding: 14px 28px;
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

@media (max-width: 640px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .submit-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
