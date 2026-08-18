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
            tagline="AI-assisted appliance management"
            class="hero-brand reveal"
          />
          <h2 class="hero-title reveal">Operate NetScaler, Cisco, and F5 with confidence</h2>
          <p class="hero-description reveal">
            JPilot connects your appliance inventory to your own AI provider keys — so your team can plan, configure, and troubleshoot with vendor-aware tools, not generic chat.
          </p>
          <p class="hero-subline reveal reveal-delay-1">
            Free edition. Bring your own AI keys. Credentials never leave your network.
          </p>
          <div class="hero-stats reveal reveal-delay-1">
            <div v-for="stat in heroStats" :key="stat.label" class="hero-stat">
              <span class="hero-stat-value">{{ stat.value }}</span>
              <span class="hero-stat-label">{{ stat.label }}</span>
            </div>
          </div>
          <div class="hero-actions reveal reveal-delay-1">
            <GlowButton v-if="!registered" variant="primary">
              <a href="#register" class="btn btn-primary">Register for access</a>
            </GlowButton>
            <GlowButton v-else variant="primary">
              <a href="https://jpilot.nexxus-tech.com" class="btn btn-primary">Open JPilot</a>
            </GlowButton>
            <GlowButton variant="secondary">
              <a :href="registered ? '#install' : '#register'" class="btn btn-secondary">
                {{ registered ? 'Install JPilot' : 'Get install access' }}
              </a>
            </GlowButton>
          </div>
        </div>

        <div class="hero-video reveal reveal-delay-2">
          <DemoVideo name="install" variant="hero" :lazy="false" />
        </div>

        <div v-if="registered" id="install" class="hero-install reveal reveal-delay-3">
          <InstallBlock copy-id="hero" />
        </div>
      </div>
    </section>

    <!-- Early Access -->
    <section class="early-access-section section-light">
      <div class="container early-access-inner reveal">
        <h2>Early adopters get a free license</h2>
        <p>
          The Free edition lets your team explore JPilot with your own AI provider keys, on your own infrastructure. Install during Early Access and we'll issue a free license under our Terms of Use.
        </p>
        <RouterLink to="/legal" class="early-access-terms-link">Read the Terms of Use</RouterLink>
      </div>
    </section>

    <!-- Section 1 -->
    <section class="feature-section section-light">
      <div class="container feature-grid">
        <div class="feature-copy reveal">
          <span class="feature-badge">Operations</span>
          <h2>From design to execution</h2>
          <p>
            Start in Architect for structured discovery and formal design documents, then hand off to Operator for implementation — without leaving the conversation.
          </p>
          <ul class="feature-list">
            <li>Guided jpilot-form blocks for load balancers and policies</li>
            <li>Send to Operator from design deliverables in one click</li>
            <li>Memory-guided RAG gates API and CLI usage before execution</li>
          </ul>
        </div>
        <div class="feature-media reveal reveal-delay-1">
          <FeatureZoomImage
            src="/jpilot/feature-operations.png"
            alt="JPilot design-to-execution workflow"
            :width="720"
            :height="480"
          />
        </div>
      </div>
    </section>

    <!-- Section 2 -->
    <section class="feature-section">
      <div class="container feature-grid feature-grid--reverse">
        <div class="feature-copy reveal">
          <span class="feature-badge">Reliability</span>
          <h2>Troubleshoot with context</h2>
          <p>
            Analyst mode stays read-first while diagnostics, official documentation search, and appliance telemetry keep investigations grounded in your environment.
          </p>
          <ul class="feature-list">
            <li>NetScaler ping, traceroute, port checks, and nsconmsg collection</li>
            <li>Brave Search limited to vendor official domains per platform</li>
            <li>Dual-pane chat with model-aware context usage rings</li>
          </ul>
        </div>
        <div class="feature-media reveal reveal-delay-1">
          <FeatureZoomImage
            src="/jpilot/feature-reliability.png"
            alt="JPilot troubleshooting and diagnostics"
            :width="720"
            :height="480"
          />
        </div>
      </div>
    </section>

    <!-- Section 3 -->
    <section class="feature-section section-light">
      <div class="container feature-grid">
        <div class="feature-copy reveal">
          <h2>Your keys, your infrastructure</h2>
          <p>
            Point JPilot at a local model (LM Studio) or your enterprise LLM (Azure OpenAI, AWS Bedrock, private endpoints). Traffic and appliance context stay inside your infrastructure — not a shared SaaS pool. You choose the provider and pay for inference.
          </p>
        </div>
        <div class="feature-media reveal reveal-delay-1">
          <FeatureZoomImage
            src="/jpilot/feature-isolation.png"
            alt="JPilot enterprise isolation — credentials stay on your infrastructure"
            :width="720"
            :height="480"
          />
        </div>
      </div>
    </section>

    <!-- Section 4 -->
    <section class="feature-section">
      <div class="container feature-grid feature-grid--reverse">
        <div class="feature-copy reveal">
          <h2>Built on MCP</h2>
          <p>
            The copilot runs on a Model Context Protocol server with tools for the Next-Gen API, classic CLI over SSH, NITRO helpers, diagnostics, and SSL CSR generation. Architect, Operator, and Analyst workflows are shaped by NetScaler, Cisco, and F5 SME practice — plus recommended actions in the command menu.
          </p>
        </div>
        <div class="feature-media reveal reveal-delay-1">
          <FeatureZoomImage
            src="/jpilot/feature-mcp.png"
            alt="JPilot MCP server connecting the copilot to appliance tools"
            :width="720"
            :height="420"
          />
        </div>
      </div>
    </section>

    <!-- Supported Platforms -->
    <section class="platforms-section section-light">
      <div class="container platforms-inner">
        <div class="platforms-header reveal">
          <h2>Supported platforms</h2>
          <p>Register NetScaler ADC, SDX, Cisco IOS/XE, and F5 BIG-IP — one inventory, native CLI and API for each vendor.</p>
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

    <!-- Registration CTA -->
    <section id="register" class="cta-section">
      <div class="container cta-inner reveal">
        <template v-if="!registered">
          <h2>Register for JPilot access</h2>
          <p>Leave your details to unlock the install command and continue to the platform.</p>
          <JpilotRegisterForm class="cta-form" @registered="onRegistered" />
        </template>
        <template v-else>
          <h2>You're registered</h2>
          <p>Install JPilot with one command, then continue to the platform.</p>
          <div class="cta-install">
            <InstallBlock copy-id="footer" />
          </div>
        </template>
        <div class="cta-actions">
          <GlowButton v-if="registered" variant="primary">
            <a href="https://jpilot.nexxus-tech.com" class="btn btn-primary">Open JPilot</a>
          </GlowButton>
          <GlowButton variant="secondary">
            <router-link to="/book-demo" class="btn btn-secondary">Book a demo</router-link>
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
          JPilot is an independent product by Nexxus-Tech SAS. It is not affiliated with, endorsed by, sponsored by, or certified by Cloud Software Group (Citrix / NetScaler), Cisco Systems, F5 Networks, or their affiliates. NetScaler, Citrix, Cisco, F5 BIG-IP, and related names are trademarks of their respective owners and are used here only for identification and interoperability.
        </p>
      </div>
    </section>

    <!-- ConneXt -->
    <section id="connext" class="cafeina-teaser-section">
      <div class="container cafeina-teaser reveal">
        <span class="section-label">iOS &amp; iPadOS</span>
        <h2>ConneXt</h2>
        <p>
          A free native SSH terminal for iPhone and iPad. Liquid Glass navigation,
          split terminals, reusable imported keys, and an optional Command Assistant.
          No subscription. No in-app purchases.
        </p>
        <div class="cafeina-teaser-actions">
          <RouterLink to="/connext" class="btn btn-primary">Learn more</RouterLink>
          <RouterLink to="/connext/privacy" class="btn btn-secondary">Privacy Policy</RouterLink>
          <RouterLink to="/connext/support" class="btn btn-outline">Support</RouterLink>
        </div>
      </div>
    </section>

    <!-- Cafeina -->
    <section id="cafeina" class="cafeina-teaser-section">
      <div class="container cafeina-teaser reveal">
        <span class="section-label">Also available</span>
        <h2>Cafeina</h2>
        <p>
          A personal macOS menu bar utility that keeps your Mac awake while enabled.
          Runs locally — no personal data collection. Requires macOS 13 or later.
        </p>
        <div class="cafeina-teaser-actions">
          <RouterLink to="/cafeina" class="btn btn-primary">Learn more</RouterLink>
          <RouterLink to="/cafeina/privacy" class="btn btn-secondary">Privacy Policy</RouterLink>
          <a
            href="https://github.com/juandiab/Cafeina"
            class="btn btn-outline"
            target="_blank"
            rel="noopener noreferrer"
          >GitHub</a>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import InstallBlock from '@/components/shared/InstallBlock.vue'
