const STORAGE_KEY = 'jpilotRegistered'
const COOKIE_NAME = 'jpilot_registered'
const COOKIE_MAX_AGE = 60 * 60 * 24 * 365

function readCookie(name) {
  return document.cookie.split(';').some((part) => part.trim().startsWith(`${name}=`))
}

export function isJpilotRegistered() {
  try {
    if (localStorage.getItem(STORAGE_KEY)) return true
  } catch {
    /* private mode */
  }
  return readCookie(COOKIE_NAME)
}

export function markJpilotRegistered(email = '') {
  const payload = JSON.stringify({ email: email.trim().toLowerCase(), at: Date.now() })
  try {
    localStorage.setItem(STORAGE_KEY, payload)
  } catch {
    /* private mode */
  }
  document.cookie = `${COOKIE_NAME}=1; Max-Age=${COOKIE_MAX_AGE}; Path=/; SameSite=Lax`
}
