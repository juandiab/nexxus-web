<template>
  <div class="install-block">
    <div class="install-terminal">
      <div class="terminal-bar">
        <span class="terminal-dot"></span>
        <span class="terminal-dot"></span>
        <span class="terminal-dot"></span>
        <span class="terminal-title">{{ activePlatformMeta.terminalTitle }}</span>
      </div>
      <div class="install-terminal-body">
        <pre class="install-command"><code><span v-if="activePlatform !== 'windows'" class="cmd-prompt">$ </span>{{ activeInstallCommand }}</code></pre>
        <button
          type="button"
          class="install-copy-btn"
          :class="{ copied: copiedId === copyId }"
          :aria-label="`Copy ${activePlatformMeta.name} install command`"
          @click="copyCommand(activeInstallCommand)"
        >
          <i :class="copiedId === copyId ? 'pi pi-check' : 'pi pi-copy'"></i>
          {{ copiedId === copyId ? 'Copied' : 'Copy' }}
        </button>
      </div>
    </div>

    <div class="install-platform-tabs" role="tablist" aria-label="Install platform">
      <button
        v-for="platform in platforms"
        :key="platform.id"
        type="button"
        role="tab"
        class="install-platform-tab"
        :class="{ active: activePlatform === platform.id }"
        :aria-selected="activePlatform === platform.id"
        @click="activePlatform = platform.id"
      >
        <i :class="platform.icon" aria-hidden="true"></i>
        {{ platform.name }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, onUnmounted, ref } from 'vue'

const props = defineProps({
  copyId: {
    type: String,
    default: 'install',
  },
})

const platforms = [
  {
    id: 'macos',
    name: 'macOS',
    terminalTitle: 'Terminal · macOS',
    icon: 'pi pi-apple',
    command: 'curl -fsSL https://install.nexxus-tech.com/jpilot | bash',
  },
  {
    id: 'linux',
    name: 'Linux',
    terminalTitle: 'Terminal · Linux (Ubuntu recommended)',
    icon: 'pi pi-desktop',
    command: 'curl -fsSL https://install.nexxus-tech.com/jpilot | bash',
  },
  {
    id: 'windows',
    name: 'Windows',
    terminalTitle: 'Terminal · Windows (Server / 11) · PowerShell',
    icon: 'pi pi-microsoft',
    command: 'irm https://install.nexxus-tech.com/jpilot/ps1 | iex',
  },
]

const activePlatform = ref('macos')
const copiedId = ref(null)
let copyResetTimer

const activePlatformMeta = computed(() => {
  return platforms.find((p) => p.id === activePlatform.value) ?? platforms[0]
})

const activeInstallCommand = computed(() => activePlatformMeta.value.command)

async function copyCommand(command) {
  try {
    await navigator.clipboard.writeText(command)
  } catch {
    const textarea = document.createElement('textarea')
    textarea.value = command
    textarea.setAttribute('readonly', '')
    textarea.style.position = 'absolute'
    textarea.style.left = '-9999px'
    document.body.appendChild(textarea)
    textarea.select()
    document.execCommand('copy')
    document.body.removeChild(textarea)
  }

  copiedId.value = props.copyId
  clearTimeout(copyResetTimer)
  copyResetTimer = setTimeout(() => {
    copiedId.value = null
  }, 2000)
}

onUnmounted(() => {
  clearTimeout(copyResetTimer)
})
</script>

<style scoped>
.install-block {
  width: 100%;
  max-width: 720px;
}

.install-terminal {
  text-align: left;
  background: #0b1220;
  border: 1px solid #1e293b;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.45);
  margin-bottom: 16px;
}

.install-terminal-body {
  display: flex;
  align-items: stretch;
}

.install-terminal-body .install-command {
  flex: 1;
  border: none;
  border-radius: 0;
  background: #020617;
  min-width: 0;
  margin: 0;
  padding: 16px 18px;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.install-terminal-body .install-copy-btn {
  border-radius: 0;
  border: none;
  border-left: 1px solid #1e293b;
  padding: 16px 18px;
  align-self: stretch;
}

.install-command code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace;
  font-size: clamp(0.72rem, 2.5vw, 0.84rem);
  line-height: 1.65;
  color: #e2e8f0;
  white-space: pre-wrap;
  word-break: break-all;
}

.cmd-prompt {
  color: var(--nt-primary-l);
  user-select: none;
}

.install-platform-tabs {
  display: flex;
  gap: 8px;
  justify-content: center;
  flex-wrap: wrap;
}

.install-platform-tab {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 8px;
  border: 1px solid rgba(0, 168, 224, 0.2);
  background: rgba(0, 0, 0, 0.2);
  color: var(--nt-text-muted);
  font-size: 0.8rem;
  font-weight: 600;
  font-family: var(--font-heading);
  cursor: pointer;
  transition: all 0.2s ease;
}

.install-platform-tab:hover,
.install-platform-tab.active {
  border-color: var(--nt-primary);
  color: var(--nt-primary-l);
  background: rgba(0, 123, 167, 0.15);
}

.install-copy-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid #334155;
  background: #1e293b;
  color: #cbd5e1;
  font-size: 0.75rem;
  font-weight: 700;
  font-family: var(--font-heading);
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.install-copy-btn:hover {
  border-color: var(--nt-primary);
  color: var(--nt-primary-l);
}

.install-copy-btn.copied {
  border-color: rgba(34, 197, 94, 0.45);
  background: rgba(34, 197, 94, 0.12);
  color: #4ade80;
}

.terminal-bar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 12px 16px;
  background: rgba(0, 0, 0, 0.35);
  border-bottom: 1px solid #1e293b;
}

.terminal-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #334155;
}

.terminal-dot:first-child {
  background: #ef4444;
}

.terminal-dot:nth-child(2) {
  background: #f59e0b;
}

.terminal-dot:nth-child(3) {
  background: #22c55e;
}

.terminal-title {
  margin-left: 8px;
  font-size: 0.72rem;
  font-family: var(--font-heading);
  color: #94a3b8;
  letter-spacing: 0.04em;
}

@media (max-width: 767px) {
  .install-terminal-body {
    flex-direction: column;
  }

  .install-terminal-body .install-copy-btn {
    width: 100%;
    justify-content: center;
    border-left: none;
    border-top: 1px solid #1e293b;
    padding: 14px;
    font-size: 0.82rem;
  }
}
</style>
