<template>
  <header :class="['navbar', { scrolled: isScrolled, 'menu-open': menuOpen }]">
    <div class="container navbar-inner">
      <!-- Logo -->
      <RouterLink to="/" class="navbar-logo" @click="menuOpen = false">
        <NxConnectionRings size="nav" class="navbar-rings-mark" />
        <span class="navbar-logo-stack">
          <span class="navbar-wordmark ld-cursor">
            <span class="navbar-wordmark__nexxus">NEXXUS</span><span class="navbar-wordmark__tech">TECH</span>
          </span>
          <span class="navbar-tagline">Consulting . Cloud . Security . AI</span>
        </span>
      </RouterLink>

      <!-- Desktop nav -->
      <nav class="navbar-links" aria-label="Main navigation">
        <RouterLink v-for="link in links" :key="link.to" :to="link.to" class="nav-link">
          {{ link.label }}
        </RouterLink>
        <GlowButton variant="primary" class="nav-cta-glow">
          <RouterLink to="/contact" class="btn btn-primary nx-btn nx-btn--primary nav-cta">Get in Touch</RouterLink>
        </GlowButton>
      </nav>

      <!-- Mobile hamburger -->
      <button class="hamburger" @click="menuOpen = !menuOpen" aria-label="Toggle menu">
        <span :class="{ open: menuOpen }"></span>
        <span :class="{ open: menuOpen }"></span>
        <span :class="{ open: menuOpen }"></span>
      </button>
    </div>

    <!-- Mobile menu -->
    <Transition name="mobile-menu">
      <div v-if="menuOpen" class="mobile-nav" role="navigation" aria-label="Mobile navigation">
        <RouterLink
          v-for="link in links"
          :key="link.to"
          :to="link.to"
          class="mobile-nav-link"
          @click="menuOpen = false"
        >
          {{ link.label }}
        </RouterLink>
        <GlowButton variant="primary" class="mobile-nav-glow mobile-nav-cta-glow">
          <RouterLink to="/contact" class="btn btn-primary nx-btn nx-btn--primary w-full" @click="menuOpen = false">
            Get in Touch
          </RouterLink>
        </GlowButton>
      </div>
    </Transition>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import GlowButton from '@/components/shared/GlowButton.vue'
import NxConnectionRings from '@/components/shared/NxConnectionRings.vue'

const isScrolled = ref(false)
const menuOpen = ref(false)

const links = [
  { to: '/', label: 'Home' },
  { to: '/services', label: 'Services' },
  { to: '/products', label: 'Products' },
  { to: '/about', label: 'About' },
  { to: '/blog', label: 'Blog' },
  { to: '/book-demo', label: 'Book a Demo' },
]

const onScroll = () => { isScrolled.value = window.scrollY > 40 }
onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 1000;
  transition: background var(--nx-dur) var(--nx-ease),
    padding var(--nx-dur) var(--nx-ease),
    border-color var(--nx-dur) var(--nx-ease),
    box-shadow var(--nx-dur) var(--nx-ease);
  background: transparent;
  padding: 16px 0;
  border-bottom: 1px solid transparent;
  min-height: 88px;
}
.navbar.scrolled {
  background: rgba(7, 11, 18, 0.92);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  padding: 10px 0;
  border-bottom-color: var(--nx-border-strong);
}
.navbar-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 72px;
}
.navbar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}
.navbar-rings-mark {
  color: var(--nx-cyan-400);
  filter: drop-shadow(0 0 6px rgba(56, 198, 244, 0.45));
}
.navbar-logo-stack {
  display: flex;
  flex-direction: column;
  gap: 2px;
  container-type: inline-size;
  min-width: 0;
}
.navbar-wordmark {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-weight: 600;
  line-height: 1;
  white-space: nowrap;
}
.navbar-wordmark.ld-cursor {
  font-size: clamp(1.15rem, 2.4vw, 1.5rem);
  letter-spacing: 0.1em;
}
.navbar-wordmark.ld-cursor::after {
  color: var(--nx-cyan-400);
  font-size: 1.05em;
}
.navbar-wordmark__nexxus {
  color: var(--nx-text-hi);
}
.navbar-wordmark__tech {
  color: var(--nx-cyan-400);
}
.navbar-tagline {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: clamp(0.625rem, 4.2cqi, 0.7rem);
  font-weight: 400;
  line-height: 1.2;
  letter-spacing: 0.024em;
  word-spacing: -0.1em;
  color: rgba(255, 255, 255, 0.72);
  white-space: nowrap;
}

