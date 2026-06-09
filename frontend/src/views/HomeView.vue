<template>
  <div class="home">
    <!-- ── HERO ─────────────────────────────────────────────────────────────── -->
    <section class="hero">
      <canvas ref="heroCanvas" class="hero-canvas" aria-hidden="true"></canvas>
      <div class="hero-overlay"></div>
      <div class="container hero-content">
        <div class="hero-badge reveal">
          <span class="glow-dot"></span>
          <span>Trusted by Fortune 500 &amp; Government Agencies Worldwide</span>
        </div>
        <h1 class="hero-title reveal reveal-delay-1">
          Securing the World's<br />
          <span class="gradient-text">Most Critical Applications</span>
        </h1>
        <p class="hero-subtitle reveal reveal-delay-2">
          <strong>Making expertise more accessible.</strong><br />
          Through consulting, shared knowledge, and <strong>AI-driven innovation</strong>.<br />
          <strong>Helping people and organizations</strong> learn, grow, and solve complex challenges.<br />
          <strong>Inspiring the next generation of technology leaders</strong> across <strong>54+ countries</strong>.
        </p>
        <div class="hero-actions reveal reveal-delay-3">
          <RouterLink to="/services" class="btn btn-primary">
            <i class="pi pi-shield"></i> Explore Services
          </RouterLink>
          <RouterLink to="/contact" class="btn btn-secondary">
            <i class="pi pi-send"></i> Start a Project
          </RouterLink>
        </div>
        <div class="hero-tech-stack reveal reveal-delay-4">
          <span class="tech-label">SPECIALIZED IN</span>
          <div class="tech-pills">
            <span class="tech-pill">NetScaler WAF</span>
            <span class="tech-pill">F5 BIG-IP</span>
            <span class="tech-pill">Zero-Trust</span>
            <span class="tech-pill">AWS Security</span>
            <span class="tech-pill">Azure AD</span>
            <span class="tech-pill">Okta</span>
            <span class="tech-pill">AI Automation</span>
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
    <section class="section services-section">
      <div class="container">
        <div class="section-header reveal">
          <span class="section-label">What We Do</span>
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
            :class="`card service-card reveal reveal-delay-${(i % 4) + 1}`"
            @click="$router.push(`/services#${svc.serviceHash || svc.id}`)"
          >
            <div class="service-icon" :style="{ background: svc.bg }">
              <i :class="svc.icon"></i>
            </div>
            <h3 class="service-title">{{ svc.title }}</h3>
            <p class="service-desc">{{ svc.desc }}</p>
            <div class="service-tags">
              <span v-for="tag in svc.tags" :key="tag" class="tag">{{ tag }}</span>
            </div>
            <span class="service-arrow">
              Learn more <i class="pi pi-arrow-right"></i>
            </span>
          </div>
        </div>
        <div class="services-cta reveal">
          <RouterLink to="/services" class="btn btn-outline">
            View All Services <i class="pi pi-arrow-right"></i>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- ── PRODUCTS ───────────────────────────────────────────────────────────── -->
    <section class="section section-dark products-section">
      <div class="container">
        <div class="section-header reveal" style="text-align:center">
          <span class="section-label">Our Products</span>
          <h2 class="section-title">Technology That Empowers</h2>
          <p class="section-subtitle" style="margin:0 auto">
            Tools that serve as a bridge between people, knowledge, and technology—
            so engineers can learn, grow, and move forward with confidence.
          </p>
        </div>
        <div
          v-for="product in products"
          :key="product.id"
          class="product-feature-card card reveal"
          @click="$router.push(`/products#${product.id}`)"
        >
          <div class="product-feature-grid">
            <div class="product-feature-logo-wrap">
              <JpilotLogo theme="dark" :alt="product.logoAlt" img-class="product-feature-logo" />
            </div>
            <div class="product-feature-body">
              <span class="section-label">{{ product.label }}</span>
              <h3 class="product-feature-title">
                {{ product.name }}
                <span class="product-version">{{ product.edition }}</span>
              </h3>
              <p class="product-feature-tagline">{{ product.tagline }}</p>
              <p class="product-feature-desc">{{ product.excerpt }}</p>
              <div class="product-feature-tags">
                <span v-for="tag in product.tags.slice(0, 4)" :key="tag" class="tag">{{ tag }}</span>
              </div>
            </div>
            <div class="product-feature-metrics">
              <div v-for="m in product.metrics" :key="m.label" class="product-metric">
                <span class="product-metric-value">{{ m.value }}</span>
                <span class="product-metric-label">{{ m.label }}</span>
              </div>
            </div>
          </div>
          <span class="product-feature-arrow">
            Explore {{ product.name }} <i class="pi pi-arrow-right"></i>
          </span>
        </div>
        <div class="products-cta reveal">
          <RouterLink to="/products" class="btn btn-outline">
            View All Products <i class="pi pi-arrow-right"></i>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- ── WHY NEXXUS TECH ────────────────────────────────────────────────────── -->
    <section class="section section-dark why-section">
      <div class="container">
        <div class="why-grid">
          <div class="why-left reveal">
            <span class="section-label">Why Nexxus Tech</span>
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
            <RouterLink to="/about" class="btn btn-primary">
              Meet the Team <i class="pi pi-arrow-right"></i>
            </RouterLink>
          </div>
          <div class="why-right reveal reveal-delay-2">
            <div class="globe-card">
              <div class="globe-header">
                <span class="section-label">Global Reach</span>
                <h3>54+ Countries.<br/>One Standard of Excellence.</h3>
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
    <section class="section section-light clients-section">
      <div class="container">
        <div class="section-header reveal" style="text-align:center">
          <span class="section-label">Key Engagements</span>
          <h2 class="section-title" style="color:var(--nt-navy)">Trusted by Industry Leaders</h2>
          <p class="section-subtitle" style="margin:0 auto;color:#4A5568">
            Delivered security transformations for organizations across
            government, defense, finance, telecom, and aviation.
          </p>
        </div>
        <div class="industries-grid">
          <div
            v-for="ind in industries"
            :key="ind.sector"
            class="industry-card card reveal"
          >
            <div class="industry-icon">
              <i :class="ind.icon"></i>
            </div>
            <h4>{{ ind.sector }}</h4>
            <p>{{ ind.clients }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── BLOG PREVIEW ───────────────────────────────────────────────────────── -->
    <section class="section blog-preview-section">
      <div class="container">
        <div class="section-header-row reveal">
          <div>
            <span class="section-label">Latest Insights</span>
            <h2 class="section-title">From the Nexxus Tech Blog</h2>
          </div>
          <RouterLink to="/blog" class="btn btn-outline">
            All Posts <i class="pi pi-arrow-right"></i>
          </RouterLink>
        </div>
        <div class="blog-grid" v-if="blogPosts.length">
          <article
            v-for="(post, i) in blogPosts"
            :key="post.id"
            :class="`card blog-card reveal reveal-delay-${i + 1}`"
            @click="$router.push(`/blog/${post.slug}`)"
          >
            <div class="blog-card-header" :style="{ background: post.cover_color }">
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
        </div>
        <div v-else class="blog-loading">
          <i class="pi pi-spin pi-spinner"></i> Loading posts...
        </div>
      </div>
    </section>

    <!-- ── CTA ────────────────────────────────────────────────────────────────── -->
    <section class="section cta-section">
      <div class="container">
        <div class="cta-box reveal">
          <div class="cta-glow"></div>
          <span class="section-label">Ready to Get Started?</span>
          <h2 class="cta-title">
            Let's Secure Your<br /><span class="gradient-text">Infrastructure Together</span>
          </h2>
          <p class="cta-desc">
            Whether you need a WAF deployment, a Zero-Trust roadmap, or AI-powered
            NetScaler automation — we're ready to help. Remote engagements worldwide.
          </p>
          <div class="cta-actions">
            <RouterLink to="/contact" class="btn btn-primary">
              <i class="pi pi-send"></i> Start a Conversation
            </RouterLink>
            <a href="mailto:contact@nexxus-tech.com" class="btn btn-outline">
              <i class="pi pi-envelope"></i> contact@nexxus-tech.com
            </a>
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
import JpilotLogo from '@/components/shared/JpilotLogo.vue'

const heroCanvas = ref(null)
const blogPosts = ref([])

// ── Stats ─────────────────────────────────────────────────────────────────────
const stats = [
  { value: '15+',  label: 'Years of Experience' },
  { value: '54+',  label: 'Countries Served' },
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
          ctx.strokeStyle = `rgba(0,123,167,${alpha})`
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
      ctx.fillStyle = 'rgba(0,168,224,0.7)'
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
  background: var(--nt-dark);
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
  background: radial-gradient(ellipse at 60% 50%, rgba(0,123,167,0.12) 0%, transparent 65%),
              linear-gradient(180deg, transparent 60%, var(--nt-dark) 100%);
}
.hero-content {
  position: relative;
  z-index: 2;
  padding-top: 120px;
  padding-bottom: 80px;
  max-width: 760px;
}
.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: rgba(0,123,167,0.1);
  border: 1px solid rgba(0,123,167,0.3);
  border-radius: 100px;
  padding: 8px 18px;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--nt-primary-l);
  margin-bottom: 24px;
  letter-spacing: 0.03em;
}
.hero-title {
  font-size: clamp(2.4rem, 5.5vw, 4.2rem);
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 24px;
}
.hero-subtitle {
  font-size: 1.15rem;
  color: var(--nt-text-muted);
  margin-bottom: 40px;
  line-height: 1.75;
  max-width: 600px;
}
.hero-subtitle strong { color: var(--nt-secondary); font-weight: 600; }
.hero-actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 48px;
}
.tech-label {
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.2em;
  color: var(--nt-text-muted);
  margin-bottom: 12px;
  display: block;
  font-family: var(--font-heading);
}
.tech-pills { display: flex; flex-wrap: wrap; gap: 8px; }
.tech-pill {
  padding: 5px 14px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 100px;
  font-size: 0.8rem;
  color: var(--nt-text-muted);
  font-family: var(--font-heading);
  font-weight: 600;
  transition: var(--nt-transition);
}
.tech-pill:hover {
  border-color: var(--nt-primary);
  color: var(--nt-primary-l);
  background: rgba(0,123,167,0.08);
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
  color: var(--nt-text-muted);
  font-size: 0.7rem;
  letter-spacing: 0.15em;
  font-family: var(--font-heading);
  animation: scrollBounce 2s ease-in-out infinite;
}
.scroll-line {
  width: 1px;
  height: 40px;
  background: linear-gradient(to bottom, var(--nt-primary), transparent);
}
@keyframes scrollBounce {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50% { transform: translateX(-50%) translateY(8px); }
}

