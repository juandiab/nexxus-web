<template>
  <div class="chat-widget" :class="{ 'is-expanded': isOpen && chatSize === 'expanded' }">
    <div
      v-if="isOpen && chatSize === 'expanded'"
      class="chat-backdrop"
      aria-hidden="true"
      @click="closeChat"
    ></div>

    <Transition name="chat-window">
      <div v-if="isOpen" class="chat-window" :class="`chat-window--${chatSize}`">
        <div class="chat-header">
          <div class="chat-header-info">
            <div class="chat-avatar"><i class="pi pi-bolt"></i></div>
            <div>
              <span class="chat-name">JPbot</span>
              <span class="chat-status">
                <span class="status-dot"></span>
                Contact us · Nexxus Tech
              </span>
            </div>
          </div>
          <div class="chat-header-actions">
            <button
              type="button"
              class="chat-resize"
              @click="toggleChatSize"
              :aria-label="chatSize === 'expanded' ? 'Use smaller chat window' : 'Use full screen chat'"
              :title="chatSize === 'expanded' ? 'Smaller window' : 'Full screen'"
            >
              <i :class="chatSize === 'expanded' ? 'pi pi-window-minimize' : 'pi pi-window-maximize'"></i>
            </button>
            <button class="chat-close" @click="closeChat" aria-label="Close chat">
              <i class="pi pi-times"></i>
            </button>
          </div>
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
            <div class="msg-bubble"><p>{{ msg.content }}</p></div>
          </div>
          <div v-if="loading" class="chat-msg chat-msg--assistant">
            <div class="msg-avatar"><i class="pi pi-bolt"></i></div>
            <div class="msg-bubble typing"><span></span><span></span><span></span></div>
          </div>
        </div>

        <!-- Intake panels -->
        <div v-if="phase === 'intake' && intakePanel" class="chat-intake-panel">
          <template v-if="intakePanel === 'enquiry_type'">
            <label>What do you need help with?</label>
            <div class="enquiry-options">
              <button
                v-for="opt in enquiryTypes"
                :key="opt.value"
                type="button"
                class="enquiry-option"
                :class="{ selected: panelValues.enquiry_type === opt.value }"
                @click="panelValues.enquiry_type = opt.value"
              >
                <i :class="['pi', opt.icon]"></i>
                <span class="enquiry-option-label">{{ opt.label }}</span>
                <span class="enquiry-option-desc">{{ opt.desc }}</span>
              </button>
            </div>
            <button
              class="btn-intake"
              @click="confirmEnquiryType"
              :disabled="!panelValues.enquiry_type"
            >
              Continue
            </button>
          </template>

          <template v-else-if="intakePanel === 'service'">
            <label for="jpbot-service">Service of interest</label>
            <select id="jpbot-service" v-model="panelValues.service">
              <option value="">Select...</option>
              <option v-for="s in services" :key="s" :value="s">{{ s }}</option>
            </select>
            <button class="btn-intake" @click="confirmService" :disabled="!panelValues.service">Continue</button>
          </template>

          <template v-else-if="intakePanel === 'criticality'">
            <label for="jpbot-crit">How critical is this?</label>
            <select id="jpbot-crit" v-model="panelValues.criticality">
              <option value="">Select...</option>
              <option v-for="c in criticalityOptions" :key="c" :value="c">{{ c }}</option>
            </select>
            <button class="btn-intake" @click="confirmCriticality" :disabled="!panelValues.criticality">Continue</button>
          </template>

          <template v-else-if="intakePanel === 'users'">
            <label for="jpbot-users">Users affected</label>
            <input
              id="jpbot-users"
              v-model="panelValues.users_affected"
              type="text"
              placeholder="e.g. All staff (~200), admins only..."
            />
            <button class="btn-intake" @click="confirmUsers" :disabled="!panelValues.users_affected.trim()">Continue</button>
          </template>

          <template v-else-if="intakePanel === 'technologies'">
            <label>Technologies involved</label>
            <div class="tech-checkboxes">
              <label v-for="t in technologyOptions" :key="t" class="tech-check">
                <input type="checkbox" :value="t" v-model="panelValues.technologies" />
                <span>{{ t }}</span>
              </label>
            </div>
            <input
              v-if="panelValues.technologies.includes('Other')"
              v-model="panelValues.technology_other"
              type="text"
              placeholder="Describe other technology..."
              class="tech-other"
            />
            <button
              class="btn-intake"
              @click="confirmTechnologies"
              :disabled="!panelValues.technologies.length"
            >
              Continue
            </button>
          </template>

          <template v-else-if="intakePanel === 'version'">
            <label for="jpbot-ver">Platform version <span class="optional">(optional)</span></label>
            <input id="jpbot-ver" v-model="panelValues.platform_version" type="text" placeholder="e.g. 14.1, 13.1-48.47..." />
            <div class="panel-actions">
              <button type="button" class="btn-skip" @click="skipVersion">Skip</button>
              <button class="btn-intake" @click="confirmVersion">Continue</button>
            </div>
          </template>

          <template v-else-if="intakePanel === 'model'">
            <label for="jpbot-model">Platform model <span class="optional">(optional)</span></label>
            <input id="jpbot-model" v-model="panelValues.platform_model" type="text" placeholder="e.g. VPX, MPX, SDX..." />
            <div class="panel-actions">
              <button type="button" class="btn-skip" @click="skipModel">Skip</button>
              <button class="btn-intake" @click="confirmModel">Continue</button>
            </div>
          </template>
        </div>

        <div v-else-if="phase === 'discovery' && !submitted" class="chat-submit-bar">
          <button class="btn-submit-enquiry" :disabled="!canSubmit || submitting" @click="submitEnquiry">
            <i :class="submitting ? 'pi pi-spin pi-spinner' : 'pi pi-send'"></i>
            {{ submitting ? 'Sending...' : 'Send enquiry to Nexxus' }}
          </button>
          <p v-if="!canSubmit" class="submit-hint">JPbot will enable this once your needs are clear.</p>
          <router-link v-if="canSubmit" to="/contact" class="contact-link" @click="prefillContact">
            Or review on the contact page
          </router-link>
        </div>

        <div v-if="submitted" class="chat-success">
          <i class="pi pi-check-circle"></i>
          <p>Enquiry sent! Check your inbox for a summary.</p>
        </div>

        <div
          v-if="phase !== 'submitted' && phase === 'intake' && !intakePanel && intakeTextStep <= 2"
          class="chat-input-area"
        >
          <input
            v-model="inputText"
            :type="intakeTextStep === 1 ? 'email' : 'text'"
            :placeholder="textPlaceholder"
            @keydown.enter="handleEnter"
            :disabled="loading || submitting"
            ref="inputEl"
          />
          <button class="chat-send" @click="handleEnter" :disabled="loading || !inputText.trim()">
            <i class="pi pi-send"></i>
          </button>
        </div>

        <div v-else-if="phase === 'discovery' && !submitted" class="chat-input-area">
          <input
            v-model="inputText"
            type="text"
            placeholder="Describe your issue..."
            @keydown.enter="handleEnter"
            :disabled="loading || submitting"
            ref="inputEl"
          />
          <button class="chat-send" @click="handleEnter" :disabled="loading || submitting || !inputText.trim()">
            <i class="pi pi-send"></i>
          </button>
        </div>

        <p class="chat-disclaimer">
          Chat with JPbot to reach our team — WAF, NetScaler, Zero-Trust &amp; cloud security.
        </p>
      </div>
    </Transition>

    <!-- Prominent contact invitation -->
    <Transition name="invite-pop">
      <div
        v-if="showInvite && !isOpen"
        class="chat-invite-card"
        role="dialog"
        aria-label="Contact us via chat"
      >
        <button class="invite-close" @click="dismissInvite" aria-label="Dismiss">
          <i class="pi pi-times"></i>
        </button>
        <div class="invite-icon"><i class="pi pi-comments"></i></div>
        <p class="invite-eyebrow">Contact us</p>
        <h3 class="invite-title">Chat with JPbot</h3>
        <p class="invite-body">
          Tell us about your project or issue — we'll collect the details and a Nexxus specialist will follow up.
        </p>
        <button class="invite-cta" @click="openFromInvite">
          <i class="pi pi-arrow-right"></i>
          Start chat
        </button>
      </div>
    </Transition>

    <button
      class="chat-bubble"
      @click="toggleChat"
      :class="{ active: isOpen, 'has-invite': showInvite && !isOpen }"
      aria-label="Open chat to contact Nexxus Tech"
    >
      <span v-if="showInvite && !isOpen" class="bubble-badge" aria-hidden="true">1</span>
      <span v-if="!isOpen" class="bubble-hint">Chat</span>
      <Transition name="icon-flip" mode="out-in">
        <i v-if="isOpen" key="close" class="pi pi-times"></i>
        <i v-else key="open" class="pi pi-comments"></i>
      </Transition>
      <div class="bubble-ring"></div>
    </button>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, onUnmounted, watch } from 'vue'
