<template>
  <div class="chat-widget">
    <Transition name="chat-window">
      <div v-if="isOpen" class="chat-window">
        <div class="chat-header">
          <div class="chat-header-info">
            <div class="chat-avatar">
              <i class="pi pi-bolt"></i>
            </div>
            <div>
              <span class="chat-name">JPbot</span>
              <span class="chat-status">
                <span class="status-dot"></span>
                Intake Assistant · Nexxus Tech
              </span>
            </div>
          </div>
          <button class="chat-close" @click="isOpen = false" aria-label="Close chat">
            <i class="pi pi-times"></i>
          </button>
        </div>

        <div class="chat-messages" ref="messagesEl">
          <div
            v-for="(msg, i) in messages"
            :key="i"
            :class="['chat-msg', `chat-msg--${msg.role}`]"
          >
            <div class="msg-avatar" v-if="msg.role === 'assistant'">
              <i class="pi pi-bolt"></i>
            </div>
            <div class="msg-bubble">
              <p>{{ msg.content }}</p>
            </div>
          </div>
          <div v-if="loading" class="chat-msg chat-msg--assistant">
            <div class="msg-avatar"><i class="pi pi-bolt"></i></div>
            <div class="msg-bubble typing">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>

        <!-- Intake: service picker -->
        <div v-if="phase === 'intake' && intakeStep === 3" class="chat-intake-panel">
          <label for="jpbot-service">Service of interest</label>
          <select id="jpbot-service" v-model="serviceChoice">
            <option value="">Select a service...</option>
            <option v-for="s in services" :key="s" :value="s">{{ s }}</option>
          </select>
          <button
            class="btn-intake"
            @click="finishService"
            :disabled="!serviceChoice"
          >
            Continue
          </button>
        </div>

        <!-- Discovery submit -->
        <div v-else-if="phase === 'discovery' && !submitted" class="chat-submit-bar">
          <button
            class="btn-submit-enquiry"
            :disabled="!canSubmit || submitting"
            @click="submitEnquiry"
          >
            <i :class="submitting ? 'pi pi-spin pi-spinner' : 'pi pi-send'"></i>
            {{ submitting ? 'Sending...' : 'Send enquiry to Nexxus' }}
          </button>
          <p v-if="!canSubmit" class="submit-hint">
            JPbot will enable this once your needs are clear.
          </p>
          <router-link
            v-if="canSubmit"
            to="/contact"
            class="contact-link"
            @click="prefillContact"
          >
            Or review on the contact page
          </router-link>
        </div>

        <div v-if="submitted" class="chat-success">
          <i class="pi pi-check-circle"></i>
          <p>Enquiry sent! Check your inbox for a confirmation.</p>
        </div>

        <div v-if="phase !== 'submitted' && !(phase === 'intake' && intakeStep === 3)" class="chat-input-area">
          <input
            v-model="inputText"
            :type="intakeStep === 1 ? 'email' : 'text'"
            :placeholder="inputPlaceholder"
            @keydown.enter="handleEnter"
            :disabled="loading || submitting || submitted"
            ref="inputEl"
          />
          <button
            class="chat-send"
            @click="handleEnter"
            :disabled="loading || submitting || submitted || !inputText.trim()"
          >
            <i class="pi pi-send"></i>
          </button>
        </div>
        <p class="chat-disclaimer">
          JPbot collects details to route your enquiry. A consultant will follow up — not a substitute for professional advice.
        </p>
      </div>
    </Transition>

    <Transition name="bubble-pulse">
      <div class="chat-notification" v-if="!isOpen && hasNotification">
        <span>{{ notificationText }}</span>
        <button @click="hasNotification = false" class="notif-close">
          <i class="pi pi-times"></i>
        </button>
      </div>
    </Transition>

    <button class="chat-bubble" @click="toggleChat" :class="{ active: isOpen }" aria-label="Open chat">
      <Transition name="icon-flip" mode="out-in">
        <i v-if="isOpen" key="close" class="pi pi-times"></i>
        <i v-else key="open" class="pi pi-comments"></i>
      </Transition>
      <div class="bubble-ring"></div>
    </button>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted } from 'vue'
import axios from 'axios'
import { saveJpbotDraft } from '@/utils/jpbotDraft.js'

