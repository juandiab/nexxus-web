<template>
  <div id="jpilot" class="products-page">
    <!-- Hero -->
    <section class="hero">
      <div class="hero-bg" aria-hidden="true">
        <MagicRings
          v-if="HERO_BG_MAGIC_RINGS"
          class="hero-bg-layer"
          color="#00A8E0"
          color-two="#007BA7"
          :ring-count="6"
          :speed="0.75"
          :attenuation="11"
          :line-thickness="1.8"
          :base-radius="0.32"
          :radius-step="0.09"
          :scale-rate="0.09"
          :opacity="0.55"
          :noise-amount="0.06"
          :ring-gap="1.5"
          :fade-in="0.7"
          :fade-out="0.5"
        />
        <Strands
          v-if="HERO_BG_STRANDS"
          class="hero-bg-layer"
          :colors="['#00A8E0', '#007BA7', '#4DB8E0']"
          :count="3"
          :speed="0.45"
          :amplitude="0.85"
          :waviness="1"
          :thickness="0.65"
          :glow="2.2"
          :taper="3"
          :spread="1"
          :intensity="0.55"
          :saturation="1.3"
          :opacity="0.85"
          :scale="1.4"
        />
      </div>
      <div class="container hero-inner">
        <div class="hero-lockup">
          <p class="hero-eyebrow reveal">Introducing</p>
          <JpilotLogo
            variant="hero"
            tagline="AI Copilot for Network Appliances"
            class="hero-brand reveal"
          />
          <p class="hero-description reveal">
            JPilot is an AI management platform for your network appliances — chat to plan, configure, and troubleshoot your ADCs and network infrastructure, all running on hardware you control.
          </p>
          <p class="hero-subline reveal reveal-delay-1">
            Free edition. Bring your own AI keys. Your credentials never leave your network.
          </p>
        </div>

        <div id="install" class="hero-install reveal reveal-delay-2">
          <InstallBlock copy-id="hero" />
        </div>

        <div class="hero-video reveal reveal-delay-3">
          <DemoVideo name="install" variant="hero" :lazy="false" />
        </div>
      </div>
    </section>

    <!-- Early Access -->
    <section class="early-access-section section-light">
      <div class="container early-access-inner reveal">
        <h2>Early adopters get a free license</h2>
        <p>
          Install JPilot during Early Access and we'll issue you a free license under our Terms of Use. Bring your own AI keys, run it on your own infrastructure — no cost during Early Access. It's our thank-you for trying JPilot early and helping shape it.
        </p>
        <RouterLink to="/legal" class="early-access-terms-link">Read the Terms of Use</RouterLink>
      </div>
    </section>

    <!-- Section 1 -->
    <section class="feature-section section-light">
      <div class="container feature-grid">
        <div class="feature-copy reveal">
          <h2>Talk to your appliances in plain language</h2>
          <p>
            Ask JPilot to check a vServer's health, trace an nFactor flow, or explain why a policy isn't binding. It knows the CLI, the Next-Gen API, and the diagnostics — across NetScaler, F5 BIG-IP, and Cisco IOS/XE — so you don't have to remember every command.
          </p>
        </div>
        <div class="feature-media reveal reveal-delay-1">
          <DemoVideo name="section-chat" />
        </div>
      </div>
    </section>

    <!-- Section 2 -->
    <section class="feature-section">
      <div class="container feature-grid feature-grid--reverse">
        <div class="feature-copy reveal">
          <h2>Architect, Operator, Analyst</h2>
          <p>
            Three roles, one platform. Architect plans designs and produces formal docs. Operator makes the changes on the appliance. Analyst troubleshoots read-first. Hand off a design straight to Operator with one click.
          </p>
        </div>
        <div class="feature-media reveal reveal-delay-1">
          <DemoVideo name="section-roles" />
        </div>
      </div>
    </section>

    <!-- Section 3 -->
    <section class="feature-section section-light">
      <div class="container feature-grid">
        <div class="feature-copy reveal">
          <h2>Your keys, your data, your hardware</h2>
          <p>
            JPilot is self-hosted Docker. Bring your own AI provider — OpenAI, Anthropic, Gemini, Bedrock, or a local LM Studio model. Appliance credentials are encrypted at rest with Fernet and are never sent to the LLM. Nexxus-Tech never sees your traffic or pays for your inference.
          </p>
        </div>
        <div class="feature-media reveal reveal-delay-1">
          <DemoVideo name="section-providers" />
        </div>
      </div>
    </section>

    <!-- Section 4 -->
    <section class="feature-section">
      <div class="container feature-grid feature-grid--reverse">
        <div class="feature-copy reveal">
          <h2>Built on MCP</h2>
          <p>
            The copilot runs on a Model Context Protocol server with tools for the Next-Gen API, classic CLI over SSH, diagnostics, and SSL/CSR generation. Each vendor's knowledge lives in editable memory files — yours to audit and extend.
          </p>
        </div>
        <div class="feature-media reveal reveal-delay-1">
          <DemoVideo name="section-mcp" />
        </div>
      </div>
    </section>

    <!-- Supported Platforms -->
    <section class="platforms-section section-light">
      <div class="container platforms-inner">
        <div class="platforms-header reveal">
          <h2>Supported platforms</h2>
          <p>JPilot speaks each vendor's native CLI and API. More vendors are on the way.</p>
        </div>
        <ul class="platforms-grid reveal reveal-delay-1">
          <li v-for="vendor in supportedVendors" :key="vendor.name" class="platform-card">
            <span class="platform-name">{{ vendor.name }}</span>
            <span
              class="platform-badge"
              :class="vendor.status === 'available' ? 'platform-badge--available' : 'platform-badge--beta'"
            >
              {{ vendor.status === 'available' ? 'Available' : 'Beta' }}
            </span>
          </li>
        </ul>
        <p class="platforms-footnote reveal reveal-delay-2">More vendors coming soon.</p>
      </div>
    </section>

    <!-- Bottom CTA -->
    <section class="cta-section">
      <div class="container cta-inner reveal">
        <h2>Get started</h2>
        <p>One command. Self-hosted. Your infrastructure.</p>
        <InstallBlock copy-id="footer" />
        <div class="cta-actions">
          <GlowButton variant="primary">
            <a href="#install" class="btn btn-primary">Install now</a>
          </GlowButton>
          <GlowButton variant="secondary">
            <router-link to="/book-demo" class="btn btn-secondary">Book a demo</router-link>
          </GlowButton>
          <GlowButton variant="secondary">
            <a href="mailto:support@nexxus-tech.com" class="btn btn-secondary">Contact us</a>
          </GlowButton>
        </div>
      </div>
    </section>

    <!-- Disclaimer -->
    <section class="disclaimer-section">
      <div class="container">
        <p class="product-support reveal">
          Questions or need help? Email
          <a href="mailto:support@nexxus-tech.com">support@nexxus-tech.com</a>
        </p>
        <p class="product-disclaimer reveal">
          Not affiliated with, endorsed by, or sponsored by Citrix, F5, or Cisco. All trademarks belong to their owners.
        </p>
      </div>
    </section>
  </div>
