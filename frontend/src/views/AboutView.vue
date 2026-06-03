<template>
  <div class="about-page">
    <!-- Hero -->
    <section class="page-hero">
      <div class="page-hero-bg"></div>
      <div class="container page-hero-content">
        <span class="section-label reveal">About Nexxus Tech</span>
        <h1 class="reveal reveal-delay-1">Built by Architects.<br /><span class="gradient-text">Trusted by Leaders.</span></h1>
        <p class="page-hero-subtitle reveal reveal-delay-2">
          We exist to bring principal-level expertise to organizations that need it most —
          from government defense ministries to global financial institutions.
        </p>
      </div>
    </section>

    <!-- Mission -->
    <section class="section section-dark">
      <div class="container">
        <div class="mission-grid">
          <div class="reveal">
            <span class="section-label">Our Mission</span>
            <h2 class="section-title">Connecting Expertise<br />to Complex Problems</h2>
            <p class="section-subtitle">
              Nexxus Tech was founded on a simple premise: the world's most critical infrastructure
              deserves the best security minds, not the most available ones. We specialize in the
              hardest problems — WAF policy at global scale, Zero-Trust for nation-state-level threats,
              and AI automation for infrastructure that never sleeps.
            </p>
            <p class="section-subtitle" style="margin-top:16px">
              With a presence in Colombia, UAE, UK, and the US, we operate remotely but think globally —
              having delivered engagements across 54+ countries and every major industry vertical.
            </p>
          </div>
          <div class="mission-values reveal reveal-delay-2">
            <div v-for="v in values" :key="v.title" class="value-item">
              <div class="value-icon"><i :class="v.icon"></i></div>
              <div>
                <h4>{{ v.title }}</h4>
                <p>{{ v.desc }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Team -->
    <section class="section section-light team-section">
      <div class="container">
        <div class="section-header reveal" style="text-align:center">
          <span class="section-label">The Team</span>
          <h2 class="section-title" style="color:var(--nt-navy)">Meet the Team</h2>
        </div>
        <div class="team-carousel reveal">
          <Carousel
            :value="teamMembers"
            :numVisible="1"
            :numScroll="1"
            :responsiveOptions="teamCarouselOptions"
            circular
            :autoplayInterval="3000"
          >
            <template #item="{ data: member }">
              <div class="team-card">
                <div class="team-card-left">
                  <div class="team-avatar">
                    <span>{{ member.initials }}</span>
                  </div>
                  <div class="team-badges">
                    <span v-for="badge in member.badges" :key="badge.label" class="tag" :class="{ 'tag-teal': badge.highlight }">{{ badge.label }}</span>
                  </div>
                </div>
                <div class="team-card-right">
                  <h2 class="team-name">{{ member.name }}</h2>
                  <p class="team-role">{{ member.role }}</p>
                  <p class="team-tagline">{{ member.tagline }}</p>
                  <p v-for="(paragraph, pIndex) in member.bio" :key="pIndex" class="team-bio" v-html="paragraph"></p>

                  <div v-if="member.certs?.length" class="team-certs">
                    <h4>Certifications</h4>
                    <div class="cert-grid">
                      <div v-for="c in member.certs" :key="c" class="cert-item">
                        <i class="pi pi-verified"></i>
                        <span>{{ c }}</span>
                      </div>
                    </div>
                  </div>

                  <div class="team-skills">
                    <h4>Core Expertise</h4>
                    <div class="skills-grid">
                      <div v-for="skill in member.skills" :key="skill.category" class="skill-group">
                        <span class="skill-category">{{ skill.category }}</span>
                        <div class="skill-tags">
                          <span v-for="t in skill.items" :key="t" class="tag">{{ t }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </template>
          </Carousel>
        </div>
      </div>
    </section>

    <!-- Presence -->
    <section class="section">
      <div class="container">
        <div class="section-header reveal" style="text-align:center">
          <span class="section-label">Global Presence</span>
          <h2 class="section-title">Remote-First. Worldwide Reach.</h2>
          <p class="section-subtitle" style="margin:0 auto">
            With offices and presence in 4 countries and clients in 54+,
            we operate wherever our clients need us — without compromise.
          </p>
        </div>
        <div class="presence-grid">
          <div v-for="p in presence" :key="p.country" class="presence-card card reveal">
            <div class="presence-flag">{{ p.flag }}</div>
            <h3>{{ p.country }}</h3>
            <p>{{ p.desc }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import Carousel from 'primevue/carousel'

const teamCarouselOptions = [
  { breakpoint: '1024px', numVisible: 1, numScroll: 1 },
  { breakpoint: '767px', numVisible: 1, numScroll: 1 },
  { breakpoint: '575px', numVisible: 1, numScroll: 1 },
]

const values = [
  { icon: 'pi pi-star', title: 'Principal-Only Delivery', desc: 'Every engagement is led by a principal-level architect. No juniors, no handoffs.' },
  { icon: 'pi pi-globe', title: 'Global Perspective', desc: 'Having worked in 54+ countries, we understand diverse regulatory and cultural environments.' },
  { icon: 'pi pi-bolt', title: 'AI-First Approach', desc: 'We automate where possible — so your team can focus on what matters.' },
  { icon: 'pi pi-shield', title: 'Security Above All', desc: 'We never recommend solutions that sacrifice security for convenience.' },
]

const teamMembers = [
  {
    initials: 'JP',
    name: 'Juan Pablo Otalvaro',
    role: 'Founder & Principal Cloud & Security Architect',
    tagline: 'Zero-Trust · WAF & API Protection · Multicloud Security · AI & LLM Engineering',
    badges: [
      { label: 'Citrix SME' },
      { label: 'AWS Security', highlight: true },
      { label: 'AI & LLM Engineering' },
    ],
    bio: [
      'Principal Cloud & Security Architect with <strong>15+ years</strong> leading large-scale multicloud, hybrid, and on-premises security transformations across <strong>50+ countries</strong>. Recognized Subject Matter Expert in Web Application Firewall and API protection (Citrix NetScaler/ADC, F5), Zero-Trust Architecture, and secure application delivery for finance, defense, telecom, and government sectors.',
      'Designs, deploys, and customizes <strong>AI and LLM solutions</strong> for production—model selection, guardrails, RAG, and agent workflows integrated with enterprise infrastructure (including JPilot and NetScaler automation). Co-authored NetScaler certification exams (versions 10 and 11), recipient of the <em>Citrix SME of the Year 2013 & 2014</em> award, and a Citrix Education MVP. Delivered security transformations for UAE Ministry of Defense, Barclays, Emirates Airlines, Central Bank of Oman, United Nations, and Smart Dubai.',
    ],
    certs: [
      'AWS Certified Security – Specialty',
      'AWS Solutions Architect – Associate',
      'Citrix SME – Networking & Project Avalon',
      'CCP-AppDS – App Delivery and Security',
      'CCA-AppDS – Citrix Certified Associate',
      'Citrix Certified Specialist – Networking',
      'CCP-N – Citrix Certified Professional Networking',
      'CCI-N – Citrix Certified Instructor Networking',
    ],
    skills: [
      { category: 'Security', items: ['WAF', 'Zero-Trust', 'API Security', 'IAM', 'MFA', 'SASE', 'Bot Management'] },
      { category: 'ADC / Networking', items: ['NetScaler', 'F5 BIG-IP', 'GSLB', 'SD-WAN', 'SSL Offload'] },
      { category: 'Cloud', items: ['AWS', 'Azure', 'Azure AD', 'Okta', 'DUO', 'CSPM'] },
      { category: 'AI & Automation', items: ['LLM Deployment', 'Model Customization', 'RAG & Agents', 'OpenAI', 'Python', 'Node.js', 'Docker'] },
      { category: 'ADC Tooling', items: ['NITRO API', 'GraphQL', 'NetScaler Automation'] },
    ],
  },
  {
    initials: 'JL',
    name: 'Jhonny León',
    role: 'Principal Engineer · Telecom & Cloud Solutions Architect',
    tagline: 'SS7 · Diameter · STP (EAGLE/EPAP) · DSR/DIH · OCI · vPIC · AI Data Modeling',
    badges: [
      { label: 'SS7 & Diameter' },
      { label: 'Oracle Signaling', highlight: true },
      { label: 'OCI & vPIC' },
    ],
    bio: [
      'Telecom &amp; Cloud Solutions Architect with <strong>15+ years</strong> in core networks, signaling (SS7/Diameter), and mission-critical telecom infrastructure. Principal-level specialist in Oracle signaling platforms—STP (EAGLE/EPAP), PIC/vPIC, and DSR/DIH—with a proven record delivering high-impact solutions for Tier-1 operators across Latin America.',
      'As Principal Consultant at Oracle, orchestrated advanced signaling deliveries and led end-to-end <strong>vPIC</strong> deployments on-premises and on <strong>OCI</strong>—including engineering the first vPIC implementation on OCI (OS, middleware, and database). Former Signaling Architect at ICSRED (Interoptics); Oracle technical instructor for Diameter (DSR, DIH, mediation). Key engagements: AT&amp;T Mexico, Claro Colombia, Claro Argentina, Claro Ecuador, and Liberty. Based in Bogotá, Colombia; remote and international delivery.',
    ],
    certs: [
      'Oracle Cloud Infrastructure Foundations (2021)',
      'Scrum Fundamentals Certified (2021)',
      'Telecommunications Engineer – Universidad Católica Andrés Bello (2008)',
      'Oracle Technical Instructor – DSR, DIH & Diameter Mediation (2015)',
    ],
    skills: [
      { category: 'Telecom & Signaling', items: ['SS7', 'Diameter', 'STP (EAGLE)', 'EPAP', 'DSR', 'DIH', 'PIC', 'vPIC'] },
      { category: 'Cloud & Infrastructure', items: ['OCI', 'Cloud Migrations', 'Middleware', 'Database Integration', 'Workload Validation'] },
      { category: 'Architecture & Operations', items: ['Solution Architecture', 'Telecom Core', 'KPIs & Monitoring', 'Incident Management', 'Root Cause Analysis'] },
      { category: 'Emerging Tech', items: ['AI Data Modeling', 'Prompt Validation', 'AI Agent Testing'] },
    ],
  },
  {
    initials: 'VC',
    name: 'Vanessa Cabrera Figueredo',
    role: 'Principal Product Experience Designer · AI & Enterprise UX',
    tagline: 'AI-Driven Experience · Human-Centered Design · Fintech & HealthTech · Data-Informed UX',
    badges: [
      { label: 'AI-Driven UX', highlight: true },
      { label: 'Fintech & Payments' },
      { label: 'Enterprise Platforms' },
    ],
    bio: [
      'Product Experience Designer with <strong>10+ years</strong> of professional experience and <strong>6+ years</strong> specializing in product experience and digital product design. Expert in Design Thinking, AI-enabled experiences, and data-informed UX across payments, fintech, healthtech, proptech, and enterprise platforms—translating complex systems into clear experience strategies and actionable concepts that drive business outcomes.',
      'Led human-centered digital experiences at Publicis Sapient for global enterprise clients including Invesco and Verizon, designing GenAI-powered workflows and data-intensive financial platforms. At Osigu, owned product experience strategy for RCM and payments SaaS across LATAM—including a Visa healthcare payments partnership and a payments platform that increased processing efficiency by <strong>40%</strong>. At Nueva EPS, designed experiences impacting <strong>8+ million users</strong> and raised NPS to <strong>80+</strong>. Based in Colombia; bilingual (Spanish native, English C1).',
    ],
    certs: [
      'Certified Scrum Master (2020)',
      'Customer Experience Certification – Umuntu (2020)',
      "Master's Degree in Design & Innovation – IED (2019)",
      'Postgraduate Degree in Design Management – Universidad Jorge Tadeo Lozano (2016)',
    ],
    skills: [
      { category: 'Product & UX', items: ['Product Experience Strategy', 'Design Thinking', 'Service Design', 'Visual Storytelling', 'Prototyping'] },
      { category: 'AI & Data', items: ['AI-Driven Experience Design', 'GenAI Workflows', 'Data-Informed Design', 'Decision Support UX'] },
      { category: 'Domains', items: ['Fintech', 'Payments', 'HealthTech', 'PropTech', 'Enterprise Platforms'] },
      { category: 'Tools & Leadership', items: ['Figma', 'Miro', 'Design Systems', 'Cross-Functional Leadership', 'Jira', 'Confluence'] },
    ],
  },
]

const presence = [
  { flag: '🇨🇴', country: 'Colombia', desc: 'Headquarters and primary engineering base. Deep LATAM network and Spanish/Portuguese-speaking engagements.' },
  { flag: '🇦🇪', country: 'UAE', desc: 'Middle East hub. Extensive experience with UAE government, financial, and telecom sectors.' },
  { flag: '🇬🇧', country: 'United Kingdom', desc: 'European base for EMEA engagements. Strong relationships with UK financial and defense clients.' },
  { flag: '🇺🇸', country: 'United States', desc: 'North American presence for Fortune 500 and government clients. Remote-capable nationwide.' },
]
</script>

<style scoped>
.page-hero {
  min-height: 45vh;
  display: flex; align-items: center;
  background: var(--nt-dark);
  padding: 120px 0 60px;
  position: relative; overflow: hidden;
}
.page-hero-bg {
  position: absolute; inset: 0;
  background: radial-gradient(ellipse at 70% 50%, rgba(0,123,167,0.15) 0%, transparent 60%);
}
.page-hero-content { position: relative; z-index: 1; max-width: 700px; }
.page-hero-subtitle { font-size: 1.1rem; color: var(--nt-text-muted); margin-top: 16px; max-width: 560px; line-height: 1.75; }

.mission-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 80px; align-items: start; }
.mission-values { display: flex; flex-direction: column; gap: 24px; }
.value-item { display: flex; gap: 16px; align-items: flex-start; }
.value-icon {
  width: 44px; height: 44px; border-radius: 12px;
  background: rgba(0,123,167,0.12);
  border: 1px solid rgba(0,123,167,0.25);
  display: flex; align-items: center; justify-content: center;
  color: var(--nt-primary-l); font-size: 1rem; flex-shrink: 0;
}
.value-item h4 { font-size: 0.95rem; margin-bottom: 4px; }
.value-item p { font-size: 0.875rem; color: var(--nt-text-muted); }

.team-section { background: var(--nt-light-bg); }
.team-carousel { margin-top: 48px; }
.team-carousel :deep(.p-carousel-content-container) { overflow: visible; }
.team-carousel :deep(.p-carousel-item) { flex: 1 0 100%; }
.team-carousel :deep(.p-carousel-prev-button),
.team-carousel :deep(.p-carousel-next-button) {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: white;
  border: 1px solid #E2E8F0;
  color: var(--nt-primary);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  transition: var(--nt-transition);
}
.team-carousel :deep(.p-carousel-prev-button:hover),
.team-carousel :deep(.p-carousel-next-button:hover) {
  background: var(--nt-primary);
  color: white;
  border-color: var(--nt-primary);
}
.team-carousel :deep(.p-carousel-indicator-list) { margin-top: 24px; gap: 8px; }
.team-carousel :deep(.p-carousel-indicator-button) {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #CBD5E1;
  transition: var(--nt-transition);
}
.team-carousel :deep(.p-carousel-indicator-active .p-carousel-indicator-button) {
  background: var(--nt-primary);
  width: 28px;
  border-radius: 5px;
}
.team-card {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 48px;
  background: white;
  border: 1px solid #E2E8F0;
  border-radius: var(--nt-radius-lg);
  padding: 48px;
  box-shadow: 0 4px 32px rgba(0,0,0,0.08);
}
.team-card-left { display: flex; flex-direction: column; align-items: center; gap: 20px; }
.team-avatar {
  width: 140px; height: 140px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--nt-primary), var(--nt-secondary));
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-heading);
  font-size: 2.5rem;
  font-weight: 900;
  color: white;
  box-shadow: 0 8px 32px rgba(0,123,167,0.35);
}
.team-badges { display: flex; flex-direction: column; gap: 8px; align-items: center; }
.team-name { font-size: 1.8rem; color: var(--nt-navy); margin-bottom: 4px; }
.team-role { font-size: 1rem; font-weight: 600; color: var(--nt-primary); margin-bottom: 4px; }
.team-tagline { font-size: 0.82rem; color: #64748B; margin-bottom: 20px; letter-spacing: 0.03em; }
.team-bio { font-size: 0.9rem; color: #374151; line-height: 1.75; margin-bottom: 12px; }
.team-bio strong { color: var(--nt-navy); }
.team-certs { margin-top: 24px; }
.team-certs h4, .team-skills h4 { font-size: 0.85rem; font-weight: 700; color: var(--nt-navy); margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.1em; }
.cert-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 24px; }
.cert-item { display: flex; align-items: center; gap: 8px; font-size: 0.8rem; color: #374151; }
.cert-item .pi { color: var(--nt-primary); font-size: 0.8rem; flex-shrink: 0; }
.skills-grid { display: flex; flex-direction: column; gap: 12px; }
.skill-group { display: flex; flex-direction: column; gap: 6px; }
.skill-category { font-size: 0.72rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.12em; }
.skill-tags { display: flex; flex-wrap: wrap; gap: 6px; }

.presence-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-top: 48px; }
.presence-card { text-align: center; }
.presence-flag { font-size: 2.5rem; margin-bottom: 12px; }
.presence-card h3 { font-size: 1.1rem; margin-bottom: 8px; }
.presence-card p { font-size: 0.875rem; color: var(--nt-text-muted); line-height: 1.6; }

@media (max-width: 1024px) {
  .mission-grid { grid-template-columns: 1fr; gap: 48px; }
  .team-card { grid-template-columns: 1fr; }
  .team-card-left { flex-direction: row; justify-content: flex-start; align-items: center; }
  .presence-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 640px) {
  .team-card { padding: 32px 24px; }
  .cert-grid { grid-template-columns: 1fr; }
  .presence-grid { grid-template-columns: 1fr; }
}
</style>