import axios from 'axios'
import { saveJpbotDraft } from '@/utils/jpbotDraft.js'

const INVITE_DISMISS_KEY = 'nexxus-jpbot-invite-dismissed'
const CHAT_SIZE_KEY = 'nexxus-jpbot-chat-size'
const INVITE_REMIND_MS = 90_000

const SERVICES = [
  'WAF & API Protection',
  'NetScaler / ADC',
  'Zero-Trust Architecture',
  'Multicloud Security',
  'AI & Automation',
  'Citrix Virtual Apps & Desktops',
  'Other / Discovery Call',
]

const CRITICALITY = [
  'Planning — not happening yet',
  'Low — minor impact',
  'Medium — degraded service',
  'High — major impact',
  'Critical — production down',
]

const TECHNOLOGIES = [
  'NetScaler ADC',
  'NetScaler Gateway',
  'F5 BIG-IP',
  'Citrix Virtual Apps & Desktops',
  'Citrix Cloud',
  'Okta / Identity',
  'Active Directory',
  'AWS',
  'Google Cloud',
  'Azure',
  'AI Deployments',
  'Other',
]

const ENQUIRY_TYPES = [
  {
    value: 'Troubleshooting / incident',
    label: 'Troubleshooting',
    desc: 'Something is broken or urgent',
    icon: 'pi-exclamation-triangle',
  },
  {
    value: 'Support request',
    label: 'Support',
    desc: 'Help with an existing setup',
    icon: 'pi-wrench',
  },
  {
    value: 'New project / implementation',
    label: 'New project',
    desc: 'Rollout or new implementation',
    icon: 'pi-plus-circle',
  },
  {
    value: 'Assessment / discovery',
    label: 'Assessment',
    desc: 'Explore options or get guidance',
    icon: 'pi-search',
  },
  {
    value: 'General enquiry',
    label: 'General',
    desc: 'Other questions for our team',
    icon: 'pi-question-circle',
  },
]