.navbar-links {
  display: flex;
  align-items: center;
  gap: 6px;
}
.nav-link {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
  min-width: 48px;
  font-family: var(--font-heading);
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--nx-text-mut);
  padding: 8px 16px;
  border-radius: 6px;
  transition: color var(--nx-dur-fast) var(--nx-ease);
  text-decoration: none;
}
.nav-link::after {
  content: '';
  position: absolute;
  left: 16px;
  right: 16px;
  bottom: 6px;
  height: 2px;
  background: linear-gradient(90deg, var(--nx-cyan-400), var(--nx-blue-500));
  transform: scaleX(0);
  transform-origin: left;
  opacity: 1;
  transition: transform var(--nx-dur) var(--nx-ease), opacity var(--nx-dur) var(--nx-ease);
}
.nav-link:hover {
  color: var(--nx-text-hi);
}
.nav-link:hover::after {
  transform: scaleX(1);
}
.nav-link.router-link-active {
  color: var(--nx-text-hi);
}
.nav-link.router-link-active::after {
  transform: scaleX(1);
  opacity: 0.7;
}
.nav-cta-glow {
  margin-left: 6px;
}
.nav-cta {
  padding: 10px 24px;
  font-size: 0.85rem;
  transition: background var(--nx-dur) var(--nx-ease),
    border-color var(--nx-dur) var(--nx-ease),
    box-shadow var(--nx-dur) var(--nx-ease),
    color var(--nx-dur) var(--nx-ease),
    transform var(--nx-dur-fast) var(--nx-ease);
}
.nav-cta:active {
  transform: translateY(1px);
  box-shadow: var(--nx-shadow-1);
}
.nav-cta:focus-visible {
  outline: 2px solid var(--nx-blue-400);
  outline-offset: 2px;
}

/* Hamburger */
.hamburger {
  display: none;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;
  min-width: 48px;
  min-height: 48px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
}
.hamburger span {
  display: block;
  width: 26px;
  height: 2px;
  background: var(--nx-text-hi);
  border-radius: 2px;
  transition: transform var(--nx-dur) var(--nx-ease), opacity var(--nx-dur) var(--nx-ease);
  transform-origin: center;
}
.hamburger span.open:nth-child(1) { transform: rotate(45deg) translate(5px, 5px); }
.hamburger span.open:nth-child(2) { opacity: 0; transform: scaleX(0); }
.hamburger span.open:nth-child(3) { transform: rotate(-45deg) translate(5px, -5px); }

/* Mobile menu */
.mobile-nav {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 16px 24px 24px;
  background: rgba(7, 11, 18, 0.98);
  border-top: 1px solid var(--nx-border);
}
.mobile-nav-glow {
  width: 100%;
}
.mobile-nav-cta-glow {
  margin-top: 8px;
}
.mobile-nav-link {
  display: flex;
  align-items: center;
  min-height: 48px;
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 600;
  color: var(--nx-text-mut);
  padding: 14px 16px;
  border-radius: 8px;
  text-decoration: none;
  transition: color var(--nx-dur) var(--nx-ease), background var(--nx-dur) var(--nx-ease);
}
.mobile-nav-link:hover,
.mobile-nav-link.router-link-active {
  color: var(--nx-text-hi);
  background: rgba(61, 139, 253, 0.12);
}
.w-full { width: 100%; justify-content: center; }

/* Transition */
.mobile-menu-enter-active, .mobile-menu-leave-active {
  transition: opacity var(--nx-dur) var(--nx-ease), transform var(--nx-dur) var(--nx-ease);
}
.mobile-menu-enter-from, .mobile-menu-leave-to { opacity: 0; transform: translateY(-10px); }

@media (max-width: 768px) {
  .navbar-links { display: none; }
  .hamburger { display: flex; }
}

@media (max-width: 480px) {
  .navbar-wordmark.ld-cursor {
    font-size: 1rem;
  }

  .navbar-tagline {
    font-size: 0.48rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .navbar,
  .nav-link,
  .nav-link::after,
  .nav-cta,
  .hamburger span,
  .mobile-nav-link {
    transition-duration: 0.01ms !important;
  }
  .nav-cta:active {
    transform: none;
  }
  .mobile-menu-enter-active, .mobile-menu-leave-active {
    transition: opacity 0.01ms linear !important;
  }
  .mobile-menu-enter-from, .mobile-menu-leave-to {
    transform: none;
  }
}
</style>