/* ── Stats ─────────────────────────────────────────────────────────────────── */
.stats-bar {
  background: var(--nt-dark-2);
  border-top: 1px solid var(--nt-border);
  border-bottom: 1px solid var(--nt-border);
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
  border-right: 1px solid var(--nt-border);
}
.stat-item:last-child { border-right: none; }
.stat-value {
  display: block;
  font-family: var(--font-heading);
  font-size: 2.8rem;
  font-weight: 900;
  background: linear-gradient(135deg, var(--nt-primary-l), var(--nt-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 6px;
}
.stat-label {
  font-size: 0.8rem;
  color: var(--nt-text-muted);
  font-family: var(--font-heading);
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

/* ── Services ──────────────────────────────────────────────────────────────── */
.section-header { margin-bottom: 56px; }
.services-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}
.service-card { cursor: pointer; }
.service-icon {
  width: 56px; height: 56px;
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 20px;
  font-size: 1.4rem;
  color: var(--nt-primary-l);
}
.service-title {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 10px;
}
.service-desc {
  font-size: 0.9rem;
  color: var(--nt-text-muted);
  line-height: 1.65;
  margin-bottom: 16px;
  flex: 1;
}
.service-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 20px; }
.service-arrow {
  font-size: 0.82rem;
  color: var(--nt-primary-l);
  font-weight: 600;
  font-family: var(--font-heading);
  opacity: 0;
  transition: opacity 0.25s;
}
.service-card:hover .service-arrow { opacity: 1; }
.services-cta { text-align: center; margin-top: 48px; }

/* ── Products ───────────────────────────────────────────────────────────────── */
.products-section { background: var(--nt-dark-2); border-top: 1px solid var(--nt-border); }
.product-feature-card {
  cursor: pointer;
  padding: 32px;
  margin-top: 48px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.product-feature-grid {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 28px;
  align-items: center;
}
.product-feature-logo-wrap {
  width: 120px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--nt-border);
  border-radius: 16px;
}
.product-feature-logo {
  width: 100%;
  height: auto;
  max-height: 48px;
  object-fit: contain;
  display: block;
}
.product-feature-tagline {
  font-size: 0.88rem;
  color: var(--nt-secondary);
  font-weight: 600;
  margin-bottom: 10px;
  font-family: var(--font-heading);
}
.product-feature-title {
  font-size: 1.35rem;
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
  background: rgba(0, 168, 224, 0.15);
  border: 1px solid rgba(0, 168, 224, 0.3);
  color: var(--nt-secondary);
  font-family: var(--font-heading);
  letter-spacing: 0.04em;
}
.product-feature-desc {
  font-size: 0.92rem;
  color: var(--nt-text-muted);
  line-height: 1.65;
  margin-bottom: 14px;
}
.product-feature-tags { display: flex; flex-wrap: wrap; gap: 6px; }
.product-feature-metrics {
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-width: 140px;
}
.product-metric { text-align: center; }
.product-metric-value {
  display: block;
  font-family: var(--font-heading);
  font-size: 1.2rem;
  font-weight: 900;
  color: var(--nt-secondary);
  line-height: 1.1;
  margin-bottom: 4px;
}
.product-metric-label {
  font-size: 0.68rem;
  color: var(--nt-text-muted);
  font-weight: 600;
  font-family: var(--font-heading);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  line-height: 1.3;
}
.product-feature-arrow {
  font-size: 0.82rem;
  color: var(--nt-primary-l);
  font-weight: 600;
  font-family: var(--font-heading);
  align-self: flex-end;
  opacity: 0;
  transition: opacity 0.25s;
}
.product-feature-card:hover .product-feature-arrow { opacity: 1; }
.products-cta { text-align: center; margin-top: 40px; }

/* ── Why section ───────────────────────────────────────────────────────────── */
.section-dark { background: var(--nt-dark-2); }
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
  background: rgba(0,168,224,0.12);
  border: 1px solid rgba(0,168,224,0.3);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  color: var(--nt-secondary);
  font-size: 0.75rem;
  margin-top: 2px;
}
.why-item strong { display: block; color: var(--nt-white); margin-bottom: 2px; font-size: 0.95rem; }
.why-item p { font-size: 0.875rem; color: var(--nt-text-muted); }

