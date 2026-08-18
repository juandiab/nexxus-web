<template>
  <div class="support-page">
    <section class="page-hero">
      <div class="page-hero-bg"></div>
      <div class="container page-hero-content">
        <span class="section-label reveal">ConneXt</span>
        <h1 class="reveal reveal-delay-1">ConneXt Support</h1>
        <p class="page-hero-subtitle reveal reveal-delay-2">
          How to get help with the free native SSH terminal for iPhone and iPad.
        </p>
      </div>
    </section>

    <section class="section support-body">
      <div class="container support-inner">
        <article class="support-card reveal">
          <h2>What ConneXt is</h2>
          <p>
            ConneXt is a free native SSH client for iPhone and iPad by
            Juan Pablo Otalvaro (Nexxus-Tech). Liquid Glass navigation, split
            terminals, reusable imported keys, and an optional Command Assistant
            that uses your own OpenAI, Gemini, or Anthropic key. There is no
            subscription and no in-app purchase.
          </p>
        </article>

        <article class="support-card reveal reveal-delay-1">
          <h2>Requirements</h2>
          <ul class="support-list">
            <li>An iPhone or iPad running iOS or iPadOS</li>
            <li>A host you can reach over SSH (the servers you configure)</li>
            <li>Optional: your own API key if you enable Command Assistant</li>
          </ul>
        </article>

        <article class="support-card reveal reveal-delay-2">
          <h2>How to get help</h2>
          <p>
            Email
            <a href="mailto:support@nexxus-tech.com">support@nexxus-tech.com</a>
            with the device and iOS / iPadOS version, what you expected, and
            what happened. There are no ConneXt accounts — we cannot reset an
            app login because the app does not have one.
          </p>
          <ul class="support-links">
            <li>
              <a href="mailto:support@nexxus-tech.com">support@nexxus-tech.com</a>
            </li>
            <li>
              <RouterLink to="/connext">ConneXt product page</RouterLink>
            </li>
            <li>
              <RouterLink to="/connext/privacy">Privacy Policy</RouterLink>
            </li>
            <li>
              <RouterLink to="/">nexxus-tech.com</RouterLink>
            </li>
          </ul>
        </article>

        <article class="support-card reveal reveal-delay-3">
          <h2>Connection issues</h2>
          <p>
            Sessions go to the servers you add. If a host will not connect,
            check reachability from the device (VPN, firewall, DNS), the port,
            and that the imported key or password is the one that host expects.
            Nexxus-Tech does not proxy your SSH traffic.
          </p>
          <p class="copyright">
            © {{ year }} Nexxus-Tech / Juan Pablo Otalvaro. All rights reserved.
          </p>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup>
const year = new Date().getFullYear()
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
  max-width: 560px;
  line-height: 1.75;
}

.support-body {
  padding: 48px 0 100px;
  background: var(--nt-dark-2);
  border-top: 1px solid var(--nt-border);
}
.support-inner { max-width: 720px; }
.support-card {
  padding: 28px 0;
  border-bottom: 1px solid var(--nt-border);
}
.support-card:last-child { border-bottom: none; }
.support-card h2 {
  font-size: 1.2rem;
  margin-bottom: 12px;
}
.support-card p {
  color: var(--nt-text-muted);
  line-height: 1.8;
  margin-bottom: 14px;
}
.support-list,
.support-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 8px;
}
.support-list li {
  color: var(--nt-text-muted);
  padding-left: 18px;
  position: relative;
  line-height: 1.6;
}
.support-list li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.65em;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--nt-primary);
}
.support-links a {
  color: var(--nt-secondary);
  font-weight: 600;
}
.support-links a:hover { text-decoration: underline; }
.copyright {
  margin-top: 20px;
  font-size: 0.85rem;
  color: #94a3b8;
}
</style>
