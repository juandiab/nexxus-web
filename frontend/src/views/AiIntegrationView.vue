<template>
  <div class="ai-integration-page" :lang="locale">
    <!-- Locale toggle -->
    <div class="locale-bar">
      <div class="container locale-bar-inner">
        <div
          class="locale-toggle"
          role="group"
          :aria-label="copy.toggle.aria"
        >
          <button
            type="button"
            class="locale-btn"
            :class="{ active: locale === 'en' }"
            :aria-pressed="locale === 'en'"
            @click="setLocale('en')"
          >
            {{ copy.toggle.en }}
          </button>
          <button
            type="button"
            class="locale-btn"
            :class="{ active: locale === 'es' }"
            :aria-pressed="locale === 'es'"
            @click="setLocale('es')"
          >
            {{ copy.toggle.es }}
          </button>
        </div>
      </div>
    </div>

    <!-- Hero -->
    <section class="page-hero">
      <div class="page-hero-bg"></div>
      <div class="container page-hero-content">
        <span class="section-label reveal">{{ copy.hero.label }}</span>
        <h1 class="reveal reveal-delay-1">
          {{ copy.hero.h1Before }}<br /><span class="gradient-text">{{ copy.hero.h1Highlight }}</span>
        </h1>
        <p class="page-hero-subtitle reveal reveal-delay-2">
          {{ copy.hero.subtitle }}
        </p>
        <div class="hero-actions reveal reveal-delay-3">
          <GlowButton variant="primary">
            <RouterLink :to="contactLink()" class="btn btn-primary">
              {{ copy.hero.primaryCta }} <i class="pi pi-arrow-right"></i>
            </RouterLink>
          </GlowButton>
          <RouterLink to="/book-demo" class="btn btn-secondary">
            <i class="pi pi-calendar"></i> {{ copy.hero.secondaryCta }}
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- For whom -->
    <section class="section section-dark audience-section">
      <div class="container">
        <div class="section-header reveal">
          <span class="section-label">{{ copy.audience.label }}</span>
          <h2 class="section-title">{{ copy.audience.title }}</h2>
          <p class="section-subtitle audience-copy">
            {{ copy.audience.subtitle }}
          </p>
        </div>
        <div class="audience-tags reveal reveal-delay-2">
          <span v-for="tag in copy.audience.tags" :key="tag" class="tag">{{ tag }}</span>
        </div>
      </div>
    </section>

    <!-- Packages -->
    <section class="section packages-section">
      <div class="container">
        <div class="section-header reveal section-header-center">
          <span class="section-label">{{ copy.packages.label }}</span>
          <h2 class="section-title">{{ copy.packages.title }}</h2>
          <p class="section-subtitle section-subtitle-center">
            {{ copy.packages.subtitle }}
          </p>
        </div>
        <div class="packages-grid">
          <article
            v-for="(pkg, i) in copy.packages.items"
            :key="pkg.id"
            :class="`card package-card reveal reveal-delay-${(i % 4) + 1}`"
          >
            <div class="package-header">
              <div class="package-icon"><i :class="pkg.icon"></i></div>
              <div>
                <h3 class="package-name">{{ pkg.name }}</h3>
                <span class="package-duration">{{ pkg.duration }}</span>
              </div>
            </div>
            <p class="package-outcome">{{ pkg.outcome }}</p>
            <ul class="package-bullets">
              <li v-for="bullet in pkg.bullets" :key="bullet">
                <i class="pi pi-check-circle"></i>
                <span>{{ bullet }}</span>
              </li>
            </ul>
            <RouterLink :to="contactLink(pkg.id)" class="btn btn-primary package-cta">
              {{ copy.packages.cta }} <i class="pi pi-arrow-right"></i>
            </RouterLink>
          </article>
        </div>
      </div>
    </section>

    <!-- How we work -->
    <section class="section section-light process-section">
      <div class="container">
        <div class="process-grid">
          <div class="process-text reveal">
            <span class="section-label">{{ copy.process.label }}</span>
            <h2 class="section-title">{{ copy.process.title }}</h2>
            <p class="section-subtitle process-copy">
              {{ copy.process.subtitle }}
            </p>
            <div class="process-steps">
              <div v-for="(step, i) in copy.process.steps" :key="step.name" class="process-step">
                <span class="step-num">{{ i + 1 }}</span>
                <div>
                  <strong>{{ step.name }}</strong>
                  <p>{{ step.desc }}</p>
                </div>
              </div>
            </div>
            <p class="jpilot-bridge">
              {{ copy.process.jpilotBefore }}
              <RouterLink to="/products#jpilot">{{ copy.process.jpilotLink }}</RouterLink>
              {{ copy.process.jpilotAfter }}
            </p>
          </div>
          <div class="process-visual reveal reveal-delay-2">
            <div class="visual-card">
              <div class="visual-header">
                <i class="pi pi-sync visual-icon"></i>
                <h3>{{ copy.process.visualTitle }}</h3>
              </div>
              <div class="visual-body">
                <div v-for="item in copy.process.principles" :key="item" class="principle-item">
                  <i class="pi pi-check"></i>
                  <span>{{ item }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Proof stats -->
    <section class="stats-bar">
      <div class="container">
        <div class="stats-grid">
          <div v-for="stat in copy.proof.stats" :key="stat.label" class="stat-item reveal">
            <span class="stat-value">{{ stat.value }}</span>
            <span class="stat-label">{{ stat.label }}</span>
          </div>
        </div>
      </div>
    </section>

    <section class="section section-dark proof-section">
      <div class="container">
        <div class="section-header reveal section-header-center">
          <span class="section-label">{{ copy.proof.label }}</span>
          <h2 class="section-title">{{ copy.proof.title }}</h2>
          <p class="section-subtitle section-subtitle-center">
            {{ copy.proof.subtitle }}
          </p>
        </div>
        <div class="proof-tags reveal reveal-delay-2">
          <span v-for="industry in copy.proof.industries" :key="industry" class="tag">{{ industry }}</span>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="section cta-section">
      <div class="container">
        <div class="cta-box reveal">
          <div class="cta-glow"></div>
          <span class="section-label">{{ copy.cta.label }}</span>
          <h2>{{ copy.cta.title }}</h2>
          <p>
            {{ copy.cta.bodyBefore }}
            <a href="mailto:business@nexxus-tech.com">business@nexxus-tech.com</a>
            {{ copy.cta.bodyAfter }}
          </p>
          <div class="cta-actions">
            <GlowButton variant="primary">
              <RouterLink :to="contactLink()" class="btn btn-primary">
                <i class="pi pi-send"></i> {{ copy.cta.primaryCta }}
              </RouterLink>
            </GlowButton>
            <RouterLink to="/book-demo" class="btn btn-secondary">
              <i class="pi pi-calendar"></i> {{ copy.cta.secondaryCta }}
            </RouterLink>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import GlowButton from '@/components/shared/GlowButton.vue'
import { useAiIntegrationLocale } from '@/composables/useAiIntegrationLocale.js'
import { aiIntegrationContactQuery } from '@/utils/leads.js'

const { locale, copy, setLocale } = useAiIntegrationLocale()

function contactLink(packageId = null) {
  return {
    path: '/contact',
    query: aiIntegrationContactQuery(locale.value, packageId),
  }
}
</script>

<style scoped>
.locale-bar {
  position: relative;
  z-index: 2;
  background: var(--nt-dark);
  border-bottom: 1px solid var(--nt-border);
  padding: 8px 0;
  margin-top: 88px;
}
.locale-bar-inner {
  display: flex;
  justify-content: flex-end;
}
.locale-toggle {
  display: inline-flex;
  border: 1px solid var(--nt-border);
  border-radius: 8px;
  overflow: hidden;
  background: var(--nt-dark-2);
}
.locale-btn {
  min-width: 48px;
  min-height: 36px;
  padding: 6px 16px;
  border: none;
  background: transparent;
  color: var(--nt-text-muted);
  font-family: var(--font-heading);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  cursor: pointer;
  transition: var(--nt-transition);
}
.locale-btn:hover {
  color: var(--nt-white);
  background: rgba(0, 123, 167, 0.12);
}
.locale-btn.active {
  color: var(--nt-white);
  background: var(--nt-primary);
}

.page-hero {
  min-height: 50vh;
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
  background: var(--nt-dark);
  padding: 48px 0 60px;
}
.page-hero-bg {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 30% 50%, rgba(0, 123, 167, 0.15) 0%, transparent 65%);
}
.page-hero-content {
  position: relative;
  z-index: 1;
  max-width: 760px;
}
.page-hero-subtitle {
  font-size: 1.1rem;
  color: var(--nt-text-muted);
  margin-top: 16px;
  max-width: 620px;
  line-height: 1.75;
}
.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 32px;
}

