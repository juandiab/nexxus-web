<template>
  <div class="home">
    <!-- ── HERO ─────────────────────────────────────────────────────────────── -->
    <section class="hero">
      <canvas ref="heroCanvas" class="hero-canvas" aria-hidden="true"></canvas>
      <div class="hero-overlay"></div>
      <div class="container hero-content">
        <div class="hero-badge nx-badge reveal">
          <span class="glow-dot"></span>
          <span>Trusted by Fortune 500 &amp; Government Agencies Worldwide</span>
        </div>
        <h1 class="hero-title reveal reveal-delay-1">
          Securing the World's<br />
          <span class="gradient-text">Most Critical Applications</span>
        </h1>
        <p class="hero-subtitle reveal reveal-delay-2">
          Enterprise cloud, cybersecurity, and AI consulting for CTOs who can't afford downtime.
        </p>
        <p class="hero-subtitle-sub reveal reveal-delay-2">
          Principal-led engagements across <strong>20+ countries</strong> — from Zero-Trust rollouts to AI-driven NetScaler operations.
        </p>
        <p class="hero-prompt reveal reveal-delay-2" aria-hidden="true">
          <span class="hero-prompt-prefix">$</span> nexxus deploy --secure --scale global
        </p>
        <div class="hero-actions reveal reveal-delay-3">
          <RouterLink to="/services" class="btn btn-primary nx-btn nx-btn--primary">
            <i class="pi pi-shield"></i> Explore Services
          </RouterLink>
          <RouterLink to="/contact" class="btn btn-secondary nx-btn nx-btn--ghost">
            <i class="pi pi-send"></i> Start a Project
          </RouterLink>
        </div>
        <div class="hero-tech-stack reveal reveal-delay-4">
          <span class="tech-label">SPECIALIZED IN</span>
          <div class="tech-pills">
            <span class="tech-pill nx-badge">NetScaler WAF</span>
            <span class="tech-pill nx-badge">F5 BIG-IP</span>
            <span class="tech-pill nx-badge">Zero-Trust</span>
            <span class="tech-pill nx-badge">AWS Security</span>
            <span class="tech-pill nx-badge">Azure AD</span>
            <span class="tech-pill nx-badge">Okta</span>
            <span class="tech-pill nx-badge">AI Automation</span>
          </div>
        </div>
      </div>
      <div class="hero-scroll-hint">
        <span>Scroll</span>
        <div class="scroll-line"></div>
      </div>
    </section>

    <!-- ── STATS ──────────────────────────────────────────────────────────────── -->
    <section class="stats-bar">
      <div class="container">
        <div class="stats-grid">
          <div v-for="stat in stats" :key="stat.label" class="stat-item reveal">
            <span class="stat-value">{{ stat.value }}</span>
            <span class="stat-label">{{ stat.label }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ── SERVICES OVERVIEW ──────────────────────────────────────────────────── -->
    <section class="section nx-section services-section nx-grid-bg">
      <div class="container">
        <div class="section-header reveal">
          <span class="nx-eyebrow">What We Do</span>
          <h2 class="section-title">Expert-Level Security &amp; Delivery</h2>
          <p class="section-subtitle">
            From WAF policy design to AI-powered administration, we bring
            principal-architect expertise to every engagement.
          </p>
        </div>
        <div class="services-grid">
          <div
            v-for="(svc, i) in services"
            :key="svc.id"
            :class="`nx-card service-card reveal reveal-delay-${(i % 4) + 1}`"
            @click="$router.push(`/services#${svc.serviceHash || svc.id}`)"
          >
            <div class="service-icon">
              <i :class="svc.icon"></i>
            </div>
            <h3 class="service-title">{{ svc.title }}</h3>
            <p class="service-desc">{{ svc.desc }}</p>
            <div class="service-tags">
              <span v-for="tag in svc.tags" :key="tag" class="tag nx-badge">{{ tag }}</span>
            </div>
            <span class="service-arrow">
              Learn more <i class="pi pi-arrow-right"></i>
            </span>
          </div>
        </div>
        <div class="services-cta reveal">
          <RouterLink to="/services" class="btn btn-outline nx-btn nx-btn--ghost">
            View All Services <i class="pi pi-arrow-right"></i>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- ── PRODUCTS ───────────────────────────────────────────────────────────── -->
    <section class="section nx-section nx-section--navy products-section">
      <div class="container">
        <div class="section-header reveal section-header-center">
          <span class="nx-eyebrow">Our Products</span>
          <h2 class="section-title">Technology That Empowers</h2>
          <p class="section-subtitle section-subtitle-center">
            Tools that serve as a bridge between people, knowledge, and technology—
            so engineers can learn, grow, and move forward with confidence.
          </p>
        </div>
        <div
          v-for="product in products"
          :key="product.id"
          class="product-feature-card nx-card reveal"
          @click="$router.push(`/products#${product.id}`)"
        >
          <div class="product-feature-glow"></div>
          <div class="product-feature-grid">
        <div class="product-feature-logo-wrap">
              <JpilotLogo variant="compact" title-tag="span" />
        </div>
            <div class="product-feature-body">
              <span class="nx-eyebrow">{{ product.label }}</span>
              <h3 class="product-feature-title">
                {{ product.name }}
                <span class="product-version">{{ product.edition }}</span>
              </h3>
              <p class="product-feature-tagline">{{ product.tagline }}</p>
              <p class="product-feature-desc">{{ product.excerpt }}</p>
              <div class="product-feature-tags">
                <span v-for="tag in product.tags.slice(0, 4)" :key="tag" class="tag nx-badge">{{ tag }}</span>
              </div>
            </div>
          </div>
          <div class="product-feature-specs">
            <span v-for="m in product.metrics" :key="m.label" class="nx-badge product-spec-chip">
              {{ m.value }} {{ m.label }}
            </span>
          </div>
          <span class="product-feature-arrow">
            Explore {{ product.name }} <i class="pi pi-arrow-right"></i>
          </span>
        </div>
        <div class="products-cta reveal">
          <RouterLink to="/products" class="btn btn-outline nx-btn nx-btn--ghost">
            View All Products <i class="pi pi-arrow-right"></i>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- ── WHY NEXXUS TECH ────────────────────────────────────────────────────── -->
    <section class="section nx-section nx-section--raised why-section">
      <div class="container">
        <div class="why-grid">
          <div class="why-left reveal">
            <span class="nx-eyebrow">Why Nexxus Tech</span>
            <h2 class="section-title">
              Principals Who<br />
              <span class="highlight">Show Up &amp; Stay.</span>
            </h2>
            <p class="section-subtitle">
              We don't send juniors. Every engagement is led by a principal architect
              who works alongside your team — not above it. We've spent years in the
              trenches of complex security and infrastructure work, and we believe
              that expertise means little unless it helps people learn, grow, and
              move forward with confidence.
            </p>
            <div class="why-list">
              <div v-for="item in whyItems" :key="item.title" class="why-item">
                <div class="why-check"><i class="pi pi-check"></i></div>
                <div>
                  <strong>{{ item.title }}</strong>
                  <p>{{ item.desc }}</p>
                </div>
              </div>
            </div>
            <RouterLink to="/about" class="btn btn-primary nx-btn nx-btn--primary">
              Meet the Team <i class="pi pi-arrow-right"></i>
            </RouterLink>
          </div>
          <div class="why-right reveal reveal-delay-2">
            <div class="globe-card nx-card nx-grid-bg">
              <div class="globe-header">
                <span class="nx-eyebrow">Global Reach</span>
                <h3>20+ Countries.<br/>One Standard of Excellence.</h3>
              </div>
              <div class="regions-grid">
                <div v-for="region in regions" :key="region.name" class="region-item">
                  <i :class="region.icon"></i>
                  <div>
                    <strong>{{ region.name }}</strong>
                    <span>{{ region.clients }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── INDUSTRIES / KEY CLIENTS ───────────────────────────────────────────── -->
    <section class="section nx-section clients-section">
      <div class="container">
        <div class="section-header reveal section-header-center">
          <span class="nx-eyebrow">Key Engagements</span>
          <h2 class="section-title">Trusted by Industry Leaders</h2>
          <p class="section-subtitle section-subtitle-center">
            Delivered security transformations for organizations across
            government, defense, finance, telecom, and aviation.
          </p>
        </div>
        <div class="industries-grid">
          <div
            v-for="ind in industries"
            :key="ind.sector"
            class="industry-card reveal"
          >
            <div class="industry-icon">
              <i :class="ind.icon"></i>
            </div>
            <h3>{{ ind.sector }}</h3>
            <p>{{ ind.clients }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── BLOG PREVIEW ───────────────────────────────────────────────────────── -->
    <section class="section nx-section nx-section--raised blog-preview-section">
      <div class="container">
        <div class="section-header-row reveal">
          <div>
            <span class="nx-eyebrow">Latest Insights</span>
            <h2 class="section-title">From the Nexxus Tech Blog</h2>
          </div>
          <RouterLink to="/blog" class="btn btn-outline nx-btn nx-btn--ghost">
            All Posts <i class="pi pi-arrow-right"></i>
          </RouterLink>
        </div>
        <div class="blog-grid">
          <template v-if="blogLoading">
            <article
              v-for="n in 3"
              :key="`skeleton-${n}`"
              class="nx-card blog-card blog-card-skeleton"
              aria-hidden="true"
            >
              <div class="blog-card-header blog-card-skeleton-header"></div>
              <div class="blog-card-body">
                <div class="skeleton-line skeleton-line--title"></div>
                <div class="skeleton-line"></div>
                <div class="skeleton-line"></div>
                <div class="skeleton-line skeleton-line--short"></div>
              </div>
            </article>
          </template>
          <template v-else-if="blogPosts.length">
            <article
              v-for="(post, i) in blogPosts"
              :key="post.id"
              :class="`nx-card blog-card reveal reveal-delay-${i + 1}`"
              @click="$router.push(`/blog/${post.slug}`)"
            >
              <div class="blog-card-header" :class="coverColorClass(post.cover_color)">
                <span class="tag tag-on-cover">{{ post.category }}</span>
              </div>
              <div class="blog-card-body">
                <h3 class="blog-title">{{ post.title }}</h3>
                <p class="blog-excerpt">{{ post.excerpt }}</p>
                <div class="blog-meta">
                  <span><i class="pi pi-clock"></i> {{ post.read_time }} min read</span>
                  <span><i class="pi pi-calendar"></i> {{ formatDate(post.date) }}</span>
                </div>
              </div>
            </article>
          </template>
        </div>
      </div>
    </section>

    <!-- ── CTA ────────────────────────────────────────────────────────────────── -->
    <section class="section nx-section cta-section nx-grid-bg">
      <div class="container">
        <div class="cta-box reveal">
          <div class="cta-glow"></div>
          <span class="nx-eyebrow">Ready to Get Started?</span>
          <h2 class="cta-title">
            Let's Secure Your<br />Infrastructure Together
          </h2>
          <p class="cta-desc">
            Whether you need a WAF deployment, a Zero-Trust roadmap, or AI-powered
            NetScaler automation — we're ready to help. Remote engagements worldwide.
          </p>
          <div class="cta-actions">
            <GlowButton variant="primary">
              <RouterLink to="/contact" class="btn btn-primary nx-btn nx-btn--primary">
                <i class="pi pi-send"></i> Start a Conversation
              </RouterLink>
            </GlowButton>
            <GlowButton variant="outline">
              <a href="mailto:contact@nexxus-tech.com" class="btn btn-outline nx-btn nx-btn--ghost">
                <i class="pi pi-envelope"></i> contact@nexxus-tech.com
              </a>
            </GlowButton>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import { products } from '@/data/products.js'
import { coverColorClass } from '@/utils/coverColor.js'
import JpilotLogo from '@/components/shared/JpilotLogo.vue'
import GlowButton from '@/components/shared/GlowButton.vue'

const heroCanvas = ref(null)
const blogPosts = ref([])
const blogLoading = ref(true)

// ── Stats ─────────────────────────────────────────────────────────────────────
const stats = [
  { value: '15+',  label: 'Years of Experience' },
  { value: '20+',  label: 'Countries Served' },
  { value: '100+', label: 'Projects Delivered' },
  { value: '100%', label: 'Remote Capable' },
]

// ── Services ──────────────────────────────────────────────────────────────────
const services = [
  {
    id: 'waf',
    icon: 'pi pi-shield',
    bg: 'linear-gradient(135deg,rgba(0,123,167,0.2),rgba(0,123,167,0.05))',
    title: 'WAF & API Protection',
    desc: 'Enterprise-grade Web Application Firewall design, deployment, and tuning for NetScaler ADC and F5 BIG-IP. Bot management, OWASP Top 10, and API gateway security.',
    tags: ['NetScaler WAF', 'F5', 'OWASP', 'Bot Management'],
  },
  {
    id: 'netscaler',
    icon: 'pi pi-server',
    bg: 'linear-gradient(135deg,rgba(0,168,224,0.18),rgba(0,168,224,0.04))',
    title: 'NetScaler / ADC',
    desc: 'Full lifecycle NetScaler ADC services — high availability, SSL offload, GSLB, content switching, and performance optimization at any scale.',
    tags: ['NetScaler', 'ADC', 'GSLB', 'SSL Offload'],
  },
  {
    id: 'zerotrust',
    icon: 'pi pi-lock',
    bg: 'linear-gradient(135deg,rgba(0,123,167,0.2),rgba(0,168,224,0.08))',
    title: 'Zero-Trust Architecture',
    desc: 'End-to-end Zero-Trust transformations combining NetScaler Gateway, Okta, Azure AD, and DUO — proven across Fortune 500 and government deployments.',
    tags: ['Zero-Trust', 'Okta', 'Azure AD', 'DUO'],
  },
  {
    id: 'cloud',
    icon: 'pi pi-cloud',
    bg: 'linear-gradient(135deg,rgba(56,56,61,0.5),rgba(0,123,167,0.1))',
    title: 'Multicloud Security',
    desc: 'Unified security posture across AWS, Azure, and on-premises. Cloud Security Posture Management, cloud-native WAF, and secure access service edge (SASE).',
    tags: ['AWS', 'Azure', 'CSPM', 'SASE'],
  },
  {
    id: 'ai',
    icon: 'pi pi-bolt',
    bg: 'linear-gradient(135deg,rgba(0,168,224,0.18),rgba(0,123,167,0.12))',
    title: 'AI & Automation',
    desc: 'AI-powered NetScaler administration, automated WAF policy generation, configuration drift detection, and LLM-driven security operations.',
    tags: ['Python', 'LLM', 'NITRO API', 'Automation'],
  },
  {
    id: 'adc-migrations',
    serviceHash: 'netscaler',
    icon: 'pi pi-arrow-right-arrow-left',
    bg: 'linear-gradient(135deg,rgba(0,123,167,0.15),rgba(38,38,42,0.3))',
    title: 'ADC Platform Migrations',
    desc: '50+ technology migrations between F5 BIG-IP and NetScaler ADC — either direction — plus legacy load balancer transitions, WAF/LTM policy porting, and parallel-run cutovers.',
    tags: ['F5 BIG-IP', 'NetScaler', 'ADC Migration', 'WAF Policy'],
  },
]

// ── Why items ─────────────────────────────────────────────────────────────────
const whyItems = [
  { title: 'Principal-Only Delivery', desc: 'You work directly with the architects who design and deliver the solution — no handoffs, no layers in between.' },
  { title: 'Knowledge Shared Openly', desc: "We don't hoard expertise. We explain, document, and transfer what we know so your team is stronger when we step away." },
  { title: 'People Before Platforms', desc: "A successful engagement isn't just a working system — it's a team that feels more capable and confident facing what comes next." },
  { title: 'AI That Amplifies You', desc: 'We use automation and AI to support human judgment — freeing your specialists to focus on the decisions that actually matter.' },
]

// ── Regions ───────────────────────────────────────────────────────────────────
const regions = [
  { name: 'Middle East',     icon: 'pi pi-map-marker', clients: 'UAE MoD, Emirates, Central Bank of Oman' },
  { name: 'Europe',          icon: 'pi pi-map-marker', clients: 'Barclays, Virgin Atlantic, Ministry of Defense Italy' },
  { name: 'North America',   icon: 'pi pi-map-marker', clients: 'United Nations, IBM, CME Group, Fiserv' },
  { name: 'Latin America',   icon: 'pi pi-map-marker', clients: 'Banco Colpatria, Davivienda, Oi Telecom' },
  { name: 'Africa',          icon: 'pi pi-map-marker', clients: 'MTN South Africa' },
  { name: 'Asia-Pacific',    icon: 'pi pi-map-marker', clients: 'Ooredoo Qatar, TurkCell, PDO Oman' },
]

// ── Industries ────────────────────────────────────────────────────────────────
const industries = [
  { sector: 'Government & Defense', icon: 'pi pi-verified',   clients: 'UAE Ministry of Defense · Ministry of Defense Italy · Smart Dubai · Ministry of Health KSA' },
  { sector: 'Financial Services',   icon: 'pi pi-credit-card', clients: 'Barclays PLC · CME Group · Central Bank of Oman · Bank Itaú · Davivienda' },
  { sector: 'Telecommunications',  icon: 'pi pi-wifi',         clients: 'DU Telecom · Ooredoo · TurkCell · MTN · Oi Telecom' },
  { sector: 'Aviation & Hospitality', icon: 'pi pi-send',      clients: 'Emirates Airlines · Virgin Atlantic · Jumeirah Group' },
  { sector: 'Technology & Consulting', icon: 'pi pi-desktop',  clients: 'United Nations · IBM · Babcock International · Cloud Software Group' },
  { sector: 'Energy & Oil',         icon: 'pi pi-bolt',        clients: 'Saudi Aramco · PDO Oman · Maersk Oil' },
]

// ── Helpers ───────────────────────────────────────────────────────────────────
const formatDate = (d) =>
  new Date(d).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })

// ── Fetch blog posts ──────────────────────────────────────────────────────────
onMounted(async () => {
  try {
    const { data } = await axios.get('/api/blog/featured?limit=3')
    blogPosts.value = data
  } catch {
    // silently fail
  } finally {
    blogLoading.value = false
  }
  initHeroCanvas()
})

// ── Hero Canvas Network Animation ─────────────────────────────────────────────
let animFrame = null
function initHeroCanvas() {
  const canvas = heroCanvas.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')

  const resize = () => {
    canvas.width = canvas.offsetWidth
    canvas.height = canvas.offsetHeight
  }
  resize()
  window.addEventListener('resize', resize, { passive: true })

  const NODES = 80
  const nodes = Array.from({ length: NODES }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    vx: (Math.random() - 0.5) * 0.4,
    vy: (Math.random() - 0.5) * 0.4,
    r: Math.random() * 2 + 1,
  }))

  const draw = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    const W = canvas.width, H = canvas.height

    nodes.forEach((n) => {
      n.x += n.vx; n.y += n.vy
      if (n.x < 0 || n.x > W) n.vx *= -1
      if (n.y < 0 || n.y > H) n.vy *= -1
    })

    // Draw edges
    for (let i = 0; i < NODES; i++) {
      for (let j = i + 1; j < NODES; j++) {
        const dx = nodes[i].x - nodes[j].x
        const dy = nodes[i].y - nodes[j].y
        const dist = Math.sqrt(dx * dx + dy * dy)
        if (dist < 150) {
          const alpha = (1 - dist / 150) * 0.25
          ctx.strokeStyle = `rgba(61,139,253,${alpha})`
          ctx.lineWidth = 0.8
          ctx.beginPath()
          ctx.moveTo(nodes[i].x, nodes[i].y)
          ctx.lineTo(nodes[j].x, nodes[j].y)
          ctx.stroke()
        }
      }
    }

    // Draw nodes
    nodes.forEach((n) => {
      ctx.beginPath()
      ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2)
      ctx.fillStyle = 'rgba(56,198,244,0.75)'
      ctx.fill()
    })

    animFrame = requestAnimationFrame(draw)
  }
  draw()
}