const INTAKE_PANELS_BY_TYPE = {
  'Troubleshooting / incident': ['criticality', 'users', 'technologies', 'version', 'model'],
  'Support request': ['criticality', 'users', 'technologies', 'version', 'model'],
  'New project / implementation': ['technologies', 'version', 'model'],
  'Assessment / discovery': ['technologies'],
  'General enquiry': ['technologies', 'version', 'model'],
}

const isOpen = ref(false)
const chatSize = ref('expanded') // expanded | compact
const showInvite = ref(false)
const inputText = ref('')
const loading = ref(false)
const submitting = ref(false)
const submitted = ref(false)
const messagesEl = ref(null)
const inputEl = ref(null)
const services = SERVICES
const criticalityOptions = CRITICALITY
const technologyOptions = TECHNOLOGIES
const enquiryTypes = ENQUIRY_TYPES

const phase = ref('intake')
const intakeTextStep = ref(0)
const intakePanel = ref('enquiry_type')
const intakeQueue = ref([])
const canSubmit = ref(false)
let inviteTimer = null
let remindTimer = null

const panelValues = ref({
  enquiry_type: '',
  service: '',
  criticality: '',
  users_affected: '',
  technologies: [],
  technology_other: '',
  platform_version: '',
  platform_model: '',
})

