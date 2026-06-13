const BASE = '/licensing'
const TOKEN_KEY = 'nexxus-admin-token'

export function getToken() {
  return sessionStorage.getItem(TOKEN_KEY) || ''
}

export function setToken(token) {
  if (token) sessionStorage.setItem(TOKEN_KEY, token)
  else sessionStorage.removeItem(TOKEN_KEY)
}

async function request(path, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  }
  const token = getToken()
  if (token) headers.Authorization = `Bearer ${token}`

  const res = await fetch(`${BASE}${path}`, { ...options, headers })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    const detail = err.detail
    const message = Array.isArray(detail)
      ? detail.map((d) => d.msg).join(', ')
      : detail || 'Request failed'
    throw new Error(message)
  }
  if (res.status === 204) return null
  return res.json()
}

export async function login(username, password) {
  return request('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })
}

export async function fetchMe() {
  return request('/auth/me')
}

export async function changePassword(currentPassword, newPassword) {
  return request('/auth/change-password', {
    method: 'POST',
    body: JSON.stringify({ currentPassword, newPassword }),
  })
}

export async function fetchPasskeyStatus(username) {
  return request('/auth/webauthn/status', {
    method: 'POST',
    body: JSON.stringify({ username: username.trim().toLowerCase() }),
  })
}

export async function webauthnRegisterBegin(username) {
  return request('/auth/webauthn/register/begin', {
    method: 'POST',
    body: JSON.stringify({ username: username.trim().toLowerCase() }),
  })
}

export async function webauthnRegisterFinish(username, credential, label = '') {
  return request('/auth/webauthn/register/finish', {
    method: 'POST',
    body: JSON.stringify({
      username: username.trim().toLowerCase(),
      credential,
      label,
    }),
  })
}

export async function webauthnLoginBegin(username, preferCrossDevice = false) {
  return request('/auth/webauthn/login/begin', {
    method: 'POST',
    body: JSON.stringify({
      username: username.trim().toLowerCase(),
      preferCrossDevice,
    }),
  })
}

export async function webauthnLoginFinish(username, credential) {
  return request('/auth/webauthn/login/finish', {
    method: 'POST',
    body: JSON.stringify({
      username: username.trim().toLowerCase(),
      credential,
    }),
  })
}

export async function listUsers() {
  return request('/users')
}

export async function createUser(payload) {
  return request('/users', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function deleteUser(userId) {
  return request(`/users/${userId}`, { method: 'DELETE' })
}

export async function getUser(userId) {
  return request(`/users/${userId}`)
}

export async function updateUser(userId, payload) {
  return request(`/users/${userId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export async function setUserActive(userId, active) {
  return request(`/users/${userId}/active`, {
    method: 'PATCH',
    body: JSON.stringify({ active }),
  })
}

export async function resetUserPassword(userId) {
  return request(`/users/${userId}/reset-password`, { method: 'POST' })
}

export async function deletePasskey(userId, passkeyId) {
  return request(`/users/${userId}/passkeys/${passkeyId}`, { method: 'DELETE' })
}

export async function listLicenses() {
  return request('/licenses')
}

export async function createLicense(payload) {
  return request('/licenses', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function deleteLicense(licenseId) {
  return request(`/licenses/${licenseId}`, { method: 'DELETE' })
}

export async function expireLicense(licenseId) {
  return request(`/licenses/${licenseId}/expire`, { method: 'POST' })
}

export async function deactivateLicense(licenseId) {
  return request(`/licenses/${licenseId}/deactivate`, { method: 'POST' })
}

export async function reactivateLicense(licenseId) {
  return request(`/licenses/${licenseId}/reactivate`, { method: 'POST' })
}

export async function extendLicense(licenseId, days) {
  return request(`/licenses/${licenseId}/extend`, {
    method: 'POST',
    body: JSON.stringify({ days }),
  })
}

export async function changeLicenseType(licenseId, licenseType, recalculateValidity = true) {
  return request(`/licenses/${licenseId}/change-type`, {
    method: 'POST',
    body: JSON.stringify({ licenseType, recalculateValidity }),
  })
}

export async function getLicenseCode(licenseId) {
  return request(`/licenses/${licenseId}/code`)
}

const BLOG_BASE = '/api/admin/blog'

async function blogRequest(path, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  }
  const token = getToken()
  if (token) headers.Authorization = `Bearer ${token}`

  const res = await fetch(`${BLOG_BASE}${path}`, { ...options, headers })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    const detail = err.detail
    const message = Array.isArray(detail)
      ? detail.map((d) => d.msg).join(', ')
      : detail || 'Request failed'
    throw new Error(message)
  }
  if (res.status === 204) return null
  return res.json()
}

export async function listBlogPosts() {
  return blogRequest('')
}

export async function getBlogPost(postId) {
  return blogRequest(`/${postId}`)
}

export async function createBlogPost(payload) {
  return blogRequest('', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function updateBlogPost(postId, payload) {
  return blogRequest(`/${postId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export async function deleteBlogPost(postId) {
  return blogRequest(`/${postId}`, { method: 'DELETE' })
}

export async function assistBlogPost(draft) {
  return blogRequest('/assist', {
    method: 'POST',
    body: JSON.stringify({ draft }),
  })
}

export async function getBlogAssistantSettings() {
  return blogRequest('/assistant/settings')
}

export async function getBlogAssistantModels(provider, currentModel = '') {
  const params = new URLSearchParams()
  if (currentModel) params.set('current', currentModel)
  const query = params.toString()
  return blogRequest(`/assistant/models/${encodeURIComponent(provider)}${query ? `?${query}` : ''}`)
}

export async function saveBlogAssistantSettings(payload) {
  return blogRequest('/assistant/settings', {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

const ADMIN_API_BASE = '/api/admin'

async function adminApiRequest(path, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  }
  const token = getToken()
  if (token) headers.Authorization = `Bearer ${token}`

  const res = await fetch(`${ADMIN_API_BASE}${path}`, { ...options, headers })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    const detail = err.detail
    const message = Array.isArray(detail)
      ? detail.map((d) => d.msg).join(', ')
      : detail || 'Request failed'
    throw new Error(message)
  }
  if (res.status === 204) return null
  return res.json()
}

export async function getJpbotSettings() {
  return adminApiRequest('/chat/settings')
}

export async function getJpbotModels(provider, currentModel = '') {
  const params = new URLSearchParams()
  if (currentModel) params.set('current', currentModel)
  const query = params.toString()
  return adminApiRequest(`/chat/models/${encodeURIComponent(provider)}${query ? `?${query}` : ''}`)
}

export async function saveJpbotSettings(payload) {
  return adminApiRequest('/chat/settings', {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export async function testJpbotSettings(payload) {
  return adminApiRequest('/chat/settings/test', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}