</template>

<script setup>
import InstallBlock from '@/components/shared/InstallBlock.vue'
import DemoVideo from '@/components/shared/DemoVideo.vue'
import JpilotLogo from '@/components/shared/JpilotLogo.vue'
import Strands from '@/components/shared/Strands.vue'
import MagicRings from '@/components/shared/MagicRings.vue'
import GlowButton from '@/components/shared/GlowButton.vue'

/** Toggle hero background effects — flip to show Strands instead of MagicRings later. */
const HERO_BG_STRANDS = false
const HERO_BG_MAGIC_RINGS = true

const supportedVendors = [
  { name: 'NetScaler MPX', status: 'available' },
  { name: 'NetScaler VPX', status: 'available' },
  { name: 'NetScaler SDX', status: 'beta' },
  { name: 'F5 BIG-IP', status: 'beta' },
  { name: 'Cisco IOS', status: 'beta' },
]
</script>

<style scoped>
.products-page {
  background: var(--nt-dark);
  overflow-x: hidden;
}

/* ── Hero ─────────────────────────────────────────────────────────────────── */
.hero {
  position: relative;
  padding: 100px 0 48px;
  overflow: hidden;
}

.hero-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0.95;
  background:
    radial-gradient(ellipse at 50% 0%, rgba(0, 168, 224, 0.1) 0%, transparent 55%),
    radial-gradient(ellipse at 80% 60%, rgba(0, 123, 167, 0.05) 0%, transparent 45%);
}

.hero-bg-layer {
  position: absolute;
  inset: 0;
}

.hero-inner {
  position: relative;
  z-index: 1;
  max-width: 820px;
  margin: 0 auto;
  text-align: center;
}

.hero-lockup {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 24px;
}

.hero-brand {
  margin: 0 0 22px;
}

.hero-eyebrow {
  margin: 0 0 6px;
  font-family: var(--font-heading);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--nt-text-muted);
}

.hero-description {
  margin: 0 0 10px;
  max-width: 38rem;
  font-size: clamp(0.95rem, 1.8vw, 1.1rem);
  font-weight: 400;
  line-height: 1.65;
  color: var(--nt-text-muted);
}

.hero-subline {
  margin: 0;
  font-size: 0.9rem;
  color: var(--nt-text-muted);
  line-height: 1.65;
}

.hero-install {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}

.hero-video {
  width: 100%;
  max-width: 720px;
  margin: 0 auto;
}

/* ── Early Access ─────────────────────────────────────────────────────────── */
.early-access-section {
  padding: clamp(40px, 6vh, 56px) 0;
  border-bottom: 1px solid rgba(0, 123, 167, 0.12);
}

.early-access-inner {
  max-width: 720px;
  margin: 0 auto;
  text-align: center;
}

.early-access-inner h2 {
  font-size: clamp(1.25rem, 2.4vw, 1.6rem);
  font-weight: 800;
  margin-bottom: 12px;
  line-height: 1.3;
}

.early-access-inner p {
  font-size: clamp(0.92rem, 1.5vw, 1rem);
  line-height: 1.75;
  color: #4a5568;
  margin-bottom: 10px;
}

