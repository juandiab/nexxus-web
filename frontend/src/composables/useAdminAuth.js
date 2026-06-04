import { ref, computed } from 'vue'
import { login as apiLogin, fetchMe } from '@/api/licensing'

const TOKEN_KEY = 'nexxus-admin-token'

const token = ref(sessionStorage.getItem(TOKEN_KEY) || '')
const username = ref('')
const loading = ref(false)
const error = ref('')

export function useAdminAuth() {
  const isAuthenticated = computed(() => Boolean(token.value))

  function setToken(value) {
    token.value = value
    if (value) {
      sessionStorage.setItem(TOKEN_KEY, value)
    } else {
      sessionStorage.removeItem(TOKEN_KEY)
    }
  }

  async function login(user, password) {
    loading.value = true
    error.value = ''
    try {
      const data = await apiLogin(user, password)
      setToken(data.access_token)
      const me = await fetchMe(data.access_token)
      username.value = me.username
      return true
    } catch (e) {
      error.value = e.message || 'Login failed'
      setToken('')
      username.value = ''
      return false
    } finally {
      loading.value = false
    }
  }

  async function validateSession() {
    if (!token.value) return false
    try {
      const me = await fetchMe(token.value)
      username.value = me.username
      return true
    } catch {
      logout()
      return false
    }
  }

  function logout() {
    setToken('')
    username.value = ''
    error.value = ''
  }

  return {
    token,
    username,
    loading,
    error,
    isAuthenticated,
    login,
    logout,
    validateSession,
  }
}
