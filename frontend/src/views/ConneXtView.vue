<template>
  <div class="connext-page">
    <section class="page-hero">
      <div class="page-hero-bg"></div>
      <div class="container page-hero-content">
        <span class="section-label reveal">Native SSH terminal · iOS &amp; iPadOS</span>
        <h1 class="reveal reveal-delay-1">ConneXt</h1>
        <p class="page-hero-subtitle reveal reveal-delay-2">
          A native, beautiful SSH client for iPhone and iPad — Liquid Glass
          navigation, split terminals, reusable imported keys, and an optional
          Command Assistant. <strong>Free.</strong> No subscription. No in-app purchases.
        </p>
        <div class="hero-actions reveal reveal-delay-3">
          <a
            :href="product.appStoreUrl"
            class="btn btn-primary"
            target="_blank"
            rel="noopener noreferrer"
          >
            <i class="pi pi-apple"></i> Free on the App Store
          </a>
          <RouterLink to="/connext/support" class="btn btn-secondary">Support</RouterLink>
          <RouterLink to="/connext/privacy" class="btn btn-outline">Privacy Policy</RouterLink>
        </div>
      </div>
    </section>

    <section class="section connext-body">
      <div class="container connext-inner">
        <article class="connext-card reveal">
          <h2>What it is</h2>
          <p>
            ConneXt is a native SSH terminal for iPhone and iPad, created by
            Juan Pablo Otalvaro at Nexxus-Tech. It is built for the people who
            already live in a shell — not a generic chat wrapper dressed as a
            terminal.
          </p>
          <ul class="connext-list">
            <li>Free on the App Store — no subscription, no in-app purchases</li>
            <li>Native iOS / iPadOS app with Liquid Glass navigation</li>
            <li>No ConneXt accounts. Credentials stay on your device.</li>
          </ul>
        </article>

        <article class="connext-card reveal reveal-delay-1">
          <h2>Who it’s for</h2>
          <p>
            Network engineers, SREs, and anyone who needs a serious SSH client
            on iPhone or iPad — sessions you can actually work in, keys you
            import once and reuse, and an optional assistant only if you want it.
          </p>
          <ul class="connext-list">
            <li>Operators who jump on a host from a phone or iPad</li>
            <li>Engineers who keep imported keys in the iOS Keychain</li>
            <li>Anyone who wants a native client without a paywall</li>
          </ul>
        </article>
      </div>
    </section>

    <section class="section features-section">
      <div class="container">
        <div class="section-header-center reveal">
          <span class="section-label">Capabilities</span>
          <h2 class="section-title">What ConneXt does</h2>
          <p class="section-subtitle section-subtitle-center">
            The parts that matter on a phone or iPad — not a feature list for its own sake.
          </p>
        </div>
        <div class="grid-3 feature-grid">
          <article
            v-for="(feature, i) in features"
            :key="feature.title"
            class="card reveal"
            :class="`reveal-delay-${(i % 3) + 1}`"
          >
            <div class="feature-icon" aria-hidden="true">
              <i :class="feature.icon"></i>
            </div>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.body }}</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section shots-section">
      <div class="container">
        <div class="section-header-center reveal">
          <span class="section-label">Screenshots</span>
          <h2 class="section-title">On iPhone and iPad</h2>
          <p class="section-subtitle section-subtitle-center">
            App Store screenshots will land here. These frames mark the views we ship.
          </p>
        </div>
        <div class="shots-grid">
          <figure
            v-for="(shot, i) in shots"
            :key="shot.title"
            class="shot-frame reveal"
            :class="`reveal-delay-${(i % 4) + 1}`"
          >
            <div class="shot-screen" :aria-label="`${shot.title} screenshot placeholder`">
              <span class="shot-chrome">{{ shot.chrome }}</span>
              <pre class="shot-term">{{ shot.term }}<span class="ld-cursor"></span></pre>
            </div>
            <figcaption>{{ shot.title }}</figcaption>
          </figure>
        </div>
      </div>
    </section>

    <section class="section cta-section">
      <div class="container">
        <div class="cta-box reveal">
          <span class="section-label">Get ConneXt</span>
          <h2>Free on the App Store</h2>
          <p>
            No trial. No upgrade path. Download ConneXt and connect to the
            servers you configure.
          </p>
          <div class="cta-actions">
            <a
              :href="product.appStoreUrl"
              class="btn btn-primary"
              target="_blank"
              rel="noopener noreferrer"
            >
              <i class="pi pi-apple"></i> Free on the App Store
            </a>
            <RouterLink to="/connext/support" class="btn btn-outline">Get support</RouterLink>
          </div>
        </div>
      </div>
    </section>

    <section class="section author-section">
      <div class="container author-inner reveal">
        <p class="author-line">
          <strong>Juan Pablo Otalvaro</strong>
          ·
          <RouterLink to="/">Nexxus-Tech</RouterLink>
        </p>
        <p class="copyright">
          © {{ year }} Nexxus-Tech / Juan Pablo Otalvaro. All rights reserved.
        </p>
        <p class="disclaimer">{{ product.disclaimer }}</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { products } from '@/data/products.js'

const product = products.find((p) => p.id === 'connext')
const year = new Date().getFullYear()

