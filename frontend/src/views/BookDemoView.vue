<template>
  <div class="book-demo-page">
    <section class="page-hero">
      <div class="page-hero-bg"></div>
      <div class="container page-hero-content">
        <span class="section-label reveal">Book a demo</span>
        <h1 class="reveal reveal-delay-1">Schedule a<br /><span class="gradient-text">Live Walkthrough</span></h1>
        <p class="page-hero-subtitle reveal reveal-delay-2">
          Pick a time for a JPilot demo or services discovery call with a Nexxus principal architect.
          Remote worldwide — no obligation.
        </p>
      </div>
    </section>

    <section class="section scheduler-section">
      <div class="container scheduler-wrap reveal">
        <AppointmentScheduler :src="scheduleUrl" :min-height="720" />
        <p class="scheduler-note">
          Prefer to chat first?
          <router-link to="/contact">Contact us</router-link>
          or use JPbot on any page.
        </p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppointmentScheduler from '@/components/shared/AppointmentScheduler.vue'
import { buildDemoBookingUrl } from '@/utils/demoBooking.js'
import { GOOGLE_APPOINTMENT_SCHEDULE_URL } from '@/config/site.js'

const route = useRoute()

const scheduleUrl = computed(() => {
  const { name, email, company, service, topic, details, enquiry } = route.query
  if (!name && !email) return GOOGLE_APPOINTMENT_SCHEDULE_URL

  return buildDemoBookingUrl({
    name: String(name || ''),
    email: String(email || ''),
    company: String(company || ''),
    service: String(service || ''),
    demo_notes: String(topic || details || ''),
    enquiry_type: String(enquiry || 'Book a demo'),
    technologies: [],
  })
})
</script>

<style scoped>
.page-hero {
  min-height: 36vh;
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
  background: radial-gradient(ellipse at 40% 60%, rgba(91, 79, 232, 0.12) 0%, transparent 60%);
}

.page-hero-content {
  position: relative;
  z-index: 1;
}

.page-hero-subtitle {
  font-size: 1.05rem;
  color: var(--nt-text-muted);
  margin-top: 16px;
  max-width: 560px;
  line-height: 1.75;
}

.scheduler-section {
  background: var(--nt-dark-2);
  padding-bottom: 80px;
}

.scheduler-wrap {
  max-width: 920px;
  margin: 0 auto;
}

.scheduler-note {
  margin: 20px 0 0;
  text-align: center;
  font-size: 0.88rem;
  color: var(--nt-text-muted);
}

.scheduler-note a {
  color: var(--nt-primary-l);
  text-decoration: none;
  font-weight: 600;
}

.scheduler-note a:hover {
  text-decoration: underline;
}
</style>