const profile = ref({
  enquiry_type: '',
  name: '',
  email: '',
  company: '',
  service: '',
  criticality: '',
  users_affected: '',
  technologies: [],
  technology_other: '',
  platform_version: '',
  platform_model: '',
})

const discoveryMessages = ref([])

const messages = ref([
  {
    role: 'assistant',
    content:
      "Hi! I'm JPbot — the fastest way to contact Nexxus Tech. First, tell us what kind of help you need using the options below.",
  },
])

const textPlaceholder = computed(() => {
  const p = ['Your full name', 'you@company.com', 'Company (or type "none")']
  return p[intakeTextStep.value] || ''
})

const scrollToBottom = async () => {
  await nextTick()
  if (messagesEl.value) messagesEl.value.scrollTop = messagesEl.value.scrollHeight
}

const pushAssistant = (content) => messages.value.push({ role: 'assistant', content })
const pushUser = (content) => messages.value.push({ role: 'user', content })
const isValidEmail = (v) => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)

const showInvitePopup = () => {
  if (!isOpen.value) showInvite.value = true
}

const dismissInvite = () => {
  showInvite.value = false
  try {
    sessionStorage.setItem(INVITE_DISMISS_KEY, String(Date.now()))
  } catch { /* ignore */ }
  remindTimer = setTimeout(showInvitePopup, INVITE_REMIND_MS)
}

const openFromInvite = () => {
  showInvite.value = false
  isOpen.value = true
  nextTick(() => {
    if (!intakePanel.value) inputEl.value?.focus()
    scrollToBottom()
  })
}

const closeChat = () => {
  isOpen.value = false
  if (!submitted.value) {
    setTimeout(showInvitePopup, 800)
  }
}

const toggleChat = () => {
  if (isOpen.value) closeChat()
  else openFromInvite()
}

const toggleChatSize = () => {
  chatSize.value = chatSize.value === 'expanded' ? 'compact' : 'expanded'
  try {
    sessionStorage.setItem(CHAT_SIZE_KEY, chatSize.value)
  } catch { /* ignore */ }
  scrollToBottom()
}

const discoveryPromptForType = (type) => {
  const prompts = {
    'Troubleshooting / incident':
      'Describe what is happening — symptoms, error messages, and when it started.',
    'Support request':
      'What do you need help with in your environment? Include any recent changes if relevant.',
    'New project / implementation':
      'Tell us about the project — goals, scope, timeline, and what success looks like.',
    'Assessment / discovery':
      'What would you like us to assess or advise on? Any constraints or deadlines?',
    'General enquiry': 'How can our team help you today?',
  }
  return prompts[type] || 'Please share a few more details so we can route you to the right specialist.'
}

const applyIntakeDefaults = () => {
  if (!profile.value.criticality) {
    profile.value.criticality = 'Planning — not happening yet'
  }
  if (!profile.value.users_affected) {
    const preEngagement =
      profile.value.enquiry_type === 'New project / implementation' ||
      profile.value.enquiry_type === 'Assessment / discovery'
    profile.value.users_affected = preEngagement
      ? 'Not applicable (pre-engagement)'
      : 'Not specified'
  }
}

const panelPrompt = (panel) => {
  const prompts = {
    criticality: 'How critical is this right now?',
    users: 'How many users or systems are affected?',
    technologies: 'Which technologies are involved? Select all that apply.',
    version: 'Platform version? (optional — you can skip.)',
    model: 'Platform model? (optional — you can skip.)',
  }
  return prompts[panel] || ''
}