const features = [
  {
    icon: 'pi pi-mobile',
    title: 'Liquid Glass navigation',
    body: 'A native iOS / iPadOS shell — not a web view. Navigation follows Apple’s Liquid Glass language so the terminal stays the focus.',
  },
  {
    icon: 'pi pi-clone',
    title: 'Split terminals',
    body: 'Open more than one session on screen. Built for iPad space and for the times a phone has to do two jobs at once.',
  },
  {
    icon: 'pi pi-key',
    title: 'Reusable imported keys',
    body: 'Import keys once. Reuse them across hosts. Private keys stay in the iOS Keychain on your device.',
  },
  {
    icon: 'pi pi-comments',
    title: 'Optional Command Assistant',
    body: 'Bring your own OpenAI, Gemini, or Anthropic key when you want help drafting a command. Off unless you enable it.',
  },
  {
    icon: 'pi pi-lock',
    title: 'On-device credentials',
    body: 'No ConneXt account. SSH passwords and keys never leave the device Keychain. Connections go only to hosts you add.',
  },
  {
    icon: 'pi pi-heart',
    title: 'Free. No IAP.',
    body: 'The app is free. There is no subscription and nothing behind a paywall — including the Command Assistant, which uses your keys.',
  },
]

const shots = [
  {
    title: 'Sessions',
    chrome: 'ConneXt · Sessions',
    term: 'nexxus@edge-01 ~ % ssh prod-lb\nconnected.\n#',
  },
  {
    title: 'Split terminals',
    chrome: 'ConneXt · Split',
    term: 'left  nsconmsg -d current\nright show ns running',
  },
  {
    title: 'Imported keys',
    chrome: 'ConneXt · Keys',
    term: 'id_ed25519  ·  Keychain\nid_work      ·  Keychain',
  },
  {
    title: 'Command Assistant',
    chrome: 'ConneXt · Assistant',
    term: 'You: check SSL vserver bind\n→ show ssl vserver',
  },
]
</script>

<style scoped>
.page-hero {
  min-height: 48vh;
  display: flex;
  align-items: center;
  background: var(--nt-dark);
  padding: 120px 0 64px;
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
  max-width: 600px;
  line-height: 1.75;
}
.page-hero-subtitle strong { color: var(--nt-white); }
.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 28px;
}

.connext-body {
  padding: 64px 0 40px;
  background: var(--nt-dark-2);
  border-top: 1px solid var(--nt-border);
}
.connext-inner {
  display: grid;
  gap: 8px;
  max-width: 820px;
}
.connext-card {
  padding: 28px 0;
  border-bottom: 1px solid var(--nt-border);
}
.connext-card:last-child { border-bottom: none; }
.connext-card h2 {
  font-size: 1.35rem;
  margin-bottom: 12px;
}
.connext-card p {
  color: var(--nt-text-muted);
  line-height: 1.75;
  margin-bottom: 14px;
}
.connext-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 8px;
}
.connext-list li {
  color: var(--nt-text-muted);
  padding-left: 18px;
  position: relative;
  line-height: 1.6;
}
.connext-list li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.65em;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--nt-primary);
}

.features-section { background: var(--nt-dark); }
.feature-grid { margin-top: 40px; }
.feature-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  background: rgba(0, 123, 167, 0.18);
  color: var(--nt-primary-l);
  font-size: 1.2rem;
}
.features-section h3 {
  font-size: 1.15rem;
  margin-bottom: 10px;
}
.features-section .card p {
  color: var(--nt-text-muted);
  font-size: 0.95rem;
  line-height: 1.7;
}

.shots-section {
  background: var(--nt-dark-2);
  border-top: 1px solid var(--nt-border);
}
.shots-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-top: 40px;
}
.shot-frame { margin: 0; }
.shot-screen {
  aspect-ratio: 9 / 16;
  border-radius: 20px;
  border: 1px solid var(--nt-border);
  background:
    linear-gradient(180deg, rgba(0, 123, 167, 0.12), transparent 40%),
    var(--nt-dark-3);
  padding: 18px 14px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.shot-chrome {
  font-family: var(--font-heading);
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--nt-secondary);
}
.shot-term {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.72rem;
  color: var(--nt-secondary-l);
  line-height: 1.6;
  white-space: pre-wrap;
  margin: 0;
}
.shot-frame figcaption {
  margin-top: 12px;
  text-align: center;
  font-size: 0.85rem;
  color: var(--nt-text-muted);
}

.cta-section { background: var(--nt-dark); }
.cta-box {
  background: var(--nt-dark-3);
  border: 1px solid var(--nt-border);
  border-radius: var(--nt-radius-lg);
  padding: 48px 32px;
  text-align: center;
}
.cta-box h2 { margin: 8px 0 12px; }
.cta-box p {
  color: var(--nt-text-muted);
  max-width: 520px;
  margin: 0 auto 24px;
}
.cta-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
}

.author-section {
  padding: 48px 0 80px;
  background: var(--nt-dark-2);
  border-top: 1px solid var(--nt-border);
}
.author-inner { max-width: 720px; text-align: center; }
.author-line {
  color: var(--nt-text);
  margin-bottom: 8px;
}
.copyright {
  color: var(--nt-text-muted);
  font-size: 0.9rem;
  margin-bottom: 16px;
}
.disclaimer {
  font-size: 0.78rem;
  color: #94a3b8;
  line-height: 1.65;
}

@media (max-width: 1024px) {
  .shots-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 640px) {
  .hero-actions,
  .cta-actions { flex-direction: column; align-items: stretch; }
  .hero-actions .btn,
  .cta-actions .btn { justify-content: center; }
  .shots-grid { grid-template-columns: 1fr 1fr; }
}
</style>