.section-header-center {
  text-align: center;
  margin-bottom: 48px;
}
.section-subtitle-center {
  margin-left: auto;
  margin-right: auto;
}

.audience-copy {
  max-width: 680px;
}
.audience-tags,
.proof-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.packages-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}
.package-card {
  display: flex;
  flex-direction: column;
  padding: 32px;
}
.package-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 16px;
}
.package-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--nt-primary), var(--nt-primary-d));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.2rem;
  flex-shrink: 0;
}
.package-name {
  font-size: 1.25rem;
  margin-bottom: 4px;
}
.package-duration {
  font-size: 0.8rem;
  font-weight: 600;
  font-family: var(--font-heading);
  letter-spacing: 0.05em;
  color: var(--nt-secondary);
  text-transform: uppercase;
}
.package-outcome {
  font-size: 0.95rem;
  color: var(--nt-text-light);
  margin-bottom: 20px;
  line-height: 1.6;
}
.package-bullets {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 24px;
  flex: 1;
}
.package-bullets li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 0.9rem;
  color: var(--nt-text-muted);
}
.package-bullets .pi {
  color: var(--nt-secondary);
  font-size: 0.85rem;
  margin-top: 3px;
  flex-shrink: 0;
}
.package-cta {
  align-self: flex-start;
  padding: 12px 24px;
  font-size: 0.85rem;
}

