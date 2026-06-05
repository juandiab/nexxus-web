<template>
  <div class="faq-page">
    <section class="page-hero">
      <div class="page-hero-bg"></div>
      <div class="container page-hero-content">
        <span class="section-label reveal">FAQ</span>
        <h1 class="reveal reveal-delay-1">Frequently Asked<br /><span class="gradient-text">Questions</span></h1>
        <p class="page-hero-subtitle reveal reveal-delay-2">
          Answers about our services, delivery model, global reach, and AI-powered tooling—
          drawn from how we work with organizations worldwide.
        </p>
      </div>
    </section>

    <section class="faq-section" aria-labelledby="faq-heading">
      <div class="faq-section-bg" aria-hidden="true"></div>
      <div class="faq-section-overlay" aria-hidden="true"></div>

      <div class="container faq-section-inner">
        <div class="faq-intro reveal">
          <h2 id="faq-heading" class="faq-heading">Common Questions</h2>
          <p class="faq-subheading">
            Principal-level expertise in WAF, NetScaler, Zero-Trust, multicloud security, and AI automation—
            delivered remotely across 54+ countries.
          </p>
        </div>

        <div class="faq-accordion-wrap reveal reveal-delay-1">
          <Accordion
            :multiple="true"
            class="faq-accordion"
            :pt="{ root: { class: 'faq-accordion-root' } }"
          >
            <AccordionPanel
              v-for="(faq, index) in faqs"
              :key="index"
              :value="String(index)"
              class="faq-panel"
            >
              <AccordionHeader
                class="faq-header"
                :pt="{
                  root: { class: 'faq-header-root' },
                  toggleicon: { class: 'faq-toggle-icon' },
                }"
              >
                {{ faq.title }}
              </AccordionHeader>
              <AccordionContent
                class="faq-content"
                :pt="{ content: { class: 'faq-content-inner' } }"
              >
                <p>{{ faq.description }}</p>
              </AccordionContent>
            </AccordionPanel>
          </Accordion>
        </div>

        <div class="faq-cta reveal reveal-delay-2">
          <p>Still have a question about your environment or engagement?</p>
          <RouterLink to="/contact" class="btn btn-primary">
            <i class="pi pi-send"></i> Contact Us
          </RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import Accordion from 'primevue/accordion'
import AccordionPanel from 'primevue/accordionpanel'
import AccordionHeader from 'primevue/accordionheader'
import AccordionContent from 'primevue/accordioncontent'
import { faqs } from '@/data/faqs.js'
</script>

<style scoped>
.page-hero {
  min-height: 40vh;
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
.page-hero-content { position: relative; z-index: 1; max-width: 700px; }
.page-hero-subtitle {
  font-size: 1.05rem;
  color: var(--nt-text-muted);
  margin-top: 16px;
  max-width: 560px;
  line-height: 1.75;
}

.faq-section {
  position: relative;
  padding: 80px 0 100px;
  overflow: hidden;
}
.faq-section-bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 20% 30%, rgba(0, 123, 167, 0.18) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 70%, rgba(0, 168, 224, 0.12) 0%, transparent 45%),
    linear-gradient(160deg, var(--nt-dark-2) 0%, var(--nt-dark) 100%);
}
.faq-section-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.04);
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
}
.faq-section-inner {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 48px;
}
.faq-intro {
  text-align: center;
  max-width: 640px;
}
.faq-heading {
  font-size: clamp(1.6rem, 3vw, 2rem);
  margin-bottom: 12px;
}
.faq-subheading {
  font-size: 1rem;
  color: var(--nt-text-muted);
  line-height: 1.75;
}

.faq-accordion-wrap {
  width: 100%;
  max-width: 682px;
}

.faq-accordion :deep(.faq-accordion-root) {
  border: none;
  border-radius: var(--nt-radius);
  overflow: hidden;
}

.faq-accordion :deep(.faq-panel) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.faq-accordion :deep(.faq-panel:last-child) {
  border-bottom: none;
}

.faq-accordion :deep(.faq-header-root) {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 24px;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: var(--nt-white);
  font-family: var(--font-heading);
  font-size: 1.05rem;
  font-weight: 600;
  line-height: 1.4;
  transition: background 0.25s ease;
}
.faq-accordion :deep(.faq-header-root:hover) {
  background: rgba(255, 255, 255, 0.14);
}
.faq-accordion :deep(.faq-toggle-icon) {
  color: var(--nt-white);
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.faq-accordion :deep(.faq-content-inner) {
  padding: 24px;
  background: rgba(0, 0, 0, 0.1);
  border: none;
}
.faq-accordion :deep(.faq-content-inner p) {
  margin: 0;
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.75;
}

.faq-cta {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}
.faq-cta p {
  font-size: 0.95rem;
  color: var(--nt-text-muted);
  max-width: 420px;
  line-height: 1.65;
}

@media (max-width: 640px) {
  .faq-section { padding: 60px 0 80px; }
  .faq-accordion :deep(.faq-header-root) {
    padding: 20px;
    font-size: 0.95rem;
  }
  .faq-accordion :deep(.faq-content-inner) { padding: 20px; }
}
</style>