const goToNextIntakePanel = () => {
  if (intakeQueue.value.length) {
    const next = intakeQueue.value.shift()
    intakePanel.value = next
    pushAssistant(panelPrompt(next))
    scrollToBottom()
    return
  }
  applyIntakeDefaults()
  intakePanel.value = null
  startDiscovery()
  scrollToBottom()
}

const startDiscovery = () => {
  phase.value = 'discovery'
  pushAssistant(
    `Thanks, ${profile.value.name}! ${discoveryPromptForType(profile.value.enquiry_type)}`
  )
  discoveryMessages.value = []
  canSubmit.value = false
}

const confirmEnquiryType = () => {
  profile.value.enquiry_type = panelValues.value.enquiry_type
  pushUser(profile.value.enquiry_type)
  intakePanel.value = null
  intakeTextStep.value = 0
  pushAssistant("Great. What's your full name?")
  scrollToBottom()
}

const confirmService = () => {
  profile.value.service = panelValues.value.service
  pushUser(profile.value.service)
  intakeQueue.value = [...(INTAKE_PANELS_BY_TYPE[profile.value.enquiry_type] || ['technologies'])]
  goToNextIntakePanel()
}

const confirmCriticality = () => {
  profile.value.criticality = panelValues.value.criticality
  pushUser(profile.value.criticality)
  goToNextIntakePanel()
}

const confirmUsers = () => {
  profile.value.users_affected = panelValues.value.users_affected.trim()
  pushUser(profile.value.users_affected)
  goToNextIntakePanel()
}

const confirmTechnologies = () => {
  profile.value.technologies = [...panelValues.value.technologies]
  profile.value.technology_other = panelValues.value.technology_other.trim()
  const label = profile.value.technologies.join(', ')
  pushUser(label + (profile.value.technology_other ? ` (${profile.value.technology_other})` : ''))
  goToNextIntakePanel()
}

const skipVersion = () => {
  profile.value.platform_version = ''
  pushUser('(version skipped)')
  goToNextIntakePanel()
}

const confirmVersion = () => {
  profile.value.platform_version = panelValues.value.platform_version.trim()
  pushUser(profile.value.platform_version || '(not provided)')
  goToNextIntakePanel()
}

const skipModel = () => {
  profile.value.platform_model = ''
  pushUser('(model skipped)')
  goToNextIntakePanel()
}

const confirmModel = () => {
  profile.value.platform_model = panelValues.value.platform_model.trim()
  pushUser(profile.value.platform_model || '(not provided)')
  goToNextIntakePanel()
}

const handleTextIntake = (text) => {
  if (intakeTextStep.value === 0) {
    if (text.length < 2) {
      pushAssistant('Please enter your full name.')
      return
    }
    profile.value.name = text
    pushUser(text)
    intakeTextStep.value = 1
    pushAssistant('What email should we use to follow up?')
    return
  }
  if (intakeTextStep.value === 1) {
    if (!isValidEmail(text)) {
      pushAssistant('Please enter a valid email address.')
      return
    }
    profile.value.email = text
    pushUser(text)
    intakeTextStep.value = 2
    pushAssistant('Which company or organization? (Type "none" if personal.)')
    return
  }
  if (intakeTextStep.value === 2) {
    profile.value.company = text.toLowerCase() === 'none' ? '' : text
    pushUser(profile.value.company || '(not provided)')
    intakePanel.value = 'service'
    pushAssistant('Which service are you interested in?')
    scrollToBottom()
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
    pushAssistant('Sorry, connection failed. Email contact@nexxus-tech.com or use our contact form.')
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
  if (!text || loading.value || submitting.value) return
  if (phase.value === 'intake' && !intakePanel.value) {
    inputText.value = ''
    handleTextIntake(text)
    await scrollToBottom()
    return
  }
  if (phase.value === 'discovery') {
    inputText.value = ''
    await handleDiscovery(text)
  }
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
    showInvite.value = false
  } catch (err) {
    const detail = err.response?.data?.detail
    const msg = Array.isArray(detail) ? detail.map((d) => d.msg || d).join(', ') : detail
    pushAssistant(msg || 'Could not send. Try contact@nexxus-tech.com.')
  } finally {
    submitting.value = false
    await scrollToBottom()
  }
}