const SERVICES = [
  'WAF & API Protection',
  'NetScaler / ADC',
  'Zero-Trust Architecture',
  'Multicloud Security',
  'AI & Automation',
  'Citrix Virtual Apps & Desktops',
  'Other / Discovery Call',
]

const isOpen = ref(false)
const inputText = ref('')
const loading = ref(false)
const submitting = ref(false)
const submitted = ref(false)
const messagesEl = ref(null)
const inputEl = ref(null)
const hasNotification = ref(false)
const notificationText = ref("Hi! I'm JPbot — tell us what you need and we'll follow up 👋")

const phase = ref('intake') // intake | discovery | submitted
const intakeStep = ref(0) // 0 name, 1 email, 2 company, 3 service
const serviceChoice = ref('')
const services = SERVICES
const canSubmit = ref(false)

const profile = ref({
  name: '',
  email: '',
  company: '',
  service: '',
})

const discoveryMessages = ref([])

const messages = ref([
  {
    role: 'assistant',
    content:
      "Hi! I'm JPbot, Nexxus Tech's intake assistant. I'll ask a few quick questions, then learn about your project so our team can help. What's your full name?",
  },
])

const inputPlaceholder = computed(() => {
  if (phase.value !== 'intake') return 'Describe your project or challenge...'
  const placeholders = [
    'Your full name',
    'you@company.com',
    'Company name (or type "none")',
  ]
  return placeholders[intakeStep.value] || ''
})

const scrollToBottom = async () => {
  await nextTick()
  if (messagesEl.value) {
    messagesEl.value.scrollTop = messagesEl.value.scrollHeight
  }
}

const pushAssistant = (content) => {
  messages.value.push({ role: 'assistant', content })
}

const pushUser = (content) => {
  messages.value.push({ role: 'user', content })
}

const isValidEmail = (v) => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)

const startDiscovery = () => {
  phase.value = 'discovery'
  pushAssistant(
    `Thanks, ${profile.value.name}! You're interested in ${profile.value.service}. ` +
      'What challenge or goal should our team know about? (environment, timeline, or pain points help.)'
  )
  discoveryMessages.value = []
  canSubmit.value = false
}

const finishService = () => {
  if (!serviceChoice.value) return
  profile.value.service = serviceChoice.value
  pushUser(profile.value.service)
  startDiscovery()
  scrollToBottom()
}

const handleIntake = (text) => {
  if (intakeStep.value === 0) {
    if (text.length < 2) {
      pushAssistant('Please enter your full name so we can address you correctly.')
      return
    }
    profile.value.name = text
    pushUser(text)
    intakeStep.value = 1
    pushAssistant('What email should we use to follow up?')
    return
  }
  if (intakeStep.value === 1) {
    if (!isValidEmail(text)) {
      pushAssistant('Please enter a valid email address.')
      return
    }
    profile.value.email = text
    pushUser(text)
    intakeStep.value = 2
    pushAssistant('Which company or organization are you with? (Type "none" if personal.)')
    return
  }
  if (intakeStep.value === 2) {
    profile.value.company = text.toLowerCase() === 'none' ? '' : text
    pushUser(profile.value.company || '(not provided)')
    intakeStep.value = 3
    pushAssistant('Which service are you most interested in? Choose below.')
    return
  }
}

const handleDiscovery = async (text) => {
  pushUser(text)
  discoveryMessages.value.push({ role: 'user', content: text })
  loading.value = true
  await scrollToBottom()

  try {
    const { data } = await axios.post('/api/chat', {
      profile: profile.value,
      messages: discoveryMessages.value,
    })
    discoveryMessages.value.push({ role: 'assistant', content: data.reply })
    pushAssistant(data.reply)
    canSubmit.value = Boolean(data.ready_to_submit)
    if (canSubmit.value) saveDraft()
  } catch {
    pushAssistant(
      "Sorry, I'm having trouble connecting. You can email contact@nexxus-tech.com or use our contact form."
    )
  } finally {
    loading.value = false
    await scrollToBottom()
  }
}

const saveDraft = () => {
  const summary = discoveryMessages.value
    .filter((m) => m.role === 'user')
    .map((m) => m.content)
    .join('\n\n')
  saveJpbotDraft({
    name: profile.value.name,
    email: profile.value.email,
    company: profile.value.company,
    service: profile.value.service,
    message: summary.slice(0, 2000),
  })
}

const prefillContact = () => {
  saveDraft()
  isOpen.value = false
}

