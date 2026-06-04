<template>
  <div class="activate-page">
    <section class="page-hero">
      <div class="page-hero-bg"></div>
      <div class="container page-hero-content">
        <span class="section-label reveal">License Activation</span>
        <h1 class="reveal reveal-delay-1">Activate Your<br /><span class="gradient-text">Application</span></h1>
        <p class="page-hero-subtitle reveal reveal-delay-2">
          Confirm deployment details and enter your information to receive a license code by email.
        </p>
      </div>
    </section>

    <section class="section activate-section">
      <div class="container activate-grid">
        <div class="deployment-card reveal">
          <h2>Deployment details</h2>
          <p class="card-subtitle">Received from your application.</p>
          <dl class="param-list">
            <div class="param-row">
              <dt>App fingerprint</dt>
              <dd>{{ appFingerprint || '—' }}</dd>
            </div>
            <div class="param-row">
              <dt>App name</dt>
              <dd>{{ appName || '—' }}</dd>
            </div>
            <div class="param-row">
              <dt>Activation date</dt>
              <dd>{{ activationDate || '—' }}</dd>
            </div>
          </dl>

          <div class="license-meta">
            <div class="meta-item">
              <span class="meta-label">License type</span>
              <span class="meta-value">{{ licensePreview.type }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Validity</span>
              <span class="meta-value">{{ licensePreview.days }} days</span>
            </div>
          </div>
        </div>

        <div class="form-card reveal reveal-delay-1">
          <h2>{{ stepTitle }}</h2>
          <p class="card-subtitle">{{ stepSubtitle }}</p>

          <form class="activate-form" @submit.prevent="step === 'form' ? handleRequest() : step === 'otp' ? handleVerify() : undefined">
            <template v-if="step === 'form'">
              <div class="form-row">
                <div class="form-group">
                  <label>Full Name *</label>
                  <input v-model="form.name" type="text" placeholder="Jane Smith" required />
                </div>
                <div class="form-group">
                  <label>Email Address *</label>
                  <input v-model="form.email" type="email" placeholder="jane@company.com" required />
                </div>
              </div>
              <div class="form-group usage-group">
                <label>License use *</label>
                <div class="usage-segments" role="radiogroup" aria-label="License use">
                  <label
                    v-for="option in usageOptions"
                    :key="option.value"
                    class="usage-segment"
                    :class="{ selected: form.usageType === option.value }"
                  >
                    <input
                      v-model="form.usageType"
                      type="radio"
                      name="usageType"
                      class="usage-segment-input"
                      :value="option.value"
                      required
                    />
                    <span>{{ option.shortLabel }}</span>
                  </label>
                </div>
                <p class="usage-hint">{{ selectedUsageHint }}</p>
              </div>
              <div class="form-group">
                <label>{{ companyRequired ? 'Company *' : 'Company' }}</label>
                <input
                  v-model="form.company"
                  type="text"
                  :placeholder="companyRequired ? 'Your organization name' : 'Optional for personal use'"
                  :required="companyRequired"
                />
              </div>
            </template>

            <template v-else-if="step === 'done'">
              <div class="offline-panel">
                <p class="offline-lead">
                  Your license is active. Enter the license code from your email in JPilot, or download
                  the offline license file for air-gapped activation.
                </p>
                <button
                  type="button"
                  class="btn btn-secondary download-btn"
                  :disabled="!offlineLicense"
                  @click="downloadOfflineLicense"
                >
                  <i class="pi pi-download"></i>
                  Download offline license
                </button>
                <small class="field-hint">
                  Save the <strong>.lic</strong> file and import it in JPilot on systems without internet access.
                </small>
              </div>
            </template>

            <template v-else-if="step === 'otp'">
              <div class="form-group">
                <label>Email verification code *</label>
                <input
                  v-model="otp"
                  type="text"
                  inputmode="numeric"
                  maxlength="6"
                  placeholder="000000"
                  class="otp-input"
                  autocomplete="one-time-code"
                  required
                  @input="onOtpInput"
                />
                <small class="field-hint">
                  Enter the <strong>6-digit verification code</strong> from your email — not the license code (which looks like XXXX-XXXX-XXXX-XXXX).
                </small>
              </div>
            </template>

            <div v-if="submitStatus === 'success'" class="alert alert-success">
              <i class="pi pi-check-circle"></i>
              <span v-if="step === 'done'">
                Email verified. Your license is active — use the license code from your email in your application.
              </span>
              <span v-else>
                Codes sent to <strong>{{ submittedEmail }}</strong>. Enter the verification code to complete activation.
              </span>
            </div>
            <div v-if="submitStatus === 'error'" class="alert alert-error">
              <i class="pi pi-times-circle"></i>
              {{ errorMessage }}
            </div>

            <div class="actions">
              <button
                v-if="step === 'otp'"
                type="button"
                class="btn btn-secondary"
                :disabled="submitting"
                @click="backToForm"
              >
                Back
              </button>
              <button
                v-if="step === 'form' || step === 'otp'"
                type="submit"
                class="btn btn-primary submit-btn"
                :disabled="submitting || !canSubmit"
              >
                <i :class="submitting ? 'pi pi-spin pi-spinner' : step === 'form' ? 'pi pi-envelope' : 'pi pi-check'"></i>
                {{
                  submitting
                    ? 'Please wait…'
                    : step === 'form'
                      ? 'Generate license code'
                      : step === 'done'
                        ? 'Activation complete'
                        : 'Confirm email'
                }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'
import { requestActivation, verifyActivationOtp } from '@/api/licensing.js'

const route = useRoute()

const appFingerprint = computed(() => String(route.query.appfingerprint || '').trim())
const appName = computed(() => String(route.query.appname || '').trim())
const activationDate = computed(() => String(route.query.activationdate || '').trim())

const step = ref('form')
const usageOptions = [
  {
    value: 'personal',
    shortLabel: 'Personal',
    description: 'Individual learning, testing, or non-commercial projects.',
  },
  {
    value: 'onprem',
    shortLabel: 'On-premises',
    description: 'Internal deployment in infrastructure owned by your organization.',
  },
  {
    value: 'cloud',
    shortLabel: 'Cloud',
    description: 'Internal deployment in cloud resources owned by your organization.',
  },
  {
    value: 'consulting',
    shortLabel: 'Consulting',
    description: 'Deployment for a client organization, not your employer.',
  },
]
const form = reactive({
  name: '',
  email: '',
  company: '',
  usageType: 'personal',
})

const licensePreview = computed(() => {
  if (form.usageType === 'consulting') {
    return { type: 'Trial', days: 30 }
  }
  return { type: 'Free', days: 90 }
})

const selectedUsageHint = computed(() => {
  const match = usageOptions.find((option) => option.value === form.usageType)
  return match?.description ?? ''
})

const companyRequired = computed(() => form.usageType !== 'personal')
const otp = ref('')

const submitting = ref(false)
const submitStatus = ref('')
const errorMessage = ref('')
const submittedEmail = ref('')
const offlineLicense = ref(null)

const stepTitle = computed(() => {
  if (step.value === 'form') return 'Your information'
  if (step.value === 'otp') return 'Confirm your email'
  return 'Activation complete'
})

const stepSubtitle = computed(() => {
  if (step.value === 'form') return 'Required to generate and email your license code.'
  if (step.value === 'otp') return `Enter the 6-digit code sent to ${submittedEmail.value}.`
  return 'Use your license code in JPilot or download the offline license file below.'
})

const canSubmit = computed(() => {
  if (step.value === 'form') {
    return (
      appFingerprint.value &&
      appName.value &&
      activationDate.value &&
      form.name.trim() &&
      form.email.trim() &&
      form.usageType &&
      (!companyRequired.value || form.company.trim())
    )
  }
  if (step.value === 'otp') {
    return normalizeOtp(otp.value).length === 6
  }
  return false
})

function normalizeOtp(value) {
  return String(value || '').replace(/\D/g, '').slice(0, 6)
}

function onOtpInput(event) {
  otp.value = normalizeOtp(event.target.value)
}

function backToForm() {
  step.value = 'form'
  otp.value = ''
  submitStatus.value = ''
  errorMessage.value = ''
  offlineLicense.value = null
}

function buildOfflineLicenseFilename(appNameValue, exportedAt) {
  const safeName = String(appNameValue || 'app').replace(/[^\w-]+/g, '') || 'app'
  const date = exportedAt ? new Date(exportedAt) : new Date()
  const dd = String(date.getUTCDate()).padStart(2, '0')
  const mm = String(date.getUTCMonth() + 1).padStart(2, '0')
  const yyyy = String(date.getUTCFullYear())
  return `${safeName}_app_${dd}${mm}${yyyy}.lic`
}

function downloadOfflineLicense() {
  if (!offlineLicense.value) return
  const blob = new Blob([JSON.stringify(offlineLicense.value, null, 2)], {
    type: 'application/octet-stream',
  })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = buildOfflineLicenseFilename(appName.value, offlineLicense.value.exportedAt)
  link.click()
  URL.revokeObjectURL(url)
}

async function handleRequest() {
  if (!canSubmit.value) return
  submitting.value = true
  submitStatus.value = ''
  errorMessage.value = ''
  try {
    await requestActivation({
      appFingerprint: appFingerprint.value,
      appName: appName.value,
      activationDate: activationDate.value,
      name: form.name.trim(),
      email: form.email.trim().toLowerCase(),
      company: form.company.trim(),
      usageType: form.usageType,
    })
    submittedEmail.value = form.email.trim().toLowerCase()
    step.value = 'otp'
    submitStatus.value = 'success'
  } catch (error) {
    submitStatus.value = 'error'
    errorMessage.value = error.message || 'Something went wrong. Please try again.'
  } finally {
    submitting.value = false
  }
}

async function handleVerify() {
  if (!canSubmit.value) return
  submitting.value = true
  submitStatus.value = ''
  errorMessage.value = ''
  try {
    const result = await verifyActivationOtp({
      appFingerprint: appFingerprint.value,
      appName: appName.value,
      email: submittedEmail.value || form.email.trim().toLowerCase(),
      otp: normalizeOtp(otp.value),
    })
    offlineLicense.value = result.offlineLicense || null
    step.value = 'done'
    submitStatus.value = 'success'
  } catch (error) {
    submitStatus.value = 'error'
    errorMessage.value = error.message || 'Invalid verification code. Please try again.'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.page-hero {
  min-height: 40vh;
  display: flex;
  align-items: center;
  background: var(--nt-dark);
  padding: 120px 0 60px;
  position: relative;
  overflow: hidden;
}
.page-hero-bg {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 40% 60%, rgba(0, 123, 167, 0.14) 0%, transparent 60%);
}
.page-hero-content { position: relative; z-index: 1; }
.page-hero-subtitle {
  font-size: 1.05rem;
  color: var(--nt-text-muted);
  margin-top: 16px;
  max-width: 560px;
  line-height: 1.75;
}

.activate-section { background: var(--nt-dark-2); }
.activate-grid {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 32px;
  align-items: start;
}

.deployment-card,
.form-card {
  background: var(--nt-card-bg);
  border: 1px solid var(--nt-border);
  border-radius: var(--nt-radius);
  padding: 28px;
}

.deployment-card h2,
.form-card h2 {
  font-size: 1.35rem;
  margin-bottom: 8px;
}

.card-subtitle {
  color: var(--nt-text-muted);
  font-size: 0.9rem;
  margin-bottom: 24px;
}

.param-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.param-row {
  display: grid;
  grid-template-columns: 8.5rem 1fr;
  gap: 12px;
  align-items: start;
}

.param-row dt {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--nt-text-muted);
  font-family: var(--font-heading);
}

.param-row dd {
  margin: 0;
  font-family: Consolas, 'Courier New', monospace;
  font-size: 0.82rem;
  word-break: break-all;
  color: var(--nt-text-light);
}

.license-meta {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid var(--nt-border);
}

.meta-item {
  background: var(--nt-dark-3);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  padding: 14px 16px;
}

.meta-label {
  display: block;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--nt-text-muted);
  font-family: var(--font-heading);
  margin-bottom: 6px;
}

.meta-value {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--nt-text-light);
}

