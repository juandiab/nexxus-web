import { Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import axios from 'axios'
import { ArrowRight, Shield, Server, Lock, Cloud, Zap } from 'lucide-react'
import BlurText from '@/components/BlurText'
import Aurora from '@/components/Aurora'
import SpotlightCard from '@/components/SpotlightCard'
import { SeoHead } from '@/components/SeoHead'
import { ROUTE_SEO } from '@/config/site'
import { jsonLdForRoute } from '@/data/structuredData'
import { products } from '@/data/products'

const stats = [
  { value: '15+', label: 'Years of Experience' },
  { value: '20+', label: 'Countries Served' },
  { value: '100+', label: 'Projects Delivered' },
  { value: '100%', label: 'Remote Capable' },
]

const services = [
  {
    id: 'waf',
    icon: Shield,
    title: 'WAF & API Protection',
    desc: 'Enterprise-grade Web Application Firewall design, deployment, and tuning for NetScaler ADC and F5 BIG-IP.',
    tags: ['NetScaler WAF', 'F5', 'OWASP', 'Bot Management'],
  },
  {
    id: 'netscaler',
    icon: Server,
    title: 'NetScaler / ADC',
    desc: 'Full lifecycle NetScaler ADC services — high availability, SSL offload, GSLB, and performance optimization.',
    tags: ['NetScaler', 'GSLB', 'SSL Offload', 'Citrix'],
  },
  {
    id: 'zerotrust',
    icon: Lock,
    title: 'Zero-Trust Architecture',
    desc: 'End-to-end Zero-Trust transformations combining NetScaler Gateway, Okta, Azure AD, and DUO.',
    tags: ['Zero-Trust', 'Okta', 'Azure AD', 'MFA'],
  },
  {
    id: 'cloud',
    icon: Cloud,
    title: 'Multicloud Security',
    desc: 'Consistent security posture across AWS, Azure, and on-premises with NetScaler as the unified layer.',
    tags: ['AWS', 'Azure', 'NetScaler VPX', 'CSPM'],
  },
  {
    id: 'ai',
    icon: Zap,
    title: 'AI & Automation',
    desc: 'AI-assisted NetScaler administration, WAF policy drafting, and automation with human review guardrails.',
    tags: ['Python', 'LLM', 'NITRO API', 'Automation'],
  },
]

const whyItems = [
  { title: 'Principal-Led Engagements', desc: 'Every project is led by a senior architect — no bait-and-switch.' },
  { title: 'Global Delivery', desc: 'Remote-first team across Colombia, UAE, UK, and US.' },
  { title: 'Vendor Deep Expertise', desc: 'Citrix SME, AWS Security Specialty, and 15+ years in the trenches.' },
]

interface BlogPost {
  id: string
  slug: string
  title: string
  excerpt: string
  category: string
  read_time: number
  date: string
  cover_color?: string
}

export default function HomePage() {
  const [blogPosts, setBlogPosts] = useState<BlogPost[]>([])
  const [blogLoading, setBlogLoading] = useState(true)
  const seo = ROUTE_SEO.home

  useEffect(() => {
    axios
      .get('/api/blog/featured')
      .then((res) => setBlogPosts(res.data?.slice(0, 3) ?? []))
      .catch(() => setBlogPosts([]))
      .finally(() => setBlogLoading(false))
  }, [])

  return (
    <div className="home">
      <SeoHead {...seo} jsonLd={jsonLdForRoute('home')} />

      <section className="relative flex min-h-screen items-center overflow-hidden pt-24">
        <div className="absolute inset-0 z-0">
          <Aurora colorStops={['#007BA7', '#00A8E0', '#4DB8E0']} amplitude={1.2} blend={0.6} />
        </div>
        <div className="absolute inset-0 z-[1] bg-gradient-to-b from-[var(--nt-dark)]/40 via-transparent to-[var(--nt-dark)]" />

        <div className="container relative z-[2] py-20">
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-[var(--nt-border)] bg-white/5 px-4 py-2 text-sm text-[var(--nt-text-muted)] reveal visible">
            <span className="h-2 w-2 rounded-full bg-[var(--nt-primary-l)] shadow-[0_0_8px_var(--nt-primary-l)]" />
            Trusted by Fortune 500 &amp; Government Agencies Worldwide
          </div>

          <h1 className="mb-6 max-w-4xl reveal visible reveal-delay-1">
            <BlurText
              text="Securing the World's"
              className="block text-white"
              delay={80}
            />
            <span className="gradient-text block">
              <BlurText text="Most Critical Applications" delay={120} />
            </span>
          </h1>

          <p className="mb-8 max-w-2xl text-lg leading-relaxed text-[var(--nt-text-muted)] reveal visible reveal-delay-2">
            <strong className="text-white">Making expertise more accessible.</strong> Through consulting,
            shared knowledge, and <strong className="text-white">AI-driven innovation</strong> across{' '}
            <strong className="text-white">20+ countries</strong>.
          </p>

          <div className="mb-12 flex flex-wrap gap-4 reveal visible reveal-delay-3">
            <Link to="/services" className="btn btn-primary">
              <Shield className="h-4 w-4" /> Explore Services
            </Link>
            <Link to="/contact" className="btn btn-secondary">
              Start a Project
            </Link>
          </div>

          <div className="reveal visible reveal-delay-4">
            <span className="mb-3 block font-[family-name:var(--font-heading)] text-xs font-bold tracking-widest text-[var(--nt-text-muted)] uppercase">
              Specialized In
            </span>
            <div className="flex flex-wrap gap-2">
              {['NetScaler WAF', 'F5 BIG-IP', 'Zero-Trust', 'AWS Security', 'Azure AD', 'Okta', 'AI Automation'].map(
                (pill) => (
                  <span key={pill} className="tag">
                    {pill}
                  </span>
                )
              )}
            </div>
          </div>
        </div>
      </section>

      <section className="border-y border-[var(--nt-border)] bg-[var(--nt-dark-2)] py-12">
        <div className="container">
          <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
            {stats.map((stat) => (
              <div key={stat.label} className="text-center reveal">
                <div className="text-3xl font-bold text-[var(--nt-primary-l)]">{stat.value}</div>
                <div className="mt-1 text-sm text-[var(--nt-text-muted)]">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="mb-12 reveal">
            <span className="section-label">What We Do</span>
            <h2 className="section-title">Expert-Level Security &amp; Delivery</h2>
            <p className="section-subtitle">
              From WAF policy design to AI-powered administration, we bring principal-architect expertise to every engagement.
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {services.map((svc, i) => {
              const Icon = svc.icon
              return (
                <SpotlightCard
                  key={svc.id}
                  className={`card cursor-pointer reveal reveal-delay-${(i % 4) + 1}`}
                  spotlightColor="rgba(0, 168, 224, 0.15)"
                >
                  <Link to={`/services#${svc.id}`} className="block text-inherit no-underline">
                    <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-[var(--nt-primary)]/20 text-[var(--nt-primary-l)]">
                      <Icon className="h-6 w-6" />
                    </div>
                    <h3 className="mb-3 text-lg">{svc.title}</h3>
                    <p className="mb-4 text-sm text-[var(--nt-text-muted)]">{svc.desc}</p>
                    <div className="mb-4 flex flex-wrap gap-2">
                      {svc.tags.map((tag) => (
                        <span key={tag} className="tag">
                          {tag}
                        </span>
                      ))}
                    </div>
                    <span className="inline-flex items-center gap-1 text-sm text-[var(--nt-primary-l)]">
                      Learn more <ArrowRight className="h-4 w-4" />
                    </span>
                  </Link>
                </SpotlightCard>
              )
            })}
          </div>

          <div className="mt-10 text-center reveal">
            <Link to="/services" className="btn btn-outline">
              View All Services <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </div>
      </section>

      <section className="section section-dark">
        <div className="container">
          <div className="mb-12 text-center reveal">
            <span className="section-label">Our Products</span>
            <h2 className="section-title">Technology That Empowers</h2>
            <p className="section-subtitle mx-auto">
              Tools that serve as a bridge between people, knowledge, and technology.
            </p>
          </div>

          {products.map((product) => (
            <SpotlightCard
              key={product.id}
              className="card mb-6 cursor-pointer reveal"
              spotlightColor="rgba(0, 123, 167, 0.2)"
            >
              <Link to={`/products#${product.id}`} className="block text-inherit no-underline">
                <div className="grid gap-8 md:grid-cols-[auto_1fr_auto] md:items-center">
                  <img
                    src={product.logo}
                    alt={product.logoAlt}
                    className="h-12 w-auto"
                    width={88}
                    height={48}
                  />
                  <div>
                    <span className="section-label">{product.label}</span>
                    <h3 className="text-xl">
                      {product.name}{' '}
                      <span className="text-sm font-normal text-[var(--nt-text-muted)]">
                        {product.edition}
                      </span>
                    </h3>
                    <p className="mt-2 text-[var(--nt-text-muted)]">{product.tagline}</p>
                    <div className="mt-3 flex flex-wrap gap-2">
                      {product.tags.slice(0, 4).map((tag: string) => (
                        <span key={tag} className="tag">
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="flex gap-6">
                    {product.metrics.map((m: { value: string; label: string }) => (
                      <div key={m.label} className="text-center">
                        <div className="text-2xl font-bold text-[var(--nt-primary-l)]">{m.value}</div>
                        <div className="text-xs text-[var(--nt-text-muted)]">{m.label}</div>
                      </div>
                    ))}
                  </div>
                </div>
              </Link>
            </SpotlightCard>
          ))}
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="grid gap-12 lg:grid-cols-2 lg:items-center">
            <div className="reveal">
              <span className="section-label">Why Nexxus Tech</span>
              <h2 className="section-title">
                Principals Who <span className="text-[var(--nt-primary-l)]">Show Up &amp; Stay.</span>
              </h2>
              <p className="section-subtitle mb-8">
                We don&apos;t send juniors. Every engagement is led by a principal architect who works alongside your team.
              </p>
              <div className="mb-8 space-y-4">
                {whyItems.map((item) => (
                  <div key={item.title} className="flex gap-4">
                    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-[var(--nt-primary)]/20 text-[var(--nt-primary-l)]">
                      ✓
                    </div>
                    <div>
                      <strong className="text-white">{item.title}</strong>
                      <p className="text-sm text-[var(--nt-text-muted)]">{item.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
              <Link to="/about" className="btn btn-primary">
                Meet the Team <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      <section className="section section-dark">
        <div className="container">
          <div className="mb-8 flex flex-wrap items-end justify-between gap-4 reveal">
            <div>
              <span className="section-label">Latest Insights</span>
              <h2 className="section-title">From the Nexxus Tech Blog</h2>
            </div>
            <Link to="/blog" className="btn btn-outline">
              All Posts <ArrowRight className="h-4 w-4" />
            </Link>
          </div>

          <div className="grid gap-6 md:grid-cols-3">
            {blogLoading
              ? Array.from({ length: 3 }).map((_, i) => (
                  <div key={i} className="card h-64 animate-pulse bg-[var(--nt-dark-3)]" />
                ))
              : blogPosts.map((post, i) => (
                  <Link
                    key={post.id}
                    to={`/blog/${post.slug}`}
                    className={`card block text-inherit no-underline reveal reveal-delay-${i + 1}`}
                  >
                    <div className="mb-4 h-2 w-16 rounded bg-[var(--nt-primary)]" />
                    <span className="tag mb-3">{post.category}</span>
                    <h3 className="mb-2 text-lg">{post.title}</h3>
                    <p className="text-sm text-[var(--nt-text-muted)]">{post.excerpt}</p>
                    <div className="mt-4 flex gap-4 text-xs text-[var(--nt-text-muted)]">
                      <span>{post.read_time} min read</span>
                      <span>{new Date(post.date).toLocaleDateString()}</span>
                    </div>
                  </Link>
                ))}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="relative overflow-hidden rounded-[var(--nt-radius-lg)] border border-[var(--nt-border)] bg-[var(--nt-card-bg)] p-12 text-center reveal">
            <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(0,123,167,0.15),transparent_70%)]" />
            <div className="relative">
              <span className="section-label">Ready to Get Started?</span>
              <h2 className="mb-4 text-3xl">
                Let&apos;s Secure Your <span className="gradient-text">Infrastructure Together</span>
              </h2>
              <p className="mx-auto mb-8 max-w-xl text-[var(--nt-text-muted)]">
                Whether you need a WAF deployment, a Zero-Trust roadmap, or AI-powered NetScaler automation — we&apos;re ready to help.
              </p>
              <div className="flex flex-wrap justify-center gap-4">
                <Link to="/contact" className="btn btn-primary">Start a Conversation</Link>
                <a href="mailto:contact@nexxus-tech.com" className="btn btn-outline">
                  contact@nexxus-tech.com
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