const handleEnter = async () => {
  const text = inputText.value.trim()
  if (!text || loading.value || submitting.value || submitted.value) return

  if (phase.value === 'intake') {
    if (intakeStep.value === 3) return
    inputText.value = ''
    handleIntake(text)
    await scrollToBottom()
    if (intakeStep.value === 3) await scrollToBottom()
    return
  }

  inputText.value = ''
  await handleDiscovery(text)
}

const submitEnquiry = async () => {
  if (!canSubmit.value || submitting.value) return
  submitting.value = true
  try {
    await axios.post('/api/chat/submit', {
      profile: profile.value,
      messages: discoveryMessages.value,
    })
    submitted.value = true
    phase.value = 'submitted'
  } catch (err) {
    const detail = err.response?.data?.detail
    const msg = Array.isArray(detail)
      ? detail.map((d) => d.msg || d).join(', ')
      : detail
    pushAssistant(
      msg || 'Could not send your enquiry. Please try the contact form or email contact@nexxus-tech.com.'
    )
  } finally {
    submitting.value = false
    await scrollToBottom()
  }
}

const toggleChat = () => {
  isOpen.value = !isOpen.value
  hasNotification.value = false
  if (isOpen.value) {
    nextTick(() => inputEl.value?.focus())
    scrollToBottom()
  }
}

onMounted(() => {
  setTimeout(() => {
    if (!isOpen.value) hasNotification.value = true
  }, 5000)
})
</script>

<style scoped>
.chat-widget {
  position: fixed;
  bottom: 28px;
  right: 28px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 12px;
}

.chat-bubble {
  width: 60px; height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--nt-primary), var(--nt-secondary));
  border: none;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.3rem; color: white;
  box-shadow: 0 4px 24px rgba(0,123,167,0.5);
  transition: var(--nt-transition);
  position: relative;
}
.chat-bubble:hover { transform: scale(1.08); box-shadow: 0 6px 30px rgba(0,123,167,0.6); }
.chat-bubble.active { background: linear-gradient(135deg, #005F7F, #005F7F); }
.bubble-ring {
  position: absolute; inset: -6px;
  border-radius: 50%;
  border: 2px solid rgba(0,123,167,0.3);
  animation: bubbleRing 2s ease-in-out infinite;
}
@keyframes bubbleRing {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.15); opacity: 0; }
}

.chat-notification {
  background: var(--nt-dark-3);
  border: 1px solid var(--nt-border);
  border-radius: 12px;
  padding: 10px 14px;
  max-width: 260px;
  font-size: 0.82rem;
  color: var(--nt-text-light);
  display: flex; align-items: center; gap: 8px;
  box-shadow: var(--nt-shadow);
}
.notif-close {
  background: none; border: none; cursor: pointer;
  color: var(--nt-text-muted); font-size: 0.7rem;
  padding: 2px; flex-shrink: 0;
}

.chat-window {
  width: 360px;
  max-height: 560px;
  background: var(--nt-dark-2);
  border: 1px solid var(--nt-border);
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 16px 60px rgba(0,0,0,0.5), 0 0 0 1px rgba(0,123,167,0.1);
  overflow: hidden;
}

.chat-header {
  background: linear-gradient(135deg, var(--nt-primary), var(--nt-primary-d));
  padding: 16px 20px;
  display: flex; justify-content: space-between; align-items: center;
}
.chat-header-info { display: flex; align-items: center; gap: 12px; }
.chat-avatar {
  width: 38px; height: 38px;
  background: rgba(255,255,255,0.2);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  color: white; font-size: 1rem;
}
.chat-name { display: block; font-weight: 700; color: white; font-size: 0.9rem; font-family: var(--font-heading); }
.chat-status {
  display: flex; align-items: center; gap: 5px;
  font-size: 0.72rem; color: rgba(255,255,255,0.75);
}
.status-dot {
  width: 7px; height: 7px;
  background: var(--nt-secondary);
  border-radius: 50%;
  animation: pulse 2s infinite;
}
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
.chat-close {
  background: rgba(255,255,255,0.15); border: none; border-radius: 6px;
  width: 28px; height: 28px;
  display: flex; align-items: center; justify-content: center;
  color: white; cursor: pointer; font-size: 0.8rem;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 300px;
  scroll-behavior: smooth;
}