.activate-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 0.8rem;
  font-weight: 700;
  font-family: var(--font-heading);
  letter-spacing: 0.06em;
  color: var(--nt-text-muted);
  text-transform: uppercase;
}

input {
  background: var(--nt-dark-3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 12px 16px;
  color: var(--nt-text);
  font-size: 0.9rem;
  font-family: var(--font-body);
  transition: var(--nt-transition);
  outline: none;
  width: 100%;
}

input:focus {
  border-color: var(--nt-primary);
  box-shadow: 0 0 0 3px rgba(0, 123, 167, 0.15);
}

.field-hint {
  color: var(--nt-text-muted);
  font-size: 0.78rem;
  line-height: 1.5;
}

.otp-input {
  font-family: Consolas, 'Courier New', monospace;
  font-size: 1.25rem;
  letter-spacing: 0.35em;
  text-align: center;
}

.usage-group {
  gap: 8px;
}

.usage-segments {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.usage-segment {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background: var(--nt-dark-3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 9px 14px;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--nt-text-muted);
  transition: var(--nt-transition);
  user-select: none;
}

.usage-segment:hover {
  border-color: rgba(0, 123, 167, 0.35);
  color: var(--nt-text-light);
}

.usage-segment.selected {
  border-color: var(--nt-primary);
  background: rgba(0, 123, 167, 0.1);
  color: var(--nt-text-light);
  box-shadow: 0 0 0 1px rgba(0, 123, 167, 0.2);
}

.usage-segment-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
  pointer-events: none;
}

.usage-hint {
  margin: 0;
  font-size: 0.76rem;
  line-height: 1.45;
  color: var(--nt-text-muted);
}

.offline-panel {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.offline-lead {
  margin: 0;
  color: var(--nt-text-muted);
  font-size: 0.92rem;
  line-height: 1.6;
}

.download-btn {
  align-self: flex-start;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.actions {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.alert {
  padding: 14px 18px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.9rem;
}

.alert-success {
  background: rgba(34, 197, 94, 0.1);
  border: 1px solid rgba(34, 197, 94, 0.3);
  color: #4ade80;
}

.alert-error {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
}

.submit-btn {
  padding: 14px 32px;
  font-size: 0.95rem;
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none !important;
}

@media (max-width: 1024px) {
  .activate-grid { grid-template-columns: 1fr; }
}

@media (max-width: 640px) {
  .form-row,
  .param-row,
  .license-meta { grid-template-columns: 1fr; }

  .usage-segment {
    flex: 1 1 calc(50% - 4px);
    min-width: 0;
  }
}
</style>
