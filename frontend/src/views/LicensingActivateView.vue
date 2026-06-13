<template>
  <div class="activate-page">
    <section class="page-hero">
      <div class="page-hero-bg"></div>
      <div class="container page-hero-content">
        <span class="section-label reveal">License Activation</span>
        <h1 class="reveal reveal-delay-1">Activate Your<br /><span class="gradient-text">Application</span></h1>
        <p class="page-hero-subtitle reveal reveal-delay-2">{{ ui.heroSubtitle }}</p>
      </div>
    </section>

    <section class="section activate-section">
      <div class="container activate-grid">
        <aside class="letter-card reveal">
          <div class="letter-toolbar">
            <div class="lang-flags" role="group" aria-label="Language">
              <button
                v-for="code in LETTER_LOCALES"
                :key="code"
                type="button"
                class="lang-flag"
                :class="{ active: locale === code }"
                :title="LOCALE_FLAGS[code].label"
                :aria-label="LOCALE_FLAGS[code].label"
                :aria-pressed="locale === code"
                @click="locale = code"
              >
                <img
                  class="lang-flag-img"
                  :src="`/flags/${LOCALE_FLAGS[code].iso}.png`"
                  :alt="LOCALE_FLAGS[code].label"
                  width="28"
                  height="20"
                  loading="lazy"
                  decoding="async"
                />
              </button>
            </div>
          </div>

          <div
            class="letter-scroll"
            :class="{ 'letter-scroll-rtl': letter.rtl }"
            :dir="letter.rtl ? 'rtl' : 'ltr'"
          >
            <p class="letter-greeting">{{ letter.greeting }}</p>
            <p
              v-for="(paragraph, index) in letter.paragraphs"
              :key="index"
              class="letter-paragraph"
            >
              <template v-for="(segment, segIndex) in splitBoldSegments(paragraph)" :key="segIndex">
                <strong v-if="segment.bold">{{ segment.text }}</strong>
                <span v-else>{{ segment.text }}</span>
              </template>
            </p>
            <div class="letter-signature">
              <p class="letter-closing">{{ letter.closing }}</p>
              <p class="letter-author">{{ letter.author }}</p>
              <p class="letter-role">{{ letter.role }}</p>
              <p class="letter-company">{{ letter.company }}</p>
              <a :href="letter.website" class="letter-link" target="_blank" rel="noopener noreferrer">
                {{ letter.website }}
              </a>
            </div>
          </div>
        </aside>

        <div class="form-card reveal reveal-delay-1">
          <h2>{{ stepTitle }}</h2>
          <p class="card-subtitle">{{ stepSubtitle }}</p>

          <form
            class="activate-form"
            @submit.prevent="
              step === 'recover'
                ? handleRecover()
                : step === 'form'
                  ? handleRequest()
                  : step === 'otp'
                    ? handleVerify()
                    : undefined
            "
          >
            <template v-if="step === 'checking'">
              <div class="checking-panel">
                <i class="pi pi-spin pi-spinner"></i>
                <p>{{ ui.checkingDeployment }}</p>
              </div>
            </template>

            <template v-else-if="step === 'recover'">
              <p class="recover-lead">{{ ui.recoverLead }}</p>
              <div class="form-group">
                <label>{{ ui.email }} *</label>
                <input
                  v-model="form.email"
                  type="email"
                  placeholder="jane@company.com"
                  required
                />
              </div>
              <div class="form-group">
                <label>{{ ui.licenseCodeOptional }}</label>
                <input
                  v-model="recoverLicenseCode"
                  type="text"
                  :placeholder="ui.licenseCodePlaceholder"
                  autocomplete="off"
                />
                <small class="field-hint">{{ ui.licenseCodeHint }}</small>
              </div>
              <button type="button" class="link-btn" @click="goToNewActivation">
                {{ ui.newActivationInstead }}
              </button>
            </template>

            <template v-else-if="step === 'form'">
              <div class="form-row">
                <div class="form-group">
                  <label>{{ ui.fullName }} *</label>
                  <input v-model="form.name" type="text" placeholder="Jane Smith" required />
                </div>
                <div class="form-group">
                  <label>{{ ui.email }} *</label>
                  <input v-model="form.email" type="email" placeholder="jane@company.com" required />
                </div>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label>{{ ui.country }} *</label>
                  <AutoComplete
                    v-model="selectedCountry"
                    option-label="name"
                    :suggestions="filteredCountries"
                    :placeholder="ui.countryPlaceholder"
                    force-selection
                    dropdown
                    class="country-autocomplete w-full"
                    @complete="searchCountries"
                  />
                </div>
                <div class="form-group">
                  <label>{{ companyRequired ? `${ui.company} *` : ui.company }}</label>
                  <input
                    v-model="form.company"
                    type="text"
                    :placeholder="companyRequired ? ui.companyRequired : ui.companyOptional"
                    :required="companyRequired"
                  />
                </div>
              </div>
              <div class="form-group usage-group">
                <label>{{ ui.licenseUse }} *</label>
                <div class="usage-segments" role="radiogroup" :aria-label="ui.licenseUse">
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

              <div class="deployment-panel">
                <h3 class="deployment-heading">{{ ui.deploymentTitle }}</h3>
                <p class="deployment-subtitle">{{ ui.deploymentSubtitle }}</p>
                <dl class="param-list">
                  <div class="param-row">
                    <dt>{{ ui.appName }}</dt>
                    <dd class="param-value">{{ appName || '—' }}</dd>
                  </div>
                  <div class="param-row">
                    <dt>{{ ui.activationDate }}</dt>
                    <dd class="param-value">{{ activationDateDisplay }}</dd>
                  </div>
                </dl>
                <div class="license-meta">
                  <div class="meta-item">
                    <span class="meta-label">{{ ui.licenseType }}</span>
                    <span class="meta-value">{{ licensePreview.type }}</span>
                  </div>
                  <div class="meta-item">
                    <span class="meta-label">{{ ui.validity }}</span>
                    <span class="meta-value">{{ licensePreview.days }} {{ ui.days }}</span>
                  </div>
                </div>
              </div>
            </template>

            <template v-else-if="step === 'done'">
              <div v-if="existingActivation && assignedLicense" class="assigned-license-panel">
                <h3 class="deployment-heading">{{ ui.assignedLicenseTitle }}</h3>
                <dl class="param-list">
                  <div class="param-row">
                    <dt>{{ ui.licenseHolder }}</dt>
                    <dd class="param-value">{{ assignedLicense.name || '—' }}</dd>
                  </div>
                  <div class="param-row">
                    <dt>{{ ui.email }}</dt>
                    <dd class="param-value">{{ assignedLicense.email || '—' }}</dd>
                  </div>
                  <div class="param-row">
                    <dt>{{ ui.appName }}</dt>
                    <dd class="param-value">{{ assignedLicense.application || appName || '—' }}</dd>
                  </div>
                  <div class="param-row">
                    <dt>{{ ui.licenseType }}</dt>
                    <dd class="param-value">{{ formatLicenseType(assignedLicense.licenseType) }}</dd>
                  </div>
                  <div class="param-row">
                    <dt>{{ ui.registeredOn }}</dt>
                    <dd class="param-value">{{ formatLicenseDate(assignedLicense.registrationDate) }}</dd>
                  </div>
                  <div class="param-row">
                    <dt>{{ ui.expiresOn }}</dt>
                    <dd class="param-value">{{ formatLicenseDate(assignedLicense.expirationDate) }}</dd>
                  </div>
                  <div class="param-row">
                    <dt>{{ ui.licenseStatus }}</dt>
                    <dd class="param-value">{{ formatLicenseStatus(assignedLicense.status) }}</dd>
                  </div>
                </dl>
              </div>

              <div class="offline-panel">
                <div v-if="licenseCode" class="license-code-panel">
                  <span class="meta-label">{{ ui.licenseCode }}</span>
                  <div class="license-code-row">
                    <code class="license-code">{{ licenseCode }}</code>
                    <button type="button" class="btn btn-secondary copy-btn" @click="copyLicenseCode">
                      {{ copiedLicenseCode ? ui.copiedLicenseCode : ui.copyLicenseCode }}
                    </button>
                  </div>
                </div>
                <p class="offline-lead">
                  {{ existingActivation ? ui.stepExistingSubtitle : ui.offlineLead }}
                </p>
                <button
                  type="button"
                  class="btn btn-secondary download-btn"
                  :disabled="!offlineLicense"
                  @click="downloadOfflineLicense"
                >
                  <i class="pi pi-download"></i>
                  {{ ui.downloadOffline }}
                </button>
                <small class="field-hint">{{ ui.offlineHint }}</small>
              </div>
            </template>

            <template v-else-if="step === 'otp'">
              <div class="form-group">
                <label>{{ ui.otpLabel }} *</label>
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
                <small class="field-hint">{{ ui.otpHint }}</small>
              </div>
            </template>

            <div v-if="submitStatus === 'success'" class="alert alert-success">
              <i class="pi pi-check-circle"></i>
              <span v-if="step === 'done'">{{ ui.successDone }}</span>
              <span v-else>{{ ui.successOtp(submittedEmail) }}</span>
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
                {{ ui.back }}
              </button>
              <button
                v-if="step === 'recover' || step === 'form' || step === 'otp'"
                type="submit"
                class="btn btn-primary submit-btn"
                :disabled="submitting || !canSubmit"
              >
                <i
                  :class="
                    submitting
                      ? 'pi pi-spin pi-spinner'
                      : step === 'recover'
                        ? 'pi pi-search'
                        : step === 'form'
                          ? 'pi pi-envelope'
                          : 'pi pi-check'
                  "
                ></i>
                {{
                  submitting
                    ? ui.submitWait
                    : step === 'recover'
                      ? ui.submitRecover
                      : step === 'form'
                        ? ui.submitGenerate
                        : ui.submitConfirm
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
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import AutoComplete from 'primevue/autocomplete'
import {
  checkRecoverableLicense,
  fetchExistingActivation,
  requestActivation,
  requestLicenseRecovery,
  verifyActivationOtp,
  verifyLicenseRecovery,
} from '@/api/licensing.js'
import { CountryService } from '@/service/CountryService'
import {
  ACTIVATION_LETTERS,
  ACTIVATION_UI,
  LETTER_LOCALES,
  LOCALE_FLAGS,
  splitBoldSegments,
  uiLocaleFor,
} from '@/data/activation-i18n.js'

const route = useRoute()
const locale = ref('en')

const letter = computed(() => ACTIVATION_LETTERS[locale.value])
const ui = computed(() => ACTIVATION_UI[uiLocaleFor(locale.value)] || ACTIVATION_UI.en)

const appFingerprint = computed(() => String(route.query.appfingerprint || '').trim())
const appName = computed(() => String(route.query.appname || '').trim())
const activationDate = computed(() => String(route.query.activationdate || '').trim())
const licenseCodeFromQuery = computed(() => String(route.query.licensecode || route.query.licenseCode || '').trim())

function formatActivationDate(value) {
  if (!value) return '—'
  const text = String(value).trim()
  const normalized = /[zZ]$/.test(text) || /[+-]\d{2}:\d{2}$/.test(text) ? text : `${text}Z`
  const date = new Date(normalized)
  if (Number.isNaN(date.getTime())) return '—'
  const dd = String(date.getUTCDate()).padStart(2, '0')
  const mm = String(date.getUTCMonth() + 1).padStart(2, '0')
  const yyyy = String(date.getUTCFullYear())
  return `${dd}-${mm}-${yyyy}`
}

const activationDateDisplay = computed(() => formatActivationDate(activationDate.value))
const hasDeploymentParams = computed(() => Boolean(appFingerprint.value && appName.value))

const step = ref(hasDeploymentParams.value ? 'checking' : 'form')
const checkingDeployment = ref(hasDeploymentParams.value)
const existingActivation = ref(false)
const assignedLicense = ref(null)
const recoverMode = ref(false)
const recoverLicenseCode = ref('')
const usageOptionKeys = ['personal', 'onprem', 'cloud', 'consulting']

const usageOptions = computed(() =>
  usageOptionKeys.map((value) => ({
    value,
    shortLabel: ui.value.usage[value].short,
    description: ui.value.usage[value].hint,
  })),
)

const form = reactive({
  name: '',
  email: '',
  company: '',
  usageType: 'personal',
})

const countries = ref([])
const selectedCountry = ref(null)
const filteredCountries = ref([])

onMounted(() => {
  CountryService.getCountries().then((data) => {
    countries.value = data
  })
})

watch([appFingerprint, appName, licenseCodeFromQuery], () => {
  if (licenseCodeFromQuery.value) {
    recoverLicenseCode.value = licenseCodeFromQuery.value
  }
  loadExistingActivation()
}, { immediate: true })

function formatLicenseDate(value) {
  if (!value) return '—'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return '—'
  return date.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })
}

