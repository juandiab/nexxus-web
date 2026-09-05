import { ref, computed, watch } from 'vue'
import { AI_INTEGRATION_COPY, AI_INTEGRATION_LOCALE_KEY } from '@/data/aiIntegrationCopy.js'
import { applySeo } from '@/utils/seo.js'

const VALID = new Set(['en', 'es'])

function readStoredLocale() {
  try {
    const stored = localStorage.getItem(AI_INTEGRATION_LOCALE_KEY)
    return VALID.has(stored) ? stored : 'en'
  } catch {
    return 'en'
  }
}

/** Page-local locale for /ai-integration only (localStorage-backed). */
export function useAiIntegrationLocale() {
  const locale = ref(readStoredLocale())

  const copy = computed(() => AI_INTEGRATION_COPY[locale.value] ?? AI_INTEGRATION_COPY.en)

  function setLocale(next) {
    if (!VALID.has(next) || next === locale.value) return
    locale.value = next
    try {
      localStorage.setItem(AI_INTEGRATION_LOCALE_KEY, next)
    } catch {
      /* private mode — in-memory only */
    }
  }

  function applyPageSeo() {
    const seo = copy.value.seo
    applySeo({
      title: seo.title,
      description: seo.description,
      path: '/ai-integration',
    })
    document.documentElement.lang = locale.value
  }

  watch(locale, applyPageSeo, { immediate: true })

  return { locale, copy, setLocale }
}