watch([isOpen, chatSize], ([open, size]) => {
  if (typeof document === 'undefined') return
  document.body.style.overflow = open && size === 'expanded' ? 'hidden' : ''
})

onMounted(() => {
  try {
    const saved = sessionStorage.getItem(CHAT_SIZE_KEY)
    if (saved === 'compact' || saved === 'expanded') chatSize.value = saved
  } catch { /* ignore */ }
  inviteTimer = setTimeout(showInvitePopup, 2500)
})

onUnmounted(() => {
  clearTimeout(inviteTimer)
  clearTimeout(remindTimer)
  if (typeof document !== 'undefined') document.body.style.overflow = ''
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
  gap: 14px;
}

/* Invitation card */
.chat-invite-card {
  position: relative;
  width: 300px;
  background: linear-gradient(160deg, var(--nt-dark-2) 0%, var(--nt-dark-3) 100%);
  border: 1px solid rgba(0, 168, 224, 0.35);
  border-radius: 16px;
  padding: 20px 20px 18px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.45), 0 0 0 1px rgba(0, 123, 167, 0.15);
  animation: inviteAttention 2.5s ease-in-out infinite;
}
@keyframes inviteAttention {
  0%, 100% { box-shadow: 0 12px 40px rgba(0, 0, 0, 0.45), 0 0 0 1px rgba(0, 123, 167, 0.15); }
  50% { box-shadow: 0 12px 48px rgba(0, 123, 167, 0.35), 0 0 0 2px rgba(0, 168, 224, 0.4); }
}
.invite-close {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(255, 255, 255, 0.08);
  border: none;
  border-radius: 6px;
  width: 26px;
  height: 26px;
  color: var(--nt-text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.invite-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--nt-primary), var(--nt-secondary));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.2rem;
  margin-bottom: 12px;
}
.invite-eyebrow {
  margin: 0 0 4px;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--nt-secondary);
}
.invite-title {
  margin: 0 0 8px;
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--nt-white);
  font-family: var(--font-heading);
}
.invite-body {
  margin: 0 0 16px;
  font-size: 0.82rem;
  line-height: 1.55;
  color: var(--nt-text-muted);
}
.invite-cta {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  border: none;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--nt-primary), var(--nt-secondary));
  color: white;
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}
.invite-cta:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(0, 123, 167, 0.45);
}

.invite-pop-enter-active,
.invite-pop-leave-active {
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
.invite-pop-enter-from,
.invite-pop-leave-to {
  opacity: 0;
  transform: translateY(16px) scale(0.92);
}

/* Bubble */
.chat-bubble {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--nt-primary), var(--nt-secondary));
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  color: white;
  box-shadow: 0 4px 24px rgba(0, 123, 167, 0.5);
  transition: var(--nt-transition);
  position: relative;
}
.chat-bubble.has-invite {
  animation: bubbleWiggle 3s ease-in-out infinite;
}
@keyframes bubbleWiggle {
  0%, 88%, 100% { transform: rotate(0); }
  90% { transform: rotate(-8deg); }
  94% { transform: rotate(8deg); }
}
.bubble-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  min-width: 20px;
  height: 20px;
  padding: 0 5px;
  border-radius: 10px;
  background: #ef4444;
  color: white;
  font-size: 0.65rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--nt-dark);
  z-index: 2;
}
.bubble-hint {
  position: absolute;
  right: calc(100% + 10px);
  white-space: nowrap;
  background: var(--nt-dark-3);
  border: 1px solid var(--nt-border);
  color: var(--nt-text-light);
  font-size: 0.75rem;
  font-weight: 700;
  padding: 6px 12px;
  border-radius: 8px;
  box-shadow: var(--nt-shadow);
  pointer-events: none;
}
.bubble-hint::after {
  content: '';
  position: absolute;
  right: -5px;
  top: 50%;
  transform: translateY(-50%);
  border: 5px solid transparent;
  border-left-color: var(--nt-border);
}
.chat-bubble:hover {
  transform: scale(1.08);
}
.chat-bubble.active {
  background: linear-gradient(135deg, #005f7f, #005f7f);
  animation: none;
}
.bubble-ring {
  position: absolute;
  inset: -6px;
  border-radius: 50%;
  border: 2px solid rgba(0, 123, 167, 0.35);
  animation: bubbleRing 2s ease-in-out infinite;
}
@keyframes bubbleRing {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.18); opacity: 0; }
}