function formatLicenseType(value) {
  if (!value) return '—'
  return String(value).replace(/_/g, ' ').replace(/\b\w/g, (char) => char.toUpperCase())
}

function formatLicenseStatus(status) {
  const labels = {
    active: ui.value.statusActive,
    expired: ui.value.statusExpired,
    deactivated: ui.value.statusDeactivated,
    expired_blocked: ui.value.statusExpiredBlocked,
  }
  return labels[status] || status || ui.value.statusActive
}

async function loadExistingActivation() {
  if (!hasDeploymentParams.value) {
    checkingDeployment.value = false
    if (step.value === 'checking') step.value = 'form'
    return
  }

  checkingDeployment.value = true
  if (step.value !== 'done' && step.value !== 'otp') step.value = 'checking'
  try {
    const existing = await fetchExistingActivation(appFingerprint.value, appName.value, {
      licenseCode: recoverLicenseCode.value || licenseCodeFromQuery.value,
      activationDate: activationDate.value,
    })
    if (existing) {
      applyExistingActivation(existing)
    } else if (step.value === 'checking') {
      step.value = 'recover'
    }
  } catch {
    if (step.value === 'checking') step.value = 'recover'
  } finally {
    checkingDeployment.value = false
  }
}

function applyExistingActivation(existing) {
  existingActivation.value = true
  assignedLicense.value = existing
  licenseCode.value = existing.licenseCode || ''
  offlineLicense.value = existing.offlineLicense || null
  submittedEmail.value = existing.email || ''
  step.value = 'done'
  submitStatus.value = 'success'
  errorMessage.value = ''
}

