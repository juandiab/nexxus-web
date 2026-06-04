<template>
  <div class="setup-page">
    <div class="setup-card">
      <h1>Complete your account setup</h1>
      <p class="subtitle">
        Set a new password and register a passkey. After this, only your passkey can sign you in.
      </p>

      <section v-if="user?.mustChangePassword" class="step">
        <h2>1. Set a new password</h2>
        <form class="form" @submit.prevent="onChangePassword">
          <div class="field">
            <label for="current">Current password</label>
            <input id="current" v-model="currentPassword" type="password" required />
          </div>
          <div class="field">
            <label for="newpass">New password</label>
            <input id="newpass" v-model="newPassword" type="password" minlength="8" required />
          </div>
          <p v-if="passwordError" class="error-msg">{{ passwordError }}</p>
          <p v-if="passwordSuccess" class="success-msg">{{ passwordSuccess }}</p>
          <button type="submit" class="btn-primary" :disabled="passwordLoading">
            {{ passwordLoading ? 'Updating…' : 'Update password' }}
          </button>
        </form>
      </section>

      <section class="step">
        <h2>{{ user?.mustChangePassword ? '2.' : '1.' }} Register a passkey</h2>
        <p class="hint">
          Use Touch ID, Face ID, Windows Hello, or a security key on this device.
        </p>
        <p v-if="passkeyError" class="error-msg">{{ passkeyError }}</p>
        <p v-if="passkeySuccess" class="success-msg">{{ passkeySuccess }}</p>
        <button
          type="button"
          class="btn-primary"
          :disabled="passkeyLoading || user?.mustChangePassword"
          @click="onRegisterPasskey"
        >
          {{ passkeyLoading ? 'Waiting for passkey…' : 'Register passkey' }}
        </button>
        <p v-if="user?.mustChangePassword" class="hint">Change your password first.</p>
      </section>

      <button v-if="user?.setupComplete" type="button" class="btn-outline" @click="goDashboard">
        Continue to dashboard
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { changePassword } from '@/api/client'
import { useAdminAuth } from '@/composables/useAdminAuth'
import { registerPasskey, passkeyErrorMessage } from '@/services/webauthn'

const router = useRouter()
const { user, refreshUser } = useAdminAuth()

const currentPassword = ref('')
const newPassword = ref('')
const passwordLoading = ref(false)
const passwordError = ref('')
const passwordSuccess = ref('')

const passkeyLoading = ref(false)
const passkeyError = ref('')
const passkeySuccess = ref('')

async function onChangePassword() {
  passwordLoading.value = true
  passwordError.value = ''
  passwordSuccess.value = ''
  try {
    await changePassword(currentPassword.value, newPassword.value)
    passwordSuccess.value = 'Password updated.'
    currentPassword.value = ''
    newPassword.value = ''
    await refreshUser()
  } catch (e) {
    passwordError.value = e.message || 'Could not update password'
  } finally {
    passwordLoading.value = false
  }
}

async function onRegisterPasskey() {
  passkeyLoading.value = true
  passkeyError.value = ''
  passkeySuccess.value = ''
  try {
    await registerPasskey(user.value.username)
    passkeySuccess.value = 'Passkey registered. You can now sign in with it.'
    await refreshUser()
  } catch (e) {
    passkeyError.value = passkeyErrorMessage(e)
  } finally {
    passkeyLoading.value = false
  }
}

function goDashboard() {
  router.push({ name: 'dashboard' })
}
</script>

<style scoped>
.setup-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: #0f0f10;
}

.setup-card {
  width: 100%;
  max-width: 520px;
  padding: 2.5rem;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: #fff;
}

.setup-card h1 {
  font-size: 1.5rem;
  margin: 0 0 0.5rem;
}

.subtitle,
.hint {
  color: rgba(255, 255, 255, 0.65);
  margin: 0 0 1.5rem;
  font-size: 0.95rem;
  line-height: 1.5;
}

.step {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.step h2 {
  font-size: 1.1rem;
  margin: 0 0 1rem;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
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

.error-msg {
  color: #ff6b6b;
  font-size: 0.9rem;
}

.success-msg {
  color: #6bcf8a;
  font-size: 0.9rem;
}

.btn-primary,
.btn-outline {
  width: 100%;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 0.5rem;
}

.btn-primary {
  border: none;
  background: #007ba7;
  color: #fff;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-outline {
  border: 1px solid rgba(255, 255, 255, 0.25);
  background: transparent;
  color: #fff;
}
</style>
