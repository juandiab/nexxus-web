const STORAGE_KEY = 'nexxus-jpbot-draft'
const MAX_AGE_MS = 60 * 60 * 1000

export function saveJpbotDraft(draft) {
  try {
    sessionStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({ ...draft, savedAt: Date.now() })
    )
  } catch {
    /* ignore quota / private mode */
  }
}

export function loadJpbotDraft() {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    if (!raw) return null
    const data = JSON.parse(raw)
    if (!data?.savedAt || Date.now() - data.savedAt > MAX_AGE_MS) {
      sessionStorage.removeItem(STORAGE_KEY)
      return null
    }
    const { savedAt, ...draft } = data
    return draft
  } catch {
    return null
  }
}

export function clearJpbotDraft() {
  try {
    sessionStorage.removeItem(STORAGE_KEY)
  } catch {
    /* ignore */
  }
}