function searchCountries(event) {
  setTimeout(() => {
    if (!event.query.trim().length) {
      filteredCountries.value = [...countries.value]
    } else {
      filteredCountries.value = countries.value.filter((country) =>
        country.name.toLowerCase().startsWith(event.query.toLowerCase()),
      )
    }
  }, 250)
}

function selectedCountryName() {
  return typeof selectedCountry.value === 'object' && selectedCountry.value?.name
    ? selectedCountry.value.name.trim()
    : ''
}

const licensePreview = computed(() => {
  if (form.usageType === 'consulting') {
    return { type: 'Trial', days: 30 }
  }
  return { type: 'Free', days: 90 }
})

const selectedUsageHint = computed(() => {
  const match = usageOptions.value.find((option) => option.value === form.usageType)
  return match?.description ?? ''
})

const companyRequired = computed(() => form.usageType !== 'personal')
const otp = ref('')

const submitting = ref(false)
const submitStatus = ref('')
const errorMessage = ref('')
const submittedEmail = ref('')
const offlineLicense = ref(null)
const licenseCode = ref('')
const copiedLicenseCode = ref(false)

const stepTitle = computed(() => {
  if (step.value === 'checking') return ui.value.stepCheckingTitle
  if (step.value === 'recover') return ui.value.stepRecoverTitle
  if (step.value === 'form') return ui.value.stepFormTitle
  if (step.value === 'otp') return recoverMode.value ? ui.value.stepRecoverOtpTitle : ui.value.stepOtpTitle
  if (existingActivation.value) return ui.value.stepExistingTitle
  return ui.value.stepDoneTitle
})

