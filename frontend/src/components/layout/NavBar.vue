<template>
  <header :class="['navbar', { scrolled: isScrolled, 'menu-open': menuOpen }]">
    <div class="container navbar-inner">
      <!-- Logo -->
      <RouterLink to="/" class="navbar-logo" @click="menuOpen = false">
        <img :src="logoSrc" alt="Nexxus Tech" class="logo-img" />
      </RouterLink>

      <!-- Desktop nav -->
      <nav class="navbar-links">
        <RouterLink v-for="link in links" :key="link.to" :to="link.to" class="nav-link">
          {{ link.label }}
        </RouterLink>
        <RouterLink to="/contact" class="btn btn-primary nav-cta">Get in Touch</RouterLink>
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
      <div v-if="menuOpen" class="mobile-nav">
        <RouterLink
          v-for="link in links"
          :key="link.to"
          :to="link.to"
          class="mobile-nav-link"
          @click="menuOpen = false"
        >
          {{ link.label }}
        </RouterLink>
        <RouterLink to="/contact" class="btn btn-primary w-full" @click="menuOpen = false">
          Get in Touch
        </RouterLink>
      </div>
    </Transition>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import logo from '@/assets/nexxus-tech-logo-full-large.svg'

const isScrolled = ref(false)
const menuOpen = ref(false)
const logoSrc = logo

const links = [
  { to: '/', label: 'Home' },
  { to: '/services', label: 'Services' },
  { to: '/about', label: 'About' },
  { to: '/blog', label: 'Blog' },
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
  transition: all 0.35s ease;
  background: transparent;
  padding: 8px 0;
}
.navbar.scrolled {
  background: rgba(28, 28, 30, 0.95);
  backdrop-filter: blur(16px);
  box-shadow: 0 1px 0 rgba(0, 123, 167, 0.15);
  padding: 4px 0;
}
.navbar-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 72px;
}
.navbar-logo { display: flex; align-items: center; }
.logo-img { height: 52px; width: auto; display: block; }

.navbar-links {
  display: flex;
  align-items: center;
  gap: 8px;
}
.nav-link {
  font-family: var(--font-heading);
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.75);
  padding: 8px 16px;
  border-radius: 6px;
  transition: var(--nt-transition);
  text-decoration: none;
}
.nav-link:hover,
.nav-link.router-link-active {
  color: var(--nt-white);
  background: rgba(0, 123, 167, 0.12);
}
.nav-cta { margin-left: 8px; padding: 10px 24px; font-size: 0.85rem; }

/* Hamburger */
.hamburger {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
}
.hamburger span {
  display: block;
  width: 26px;
  height: 2px;
  background: var(--nt-white);
  border-radius: 2px;
  transition: var(--nt-transition);
  transform-origin: center;
}
.hamburger span.open:nth-child(1) { transform: rotate(45deg) translate(5px, 5px); }
.hamburger span.open:nth-child(2) { opacity: 0; transform: scaleX(0); }
.hamburger span.open:nth-child(3) { transform: rotate(-45deg) translate(5px, -5px); }

/* Mobile menu */
.mobile-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 16px 24px 24px;
  background: rgba(28, 28, 30, 0.98);
  border-top: 1px solid rgba(0, 123, 167, 0.15);
}
.mobile-nav-link {
  font-family: var(--font-heading);
  font-size: 1rem;
  font-weight: 600;
  color: rgba(255,255,255,0.8);
  padding: 14px 16px;
  border-radius: 8px;
  text-decoration: none;
  transition: var(--nt-transition);
}
.mobile-nav-link:hover { color: white; background: rgba(0,123,167,0.15); }
.w-full { width: 100%; justify-content: center; margin-top: 8px; }

/* Transition */
.mobile-menu-enter-active, .mobile-menu-leave-active { transition: all 0.3s ease; }
.mobile-menu-enter-from, .mobile-menu-leave-to { opacity: 0; transform: translateY(-10px); }

@media (max-width: 768px) {
  .navbar-links { display: none; }
  .hamburger { display: flex; }
}
</style>
