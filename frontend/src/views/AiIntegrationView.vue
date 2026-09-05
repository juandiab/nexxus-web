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
      <div class="page-hero-bg" aria-hidden="true">
        <MagicRings
          class="hero-bg-layer"
          color="#00A8E0"
          color-two="#007BA7"
          :ring-count="5"
          :speed="0.6"
          :attenuation="12"
          :line-thickness="1.6"
          :base-radius="0.34"
          :radius-step="0.08"
          :scale-rate="0.08"
          :opacity="0.45"
          :noise-amount="0.05"
          :ring-gap="1.4"
          :fade-in="0.7"
          :fade-out="0.5"
        />
        <Strands
          class="hero-bg-layer hero-strands"
          :colors="['#00A8E0', '#007BA7', '#4DB8E0']"
          :count="2"
          :speed="0.35"
          :amplitude="0.7"
          :waviness="0.9"
          :thickness="0.55"
          :glow="2"
          :taper="3.5"
          :spread="1"
          :intensity="0.45"
          :saturation="1.2"
          :opacity="0.5"
          :scale="1.6"
        />
      </div>
      <div class="container page-hero-inner">
        <div class="page-hero-content">
          <span class="section-label reveal">{{ copy.hero.label }}</span>
          <h1 class="reveal reveal-delay-1">
            <span class="hero-brand-nowrap">{{ copy.hero.h1Before }}</span><br /><span class="gradient-text">{{ copy.hero.h1Highlight }}</span>
          </h1>
          <p class="page-hero-subtitle reveal reveal-delay-2">
            {{ copy.hero.subtitle }}
            <span class="hero-positioning">{{ copy.hero.positioningLine }}</span>
          </p>
          <div class="hero-actions reveal reveal-delay-3">
            <GlowButton variant="primary">
              <RouterLink :to="contactLink()" class="btn btn-primary">
                {{ copy.hero.primaryCta }} <i class="pi pi-arrow-right"></i>
              </RouterLink>
            </GlowButton>
            <RouterLink :to="bookDemoLink" class="btn btn-secondary">
              <i class="pi pi-calendar"></i> {{ copy.hero.secondaryCta }}
            </RouterLink>
          </div>
        </div>
        <div class="page-hero-visual reveal reveal-delay-2" aria-hidden="true">
          <CenterFlow
            :node-items="centerFlowNodes"
            :center-size="128"
            :node-size="54"
            :node-distance="0.68"
            :pulse-duration="4.5"
            :pulse-interval="8"
            :pulse-length="0.38"
            :line-width="1.5"
            :pulse-width="1.2"
            :pulse-softness="9"
            line-color="rgba(0, 168, 224, 0.12)"
            pulse-color="#7EDFFF"
            glow-color="#00A8E0"
            :max-glow-intensity="28"
            :border-radius="32"
            :aria-label="centerFlowAria"
          >
            <template #center>
              <span class="hero-center-label">{{ centerFlowShort }}</span>
            </template>
          </CenterFlow>
        </div>
      </div>
    </section>

    <!-- Use cases -->
    <section class="section use-cases-section">
      <div class="container">
        <div class="section-header reveal section-header-center">
          <span class="section-label">{{ copy.useCases.label }}</span>
          <h2 class="section-title">{{ copy.useCases.title }}</h2>
          <p class="section-subtitle section-subtitle-center">
            {{ copy.useCases.subtitle }}
          </p>
        </div>
        <div class="use-cases-grid">
          <BorderGlow
            v-for="(item, i) in copy.useCases.items"
            :key="item.id"
            class="use-case-glow reveal"
            :class="`reveal-delay-${i + 1}`"
            :background-color="'var(--nt-dark-3)'"
            :colors="['#00A8E0', '#007BA7', '#4DB8E0']"
            glow-color="192 85 62"
            :border-radius="16"
            :glow-radius="24"
            :glow-intensity="1"
            :edge-sensitivity="24"
            :cone-spread="22"
            :fill-opacity="0.38"
          >
            <article class="use-case-card">
              <div class="use-case-icon" :class="`use-case-icon--${item.id}`">
                <i :class="item.icon"></i>
              </div>
              <h3 class="use-case-title">{{ item.title }}</h3>
              <p class="use-case-desc">{{ item.desc }}</p>
              <ul class="use-case-bullets">
                <li v-for="bullet in item.bullets" :key="bullet">
                  <i class="pi pi-check"></i>
                  <span>{{ bullet }}</span>
                </li>
              </ul>
            </article>
          </BorderGlow>
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
          <p class="audience-guidance reveal reveal-delay-1">
            {{ copy.audience.guidanceLine }}
          </p>
        </div>
        <div class="audience-tags reveal reveal-delay-2">
          <span v-for="tag in copy.audience.tags" :key="tag" class="tag">{{ tag }}</span>
        </div>
      </div>
    </section>

    <!-- Engagement pipeline -->
    <section class="section pipeline-section section-dark">
      <div class="container">
        <div class="section-header reveal section-header-center">
          <h2 class="section-title">{{ copy.process.title }}</h2>
          <p class="section-subtitle section-subtitle-center">
            {{ copy.process.pipelineCaption }}
          </p>
        </div>
        <div class="reveal reveal-delay-1">
          <AiEngagementPipeline :steps="copy.process.steps" />
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
          <BorderGlow
            v-for="(pkg, i) in copy.packages.items"
            :key="pkg.id"
            class="package-glow reveal"
            :class="[`reveal-delay-${(i % 4) + 1}`, { 'package-glow--featured': pkg.id === 'pilot' }]"
            :background-color="pkg.id === 'pilot' ? 'rgba(0, 123, 167, 0.12)' : 'var(--nt-dark-3)'"
            :colors="['#00A8E0', '#007BA7', '#4DB8E0']"
            glow-color="192 85 62"
            :border-radius="16"
            :glow-radius="28"
            :glow-intensity="pkg.id === 'pilot' ? 1.15 : 1"
            :edge-sensitivity="28"
            :cone-spread="26"
            :fill-opacity="0.42"
            :animated="i === 0"
          >
            <article class="package-card">
              <div class="package-header">
                <div class="package-icon" :class="`package-icon--${pkg.id}`">
                  <i :class="pkg.icon"></i>
                </div>
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
          </BorderGlow>
        </div>
      </div>
    </section>

    <!-- How we work -->
    <section class="section section-dark process-section">
      <div class="container">
        <div class="process-grid">
          <div class="process-text reveal">
            <span class="section-label">{{ copy.process.label }}</span>
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
          </div>
          <div class="process-visual reveal reveal-delay-2">
            <div class="principles-panel">
              <div class="principles-header">
                <NxConnectionRings size="md" />
                <h3 class="principles-title">{{ copy.process.visualTitle }}</h3>
              </div>
              <div class="principles-list">
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
            <RouterLink :to="bookDemoLink" class="btn btn-secondary">
              <i class="pi pi-calendar"></i> {{ copy.cta.secondaryCta }}
            </RouterLink>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import AiEngagementPipeline from '@/components/ai-integration/AiEngagementPipeline.vue'
