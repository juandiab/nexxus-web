import { computed, watch } from 'vue'
import { AI_INTEGRATION_COPY } from '@/data/aiIntegrationCopy.js'
import { applySeo } from '@/utils/seo.js'
import { locale, setLocale as setGlobalLocale } from '@/i18n'

/** /ai-integration locale. Follows the site-wide locale (set from the navbar switch). */
export function useAiIntegrationLocale() {
  const copy = computed(() => AI_INTEGRATION_COPY[locale.value] ?? AI_INTEGRATION_COPY.en)

  function setLocale(next) {
    setGlobalLocale(next)
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
