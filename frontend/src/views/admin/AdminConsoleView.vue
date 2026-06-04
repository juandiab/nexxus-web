<template>
  <div class="admin-console">
    <div class="admin-card">
      <template v-if="!isAuthenticated">
        <h1>Admin Console</h1>
        <p class="subtitle">Sign in to manage licenses</p>

        <form class="login-form" @submit.prevent="onSubmit">
          <div class="field">
            <label for="username">Username</label>
            <input
              id="username"
              v-model="formUser"
              type="text"
              autocomplete="username"
              required
            />
          </div>
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
          <button type="submit" class="btn btn-primary w-full" :disabled="loading">
            {{ loading ? 'Signing in…' : 'Sign in' }}
          </button>
        </form>
      </template>

      <template v-else>
        <h1>Admin Console</h1>
        <p class="welcome">Signed in as <strong>{{ username }}</strong></p>
        <div class="placeholder-panel">
          <i class="pi pi-key"></i>
          <p>License management coming soon.</p>
        </div>
        <button type="button" class="btn btn-outline w-full" @click="logout">
          Sign out
        </button>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAdminAuth } from '@/composables/useAdminAuth'

const {
  username,
  loading,
  error,
  isAuthenticated,
  login,
  logout,
  validateSession,
} = useAdminAuth()

const formUser = ref('')
const formPass = ref('')

onMounted(() => {
  validateSession()
})

async function onSubmit() {
  await login(formUser.value, formPass.value)
  if (isAuthenticated.value) {
    formPass.value = ''
  }
}
</script>

<style scoped>
.admin-console {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 120px 24px 48px;
  background: var(--color-bg, #1c1c1e);
}

.admin-card {
  width: 100%;
  max-width: 420px;
  padding: 2.5rem;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.admin-card h1 {
  font-size: 1.75rem;
  margin: 0 0 0.5rem;
  color: #fff;
}

.subtitle,
.welcome {
  color: rgba(255, 255, 255, 0.65);
  margin: 0 0 1.5rem;
  font-size: 0.95rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
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
  border-color: var(--color-primary, #0a84ff);
}

.error-msg {
  color: #ff6b6b;
  font-size: 0.9rem;
  margin: 0;
}

.placeholder-panel {
  text-align: center;
  padding: 2rem 1rem;
  margin-bottom: 1.5rem;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.03);
  color: rgba(255, 255, 255, 0.6);
}

.placeholder-panel i {
  font-size: 2rem;
  margin-bottom: 0.75rem;
  display: block;
  color: var(--color-primary, #0a84ff);
}

.w-full {
  width: 100%;
}
</style>