import DemoVideo from '@/components/shared/DemoVideo.vue'
import JpilotLogo from '@/components/shared/JpilotLogo.vue'
import JpilotRegisterForm from '@/components/shared/JpilotRegisterForm.vue'
import Strands from '@/components/shared/Strands.vue'
import MagicRings from '@/components/shared/MagicRings.vue'
import GlowButton from '@/components/shared/GlowButton.vue'
import FeatureZoomImage from '@/components/shared/FeatureZoomImage.vue'
import { isJpilotRegistered, markJpilotRegistered } from '@/utils/jpilotRegistration.js'

const JPILOT_REDIRECT = 'https://jpilot.nexxus-tech.com'

/** Toggle hero background effects — flip to show Strands instead of MagicRings later. */
const HERO_BG_STRANDS = false
const HERO_BG_MAGIC_RINGS = true
const registered = ref(false)

onMounted(() => {
  registered.value = isJpilotRegistered()
})

function onRegistered(email) {
  markJpilotRegistered(email)
  registered.value = true
  window.setTimeout(() => {
    window.location.assign(JPILOT_REDIRECT)
  }, 800)
}

const heroStats = [
  { value: '4', label: 'Vendor platforms' },
  { value: 'BYOK', label: 'Your AI keys' },
  { value: 'MCP', label: 'Tool-calling agent' },
]

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
  margin: 0 0 18px;
}