const stepSubtitle = computed(() => {
  if (step.value === 'checking') return ui.value.stepCheckingSubtitle
  if (step.value === 'recover') return ui.value.stepRecoverSubtitle
  if (step.value === 'form') return ui.value.stepFormSubtitle
  if (step.value === 'otp') {
    return recoverMode.value
      ? ui.value.stepRecoverOtpSubtitle(submittedEmail.value)
      : ui.value.stepOtpSubtitle(submittedEmail.value)
  }
  if (existingActivation.value) return ui.value.stepExistingSubtitle
  return ui.value.stepDoneSubtitle
})

const canSubmit = computed(() => {
  if (step.value === 'recover') {
    return appFingerprint.value && appName.value && form.email.trim()
  }
  if (step.value === 'form') {
    return (
      appFingerprint.value &&
      appName.value &&
      activationDate.value &&
      form.name.trim() &&
      form.email.trim() &&
      selectedCountryName() &&
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
  if (existingActivation.value) return
  recoverMode.value = false
  step.value = 'recover'
  otp.value = ''
  submitStatus.value = ''
  errorMessage.value = ''
  offlineLicense.value = null
  licenseCode.value = ''
}

function goToNewActivation() {
  recoverMode.value = false
  step.value = 'form'
  submitStatus.value = ''
  errorMessage.value = ''
}

async function handleRecover() {
  if (!canSubmit.value) return
  submitting.value = true
  submitStatus.value = ''
  errorMessage.value = ''
  const email = form.email.trim().toLowerCase()
  try {
    if (recoverLicenseCode.value.trim()) {
      const existing = await fetchExistingActivation(appFingerprint.value, appName.value, {
        licenseCode: recoverLicenseCode.value.trim(),
        activationDate: activationDate.value,
      })
      if (existing) {
        applyExistingActivation(existing)
        return
      }
      throw new Error(ui.value.licenseCodeNotFound)
    }

    const check = await checkRecoverableLicense(email, appName.value)
    if (!check.found) {
      step.value = 'form'
      form.email = email
      submitStatus.value = ''
      errorMessage.value = ui.value.noExistingLicense
      return
    }

    await requestLicenseRecovery({
      appFingerprint: appFingerprint.value,
      appName: appName.value,
      activationDate: activationDate.value || new Date().toISOString(),
      email,
    })
    submittedEmail.value = email
    recoverMode.value = true
    step.value = 'otp'
    submitStatus.value = 'success'
  } catch (error) {
    submitStatus.value = 'error'
    errorMessage.value = error.message || 'Something went wrong. Please try again.'
  } finally {
    submitting.value = false
  }
}

async function copyLicenseCode() {
  if (!licenseCode.value) return
  try {
    await navigator.clipboard.writeText(licenseCode.value)
    copiedLicenseCode.value = true
    setTimeout(() => {
      copiedLicenseCode.value = false
    }, 2000)
  } catch {
    /* ignore clipboard failures */
  }
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
      country: selectedCountryName(),
      company: form.company.trim(),
      usageType: form.usageType,
    })
    submittedEmail.value = form.email.trim().toLowerCase()
    step.value = 'otp'
    submitStatus.value = 'success'
  } catch (error) {
    if (String(error.message || '').includes('already activated')) {
      try {
        const existing = await fetchExistingActivation(appFingerprint.value, appName.value)
        if (existing) {
          applyExistingActivation(existing)
          return
        }
      } catch {
        /* fall through to error message */
      }
    }
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
    const payload = {
      appFingerprint: appFingerprint.value,
      appName: appName.value,
      email: submittedEmail.value || form.email.trim().toLowerCase(),
      otp: normalizeOtp(otp.value),
    }
    const result = recoverMode.value
      ? await verifyLicenseRecovery(payload)
      : await verifyActivationOtp(payload)
    offlineLicense.value = result.offlineLicense || null
    licenseCode.value = result.licenseCode || ''
    existingActivation.value = recoverMode.value
    recoverMode.value = false
    step.value = 'done'
    submitStatus.value = 'success'
    if (result.email) assignedLicense.value = result
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
  grid-template-columns: 1.05fr 0.95fr;
  gap: 32px;
  align-items: start;
}

.letter-card {
  position: sticky;
  top: 96px;
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - 120px);
  background: var(--nt-card-bg);
  border: 1px solid var(--nt-border);
  border-radius: var(--nt-radius);
  overflow: hidden;
}

