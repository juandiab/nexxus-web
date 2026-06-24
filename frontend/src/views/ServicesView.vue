<template>
  <div class="services-page">
    <!-- Page Hero -->
    <section class="page-hero">
      <div class="page-hero-bg"></div>
      <div class="container page-hero-content">
        <span class="section-label reveal">Our Expertise</span>
        <h1 class="reveal reveal-delay-1">Expert Security &amp;<br /><span class="gradient-text">Delivery Services</span></h1>
        <p class="page-hero-subtitle reveal reveal-delay-2">
          From WAF policy design to AI-driven infrastructure automation —
          every engagement delivered at the principal architect level.
        </p>
      </div>
    </section>

    <!-- Services detail -->
    <section v-for="svc in services" :key="svc.id" :id="svc.id" class="section service-detail" :class="svc.light ? 'section-light' : ''">
      <div class="container">
        <div class="service-detail-grid" :class="{ reverse: svc.reverse }">
          <div class="service-detail-text reveal">
            <div class="service-detail-icon" :class="`service-accent-${svc.id}`">
              <i :class="svc.icon"></i>
            </div>
            <span class="section-label">{{ svc.label }}</span>
            <h2 class="section-title">{{ svc.title }}</h2>
            <p class="section-subtitle">{{ svc.desc }}</p>
            <div class="service-features">
              <div v-for="f in svc.features" :key="f" class="feature-item">
                <i class="pi pi-check-circle"></i>
                <span>{{ f }}</span>
              </div>
            </div>
            <div class="service-tags">
              <span v-for="t in svc.tags" :key="t" class="tag">{{ t }}</span>
            </div>
            <RouterLink to="/contact" class="btn btn-primary">
              Get a Consultation <i class="pi pi-arrow-right"></i>
            </RouterLink>
          </div>
          <div class="service-detail-visual reveal reveal-delay-2">
            <div class="visual-card">
              <div class="visual-header" :class="`service-accent-${svc.id}`">
                <i :class="svc.icon" class="visual-icon"></i>
                <h3>{{ svc.title }}</h3>
              </div>
              <div class="visual-metrics">
                <div v-for="m in svc.metrics" :key="m.label" class="metric">
                  <span class="metric-value">{{ m.value }}</span>
                  <span class="metric-label">{{ m.label }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="section cta-section">
      <div class="container">
        <div class="cta-box reveal">
          <div class="cta-glow"></div>
          <span class="section-label">Ready to Start?</span>
          <h2>Not sure which service you need?</h2>
          <p>Let's have a discovery call. We'll assess your environment and recommend the right approach — no obligation.</p>
          <RouterLink to="/contact" class="btn btn-primary">
            <i class="pi pi-calendar"></i> Book a Free Discovery Call
          </RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
const services = [
  {
    id: 'waf',
    label: 'WAF & API Protection',
    icon: 'pi pi-shield',
    iconBg: 'linear-gradient(135deg,#007BA7,#005F7F)',
    light: false,
    reverse: false,
    title: 'Web Application Firewall & API Protection',
    desc: 'Enterprise-grade WAF deployment, policy design, and continuous tuning for Citrix NetScaler ADC and F5 BIG-IP. We protect web applications and APIs at global scale — from OWASP Top 10 mitigation to sophisticated bot management and API gateway security.',
    features: [
      'OWASP Top 10 protection (SQL injection, XSS, CSRF, and more)',
      'Bot management with device fingerprinting and CAPTCHA enforcement',
      'API gateway security with OpenAPI schema validation',
      'Rate-limiting and DDoS mitigation at the ADC layer',
      'Custom signature development for application-specific threats',
      'WAF policy tuning to minimize false positives',
      'Response body inspection to prevent data leakage',
    ],
    tags: ['NetScaler WAF', 'F5 BIG-IP', 'OWASP', 'Bot Management', 'API Security', 'DDoS'],
    metrics: [
      { value: '99.9%', label: 'Threat Detection Rate' },
      { value: '<1%', label: 'False Positive Rate' },
      { value: '100+', label: 'WAF Deployments' },
    ],
  },
  {
    id: 'netscaler',
    label: 'Application Delivery Controllers',
    icon: 'pi pi-server',
    iconBg: 'linear-gradient(135deg,#007BA7,#005F7F)',
    light: true,
    reverse: true,
    title: 'NetScaler ADC & Application Delivery',
    desc: 'Full lifecycle Citrix NetScaler (ADC) services from architecture design to hands-on deployment — including large-scale platform migrations between F5 BIG-IP and NetScaler in either direction. As a Citrix-recognized SME and co-author of NetScaler certification exams, we bring unmatched depth to every engagement.',
    features: [
      'High-availability clustering (active-active, active-passive)',
      'SSL/TLS offloading and certificate management',
      'Global Server Load Balancing (GSLB) and multi-site failover',
      'Content switching and traffic steering policies',
      'NetScaler Gateway for secure remote access',
      'Citrix ADM integration for centralized management',
      'F5 BIG-IP ↔ NetScaler ADC migrations (bidirectional)',
      'Legacy load balancer transitions with WAF/LTM policy translation',
      'Parallel-run cutover planning for minimal service impact',
    ],
    tags: ['NetScaler', 'F5 BIG-IP', 'ADC Migration', 'GSLB', 'SSL Offload', 'Citrix Gateway'],
    metrics: [
      { value: 'SME', label: 'Citrix Recognized Expert' },
      { value: '200+', label: 'NetScaler Deployments' },
      { value: '50+', label: 'ADC Platform Migrations' },
    ],
  },
  {
    id: 'zerotrust',
    label: 'Zero-Trust Architecture',
    icon: 'pi pi-lock',
    iconBg: 'linear-gradient(135deg,#007BA7,#007BA7)',
    light: false,
    reverse: false,
    title: 'Zero-Trust Architecture & IAM',
    desc: 'End-to-end Zero-Trust transformations proven across finance, defense, and government. We combine NetScaler Gateway, Okta, Azure AD, and DUO into a unified, continuously-verifying security framework that eliminates implicit trust.',
    features: [
      'Identity federation: Okta + Azure AD + NetScaler Gateway',
      'Conditional access policy design and enforcement',
      'Multi-Factor Authentication (MFA) for all access paths',
      'Privileged Access Management (PAM) integration',
      'Endpoint Analysis (EPA) and device compliance',
      'SASE architecture consulting and design',
      'BeyondCorp-style network segmentation',
    ],
    tags: ['Zero-Trust', 'Okta', 'Azure AD', 'DUO', 'MFA', 'PAM', 'SASE'],
    metrics: [
      { value: '94%', label: 'Reduction in Unauthorized Access' },
      { value: '100%', label: 'VPN Elimination (case study)' },
      { value: '30+', label: 'ZTA Implementations' },
    ],
  },
  {
    id: 'cloud',
    label: 'Cloud & Multicloud Security',
    icon: 'pi pi-cloud',
    iconBg: 'linear-gradient(135deg,#38383D,#007BA7)',
    light: true,
    reverse: true,
    title: 'Multicloud Security Architecture',
    desc: 'Consistent security posture across AWS, Azure, and on-premises with NetScaler as the unified application delivery and security layer. AWS Security Specialty certified — we know both the cloud-native and ADC-based approaches.',
    features: [
      'AWS Security architecture (VPC, WAF v2, Shield, GuardDuty)',
      'Azure security design (Application Gateway, Front Door, NSGs)',
      'NetScaler VPX deployment on AWS and Azure Marketplace',
      'Cloud Security Posture Management (CSPM)',
      'Unified WAF policy management across clouds via Citrix ADM',
      'Cloud-native identity federation and IAM hardening',
      'Cost-optimized security architecture for e2-micro to enterprise',
    ],
    tags: ['AWS', 'Azure', 'NetScaler VPX', 'CSPM', 'Cloud WAF', 'Multicloud'],
    metrics: [
      { value: 'AWS', label: 'Security Specialty Certified' },
      { value: '3', label: 'Cloud Platforms Supported' },
      { value: '40+', label: 'Cloud Security Projects' },
    ],
  },
  {
    id: 'ai',
    label: 'AI & Automation',
    icon: 'pi pi-bolt',
    iconBg: 'linear-gradient(135deg,#007BA7,#007BA7)',
    light: false,
    reverse: false,
    title: 'AI-Powered Infrastructure & Automation',
    desc: 'Practical AI-assisted NetScaler administration, WAF policy drafting, and automation you can run in your environment—with human review, audit trails, and credentials kept on your side of the boundary.',
    features: [
      'WAF profile drafts from OpenAPI specs (reviewed before apply)',
      'Log analysis assistance and false-positive triage workflows',
      'Configuration drift checks with approval-gated remediation',
      'LLM-assisted runbooks grounded in NITRO / Next-Gen API syntax',
      'Python automation for NetScaler NITRO and Next-Gen API',
      'Slack/Teams hooks for notifications and guided diagnostics',
      'Scoped copilots (e.g. JPilot) with confirm-before-change guardrails',
    ],
    tags: ['Python', 'LLM', 'NITRO API', 'OpenAI', 'Automation', 'DevSecOps'],
    metrics: [
      { value: 'Review', label: 'Changes Approved Before Apply' },
      { value: 'Local', label: 'ADC Credentials Stay On-Prem' },
      { value: 'Pilot', label: 'Scoped Rollouts Per Engagement' },
    ],
  },
]
</script>

<style scoped>
.page-hero {
  min-height: 45vh;
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
  background: var(--nt-dark);
  padding: 120px 0 60px;
}
.page-hero-bg {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 30% 50%, rgba(0,123,167,0.15) 0%, transparent 65%);
}
.page-hero-content { position: relative; z-index: 1; max-width: 700px; }
.page-hero-subtitle {
  font-size: 1.1rem;
  color: var(--nt-text-muted);
  margin-top: 16px;
  max-width: 560px;
  line-height: 1.75;
}