.hero-title {
  margin: 0 0 12px;
  max-width: 36rem;
  font-size: clamp(1.35rem, 2.6vw, 1.85rem);
  font-weight: 800;
  line-height: 1.25;
}

.hero-stats {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 18px 28px;
  margin: 20px 0 0;
}

.hero-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 88px;
}

.hero-stat-value {
  font-family: var(--font-heading);
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--nt-primary-l);
}

.hero-stat-label {
  font-size: 0.75rem;
  color: var(--nt-text-muted);
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
  margin-top: 22px;
}

.hero-video {
  width: 100%;
  max-width: 720px;
  margin: 8px auto 28px;
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

.feature-badge {
  display: inline-block;
  margin-bottom: 10px;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--nt-primary);
  font-family: var(--font-heading);
}

.feature-list {
  margin: 16px 0 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.feature-list li {
  position: relative;
  padding-left: 1.2rem;
  font-size: 0.92rem;
  line-height: 1.55;
  color: var(--nt-text-muted);
}

.feature-list li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.55em;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--nt-primary-l);
}

.section-light .feature-list li {
  color: #4a5568;
}

.feature-media :deep(.feature-zoom-trigger) {
  width: 100%;
  height: 100%;
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
  align-items: stretch;
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
  display: flex;
  flex-direction: column;
  justify-content: center;
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
  justify-self: stretch;
  display: flex;
  align-self: stretch;
  min-height: 0;
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
  scroll-margin-top: 96px;
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

.cta-form,
.cta-install {
  max-width: 640px;
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

.cafeina-teaser-section {
  padding: 64px 0 88px;
  border-top: 1px solid var(--nt-border);
  background: var(--nt-dark-2);
}
.cafeina-teaser {
  max-width: 720px;
  text-align: center;
}
.cafeina-teaser h2 {
  font-size: clamp(1.6rem, 3vw, 2rem);
  margin: 10px 0 14px;
}
.cafeina-teaser p {
  color: var(--nt-text-muted);
  line-height: 1.75;
  margin-bottom: 24px;
}
.cafeina-teaser-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
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

  .feature-media {
    height: 240px;
    min-height: 240px;
  }

}

@media (max-width: 767px) {
  .hero {
    padding: 96px 0 40px;
  }

  .hero-brand {
    margin-bottom: 16px;
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

  .cafeina-teaser-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .cafeina-teaser-actions .btn {
    justify-content: center;
  }
}
</style>