.letter-toolbar {
  display: flex;
  justify-content: flex-end;
  padding: 14px 18px;
  border-bottom: 1px solid var(--nt-border);
  background: rgba(0, 123, 167, 0.06);
}

.lang-flags {
  display: flex;
  gap: 8px;
}

.lang-flag {
  width: 40px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 8px;
  background: var(--nt-dark-3);
  cursor: pointer;
  transition: var(--nt-transition);
  padding: 0;
  overflow: hidden;
}

.lang-flag-img {
  display: block;
  width: 28px;
  height: 20px;
  object-fit: cover;
  border-radius: 2px;
}

.lang-flag:hover {
  border-color: rgba(0, 123, 167, 0.45);
  transform: translateY(-1px);
}

.lang-flag.active {
  border-color: var(--nt-primary);
  background: rgba(0, 123, 167, 0.14);
  box-shadow: 0 0 0 1px rgba(0, 123, 167, 0.25);
}

.letter-scroll {
  padding: 24px 28px 28px;
  overflow-y: auto;
}

.letter-scroll-rtl {
  font-family: 'Segoe UI', Tahoma, 'Noto Naskh Arabic', 'Arial Unicode MS', sans-serif;
}

.letter-scroll-rtl .letter-link {
  direction: ltr;
  display: inline-block;
  unicode-bidi: embed;
}

