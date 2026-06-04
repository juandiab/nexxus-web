<template>
  <div class="login-page">
    <div class="login-card">
      <h1>Admin Console</h1>
      <p class="subtitle">Sign in with your administrator credentials</p>

      <div class="field">
        <label for="username">Username</label>
        <input
          id="username"
          v-model="formUser"
          type="text"
          autocomplete="username"
          required
          @input="onUsernameInput"
        />
      </div>

      <template v-if="statusChecked && passkeyRequired">
        <p class="hint">This account uses passkey sign-in.</p>
        <p v-if="error" class="error-msg">{{ error }}</p>
        <button type="button" class="btn-primary" :disabled="loading" @click="onPasskeyLogin">
          {{ loading ? 'Waiting for passkey…' : 'Sign in with passkey' }}
        </button>
      </template>

      <form v-else-if="statusChecked" class="login-form" @submit.prevent="onPasswordLogin">
        <div class="field">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="formPass"
            type="password"
            autocomplete="current-password"
            required
          />
        </div>
        <p v-if="error" class="error-msg">{{ error }}</p>
        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? 'Signing in…' : 'Sign in' }}
        </button>
      </form>

      <p v-else-if="checking" class="hint">Checking account…</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAdminAuth } from '@/composables/useAdminAuth'
import { getPasskeyStatus, loginWithPasskey, passkeyErrorMessage } from '@/services/webauthn'

const route = useRoute()
const router = useRouter()
const { loading, error, login, loginWithTokenResponse, user } = useAdminAuth()

const formUser = ref('')
const formPass = ref('')
const passkeyRequired = ref(false)
const statusChecked = ref(false)
const checking = ref(false)

let statusTimer = null

function redirectAfterLogin(user) {
  const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : null
  if (!user.setupComplete) {
    router.push({ name: 'setup' })
    return
  }
  router.push(redirect || { name: 'dashboard' })
}

async function checkStatus() {
  const username = formUser.value.trim()
  if (username.length < 2) {
    statusChecked.value = false
    passkeyRequired.value = false
    return
  }
  checking.value = true
  try {
    const status = await getPasskeyStatus(username)
    passkeyRequired.value = status.passkeyRequired
    statusChecked.value = true
  } catch {
    passkeyRequired.value = false
    statusChecked.value = true
  } finally {
    checking.value = false
  }
}

function onUsernameInput() {
  statusChecked.value = false
  clearTimeout(statusTimer)
  statusTimer = setTimeout(checkStatus, 350)
}

watch(formUser, () => {
  if (!formUser.value.trim()) {
    statusChecked.value = false
    passkeyRequired.value = false
  }
})

async function onPasswordLogin() {
  const ok = await login(formUser.value, formPass.value)
  if (ok) {
    formPass.value = ''
    redirectAfterLogin(user.value)
  }
}

async function onPasskeyLogin() {
  loading.value = true
  error.value = ''
  try {
    const data = await loginWithPasskey(formUser.value)
    await loginWithTokenResponse(data)
    redirectAfterLogin(data.user)
  } catch (e) {
    error.value = passkeyErrorMessage(e)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: #0f0f10;
}

.login-card {
  width: 100%;
  max-width: 420px;
  padding: 2.5rem;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.login-card h1 {
  font-size: 1.75rem;
  margin: 0 0 0.5rem;
  color: #fff;
}

.subtitle,
.hint {
  color: rgba(255, 255, 255, 0.65);
  margin: 0 0 1.5rem;
  font-size: 0.95rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.field {
  margin-bottom: 1.25rem;
}

.field label {
  display: block;
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 0.4rem;
}

.field input {
  width: 100%;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  background: rgba(0, 0, 0, 0.25);
  color: #fff;
  font-size: 1rem;
}

.field input:focus {
  outline: none;
  border-color: #007ba7;
}

.error-msg {
  color: #ff6b6b;
  font-size: 0.9rem;
  margin: 0 0 1rem;
}

.btn-primary {
  width: 100%;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 8px;
  background: #007ba7;
  color: #fff;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