onUnmounted(() => {
  if (animFrame) cancelAnimationFrame(animFrame)
})
</script>

<style scoped>
/* ── Hero ─────────────────────────────────────────────────────────────────── */
.hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
  background: var(--nx-bg-base);
}
.hero-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}
.hero-overlay {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 60% 45%, rgba(61,139,253,0.14) 0%, transparent 62%),
              radial-gradient(ellipse at 50% 100%, rgba(7,11,18,0.6) 0%, transparent 55%),
              linear-gradient(180deg, transparent 55%, var(--nx-bg-base) 100%);
}
.hero-content {
  position: relative;
  z-index: 2;
  padding-top: 120px;
  padding-bottom: 80px;
  max-width: 760px;
}
.hero-badge {
  gap: 10px;
  padding: 8px 18px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: none;
  letter-spacing: 0.03em;
  margin-bottom: 24px;
}
.hero-badge .glow-dot {
  background: var(--nx-cyan-400);
  box-shadow: 0 0 10px var(--nx-cyan-400), 0 0 22px rgba(56, 198, 244, 0.4);
  animation: badgePulse 2.2s ease-in-out infinite;
}
@keyframes badgePulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.55; transform: scale(0.82); }
}
@media (prefers-reduced-motion: reduce) {
  .hero-badge .glow-dot { animation: none; }
}
.hero-title {
  font-family: var(--font-heading);
  font-size: var(--nx-text-display);
  font-weight: 900;
  line-height: var(--nx-leading-tight);
  letter-spacing: var(--nx-tracking-tight);
  color: var(--nx-text-hi);
  margin-bottom: 24px;
}
.hero-title .gradient-text {
  background: linear-gradient(90deg, var(--nx-blue-500), var(--nx-cyan-400));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-subtitle {
  font-size: var(--nx-text-lg);
  color: var(--nx-text);
  line-height: var(--nx-leading-base);
  max-width: 56ch;
  margin-bottom: 12px;
}
.hero-subtitle strong { color: var(--nx-text-hi); font-weight: 600; }
.hero-subtitle-sub {
  font-size: var(--nx-text-base);
  color: var(--nx-text-mut);
  line-height: var(--nx-leading-base);
  max-width: 56ch;
  margin-bottom: 24px;
}
.hero-subtitle-sub strong { color: var(--nx-text); font-weight: 600; }
.hero-prompt {
  font-family: var(--nx-font-mono);
  font-size: var(--nx-text-sm);
  color: var(--nx-text-dim);
  margin-bottom: 40px;
  letter-spacing: 0.01em;
}
.hero-prompt-prefix {
  color: var(--nx-cyan-400);
  margin-right: 0.5em;
}
.hero-actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 48px;
}
.tech-label {
  font-family: var(--nx-font-mono);
  font-size: var(--nx-text-xs);
  font-weight: 500;
  letter-spacing: var(--nx-tracking-mono);
  text-transform: uppercase;
  color: var(--nx-text-mut);
  margin-bottom: 12px;
  display: block;
}
.tech-pills { display: flex; flex-wrap: wrap; gap: 8px; }
.tech-pill {
  color: var(--nx-text-mut);
  border-color: var(--nx-border-strong);
  transition: border-color var(--nx-dur) var(--nx-ease), color var(--nx-dur) var(--nx-ease), background var(--nx-dur) var(--nx-ease);
}
.tech-pill:hover {
  border-color: var(--nx-border-accent);
  color: var(--nx-text-hi);
  background: rgba(61,139,253,0.08);
}
.hero-scroll-hint {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: var(--nx-text-mut);
  font-size: 0.7rem;
  letter-spacing: 0.15em;
  font-family: var(--font-heading);
  animation: scrollBounce 2s ease-in-out infinite;
}
.scroll-line {
  width: 1px;
  height: 40px;
  background: linear-gradient(to bottom, var(--nx-cyan-400), transparent);
}
@keyframes scrollBounce {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50% { transform: translateX(-50%) translateY(8px); }
}