.letter-greeting {
  margin: 0 0 16px;
  font-family: var(--font-heading);
  font-size: 1.08rem;
  font-weight: 700;
  color: var(--nt-text-light);
}

.letter-paragraph {
  margin: 0 0 14px;
  font-size: 0.86rem;
  line-height: 1.75;
  color: var(--nt-text-muted);
}

.letter-paragraph :deep(strong) {
  color: var(--nt-text-light);
  font-weight: 600;
}

.letter-signature {
  margin-top: 22px;
  padding-top: 18px;
  border-top: 1px solid var(--nt-border);
}

.letter-closing {
  margin: 0 0 12px;
  font-size: 0.88rem;
  color: var(--nt-text-muted);
}

.letter-author {
  margin: 0;
  font-size: 0.92rem;
  font-weight: 700;
  color: var(--nt-text-light);
}

.letter-role,
.letter-company {
  margin: 4px 0 0;
  font-size: 0.82rem;
  color: var(--nt-text-muted);
}

.letter-link {
  display: inline-block;
  margin-top: 10px;
  font-size: 0.82rem;
  color: var(--nt-primary);
  text-decoration: none;
}

.letter-link:hover {
  text-decoration: underline;
}

.form-card {
  background: var(--nt-card-bg);
  border: 1px solid var(--nt-border);
  border-radius: var(--nt-radius);
  padding: 28px;
}