.chat-backdrop {
  position: fixed;
  inset: 0;
  z-index: -1;
  background: rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(2px);
}

.chat-widget.is-expanded {
  inset: 0;
  bottom: 0;
  right: 0;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  padding:
    max(8px, env(safe-area-inset-top, 0px))
    max(8px, env(safe-area-inset-right, 0px))
    max(8px, env(safe-area-inset-bottom, 0px))
    max(8px, env(safe-area-inset-left, 0px));
  align-items: stretch;
  justify-content: stretch;
  gap: 0;
}

.chat-window {
  background: var(--nt-dark-2);
  border: 1px solid var(--nt-border);
  display: flex;
  flex-direction: column;
  box-shadow: 0 16px 60px rgba(0, 0, 0, 0.5);
  overflow: hidden;
  min-height: 0;
}

.chat-window--expanded {
  width: 100%;
  height: 100%;
  max-width: 100%;
  max-height: 100%;
  border-radius: 16px;
}

.chat-window--compact {
  width: 360px;
  max-height: min(580px, calc(100dvh - 100px));
  border-radius: 20px;
}

.chat-header {
  background: linear-gradient(135deg, var(--nt-primary), var(--nt-primary-d));
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.chat-header-info { display: flex; align-items: center; gap: 12px; }
.chat-avatar {
  width: 38px;
  height: 38px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}
.chat-name {
  display: block;
  font-weight: 700;
  color: white;
  font-size: 0.9rem;
  font-family: var(--font-heading);
}
.chat-status {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.72rem;
  color: rgba(255, 255, 255, 0.75);
}
.status-dot {
  width: 7px;
  height: 7px;
  background: var(--nt-secondary);
  border-radius: 50%;
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
.chat-header-actions {
  display: flex;
  align-items: center;
  gap: 6px;
}
.chat-resize,
.chat-close {
  background: rgba(255, 255, 255, 0.15);
  border: none;
  border-radius: 6px;
  width: 32px;
  height: 32px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  transition: background 0.2s;
}
.chat-resize:hover,
.chat-close:hover {
  background: rgba(255, 255, 255, 0.28);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 0;
}
.chat-window--compact .chat-messages {
  max-height: 280px;
  flex: none;
}
.chat-msg { display: flex; gap: 8px; align-items: flex-end; }
.chat-msg--user { flex-direction: row-reverse; }
.msg-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--nt-primary), var(--nt-secondary));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  color: white;
  flex-shrink: 0;
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