.globe-card {
  background: var(--nt-card-bg);
  border: 1px solid var(--nt-border);
  border-radius: var(--nt-radius-lg);
  padding: 36px;
}
.globe-header { margin-bottom: 28px; }
.globe-header h3 { font-size: 1.4rem; margin-top: 8px; line-height: 1.3; }
.regions-grid { display: flex; flex-direction: column; gap: 16px; }
.region-item {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 14px;
  background: rgba(255,255,255,0.03);
  border-radius: 10px;
  border: 1px solid rgba(255,255,255,0.05);
}
.region-item .pi { color: var(--nt-secondary); margin-top: 3px; flex-shrink: 0; }
.region-item strong { display: block; font-size: 0.85rem; color: var(--nt-white); margin-bottom: 2px; }
.region-item span { font-size: 0.78rem; color: var(--nt-text-muted); }

/* ── Industries ──────────────────────────────────────────────────────────────── */
.clients-section { background: var(--nt-light-bg); }
.industries-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 48px;
}
.industry-card {
  background: white;
  border-color: #E2E8F0;
  text-align: center;
  padding: 28px 24px;
}
.industry-card:hover { box-shadow: 0 8px 32px rgba(0,123,167,0.12); border-color: rgba(0,123,167,0.3); transform: translateY(-3px); }
.industry-icon {
  width: 52px; height: 52px;
  background: linear-gradient(135deg, var(--nt-primary), var(--nt-secondary));
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 16px;
  font-size: 1.3rem;
  color: white;
}
.industry-card h4 { font-size: 0.95rem; color: var(--nt-navy); margin-bottom: 8px; }
.industry-card p { font-size: 0.8rem; color: #64748B; line-height: 1.5; }

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
.blog-card-body { padding: 24px; flex: 1; display: flex; flex-direction: column; }
.blog-title { font-size: 1rem; font-weight: 700; margin-bottom: 10px; line-height: 1.4; }
.blog-excerpt {
  font-size: 0.875rem;
  color: var(--nt-text-muted);
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
  font-size: 0.78rem;
  color: var(--nt-text-muted);
}
.blog-meta .pi { margin-right: 4px; }
.blog-loading { text-align: center; color: var(--nt-text-muted); padding: 40px; font-size: 0.9rem; }
.blog-loading .pi { margin-right: 8px; }

/* ── CTA ─────────────────────────────────────────────────────────────────── */
.cta-section { background: var(--nt-dark-2); }
.cta-box {
  background: var(--nt-dark-3);
  border: 1px solid var(--nt-border);
  border-radius: var(--nt-radius-lg);
  padding: 80px 60px;
  text-align: center;
  position: relative;
  overflow: hidden;
}
.cta-glow {
  position: absolute;
  top: -60px; left: 50%;
  transform: translateX(-50%);
  width: 400px; height: 200px;
  background: radial-gradient(ellipse, rgba(0,123,167,0.2) 0%, transparent 70%);
  pointer-events: none;
}
.cta-title {
  font-size: clamp(1.8rem, 3.5vw, 2.8rem);
  margin: 16px 0 20px;
}
.cta-desc {
  font-size: 1rem;
  color: var(--nt-text-muted);
  max-width: 560px;
  margin: 0 auto 40px;
  line-height: 1.75;
}
.cta-actions { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }

/* ── Responsive ──────────────────────────────────────────────────────────── */
@media (max-width: 1024px) {
  .services-grid { grid-template-columns: repeat(2, 1fr); }
  .product-feature-grid { grid-template-columns: auto 1fr; }
  .product-feature-metrics {
    grid-column: 1 / -1;
    flex-direction: row;
    justify-content: center;
    flex-wrap: wrap;
    min-width: 0;
  }
  .product-metric { min-width: 120px; }
  .why-grid { grid-template-columns: 1fr; gap: 40px; }
  .industries-grid { grid-template-columns: repeat(2, 1fr); }
  .blog-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .stat-item { border-right: none; border-bottom: 1px solid var(--nt-border); }
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
