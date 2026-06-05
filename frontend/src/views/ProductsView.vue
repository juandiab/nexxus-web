<template>
  <div class="products-page">
    <section class="page-hero">
      <div class="page-hero-bg"></div>
      <div class="container page-hero-content">
        <JpilotLogo
          theme="dark"
          :alt="products[0].logoAlt"
          img-class="product-hero-logo reveal"
        />
        <span class="section-label reveal reveal-delay-1">Our Products</span>
        <h1 class="reveal reveal-delay-1">{{ products[0].name }}</h1>
        <p class="page-hero-tagline reveal reveal-delay-2">{{ products[0].tagline }}</p>
        <p class="page-hero-subtitle reveal reveal-delay-3">
          Tools built by practitioners who believe the best solutions emerge when a
          community shares knowledge, experience, and inspiration.
        </p>
      </div>
    </section>

    <section
      v-for="product in products"
      :key="product.id"
      :id="product.id"
      class="product-block"
    >
      <!-- Overview -->
      <div class="section product-detail">
        <div class="container">
          <div class="product-detail-grid">
            <div class="product-detail-text reveal">
              <span class="section-label">Why JPilot exists</span>
              <h2 class="section-title">Technology That Empowers</h2>
              <p class="section-subtitle">{{ product.desc }}</p>
              <div class="product-tags">
                <span v-for="t in product.tags" :key="t" class="tag">{{ t }}</span>
                <span class="tag tag-teal">{{ product.version }}</span>
              </div>
              <div class="product-actions">
                <a
                  :href="product.links.github"
                  class="btn btn-primary"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <i class="pi pi-github"></i> View on GitHub
                </a>
                <a
                  :href="product.links.readme"
                  class="btn btn-outline"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <i class="pi pi-file"></i> Technical README
                </a>
                <RouterLink :to="product.links.blog" class="btn btn-outline">
                  <i class="pi pi-book"></i> Deep Dive Article
                </RouterLink>
                <RouterLink to="/contact" class="btn btn-outline">
                  <i class="pi pi-send"></i> Talk to Nexxus
                </RouterLink>
              </div>
            </div>
            <div class="product-detail-visual reveal reveal-delay-2">
              <div class="visual-card">
                <div class="visual-header" :style="{ background: product.iconBg }">
                  <JpilotLogo theme="dark" :alt="product.logoAlt" img-class="visual-logo" />
                </div>
                <div class="visual-metrics">
                  <div v-for="m in product.metrics" :key="m.label" class="metric">
                    <span class="metric-value">{{ m.value }}</span>
                    <span class="metric-label">{{ m.label }}</span>
                  </div>
                </div>
              </div>
              <p class="product-disclaimer">{{ product.disclaimer }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Vision principles (activation letter) -->
      <div class="section section-dark product-subsection">
        <div class="container">
          <div class="subsection-header reveal" style="text-align:center; margin: 0 auto 48px">
            <span class="section-label">Our Philosophy</span>
            <h3 class="subsection-title">What Guides Every Release</h3>
            <p class="subsection-desc" style="margin: 0 auto">
              The same principles behind our activation letter—for every engineer taking
              their first steps or their thousandth production change.
            </p>
          </div>
          <div class="vision-grid">
            <div
              v-for="principle in product.visionPrinciples"
              :key="principle.title"
              class="vision-card card reveal"
            >
              <h4>{{ principle.title }}</h4>
              <p>{{ principle.body }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Capabilities -->
      <div class="section section-light product-subsection">
        <div class="container capabilities-layout">
          <div class="capabilities-col reveal">
            <span class="section-label">What JPilot Does</span>
            <h3 class="subsection-title dark">Practical Help for Real Engineers</h3>
            <div class="capabilities-list">
              <div v-for="c in product.capabilities" :key="c" class="capability-item">
                <i class="pi pi-check-circle"></i>
                <span>{{ c }}</span>
              </div>
            </div>
          </div>
          <div class="capabilities-col reveal reveal-delay-2">
            <span class="section-label">JPilot Roles</span>
            <h3 class="subsection-title dark">Design · Operate · Analyze</h3>
            <div class="roles-stack">
              <div v-for="role in product.roles" :key="role.name" class="role-row">
                <div class="role-icon"><i :class="role.icon"></i></div>
                <div>
                  <strong>{{ role.name }}</strong>
                  <p>{{ role.desc }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Platforms -->
      <div class="section section-dark product-subsection">
        <div class="container">
          <div class="subsection-header reveal" style="text-align:center; margin: 0 auto 48px">
            <span class="section-label">Platforms</span>
            <h3 class="subsection-title">Where JPilot Works Today</h3>
            <p class="subsection-desc" style="margin: 0 auto">
              Multi-vendor support across the application delivery and network platforms
              JPilot was built to operate on—with the same guardrails on every stack.
            </p>
          </div>
          <div class="vision-grid">
            <div
              v-for="p in product.platforms"
              :key="p.name"
              class="vision-card card reveal"
            >
              <div class="platform-card-head">
                <h4>{{ p.name }}</h4>
                <span
                  class="platform-status"
                  :class="{ beta: p.status === 'Beta' }"
                >{{ p.status }}</span>
              </div>
              <p>{{ p.detail }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Founder note -->
      <div class="section section-dark product-subsection">
        <div class="container">
          <div class="founder-card reveal">
            <JpilotLogo theme="dark" :alt="product.logoAlt" img-class="founder-logo" />
            <blockquote class="founder-quote">
              <p>{{ product.founderNote.quote }}</p>
            </blockquote>
            <div class="founder-signature">
              <p class="founder-closing">{{ product.founderNote.closing }}</p>
              <p class="founder-author">{{ product.founderNote.author }}</p>
              <p class="founder-role">{{ product.founderNote.role }}, {{ product.founderNote.company }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section cta-section">
      <div class="container">
        <div class="cta-box reveal">
          <div class="cta-glow"></div>
          <span class="section-label">Continue the Journey</span>
          <h2>We would be honored to be part of yours</h2>
          <p>
            Whether you are exploring JPilot on your own or want help piloting it in your
            environment—we are here when you are ready to take on new challenges.
          </p>
          <div class="cta-actions">
            <a
              :href="products[0].links.github"
              class="btn btn-outline"
              target="_blank"
              rel="noopener noreferrer"
            >
              <i class="pi pi-github"></i> Get JPilot on GitHub
            </a>
            <RouterLink to="/contact" class="btn btn-primary">
              <i class="pi pi-calendar"></i> Start a Conversation
            </RouterLink>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { products } from '@/data/products.js'
import JpilotLogo from '@/components/shared/JpilotLogo.vue'
</script>

<style scoped>
.page-hero {
  min-height: 48vh;
  display: flex;
  align-items: center;
  background: var(--nt-dark);
  padding: 120px 0 70px;
  position: relative;
  overflow: hidden;
}
.page-hero-bg {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 50% 40%, rgba(0, 168, 224, 0.16) 0%, transparent 60%);
}
.page-hero-content {
  position: relative;
  z-index: 1;
  max-width: 720px;
  text-align: center;
  margin: 0 auto;
}
.product-hero-logo {
  height: 72px;
  width: auto;
  max-width: min(320px, 90vw);
  margin: 0 auto 24px;
  display: block;
}
.page-hero-content h1 {
  font-size: clamp(2rem, 4vw, 2.8rem);
  margin-bottom: 8px;
}
.page-hero-tagline {
  font-size: 1.15rem;
  color: var(--nt-secondary);
  font-weight: 600;
  margin-bottom: 16px;
  font-family: var(--font-heading);
}
.page-hero-subtitle {
  font-size: 1.02rem;
  color: var(--nt-text-muted);
  line-height: 1.75;
  max-width: 600px;
  margin: 0 auto;
}

.product-detail-grid {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 72px;
  align-items: start;
}
.section-subtitle { margin-bottom: 24px; line-height: 1.8; }
.product-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 28px; }
.product-actions { display: flex; flex-wrap: wrap; gap: 12px; }

.visual-card {
  background: var(--nt-card-bg);
  border: 1px solid var(--nt-border);
  border-radius: var(--nt-radius-lg);
  overflow: hidden;
}
.visual-header {
  padding: 40px 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.visual-logo {
  height: 72px;
  width: auto;
  max-width: 100%;
  display: block;
}
.visual-metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}
.metric {
  text-align: center;
  padding: 28px 12px;
  border-right: 1px solid var(--nt-border);
  border-top: 1px solid var(--nt-border);
}
.metric:last-child { border-right: none; }
.metric-value {
  display: block;
  font-family: var(--font-heading);
  font-size: 1.35rem;
  font-weight: 900;
  background: linear-gradient(135deg, var(--nt-primary-l), var(--nt-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 4px;
}
.metric-label {
  font-size: 0.72rem;
  color: var(--nt-text-muted);
  font-weight: 600;
  font-family: var(--font-heading);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  line-height: 1.35;
}
.product-disclaimer {
  margin-top: 16px;
  font-size: 0.78rem;
  color: var(--nt-text-muted);
  line-height: 1.6;
  font-style: italic;
}

.subsection-header { margin-bottom: 40px; max-width: 640px; }
.subsection-title {
  font-size: clamp(1.4rem, 2.5vw, 1.9rem);
  margin: 8px 0 12px;
}
.subsection-title.dark { color: var(--nt-navy); }
.subsection-desc {
  font-size: 0.95rem;
  color: var(--nt-text-muted);
  line-height: 1.75;
  max-width: 560px;
}

.vision-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}
.vision-card {
  padding: 28px;
}
.vision-card h4 {
  font-size: 1rem;
  color: var(--nt-secondary);
  margin-bottom: 10px;
}
.vision-card p {
  font-size: 0.9rem;
  color: var(--nt-text-muted);
  line-height: 1.7;
  margin: 0;
}

.capabilities-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 64px;
  align-items: start;
}
.capabilities-list { display: flex; flex-direction: column; gap: 14px; margin-top: 24px; }
.capability-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  font-size: 0.9rem;
  color: #374151;
  line-height: 1.6;
}
.capability-item .pi { color: var(--nt-primary); flex-shrink: 0; margin-top: 3px; }

.roles-stack { display: flex; flex-direction: column; gap: 18px; margin-top: 24px; }
.role-row {
  display: flex;
  gap: 14px;
  align-items: flex-start;
  padding: 18px;
  background: white;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
}
.role-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(0, 123, 167, 0.1);
  border: 1px solid rgba(0, 123, 167, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--nt-primary);
  flex-shrink: 0;
}
.role-row strong { display: block; font-size: 0.92rem; color: var(--nt-navy); margin-bottom: 4px; }
.role-row p { font-size: 0.84rem; color: #64748B; margin: 0; line-height: 1.55; }

.platform-card-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 10px;
}
.platform-card-head h4 {
  margin-bottom: 0;
}
.platform-status {
  padding: 4px 10px;
  border-radius: 100px;
  font-size: 0.68rem;
  font-weight: 700;
  font-family: var(--font-heading);
  letter-spacing: 0.04em;
  text-transform: uppercase;
  background: rgba(0, 168, 224, 0.12);
  color: var(--nt-secondary);
  border: 1px solid rgba(0, 168, 224, 0.28);
  flex-shrink: 0;
}
.platform-status.beta {
  background: rgba(245, 158, 11, 0.12);
  color: #FBBF24;
  border-color: rgba(251, 191, 36, 0.3);
}

.founder-card {
  max-width: 720px;
  margin: 0 auto;
  text-align: center;
  padding: 48px 40px;
  background: var(--nt-card-bg);
  border: 1px solid var(--nt-border);
  border-radius: var(--nt-radius-lg);
}
.founder-logo {
  height: 48px;
  width: auto;
  margin: 0 auto 28px;
  display: block;
}
.founder-quote {
  margin: 0 0 28px;
  padding: 0;
  border: none;
}
.founder-quote p {
  font-size: 1.08rem;
  font-style: italic;
  color: var(--nt-text-light);
  line-height: 1.85;
  margin: 0;
}
.founder-closing { font-size: 0.9rem; color: var(--nt-text-muted); margin-bottom: 6px; }
.founder-author { font-size: 1.05rem; font-weight: 700; color: var(--nt-white); margin-bottom: 2px; }
.founder-role { font-size: 0.85rem; color: var(--nt-secondary); }

.cta-section { background: var(--nt-dark-2); }
.cta-box {
  background: var(--nt-dark-3);
  border: 1px solid var(--nt-border);
  border-radius: var(--nt-radius-lg);
  padding: 64px;
  text-align: center;
  position: relative;
  overflow: hidden;
}
.cta-glow {
  position: absolute;
  top: -60px;
  left: 50%;
  transform: translateX(-50%);
  width: 300px;
  height: 150px;
  background: radial-gradient(ellipse, rgba(0, 123, 167, 0.2) 0%, transparent 70%);
  pointer-events: none;
}
.cta-box h2 { margin: 12px 0 16px; }
.cta-box p {
  color: var(--nt-text-muted);
  max-width: 520px;
  margin: 0 auto 32px;
  line-height: 1.75;
}
.cta-actions {
  display: flex;
  gap: 14px;
  justify-content: center;
  flex-wrap: wrap;
}

@media (max-width: 1024px) {
  .product-detail-grid,
  .capabilities-layout { grid-template-columns: 1fr; gap: 40px; }
  .vision-grid { grid-template-columns: 1fr; }
}
@media (max-width: 640px) {
  .cta-box { padding: 40px 24px; }
  .visual-metrics { grid-template-columns: 1fr; }
  .metric { border-right: none; }
  .product-actions,
  .cta-actions { flex-direction: column; }
  .product-actions .btn,
  .cta-actions .btn { width: 100%; justify-content: center; }
  .founder-card { padding: 36px 24px; }
}
</style>