.chat-msg { display: flex; gap: 8px; align-items: flex-end; }
.chat-msg--user { flex-direction: row-reverse; }
.msg-avatar {
  width: 28px; height: 28px; border-radius: 50%;
  background: linear-gradient(135deg, var(--nt-primary), var(--nt-secondary));
  display: flex; align-items: center; justify-content: center;
  font-size: 0.7rem; color: white; flex-shrink: 0;
}
.msg-bubble {
  max-width: 76%;
  padding: 10px 14px;
  border-radius: 16px;
  font-size: 0.875rem;
  line-height: 1.5;
}
.chat-msg--assistant .msg-bubble {
  background: var(--nt-dark-3);
  border: 1px solid var(--nt-border);
  color: var(--nt-text-light);
  border-bottom-left-radius: 4px;
}
.chat-msg--user .msg-bubble {
  background: var(--nt-primary);
  color: white;
  border-bottom-right-radius: 4px;
}
.msg-bubble p { margin: 0; }

.typing { display: flex; align-items: center; gap: 4px; padding: 12px 16px; }
.typing span {
  width: 7px; height: 7px;
  background: var(--nt-text-muted);
  border-radius: 50%;
  animation: typingBounce 1.2s infinite;
}
.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }
@keyframes typingBounce {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-6px); }
}

.chat-intake-panel {
  padding: 12px 16px;
  border-top: 1px solid var(--nt-border);
  background: var(--nt-dark-3);
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.chat-intake-panel label {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--nt-text-muted);
}
.chat-intake-panel select {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  padding: 10px 12px;
  color: var(--nt-text);
  font-size: 0.85rem;
}
.btn-intake {
  background: var(--nt-primary);
  border: none;
  border-radius: 10px;
  padding: 10px;
  color: white;
  font-weight: 600;
  cursor: pointer;
}
.btn-intake:disabled { opacity: 0.4; cursor: not-allowed; }

.chat-submit-bar {
  padding: 10px 16px;
  border-top: 1px solid var(--nt-border);
  background: var(--nt-dark-3);
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.btn-submit-enquiry {
  width: 100%;
  background: linear-gradient(135deg, var(--nt-secondary), var(--nt-primary));
  border: none;
  border-radius: 10px;
  padding: 12px;
  color: white;
  font-weight: 700;
  font-size: 0.85rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.btn-submit-enquiry:disabled { opacity: 0.45; cursor: not-allowed; }
.submit-hint { font-size: 0.68rem; color: var(--nt-text-muted); margin: 0; text-align: center; }
.contact-link {
  font-size: 0.72rem;
  color: var(--nt-secondary);
  text-align: center;
  text-decoration: none;
}
.contact-link:hover { text-decoration: underline; }

.chat-success {
  padding: 16px;
  text-align: center;
  color: #4ADE80;
  font-size: 0.85rem;
  border-top: 1px solid var(--nt-border);
}
.chat-success .pi { font-size: 1.5rem; margin-bottom: 8px; }

.chat-input-area {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  border-top: 1px solid var(--nt-border);
  background: var(--nt-dark-3);
}
.chat-input-area input {
  flex: 1;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  padding: 10px 14px;
  color: var(--nt-text);
  font-size: 0.875rem;
  outline: none;
}
.chat-send {
  width: 38px; height: 38px;
  background: var(--nt-primary);
  border: none; border-radius: 10px;
  color: white; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
}
.chat-send:disabled { opacity: 0.4; cursor: not-allowed; }

.chat-disclaimer {
  font-size: 0.65rem;
  color: var(--nt-text-muted);
  text-align: center;
  padding: 4px 16px 10px;
  background: var(--nt-dark-3);
}

.chat-window-enter-active, .chat-window-leave-active {
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
.chat-window-enter-from, .chat-window-leave-to {
  opacity: 0; transform: translateY(20px) scale(0.95);
}
.bubble-pulse-enter-active, .bubble-pulse-leave-active { transition: all 0.25s ease; }
.bubble-pulse-enter-from, .bubble-pulse-leave-to { opacity: 0; transform: translateX(10px); }
.icon-flip-enter-active, .icon-flip-leave-active { transition: all 0.2s ease; }
.icon-flip-enter-from, .icon-flip-leave-to { opacity: 0; transform: rotate(90deg) scale(0.8); }

@media (max-width: 480px) {
  .chat-widget { bottom: 16px; right: 16px; }
  .chat-window { width: calc(100vw - 32px); }
}
</style>
