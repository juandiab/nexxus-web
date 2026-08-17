<template>
  <div class="cafeina-page">
    <section class="page-hero">
      <div class="page-hero-bg"></div>
      <div class="container page-hero-content">
        <span class="section-label reveal">Personal macOS utility</span>
        <h1 class="reveal reveal-delay-1">Cafeina</h1>
        <p class="page-hero-subtitle reveal reveal-delay-2">
          A lightweight menu bar app that keeps your Mac awake while enabled.
          Built by Juan Pablo Otalvaro A. Requires macOS 13 or later.
        </p>
        <div class="hero-actions reveal reveal-delay-3">
          <a
            href="https://github.com/juandiab/Cafeina"
            class="btn btn-primary"
            target="_blank"
            rel="noopener noreferrer"
          >
            <i class="pi pi-github"></i> View on GitHub
          </a>
          <RouterLink to="/cafeina/privacy" class="btn btn-secondary">
            Privacy Policy
          </RouterLink>
          <a href="mailto:support@nexxus-tech.com" class="btn btn-outline">
            <i class="pi pi-envelope"></i> Support
          </a>
        </div>
      </div>
    </section>

    <section class="section cafeina-body">
      <div class="container cafeina-inner">
        <article class="cafeina-card reveal">
          <h2>What it is</h2>
          <p>
            Cafeina is a personal native macOS menu bar utility. While enabled, it
            uses system power assertions so your Mac stays awake. Preferences stay
            on your device — Cafeina does not collect personal data.
          </p>
          <ul class="cafeina-list">
            <li>Native menu bar app for macOS 13+</li>
            <li>Runs locally on your Mac</li>
            <li>No accounts, analytics, or advertising SDKs</li>
          </ul>
        </article>

        <article class="cafeina-card reveal reveal-delay-1">
          <h2>Support &amp; privacy</h2>
          <p>
            Hosted on the Nexxus Tech domain for privacy and support URLs only.
            Cafeina is a personal app by Juan Pablo Otalvaro A., not a Nexxus Tech
            company product.
          </p>
          <ul class="cafeina-links">
            <li>
              <RouterLink to="/cafeina/privacy">Cafeina Privacy Policy</RouterLink>
            </li>
            <li>
              <a href="mailto:support@nexxus-tech.com">support@nexxus-tech.com</a>
            </li>
            <li>
              <a
                href="https://github.com/juandiab/Cafeina"
                target="_blank"
                rel="noopener noreferrer"
              >github.com/juandiab/Cafeina</a>
            </li>
          </ul>
          <p class="cafeina-disclaimer">
            Cafeina is not affiliated with Caffeine or any similarly named apps.
          </p>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup>
</script>

<style scoped>
.page-hero {
  min-height: 42vh;
  display: flex;
  align-items: center;
  background: var(--nt-dark);
  padding: 120px 0 60px;
  position: relative;
  overflow: hidden;
}
.page-hero-bg {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 50% 60%, rgba(0, 123, 167, 0.14) 0%, transparent 65%);
}
.page-hero-content { position: relative; z-index: 1; max-width: 720px; }
.page-hero h1 {
  font-size: clamp(2.4rem, 5vw, 3.4rem);
  margin-top: 8px;
}
.page-hero-subtitle {
  font-size: 1.05rem;
  color: var(--nt-text-muted);
  margin-top: 16px;
  max-width: 560px;
  line-height: 1.75;
}
.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 28px;
}

.cafeina-body {
  padding: 64px 0 100px;
  background: var(--nt-dark-2);
  border-top: 1px solid var(--nt-border);
}
.cafeina-inner {
  display: grid;
  gap: 24px;
  max-width: 820px;
}
.cafeina-card {
  padding: 28px 0;
  border-bottom: 1px solid var(--nt-border);
}
.cafeina-card:last-child { border-bottom: none; }
.cafeina-card h2 {
  font-size: 1.35rem;
  margin-bottom: 12px;
}
.cafeina-card p {
  color: var(--nt-text-muted);
  line-height: 1.75;
  margin-bottom: 14px;
}
.cafeina-list,
.cafeina-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 8px;
}
.cafeina-list li {
  color: var(--nt-text-muted);
  padding-left: 18px;
  position: relative;
  line-height: 1.6;
}
.cafeina-list li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.65em;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--nt-primary);
}
.cafeina-links a {
  color: var(--nt-secondary);
  font-weight: 600;
}
.cafeina-links a:hover { text-decoration: underline; }
.cafeina-disclaimer {
  margin-top: 20px;
  font-size: 0.85rem;
  color: #94a3b8;
}

@media (max-width: 640px) {
  .hero-actions { flex-direction: column; align-items: stretch; }
  .hero-actions .btn { justify-content: center; }
}
</style>
