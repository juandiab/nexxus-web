<template>
  <!-- Chat bubble button -->
  <div class="chat-widget">
    <Transition name="chat-window">
      <div v-if="isOpen" class="chat-window">
        <!-- Header -->
        <div class="chat-header">
          <div class="chat-header-info">
            <div class="chat-avatar">
              <i class="pi pi-bolt"></i>
            </div>
            <div>
              <span class="chat-name">NexBot</span>
              <span class="chat-status">
                <span class="status-dot"></span>
                AI Assistant · Nexxus Tech
              </span>
            </div>
          </div>
          <button class="chat-close" @click="isOpen = false" aria-label="Close chat">
            <i class="pi pi-times"></i>
          </button>
        </div>

        <!-- Messages -->
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

        <!-- Input -->
        <div class="chat-input-area">
          <input
            v-model="inputText"
            type="text"
            placeholder="Ask about WAF, NetScaler, Zero-Trust..."
            @keydown.enter="sendMessage"
            :disabled="loading"
            ref="inputEl"
          />
          <button class="chat-send" @click="sendMessage" :disabled="loading || !inputText.trim()">
            <i class="pi pi-send"></i>
          </button>
        </div>
        <p class="chat-disclaimer">AI responses may not always be accurate. Contact us for professional advice.</p>
      </div>
    </Transition>

    <!-- Bubble -->
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
import { ref, nextTick, onMounted } from 'vue'
import axios from 'axios'

const isOpen = ref(false)
const inputText = ref('')
const loading = ref(false)
const messagesEl = ref(null)
const inputEl = ref(null)
const hasNotification = ref(false)
const notificationText = ref("Hi! I'm NexBot — ask me about WAF or NetScaler 👋")

const messages = ref([
  {
    role: 'assistant',
    content: "Hi! I'm NexBot, Nexxus Tech's AI assistant. I can answer questions about WAF, NetScaler ADC, Zero-Trust Architecture, and cloud security. How can I help you today?"
  }
])

const scrollToBottom = async () => {
  await nextTick()
  if (messagesEl.value) {
    messagesEl.value.scrollTop = messagesEl.value.scrollHeight
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

const sendMessage = async () => {
  const text = inputText.value.trim()
  if (!text || loading.value) return

  messages.value.push({ role: 'user', content: text })
  inputText.value = ''
  loading.value = true
  await scrollToBottom()

  try {
    const history = messages.value.map(m => ({ role: m.role, content: m.content }))
    const { data } = await axios.post('/api/chat', { messages: history })
    messages.value.push({ role: 'assistant', content: data.reply })
  } catch {
    messages.value.push({
      role: 'assistant',
      content: "Sorry, I'm having trouble connecting. Please reach out directly at contact@nexxus-tech.com — we'd love to help!"
    })
  } finally {
    loading.value = false
    await scrollToBottom()
  }
}

// Show notification after delay
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

/* Bubble */
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

/* Notification */
.chat-notification {
  background: var(--nt-dark-3);
  border: 1px solid var(--nt-border);
  border-radius: 12px;
  padding: 10px 14px;
  max-width: 240px;
  font-size: 0.82rem;
  color: var(--nt-text-light);
  display: flex; align-items: center; gap: 8px;
  box-shadow: var(--nt-shadow);
}
.notif-close {
  background: none; border: none; cursor: pointer;
  color: var(--nt-text-muted); font-size: 0.7rem;
  padding: 2px; flex-shrink: 0;
  transition: color 0.2s;
}
.notif-close:hover { color: var(--nt-white); }

/* Window */
.chat-window {
  width: 360px;
  max-height: 520px;
  background: var(--nt-dark-2);
  border: 1px solid var(--nt-border);
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 16px 60px rgba(0,0,0,0.5), 0 0 0 1px rgba(0,123,167,0.1);
  overflow: hidden;
}

/* Header */
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
  transition: background 0.2s;
}
.chat-close:hover { background: rgba(255,255,255,0.3); }

/* Messages */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 340px;
  scroll-behavior: smooth;
}
.chat-messages::-webkit-scrollbar { width: 4px; }
.chat-messages::-webkit-scrollbar-thumb { background: rgba(0,123,167,0.3); border-radius: 2px; }

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

/* Typing indicator */
.typing {
  display: flex; align-items: center; gap: 4px;
  padding: 12px 16px;
}
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

/* Input */
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
  font-family: var(--font-body);
  outline: none;
  transition: border-color 0.2s;
}
.chat-input-area input:focus { border-color: var(--nt-primary); }
.chat-input-area input::placeholder { color: rgba(255,255,255,0.25); }
.chat-input-area input:disabled { opacity: 0.5; }
.chat-send {
  width: 38px; height: 38px;
  background: var(--nt-primary);
  border: none; border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  color: white; font-size: 0.9rem;
  cursor: pointer; flex-shrink: 0;
  transition: var(--nt-transition);
}
.chat-send:hover:not(:disabled) { background: var(--nt-primary-l); transform: scale(1.05); }
.chat-send:disabled { opacity: 0.4; cursor: not-allowed; }

.chat-disclaimer {
  font-size: 0.65rem;
  color: var(--nt-text-muted);
  text-align: center;
  padding: 4px 16px 10px;
  background: var(--nt-dark-3);
}

/* Transitions */
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