.process-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 64px;
  align-items: center;
}
.process-copy {
  margin-bottom: 28px;
}
.process-steps {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 24px;
}
.process-step {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}
.step-num {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--nt-primary);
  color: white;
  font-family: var(--font-heading);
  font-weight: 800;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.process-step strong {
  display: block;
  color: var(--nt-navy);
  margin-bottom: 4px;
}
.process-step p {
  font-size: 0.9rem;
  color: #4A5568;
  margin: 0;
}
.jpilot-bridge {
  font-size: 0.9rem;
  color: #64748B;
  line-height: 1.6;
}

.visual-card {
  background: white;
  border: 1px solid #E2E8F0;
  border-radius: var(--nt-radius-lg);
  overflow: hidden;
}
.visual-header {
  padding: 28px 32px;
  background: linear-gradient(135deg, var(--nt-primary), var(--nt-primary-d));
  display: flex;
  align-items: center;
  gap: 16px;
}
.visual-icon {
  font-size: 1.8rem;
  color: white;
}
.visual-header h3 {
  color: white;
  font-size: 1.1rem;
  margin: 0;
}
.visual-body {
  padding: 28px 32px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.principle-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 0.95rem;
  color: #374151;
}
.principle-item .pi {
  color: var(--nt-primary);
  font-size: 0.85rem;
}

.stats-bar {
  background: var(--nt-dark-2);
  border-top: 1px solid var(--nt-border);
  border-bottom: 1px solid var(--nt-border);
  padding: 48px 0;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
}
.stat-item {
  text-align: center;
  padding: 20px;
  border-right: 1px solid var(--nt-border);
}
.stat-item:last-child {
  border-right: none;
}
.stat-value {
  display: block;
  font-family: var(--font-heading);
  font-size: clamp(1.8rem, 3vw, 2.4rem);
  font-weight: 900;
  background: linear-gradient(135deg, var(--nt-primary-l), var(--nt-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 6px;
}
.stat-label {
  font-size: 0.8rem;
  color: var(--nt-text-muted);
  font-weight: 600;
  font-family: var(--font-heading);
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.proof-section {
  padding-top: 60px;
}

.cta-section {
  background: var(--nt-dark-2);
}
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
.cta-box h2 {
  margin: 12px 0 16px;
  max-width: 640px;
  margin-left: auto;
  margin-right: auto;
}
.cta-box p {
  color: var(--nt-text-muted);
  max-width: 520px;
  margin: 0 auto 32px;
  line-height: 1.75;
}
.cta-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
}

@media (max-width: 1024px) {
  .packages-grid {
    grid-template-columns: 1fr;
  }
  .process-grid {
    grid-template-columns: 1fr;
    gap: 40px;
  }
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .stat-item:nth-child(2) {
    border-right: none;
  }
  .stat-item:nth-child(1),
  .stat-item:nth-child(2) {
    border-bottom: 1px solid var(--nt-border);
  }
}

@media (max-width: 640px) {
  .locale-bar-inner {
    justify-content: center;
  }
  .cta-box {
    padding: 40px 24px;
  }
  .stats-grid {
    grid-template-columns: 1fr;
  }
  .stat-item {
    border-right: none;
    border-bottom: 1px solid var(--nt-border);
  }
  .stat-item:last-child {
    border-bottom: none;
  }
  .hero-actions,
  .cta-actions {
    flex-direction: column;
    align-items: stretch;
  }
  .hero-actions .btn,
  .cta-actions .btn {
    justify-content: center;
  }
}
</style>