.form-card h2 {
  font-size: 1.35rem;
  margin-bottom: 8px;
}

.card-subtitle {
  color: var(--nt-text-muted);
  font-size: 0.9rem;
  margin-bottom: 24px;
}

.deployment-panel {
  margin-top: 4px;
  padding: 20px;
  background: var(--nt-dark-3);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
}

.deployment-heading {
  margin: 0 0 6px;
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--nt-text-light);
}

.deployment-subtitle {
  margin: 0 0 16px;
  font-size: 0.82rem;
  color: var(--nt-text-muted);
}

.param-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.param-row {
  display: grid;
  grid-template-columns: 7.5rem 1fr;
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
  word-break: break-word;
  color: var(--nt-text-light);
}

.param-row dd.param-value {
  font-family: var(--font-body);
  font-size: 0.88rem;
  font-weight: 600;
  line-height: 1.4;
}

.license-meta {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.meta-item {
  background: rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  padding: 12px 14px;
}

.meta-label {
  display: block;
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--nt-text-muted);
  font-family: var(--font-heading);
  margin-bottom: 4px;
}

.meta-value {
  font-size: 0.88rem;
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

.country-autocomplete :deep(.p-autocomplete-input) {
  width: 100%;
  background: var(--nt-dark-3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 12px 16px;
  color: var(--nt-text);
  font-size: 0.9rem;
  font-family: var(--font-body);
  transition: var(--nt-transition);
}

.country-autocomplete :deep(.p-autocomplete-input:focus) {
  border-color: var(--nt-primary);
  box-shadow: 0 0 0 3px rgba(0, 123, 167, 0.15);
}

.country-autocomplete :deep(.p-autocomplete-dropdown) {
  background: var(--nt-dark-3);
  border-color: rgba(255, 255, 255, 0.1);
  color: var(--nt-text-muted);
}

.w-full {
  width: 100%;
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

.recover-lead {
  margin: 0 0 8px;
  color: var(--nt-text-muted);
  font-size: 0.92rem;
  line-height: 1.6;
}

.link-btn {
  align-self: flex-start;
  background: none;
  border: none;
  color: var(--nt-primary);
  cursor: pointer;
  font-size: 0.86rem;
  padding: 0;
  text-decoration: underline;
  text-underline-offset: 2px;
}

.checking-panel {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 14px;
  min-height: 220px;
  color: var(--nt-text-muted);
  text-align: center;
}

.checking-panel .pi {
  font-size: 1.6rem;
  color: var(--nt-primary);
}

.checking-panel p {
  margin: 0;
  font-size: 0.92rem;
}

.assigned-license-panel {
  margin-bottom: 8px;
  padding: 20px;
  background: var(--nt-dark-3);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
}

.checking-hint {
  margin: 0;
  color: var(--nt-text-muted);
  font-size: 0.88rem;
}

.license-code-panel {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px;
  background: var(--nt-dark-3);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
}

.license-code-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}

.license-code {
  font-family: Consolas, 'Courier New', monospace;
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  color: var(--nt-text-light);
  word-break: break-all;
}

.copy-btn {
  padding: 10px 16px;
  font-size: 0.82rem;
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

@media (max-width: 1100px) {
  .activate-grid { grid-template-columns: 1fr; }
  .letter-card {
    position: static;
    max-height: none;
  }
  .letter-scroll {
    max-height: 420px;
  }
}

@media (max-width: 640px) {
  .form-row,
  .param-row,
  .license-meta { grid-template-columns: 1fr; }

  .usage-segment {
    flex: 1 1 calc(50% - 4px);
    min-width: 0;
  }

  .letter-scroll {
    padding: 18px 20px 22px;
    max-height: 360px;
  }
}
</style>
