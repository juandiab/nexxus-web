<template>
  <div class="privacy-page">
    <section class="page-hero">
      <div class="page-hero-bg"></div>
      <div class="container page-hero-content">
        <span class="section-label reveal">Cafeina</span>
        <h1 class="reveal reveal-delay-1">Cafeina Privacy Policy</h1>
        <p class="page-hero-subtitle reveal reveal-delay-2">
          Effective date: August 17, 2026
        </p>
      </div>
    </section>

    <section class="section privacy-body">
      <div class="container privacy-inner">
        <article class="privacy-prose reveal">
          <p class="lede">
            Cafeina does not collect, store, transmit, or sell personal data.
            There are no analytics, tracking, accounts, or advertising SDKs.
          </p>

          <h2>Who we are</h2>
          <p>
            Cafeina is a personal macOS menu bar utility developed by
            <strong>Juan Pablo Otalvaro A</strong>. Support and privacy pages are
            hosted on the Nexxus Tech website for App Store compliance and contact
            convenience. Cafeina is not a Nexxus Tech company product.
          </p>

          <h2>What Cafeina does locally</h2>
          <p>
            Cafeina runs entirely on your Mac. While enabled, it keeps the Mac
            awake using system power assertions. Optional Open at Login uses
            standard macOS APIs. Preferences remain on-device; Cafeina may store
            a first-run hint in UserDefaults and does not sync preferences to any
            remote service.
          </p>

          <h2>Data collection</h2>
          <p>
            Cafeina does not collect personal information. It does not create user
            accounts, does not include analytics or crash reporters that send
            identifying data, and does not use advertising or tracking SDKs.
          </p>

          <h2>Third-party sharing</h2>
          <p>
            Cafeina does not share data with third parties because it does not
            collect or transmit personal data.
          </p>

          <h2>Contact</h2>
          <p>
            Questions about this policy or Cafeina:
            <a href="mailto:support@nexxus-tech.com">support@nexxus-tech.com</a>
          </p>

          <h2>Disclaimer</h2>
          <p>
            Cafeina is not affiliated with Caffeine or any similarly named apps.
          </p>

          <p class="back-link">
            <RouterLink to="/cafeina">← Back to Cafeina</RouterLink>
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
  min-height: 32vh;
  display: flex;
  align-items: center;
  background: var(--nt-dark);
  padding: 120px 0 48px;
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
  font-size: clamp(2rem, 4.5vw, 2.8rem);
  margin-top: 8px;
}
.page-hero-subtitle {
  font-size: 1rem;
  color: var(--nt-text-muted);
  margin-top: 12px;
}

.privacy-body {
  padding: 48px 0 100px;
  background: var(--nt-dark-2);
  border-top: 1px solid var(--nt-border);
}
.privacy-inner { max-width: 720px; }
.privacy-prose h2 {
  font-size: 1.2rem;
  margin: 28px 0 10px;
}
.privacy-prose p {
  color: var(--nt-text-muted);
  line-height: 1.8;
  margin-bottom: 12px;
}
.privacy-prose .lede {
  color: var(--nt-text);
  font-size: 1.08rem;
  font-weight: 600;
  line-height: 1.7;
  margin-bottom: 8px;
  padding: 18px 20px;
  border-left: 3px solid var(--nt-primary);
  background: rgba(0, 123, 167, 0.08);
}
.privacy-prose a {
  color: var(--nt-secondary);
  font-weight: 600;
}
.privacy-prose a:hover { text-decoration: underline; }
.back-link {
  margin-top: 36px !important;
  padding-top: 24px;
  border-top: 1px solid var(--nt-border);
}
</style>
