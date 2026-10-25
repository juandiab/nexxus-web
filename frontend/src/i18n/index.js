import { ref, watch } from 'vue'
import { AI_INTEGRATION_LOCALE_KEY } from '@/data/aiIntegrationCopy.js'
import { es } from '@/i18n/messages/es.js'

/** Site-wide locale. English is the default until the visitor chooses. */
export const LOCALE_KEY = 'nexxus-locale'

const VALID = new Set(['en', 'es'])

function readStored(key) {
  try {
    const value = localStorage.getItem(key)
    return VALID.has(value) ? value : null
  } catch {
    return null
  }
}

function readInitialLocale() {
  const stored = readStored(LOCALE_KEY)
  if (stored) return stored
  // Honor an explicit choice already saved by the AI Tech page toggle.
  const legacy = readStored(AI_INTEGRATION_LOCALE_KEY)
  if (legacy) {
    try {
      localStorage.setItem(LOCALE_KEY, legacy)
    } catch {
      /* private mode */
    }
    return legacy
  }
  return 'en'
}

export const locale = ref(readInitialLocale())

function applyDocumentLang(value) {
  if (typeof document === 'undefined') return
  document.documentElement.lang = value === 'es' ? 'es' : 'en'
}

applyDocumentLang(locale.value)
watch(locale, applyDocumentLang)

export function setLocale(next) {
  if (!VALID.has(next)) return
  locale.value = next
  try {
    localStorage.setItem(LOCALE_KEY, next)
    localStorage.setItem(AI_INTEGRATION_LOCALE_KEY, next)
  } catch {
    /* private mode — in-memory only */
  }
}

/**
 * Translate `message`. English is the key and the default, returned unchanged.
 * `vars` replaces `{name}` tokens. `varI18n` marks which vars are themselves keys.
 */
export function t(message, vars, varI18n) {
  if (typeof message !== 'string') return message == null ? '' : String(message)
  const localized = locale.value === 'es' ? (es[message] ?? message) : message
  if (!vars) return localized
  return localized.replace(/\{(\w+)\}/g, (_, key) => {
    const raw = vars[key]
    if (raw == null) return ''
    return varI18n?.[key] ? t(String(raw)) : String(raw)
  })
}

export function useI18n() {
  return { locale, setLocale, t }
}

/** Same options as the existing en-US formatters; Spanish uses es-CO. */
export function formatLocaleDate(value, options) {
  const code = locale.value === 'es' ? 'es-CO' : 'en-US'
  return new Date(value).toLocaleDateString(code, options)
}