/* ── Stats ─────────────────────────────────────────────────────────────────── */
.stats-bar {
  background: var(--nx-navy-900);
  border-top: 1px solid var(--nx-border);
  border-bottom: 1px solid var(--nx-border);
  padding: 40px 0;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0;
}
.stat-item {
  text-align: center;
  padding: 20px;
  border-right: 1px solid var(--nx-border);
}
.stat-item:last-child { border-right: none; }
.stat-value {
  display: block;
  font-family: var(--font-heading);
  font-size: var(--nx-text-h2);
  font-weight: 900;
  background: linear-gradient(90deg, var(--nx-blue-500), var(--nx-cyan-400));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 6px;
}
.stat-label {
  font-family: var(--nx-font-mono);
  font-size: var(--nx-text-xs);
  color: var(--nx-text-mut);
  font-weight: 500;
  letter-spacing: var(--nx-tracking-mono);
  text-transform: uppercase;
}

/* ── Services ──────────────────────────────────────────────────────────────── */
.section-header { margin-bottom: 56px; position: relative; z-index: 1; }
.services-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  position: relative;
  z-index: 1;
}
.service-card { cursor: pointer; padding: 32px; display: flex; flex-direction: column; }
.service-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--nx-card-highlight), var(--nx-glow-blue), var(--nx-shadow-1);
  border-color: var(--nx-border-accent);
}
.service-icon {
  width: 52px; height: 52px;
  border-radius: var(--nx-radius);
  border: 1px solid var(--nx-border-accent);
  background: rgba(61, 139, 253, 0.06);
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 20px;
  font-size: 1.3rem;
  color: var(--nx-cyan-400);
}
.service-title {
  font-size: var(--nx-text-h4);
  font-weight: 700;
  color: var(--nx-text-hi);
  margin-bottom: 10px;
}
.service-desc {
  font-size: 0.9rem;
  color: var(--nx-text-mut);
  line-height: 1.65;
  margin-bottom: 16px;
  flex: 1;
}
.service-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 20px; }
.service-arrow {
  font-size: 0.82rem;
  color: var(--nx-cyan-400);
  font-weight: 600;
  font-family: var(--font-heading);
  opacity: 0;
  transition: opacity 0.25s;
}
.service-card:hover .service-arrow { opacity: 1; }
.services-cta { text-align: center; margin-top: 48px; position: relative; z-index: 1; }