.early-access-terms-link {
  display: inline-block;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--nt-primary);
  text-decoration: none;
}

.early-access-terms-link:hover {
  color: var(--nt-primary-l);
  text-decoration: underline;
}

/* ── Feature sections ─────────────────────────────────────────────────────── */
.feature-section {
  padding: clamp(48px, 7vh, 72px) 0;
}

.feature-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: clamp(28px, 4vw, 48px);
  align-items: center;
  max-width: 1080px;
  margin: 0 auto;
}

.feature-grid--reverse .feature-copy {
  order: 2;
}

.feature-grid--reverse .feature-media {
  order: 1;
}

.feature-copy {
  max-width: 34rem;
}

.feature-copy h2 {
  font-size: clamp(1.5rem, 2.8vw, 2rem);
  font-weight: 800;
  margin-bottom: 16px;
  line-height: 1.25;
}

.feature-copy p {
  font-size: clamp(0.95rem, 1.6vw, 1.05rem);
  line-height: 1.75;
  color: var(--nt-text-muted);
}

.feature-media {
  width: 100%;
  max-width: 720px;
  justify-self: center;
}

.section-light .feature-copy p {
  color: #4a5568;
}

/* ── Supported Platforms ──────────────────────────────────────────────────── */
.platforms-section {
  padding: clamp(48px, 7vh, 72px) 0;
}

.platforms-inner {
  max-width: 820px;
  margin: 0 auto;
}

.platforms-header {
  text-align: center;
  margin-bottom: 36px;
}

.platforms-header h2 {
  font-size: clamp(1.5rem, 2.8vw, 2rem);
  font-weight: 800;
  margin-bottom: 12px;
  line-height: 1.25;
}

.platforms-header p {
  font-size: clamp(0.95rem, 1.6vw, 1.05rem);
  line-height: 1.75;
  color: #4a5568;
}

.platforms-grid {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 12px;
}

.platform-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 10px;
  border: 1px solid rgba(0, 123, 167, 0.15);
  background: rgba(255, 255, 255, 0.65);
}

.platform-name {
  font-size: 0.9rem;
  font-weight: 700;
  color: #1e293b;
}

.platform-badge {
  flex-shrink: 0;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  font-family: var(--font-heading);
}

.platform-badge--available {
  background: color-mix(in srgb, var(--p-green-500, #22c55e) 18%, transparent);
  color: var(--p-green-600, #16a34a);
  border: 1px solid color-mix(in srgb, var(--p-green-500, #22c55e) 35%, transparent);
}

.platform-badge--beta {
  background: color-mix(in srgb, var(--p-yellow-500, #eab308) 20%, transparent);
  color: var(--p-yellow-700, #a16207);
  border: 1px solid color-mix(in srgb, var(--p-yellow-500, #eab308) 38%, transparent);
}

.platforms-footnote {
  margin-top: 20px;
  text-align: center;
  font-size: 0.85rem;
  color: #94a3b8;
}

/* ── CTA ──────────────────────────────────────────────────────────────────── */
.cta-section {
  padding: clamp(48px, 7vh, 72px) 0;
  border-top: 1px solid rgba(0, 123, 167, 0.15);
}

.cta-inner {
  max-width: 720px;
  margin: 0 auto;
  text-align: center;
}

.cta-inner h2 {
  font-size: clamp(1.6rem, 3vw, 2.2rem);
  margin-bottom: 8px;
}

.cta-inner > p {
  color: var(--nt-text-muted);
  margin-bottom: 28px;
  font-size: 0.95rem;
}

.cta-inner :deep(.install-block) {
  margin: 0 auto 28px;
}

.cta-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
}

/* ── Disclaimer ───────────────────────────────────────────────────────────── */
.disclaimer-section {
  padding: 0 0 64px;
}

.product-support {
  max-width: 720px;
  margin: 0 auto 12px;
  font-size: 0.85rem;
  color: #cbd5e1;
  line-height: 1.65;
  text-align: center;
}

.product-support a {
  color: var(--nt-primary-l);
  text-decoration: none;
  font-weight: 600;
}

.product-support a:hover {
  text-decoration: underline;
}

.product-disclaimer {
  max-width: 720px;
  margin: 0 auto;
  font-size: 0.78rem;
  color: #94a3b8;
  line-height: 1.65;
  text-align: center;
}

/* ── Responsive ───────────────────────────────────────────────────────────── */
@media (max-width: 900px) {
  .feature-grid,
  .feature-grid--reverse {
    grid-template-columns: 1fr;
  }

  .feature-grid--reverse .feature-copy,
  .feature-grid--reverse .feature-media {
    order: unset;
  }

}

@media (max-width: 767px) {
  .hero {
    padding: 96px 0 40px;
  }

  .hero-brand {
    margin-bottom: 18px;
  }

  .hero-description {
    font-size: 0.92rem;
  }

  .hero-lockup {
    margin-bottom: 20px;
  }

  .hero-install {
    margin-bottom: 20px;
  }

  .cta-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .cta-actions .btn {
    justify-content: center;
  }
}
</style>
