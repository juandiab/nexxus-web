<template>
  <div class="contact-page">
    <!-- Hero -->
    <section class="page-hero">
      <div class="page-hero-bg"></div>
      <div class="container page-hero-content">
        <span class="section-label reveal">Get in Touch</span>
        <h1 class="reveal reveal-delay-1">Let's Start a<br /><span class="gradient-text">Conversation</span></h1>
        <p class="page-hero-subtitle reveal reveal-delay-2">
          Whether you need a WAF assessment, a Zero-Trust roadmap, or just want to
          explore what's possible — we're here. No pressure, no obligation.
        </p>
      </div>
    </section>

    <!-- Contact content -->
    <section class="section contact-section">
      <div class="container contact-grid">

        <!-- Form -->
        <div class="contact-form-wrapper reveal">
          <h2>Send Us a Message</h2>
          <p class="form-subtitle">We respond within 24 hours on business days.</p>

          <form class="contact-form" @submit.prevent="handleSubmit">
            <div class="form-row">
              <div class="form-group">
                <label>Full Name *</label>
                <input
                  v-model="form.name"
                  type="text"
                  placeholder="John Smith"
                  :class="{ error: errors.name }"
                  required
                />
                <span v-if="errors.name" class="error-msg">{{ errors.name }}</span>
              </div>
              <div class="form-group">
                <label>Email Address *</label>
                <input
                  v-model="form.email"
                  type="email"
                  placeholder="john@company.com"
                  :class="{ error: errors.email }"
                  required
                />
                <span v-if="errors.email" class="error-msg">{{ errors.email }}</span>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Company / Organization</label>
                <input v-model="form.company" type="text" placeholder="Acme Corp" />
              </div>
              <div class="form-group">
                <label>Service Interest</label>
                <select v-model="form.service">
                  <option value="">Select a service...</option>
                  <option value="WAF & API Protection">WAF & API Protection</option>
                  <option value="NetScaler / ADC">NetScaler / ADC</option>
                  <option value="Zero-Trust Architecture">Zero-Trust Architecture</option>
                  <option value="Multicloud Security">Multicloud Security</option>
                  <option value="AI & Automation">AI & Automation</option>
                  <option value="Citrix Virtual Apps & Desktops">Citrix Virtual Apps & Desktops</option>
                  <option value="Other / Discovery Call">Other / Discovery Call</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label>Message *</label>
              <textarea
                v-model="form.message"
                rows="6"
                placeholder="Tell us about your project, environment, or challenge..."
                :class="{ error: errors.message }"
                required
              ></textarea>
              <span v-if="errors.message" class="error-msg">{{ errors.message }}</span>
            </div>

            <!-- Success / Error alert -->
            <div v-if="submitStatus === 'success'" class="alert alert-success">
              <i class="pi pi-check-circle"></i>
              Message sent! We'll be in touch within 24 hours.
            </div>
            <div v-if="submitStatus === 'error'" class="alert alert-error">
              <i class="pi pi-times-circle"></i>
              {{ errorMessage }}
            </div>

            <button type="submit" class="btn btn-primary submit-btn" :disabled="submitting">
              <i :class="submitting ? 'pi pi-spin pi-spinner' : 'pi pi-send'"></i>
              {{ submitting ? 'Sending...' : 'Send Message' }}
            </button>
          </form>
        </div>

        <!-- Info panel -->
        <div class="contact-info reveal reveal-delay-2">
          <div class="info-card">
            <h3>Contact Information</h3>
            <div class="info-items">
              <div class="info-item">
                <div class="info-icon"><i class="pi pi-envelope"></i></div>
                <div>
                  <span class="info-label">Email</span>
                  <a href="mailto:contact@nexxus-tech.com">contact@nexxus-tech.com</a>
                </div>
              </div>
              <div class="info-item">
                <div class="info-icon"><i class="pi pi-globe"></i></div>
                <div>
                  <span class="info-label">Website</span>
                  <span>nexxus-tech.com</span>
                </div>
              </div>
              <div class="info-item">
                <div class="info-icon"><i class="pi pi-map-marker"></i></div>
                <div>
                  <span class="info-label">Global Presence</span>
                  <span>Colombia · UAE · UK · US</span>
                </div>
              </div>
              <div class="info-item">
                <div class="info-icon"><i class="pi pi-check"></i></div>
                <div>
                  <span class="info-label">Availability</span>
                  <span>Remote engagements worldwide</span>
                </div>
              </div>
            </div>

            <div class="social-section">
              <span class="info-label">Social Media</span>
              <div class="social-row">
                <a href="#" class="social-btn" title="LinkedIn (coming soon)">
                  <i class="pi pi-linkedin"></i> LinkedIn
                </a>
                <a href="#" class="social-btn" title="Twitter (coming soon)">
                  <i class="pi pi-twitter"></i> Twitter
                </a>
                <a href="#" class="social-btn" title="GitHub (coming soon)">
                  <i class="pi pi-github"></i> GitHub
                </a>
              </div>
            </div>
          </div>

          <div class="response-card">
            <i class="pi pi-clock"></i>
            <div>
              <strong>Quick Response</strong>
              <p>We typically respond within 24 hours on business days. For urgent security matters, please indicate in your message.</p>
            </div>
          </div>

          <div class="expertise-card">
            <span class="section-label">Areas of Engagement</span>
            <div class="expertise-list">
              <span v-for="item in expertise" :key="item" class="tag">{{ item }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import axios from 'axios'

const form = reactive({ name: '', email: '', company: '', service: '', message: '' })
const errors = reactive({ name: '', email: '', message: '' })
const submitting = ref(false)
const submitStatus = ref('')
const errorMessage = ref('')

const expertise = [
  'WAF Policy Design', 'NetScaler ADC', 'F5 BIG-IP',
  'Zero-Trust', 'Okta / Azure AD', 'AWS Security',
  'Multicloud Security', 'AI Automation', 'Citrix Cloud',
  'DaaS / CVAD', 'GSLB', 'API Security',
]

const validate = () => {
  let valid = true
  errors.name = errors.email = errors.message = ''
  if (!form.name.trim()) { errors.name = 'Name is required'; valid = false }
  if (!form.email.trim() || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(form.email)) {
    errors.email = 'Valid email is required'; valid = false
  }
  if (!form.message.trim() || form.message.length < 10) {
    errors.message = 'Please provide a message (at least 10 characters)'; valid = false
  }
  return valid
}

const handleSubmit = async () => {
  if (!validate()) return
  submitting.value = true
  submitStatus.value = ''
  try {
    await axios.post('/api/contact', { ...form })
    submitStatus.value = 'success'
    form.name = form.email = form.company = form.service = form.message = ''
  } catch (err) {
    submitStatus.value = 'error'
    errorMessage.value = err.response?.data?.detail || 'Something went wrong. Please try emailing us directly.'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.page-hero {
  min-height: 40vh; display: flex; align-items: center;
  background: var(--nt-dark); padding: 120px 0 60px;
  position: relative; overflow: hidden;
}
.page-hero-bg {
  position: absolute; inset: 0;
  background: radial-gradient(ellipse at 40% 60%, rgba(91,79,232,0.12) 0%, transparent 60%);
}
.page-hero-content { position: relative; z-index: 1; }
.page-hero-subtitle { font-size: 1.05rem; color: var(--nt-text-muted); margin-top: 16px; max-width: 540px; line-height: 1.75; }

.contact-section { background: var(--nt-dark-2); }
.contact-grid { display: grid; grid-template-columns: 1fr 420px; gap: 64px; align-items: start; }

/* Form */
.contact-form-wrapper h2 { font-size: 1.7rem; margin-bottom: 8px; }
.form-subtitle { color: var(--nt-text-muted); font-size: 0.9rem; margin-bottom: 32px; }
.contact-form { display: flex; flex-direction: column; gap: 20px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { font-size: 0.8rem; font-weight: 700; font-family: var(--font-heading); letter-spacing: 0.06em; color: var(--nt-text-muted); text-transform: uppercase; }

input, select, textarea {
  background: var(--nt-dark-3);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  padding: 12px 16px;
  color: var(--nt-text);
  font-size: 0.9rem;
  font-family: var(--font-body);
  transition: var(--nt-transition);
  outline: none;
  width: 100%;
}
input::placeholder, textarea::placeholder { color: rgba(255,255,255,0.25); }
input:focus, select:focus, textarea:focus {
  border-color: var(--nt-primary);
  box-shadow: 0 0 0 3px rgba(91,79,232,0.15);
}
input.error, textarea.error { border-color: #EF4444; }
select { appearance: none; cursor: pointer; }
select option { background: var(--nt-dark-3); color: var(--nt-text); }
textarea { resize: vertical; min-height: 140px; }
.error-msg { font-size: 0.78rem; color: #EF4444; }

.alert {
  padding: 14px 18px;
  border-radius: 8px;
  display: flex; align-items: center; gap: 10px;
  font-size: 0.9rem;
}
.alert-success { background: rgba(34,197,94,0.1); border: 1px solid rgba(34,197,94,0.3); color: #4ADE80; }
.alert-error { background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3); color: #FCA5A5; }
.alert .pi { font-size: 1rem; flex-shrink: 0; }

.submit-btn { padding: 14px 32px; font-size: 0.95rem; }
.submit-btn:disabled { opacity: 0.7; cursor: not-allowed; transform: none !important; }

/* Info panel */
.info-card {
  background: var(--nt-card-bg);
  border: 1px solid var(--nt-border);
  border-radius: var(--nt-radius);
  padding: 28px;
  margin-bottom: 20px;
}
.info-card h3 { font-size: 1.1rem; margin-bottom: 24px; }
.info-items { display: flex; flex-direction: column; gap: 20px; margin-bottom: 28px; }
.info-item { display: flex; align-items: flex-start; gap: 14px; }
.info-icon {
  width: 40px; height: 40px;
  background: rgba(91,79,232,0.12);
  border: 1px solid rgba(91,79,232,0.25);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  color: var(--nt-primary-l); flex-shrink: 0;
}
.info-label { display: block; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: var(--nt-text-muted); margin-bottom: 2px; font-family: var(--font-heading); }
.info-item a, .info-item span { font-size: 0.875rem; color: var(--nt-text-light); }
.info-item a:hover { color: var(--nt-secondary); }

.social-section .info-label { margin-bottom: 10px; }
.social-row { display: flex; gap: 8px; flex-wrap: wrap; }
.social-btn {
  display: flex; align-items: center; gap: 6px;
  padding: 7px 14px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 6px;
  color: var(--nt-text-muted); font-size: 0.8rem; font-weight: 600;
  text-decoration: none;
  transition: var(--nt-transition);
}
.social-btn:hover { background: rgba(91,79,232,0.15); border-color: var(--nt-primary); color: var(--nt-primary-l); }

.response-card {
  background: rgba(29,212,180,0.06);
  border: 1px solid rgba(29,212,180,0.2);
  border-radius: var(--nt-radius);
  padding: 20px;
  display: flex; gap: 14px; align-items: flex-start;
  margin-bottom: 20px;
}
.response-card .pi { color: var(--nt-secondary); font-size: 1.1rem; margin-top: 2px; flex-shrink: 0; }
.response-card strong { display: block; color: var(--nt-white); font-size: 0.9rem; margin-bottom: 4px; }
.response-card p { font-size: 0.82rem; color: var(--nt-text-muted); line-height: 1.5; }

.expertise-card {
  background: var(--nt-card-bg);
  border: 1px solid var(--nt-border);
  border-radius: var(--nt-radius);
  padding: 24px;
}
.expertise-list { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }

@media (max-width: 1024px) {
  .contact-grid { grid-template-columns: 1fr; }
  .contact-info { order: -1; }
}
@media (max-width: 640px) {
  .form-row { grid-template-columns: 1fr; }
}
</style>