/* ── Products ───────────────────────────────────────────────────────────────── */
.product-feature-card {
  position: relative;
  cursor: pointer;
  padding: 32px;
  margin-top: 48px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  overflow: hidden;
}
.product-feature-glow {
  position: absolute;
  top: 0; right: 0;
  width: 320px; height: 240px;
  background: radial-gradient(ellipse at top right, rgba(61,139,253,0.14) 0%, transparent 70%);
  pointer-events: none;
}
.product-feature-grid {
  position: relative;
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 28px;
  align-items: center;
}
.product-feature-logo-wrap {
  width: 120px;
  height: 80px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--nx-border);
  border-radius: 16px;
}
.product-feature-tagline {
  font-size: 0.88rem;
  color: var(--nx-cyan-400);
  font-weight: 600;
  margin-bottom: 10px;
  font-family: var(--font-heading);
}
.product-feature-title {
  font-size: 1.35rem;
  color: var(--nx-text-hi);
  margin: 6px 0 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.product-version {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 100px;
  background: rgba(56, 198, 244, 0.15);
  border: 1px solid rgba(56, 198, 244, 0.3);
  color: var(--nx-cyan-400);
  font-family: var(--font-heading);
  letter-spacing: 0.04em;
}
.product-feature-desc {
  font-size: 0.92rem;
  color: var(--nx-text-mut);
  line-height: 1.65;
  margin-bottom: 14px;
}
.product-feature-tags { display: flex; flex-wrap: wrap; gap: 6px; }
.product-feature-specs {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.product-spec-chip {
  font-size: var(--nx-text-xs);
  color: var(--nx-text);
  border-color: var(--nx-border-accent);
}
.product-feature-arrow {
  position: relative;
  font-size: 0.82rem;
  color: var(--nx-cyan-400);
  font-weight: 600;
  font-family: var(--font-heading);
  align-self: flex-end;
  opacity: 0;
  transition: opacity 0.25s;
}
.product-feature-card:hover .product-feature-arrow { opacity: 1; }
.products-cta { text-align: center; margin-top: 40px; }

/* ── Why section ───────────────────────────────────────────────────────────── */
.why-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: center;
}
.why-list { margin: 32px 0; display: flex; flex-direction: column; gap: 18px; }
.why-item {
  display: flex;
  gap: 14px;
  align-items: flex-start;
}
.why-check {
  width: 28px; height: 28px;
  background: rgba(56, 198, 244, 0.12);
  border: 1px solid rgba(56, 198, 244, 0.3);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  color: var(--nx-cyan-400);
  font-size: 0.75rem;
  margin-top: 2px;
}
.why-item strong { display: block; color: var(--nx-text-hi); margin-bottom: 2px; font-size: 0.95rem; }
.why-item p { font-size: 0.875rem; color: var(--nx-text-mut); }

.globe-card {
  padding: 36px;
}
.globe-header { margin-bottom: 28px; position: relative; z-index: 1; }
.globe-header h3 { font-size: 1.4rem; color: var(--nx-text-hi); margin-top: 8px; line-height: 1.3; }
.regions-grid { position: relative; z-index: 1; display: flex; flex-direction: column; }
.region-item {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 14px 4px;
  border-top: 1px solid var(--nx-border);
}
.region-item:first-child { border-top: none; }
.region-item .pi { color: var(--nx-cyan-400); margin-top: 3px; flex-shrink: 0; }
.region-item strong { display: block; font-size: 0.85rem; color: var(--nx-text-hi); margin-bottom: 2px; }
.region-item span { font-size: 0.78rem; color: var(--nx-text-mut); }

/* ── Industries ──────────────────────────────────────────────────────────────── */
.clients-section { background: var(--nx-bg-base); }
.industries-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1px;
  margin-top: 48px;
  background: var(--nx-border);
  border: 1px solid var(--nx-border);
  border-radius: var(--nx-radius-lg);
  overflow: hidden;
}
.industry-card {
  background: var(--nx-bg-raised);
  text-align: left;
  padding: 32px 28px;
  transition: background var(--nx-dur) var(--nx-ease), box-shadow var(--nx-dur) var(--nx-ease);
  position: relative;
}
.industry-card:hover {
  background: var(--nx-card-bg-hover);
  box-shadow: inset 0 0 0 1px var(--nx-border-accent), var(--nx-glow-cyan);
  z-index: 1;
}
.industry-icon {
  width: 44px; height: 44px;
  border: 1px solid var(--nx-border-accent);
  background: rgba(56, 198, 244, 0.06);
  border-radius: var(--nx-radius-sm);
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 18px;
  font-size: 1.1rem;
  color: var(--nx-cyan-400);
}
.industry-card h3 {
  font-family: var(--nx-font-mono);
  font-size: var(--nx-text-xs);
  font-weight: 500;
  letter-spacing: var(--nx-tracking-mono);
  text-transform: uppercase;
  color: var(--nx-text-mut);
  margin-bottom: 10px;
}
.industry-card p { font-size: 0.88rem; color: var(--nx-text); line-height: 1.6; }

