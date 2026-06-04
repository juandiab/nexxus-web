import { ref, computed } from 'vue'
import { fetchMe, getToken, login as apiLogin, setToken } from '@/api/client'

const user = ref(null)
const loading = ref(false)
const error = ref('')

export function useAdminAuth() {
  const isAuthenticated = computed(() => Boolean(getToken() && user.value))
  const username = computed(() => user.value?.username || '')
  const isAdmin = computed(() => user.value?.role === 'admin')
  const canAccessLicensing = computed(
    () => user.value?.role === 'admin' || user.value?.role === 'licensing'
  )
  const canAccessBlog = computed(
    () => user.value?.role === 'admin' || user.value?.role === 'blog'
  )
  const canAccessSettings = computed(() => user.value?.role === 'admin')
  const setupComplete = computed(() => user.value?.setupComplete ?? false)

  function applySession(data) {
    setToken(data.accessToken)
    user.value = data.user
  }

  function clearSession() {
    setToken('')
    user.value = null
    error.value = ''
  }

  async function login(userName, password) {
    loading.value = true
    error.value = ''
    try {
      const data = await apiLogin(userName, password)
      applySession(data)
      return true
    } catch (e) {
      error.value = e.message || 'Login failed'
      clearSession()
      return false
    } finally {
      loading.value = false
    }
  }

  async function loginWithTokenResponse(data) {
    applySession(data)
  }

  async function refreshUser() {
    if (!getToken()) return false
    try {
      user.value = await fetchMe()
      return true
    } catch {
      clearSession()
      return false
    }
  }

  async function validateSession() {
    if (!getToken()) return false
    return refreshUser()
  }

  function logout() {
    clearSession()
  }

  return {
    user,
    username,
    loading,
    error,
    isAuthenticated,
    isAdmin,
    canAccessLicensing,
    canAccessBlog,
    canAccessSettings,
    setupComplete,
    login,
    loginWithTokenResponse,
    refreshUser,
    logout,
    validateSession,
  }
}