.typing { display: flex; gap: 4px; padding: 12px 16px; }
.typing span {
  width: 7px;
  height: 7px;
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
  overflow-y: auto;
  flex-shrink: 0;
  min-height: 0;
}
.chat-window--compact .chat-intake-panel {
  max-height: 200px;
}
.chat-window--expanded .chat-intake-panel {
  max-height: min(42vh, 420px);
}
.chat-intake-panel label {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--nt-text-muted);
}
.optional { font-weight: 400; text-transform: none; letter-spacing: 0; opacity: 0.8; }
.chat-intake-panel select,
.chat-intake-panel input[type='text'] {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 10px 12px;
  color: var(--nt-text);
  font-size: 0.85rem;
  width: 100%;
}
.tech-checkboxes { display: flex; flex-direction: column; gap: 6px; }
.tech-check {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.8rem;
  color: var(--nt-text-light);
  cursor: pointer;
}
.tech-check input { accent-color: var(--nt-primary); }
.tech-other { margin-top: 4px; }
.enquiry-options {
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow-y: auto;
}
.chat-window--compact .enquiry-options {
  max-height: 220px;
}
.chat-window--expanded .enquiry-options {
  max-height: none;
  flex: 1;
}
.chat-window--expanded .enquiry-option {
  padding: 14px 16px;
}
.chat-window--expanded .enquiry-option-label {
  font-size: 0.95rem;
}
.chat-window--expanded .enquiry-option-desc {
  font-size: 0.8rem;
}
.enquiry-option {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
  text-align: left;
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid var(--nt-border);
  background: rgba(255, 255, 255, 0.04);
  color: var(--nt-text-light);
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
  width: 100%;
}
.enquiry-option .pi {
  color: var(--nt-secondary);
  font-size: 0.95rem;
  margin-bottom: 2px;
}
.enquiry-option.selected {
  border-color: var(--nt-primary);
  background: rgba(0, 123, 167, 0.15);
}
.enquiry-option-label {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--nt-white);
}
.enquiry-option-desc {
  font-size: 0.72rem;
  color: var(--nt-text-muted);
  line-height: 1.35;
}
.panel-actions { display: flex; gap: 8px; }
.btn-skip {
  flex: 1;
  background: transparent;
  border: 1px solid var(--nt-border);
  border-radius: 10px;
  padding: 10px;
  color: var(--nt-text-muted);
  cursor: pointer;
  font-size: 0.85rem;
}
.btn-intake {
  flex: 1;
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

.chat-success {
  padding: 16px;
  text-align: center;
  color: #4ade80;
  font-size: 0.85rem;
  border-top: 1px solid var(--nt-border);
}
.chat-success .pi { font-size: 1.5rem; margin-bottom: 8px; display: block; }

.chat-input-area {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  border-top: 1px solid var(--nt-border);
  background: var(--nt-dark-3);
}
.chat-input-area input {
  flex: 1;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 10px 14px;
  color: var(--nt-text);
  font-size: 0.875rem;
  outline: none;
}
.chat-send {
  width: 38px;
  height: 38px;
  background: var(--nt-primary);
  border: none;
  border-radius: 10px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.chat-send:disabled { opacity: 0.4; cursor: not-allowed; }

.chat-disclaimer {
  font-size: 0.65rem;
  color: var(--nt-text-muted);
  text-align: center;
  padding: 4px 16px 10px;
  background: var(--nt-dark-3);
}

.chat-window-enter-active,
.chat-window-leave-active {
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
.chat-window-enter-from,
.chat-window-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}
.icon-flip-enter-active,
.icon-flip-leave-active {
  transition: all 0.2s ease;
}
.icon-flip-enter-from,
.icon-flip-leave-to {
  opacity: 0;
  transform: rotate(90deg) scale(0.8);
}

@media (min-width: 768px) {
  .chat-widget.is-expanded {
    padding: 20px 24px;
    align-items: flex-end;
    justify-content: flex-end;
  }
  .chat-window--expanded {
    width: min(560px, calc(100vw - 48px));
    height: min(92dvh, 880px);
    border-radius: 20px;
  }
}

@media (max-width: 767px) {
  .chat-widget.is-expanded {
    padding: 0;
  }
  .chat-window--expanded {
    border-radius: 0;
    border-left: none;
    border-right: none;
    border-bottom: none;
  }
}

@media (max-width: 480px) {
  .chat-widget:not(.is-expanded) {
    bottom: 16px;
    right: 16px;
  }
  .chat-window--compact {
    width: calc(100vw - 32px);
    max-height: calc(100dvh - 88px);
  }
  .chat-invite-card {
    width: calc(100vw - 100px);
    max-width: 300px;
  }
  .bubble-hint { display: none; }
}
</style>