/* ── Blog preview ──────────────────────────────────────────────────────────── */
.section-header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 48px;
  gap: 24px;
  flex-wrap: wrap;
}
.blog-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}
.blog-card {
  cursor: pointer;
  padding: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
.blog-card-header {
  height: 120px;
  display: flex;
  align-items: flex-end;
  padding: 16px;
  position: relative;
}
.blog-card-header::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(7,11,18,0.35), rgba(7,11,18,0.65));
}
.blog-card-header .tag { position: relative; z-index: 1; }
.blog-card-body { padding: 24px; flex: 1; display: flex; flex-direction: column; }
.blog-title { font-size: 1rem; font-weight: 700; color: var(--nx-text-hi); margin-bottom: 10px; line-height: 1.4; }
.blog-excerpt {
  font-size: 0.875rem;
  color: var(--nx-text-mut);
  line-height: 1.6;
  flex: 1;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.blog-meta {
  display: flex;
  gap: 16px;
  font-family: var(--nx-font-mono);
  font-size: var(--nx-text-xs);
  color: var(--nx-text-mut);
}
.blog-meta .pi { margin-right: 4px; }
.blog-card-skeleton { pointer-events: none; }
.blog-card-skeleton-header {
  background: linear-gradient(90deg, rgba(255,255,255,0.04) 25%, rgba(255,255,255,0.08) 50%, rgba(255,255,255,0.04) 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.4s ease-in-out infinite;
}
.skeleton-line {
  height: 14px;
  border-radius: 6px;
  margin-bottom: 12px;
  background: linear-gradient(90deg, rgba(255,255,255,0.04) 25%, rgba(255,255,255,0.08) 50%, rgba(255,255,255,0.04) 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.4s ease-in-out infinite;
}
.skeleton-line--title { height: 18px; width: 85%; margin-bottom: 16px; }
.skeleton-line--short { width: 55%; margin-bottom: 0; }
@keyframes skeleton-shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* ── CTA ─────────────────────────────────────────────────────────────────── */
.cta-section {
  padding-top: var(--nx-section-y-loose);
  padding-bottom: var(--nx-section-y-loose);
  background: linear-gradient(180deg, var(--nx-navy-800) 0%, var(--nx-bg-base) 100%);
}
.cta-box {
  background: var(--nx-card-bg);
  border: 1px solid var(--nx-border);
  border-radius: var(--nx-radius-lg);
  box-shadow: var(--nx-card-highlight), var(--nx-shadow-2);
  padding: 80px 60px;
  text-align: center;
  position: relative;
  overflow: hidden;
}
.cta-glow {
  position: absolute;
  top: -60px; left: 50%;
  transform: translateX(-50%);
  width: 500px; height: 260px;
  background: radial-gradient(ellipse, rgba(61,139,253,0.16) 0%, transparent 70%);
  pointer-events: none;
}
.cta-title {
  font-family: var(--font-heading);
  font-size: var(--nx-text-h2);
  color: var(--nx-text-hi);
  margin: 16px 0 20px;
  position: relative;
}
.cta-desc {
  font-size: 1rem;
  color: var(--nx-text-mut);
  max-width: 560px;
  margin: 0 auto 40px;
  line-height: 1.75;
  position: relative;
}
.cta-actions { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; position: relative; }

/* ── Responsive ──────────────────────────────────────────────────────────── */
@media (max-width: 1024px) {
  .services-grid { grid-template-columns: repeat(2, 1fr); }
  .product-feature-grid { grid-template-columns: 1fr; }
  .product-feature-logo-wrap { margin: 0 auto; }
  .why-grid { grid-template-columns: 1fr; gap: 40px; }
  .industries-grid { grid-template-columns: repeat(2, 1fr); }
  .blog-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .stat-item { border-right: none; border-bottom: 1px solid var(--nx-border); }
  .stat-item:nth-child(2n) { border-right: none; }
}
@media (max-width: 640px) {
  .services-grid { grid-template-columns: 1fr; }
  .blog-grid { grid-template-columns: 1fr; }
  .industries-grid { grid-template-columns: 1fr; }
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .cta-box { padding: 48px 24px; }
  .hero-actions { flex-direction: column; }
}
</style>
