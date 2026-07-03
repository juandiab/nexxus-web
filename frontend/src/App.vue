<template>
  <div class="app-root">
    <a href="#main-content" class="skip-link">Skip to main content</a>
    <NavBar />
    <main id="main-content">
      <RouterView v-slot="{ Component }">
        <Transition name="page" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </main>
    <AppFooter />
    <ChatWidget />
    <Toast />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import Toast from 'primevue/toast'
import NavBar from '@/components/layout/NavBar.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import ChatWidget from '@/components/shared/ChatWidget.vue'

// Global scroll-reveal
onMounted(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible')
        }
      })
    },
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
  )

  const observe = () => {
    document.querySelectorAll('.reveal').forEach((el) => {
      if (!el.classList.contains('visible')) observer.observe(el)
    })
  }

  observe()
  // Re-observe after route changes
  const mutationObserver = new MutationObserver(observe)
  mutationObserver.observe(document.body, { childList: true, subtree: true })
})
</script>

<style>
.app-root { min-height: 100vh; display: flex; flex-direction: column; }
main { flex: 1; }

.skip-link {
  position: absolute;
  top: -100px;
  left: 16px;
  z-index: 10000;
  padding: 10px 18px;
  background: var(--nt-primary);
  color: white;
  font-family: var(--font-heading);
  font-size: 0.85rem;
  font-weight: 700;
  text-decoration: none;
  border-radius: 6px;
  transition: top 0.2s ease;
}
.skip-link:focus {
  top: 16px;
  outline: 2px solid var(--nt-secondary);
  outline-offset: 2px;
}
</style>