.service-detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: center;
}
.service-detail-grid.reverse { direction: rtl; }
.service-detail-grid.reverse > * { direction: ltr; }

.service-detail-icon {
  width: 60px; height: 60px;
  border-radius: 16px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.6rem;
  color: white;
  margin-bottom: 20px;
}
.section-title { margin-bottom: 16px; }
.section-subtitle { margin-bottom: 28px; }

.service-features { margin-bottom: 24px; display: flex; flex-direction: column; gap: 10px; }
.feature-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.9rem;
  color: var(--nt-text-light);
}
.feature-item .pi { color: var(--nt-secondary); font-size: 0.85rem; flex-shrink: 0; }
.section-light .feature-item { color: #374151; }
.service-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 28px; }

.visual-card {
  background: var(--nt-card-bg);
  border: 1px solid var(--nt-border);
  border-radius: var(--nt-radius-lg);
  overflow: hidden;
}
.section-light .visual-card { background: white; border-color: #E2E8F0; }
.visual-header {
  padding: 32px;
  display: flex;
  align-items: center;
  gap: 16px;
}
.visual-icon { font-size: 2rem; color: white; }
.visual-header h3 { color: white; font-size: 1.2rem; margin: 0; }
.visual-metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0;
  padding: 0;
}
.metric {
  text-align: center;
  padding: 28px 16px;
  border-right: 1px solid var(--nt-border);
  border-top: 1px solid var(--nt-border);
}
.metric:last-child { border-right: none; }
.section-light .metric { border-color: #E2E8F0; }
.metric-value {
  display: block;
  font-family: var(--font-heading);
  font-size: 1.6rem;
  font-weight: 900;
  background: linear-gradient(135deg, var(--nt-primary-l), var(--nt-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 4px;
}
.metric-label { font-size: 0.75rem; color: var(--nt-text-muted); font-weight: 600; font-family: var(--font-heading); }
.section-light .metric-label { color: #64748B; }

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
  position: absolute; top: -60px; left: 50%;
  transform: translateX(-50%);
  width: 300px; height: 150px;
  background: radial-gradient(ellipse, rgba(0,123,167,0.2) 0%, transparent 70%);
  pointer-events: none;
}
.cta-box h2 { margin: 12px 0 16px; }
.cta-box p { color: var(--nt-text-muted); max-width: 500px; margin: 0 auto 32px; }

@media (max-width: 1024px) {
  .service-detail-grid { grid-template-columns: 1fr; gap: 40px; }
  .service-detail-grid.reverse { direction: ltr; }
}
@media (max-width: 640px) {
  .cta-box { padding: 40px 24px; }
  .visual-metrics { grid-template-columns: 1fr; }
  .metric { border-right: none; }
}
</style>