import CenterFlow from '@/components/ai-integration/CenterFlow.vue'
import BorderGlow from '@/components/shared/BorderGlow.vue'
import GlowButton from '@/components/shared/GlowButton.vue'
import MagicRings from '@/components/shared/MagicRings.vue'
import NxConnectionRings from '@/components/shared/NxConnectionRings.vue'
import Strands from '@/components/shared/Strands.vue'
import { computed } from 'vue'
import { AI_INTEGRATION_SERVICE } from '@/data/aiIntegrationCopy.js'
import { useAiIntegrationLocale } from '@/composables/useAiIntegrationLocale.js'
import { aiIntegrationBookDemoQuery, aiIntegrationContactQuery } from '@/utils/leads.js'

const { locale, copy, setLocale } = useAiIntegrationLocale()

const centerFlowShort = 'AI Tech'
const centerFlowAria = computed(() => AI_INTEGRATION_SERVICE[locale.value])

const centerFlowNodes = computed(() =>
  copy.value.useCases.items.map((item) => ({ label: item.flowLabel })),
)

const bookDemoLink = computed(() => ({
  path: '/book-demo',
  query: aiIntegrationBookDemoQuery(locale.value),
}))

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
  min-height: 55vh;
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
  overflow: hidden;
}
.hero-bg-layer {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}
.hero-strands {
  opacity: 0.6;
  mix-blend-mode: screen;
}
.page-hero-inner {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(260px, 42%);
  gap: 40px;
  align-items: center;
}
.page-hero-content {
  max-width: 760px;
}
.page-hero-visual {
  width: 100%;
  height: min(420px, 52vw);
  min-height: 280px;
  max-height: 440px;
  overflow: visible;
}
.page-hero-visual :deep(.center-flow__center-inner) {
  width: 92%;
  height: auto;
}
.hero-brand-nowrap {
  white-space: nowrap;
}
.hero-center-label {
  display: block;
  white-space: nowrap;
  font-family: var(--font-heading);
  font-size: clamp(0.68rem, 2vw, 0.9rem);
  font-weight: 800;
  letter-spacing: 0.03em;
  line-height: 1;
  text-align: center;
  color: var(--nt-primary-l);
  text-shadow: 0 0 12px rgba(0, 168, 224, 0.45);
}
.page-hero-subtitle {
  font-size: 1.1rem;
  color: var(--nt-text-muted);
  margin-top: 16px;
  max-width: 620px;
  line-height: 1.75;
}
.hero-positioning {
  display: block;
  margin-top: 12px;
  color: var(--nt-text-light);
  font-weight: 500;
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
.audience-guidance {
  max-width: 680px;
  margin-top: 16px;
  font-size: 1.05rem;
  font-weight: 500;
  color: var(--nt-text-light);
  line-height: 1.65;
}

.use-cases-section {
  background: var(--nt-dark-2);
  padding-top: 64px;
  padding-bottom: 64px;
}
.use-cases-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}
.use-case-glow {
  height: 100%;
}
.use-case-glow :deep(.border-glow-inner) {
  height: 100%;
}
.use-case-card {
  display: flex;
  flex-direction: column;
  padding: 28px;
  height: 100%;
}
.use-case-icon {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  background: linear-gradient(135deg, var(--nt-primary), var(--nt-primary-d));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.3rem;
  margin-bottom: 20px;
  box-shadow: 0 0 24px rgba(0, 168, 224, 0.25);
}
.use-case-icon--customers {
  background: linear-gradient(135deg, #00A8E0, #007BA7);
}
.use-case-icon--operations {
  background: linear-gradient(135deg, #007BA7, #005f82);
}
.use-case-icon--sales {
  background: linear-gradient(135deg, #4DB8E0, #007BA7);
}
.use-case-icon--website {
  background: linear-gradient(135deg, #00A8E0, #4DB8E0);
}
.use-case-title {
  font-size: 1.2rem;
  color: var(--nt-white);
  margin-bottom: 12px;
  line-height: 1.3;
}
.use-case-desc {
  font-size: 0.92rem;
  color: var(--nt-text-muted);
  line-height: 1.65;
  margin-bottom: 20px;
  flex: 1;
}
.use-case-bullets {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin: 0;
  padding-top: 16px;
  border-top: 1px solid var(--nt-border);
}
.use-case-bullets li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 0.85rem;
  color: var(--nt-text-light);
}
.use-case-bullets .pi {
  color: var(--nt-secondary);
  font-size: 0.75rem;
  margin-top: 4px;
  flex-shrink: 0;
}

.audience-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.pipeline-section {
  padding-top: 48px;
  padding-bottom: 64px;
}

.packages-section {
  background: var(--nt-dark-2);
}
.packages-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}
.package-glow {
  height: 100%;
}
.package-glow :deep(.border-glow-inner) {
  height: 100%;
}
.package-glow--featured {
  grid-row: span 1;
}
.package-card {
  display: flex;
  flex-direction: column;
  padding: 28px;
  height: 100%;
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
  box-shadow: 0 0 20px rgba(0, 168, 224, 0.2);
}
.package-icon--pilot {
  box-shadow: 0 0 28px rgba(0, 168, 224, 0.35);
}
.package-name {
  font-size: 1.25rem;
  margin-bottom: 4px;
  color: var(--nt-white);
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
  gap: 56px;
  align-items: start;
}
.process-copy {
  margin-bottom: 28px;
  font-size: 1.35rem;
  line-height: 1.45;
  color: var(--nt-white);
  max-width: 560px;
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
  box-shadow: 0 0 16px rgba(0, 168, 224, 0.3);
}
.process-step strong {
  display: block;
  color: var(--nt-white);
  margin-bottom: 4px;
}
.process-step p {
  font-size: 0.9rem;
  color: var(--nt-text-muted);
  margin: 0;
}

.process-visual {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.principles-panel {
  padding: 24px 28px;
  background: var(--nt-dark-3);
  border: 1px solid var(--nt-border);
  border-radius: var(--nt-radius-lg);
}
.principles-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 16px;
}
.principles-title {
  font-size: 1rem;
  color: var(--nt-white);
  margin: 0;
}
.principles-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.principle-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 0.9rem;
  color: var(--nt-text-light);
}
.principle-item .pi {
  color: var(--nt-primary-l);
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
  .page-hero-inner {
    grid-template-columns: 1fr;
    gap: 32px;
  }
  .page-hero-visual {
    height: min(360px, 70vw);
    max-width: 520px;
    margin: 0 auto;
  }
  .packages-grid {
    grid-template-columns: 1fr;
  }
  .use-cases-grid {
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
