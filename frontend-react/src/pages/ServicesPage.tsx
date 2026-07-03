import { Link } from 'react-router-dom'
import { ArrowRight, Shield, Server, Lock, Cloud, Zap, CheckCircle } from 'lucide-react'
import { SeoHead } from '@/components/SeoHead'
import { ROUTE_SEO } from '@/config/site'
import { jsonLdForRoute } from '@/data/structuredData'

const services = [
  {
    id: 'waf',
    label: 'WAF & API Protection',
    icon: Shield,
    light: false,
    reverse: false,
    title: 'Web Application Firewall & API Protection',
    desc: 'Enterprise-grade WAF deployment, policy design, and continuous tuning for Citrix NetScaler ADC and F5 BIG-IP.',
    features: [
      'OWASP Top 10 protection (SQL injection, XSS, CSRF, and more)',
      'Bot management with device fingerprinting and CAPTCHA enforcement',
      'API gateway security with OpenAPI schema validation',
      'Rate-limiting and DDoS mitigation at the ADC layer',
    ],
    tags: ['NetScaler WAF', 'F5 BIG-IP', 'OWASP', 'Bot Management'],
    metrics: [
      { value: '99.9%', label: 'Threat Detection Rate' },
      { value: '<1%', label: 'False Positive Rate' },
      { value: '100+', label: 'WAF Deployments' },
    ],
  },
  {
    id: 'netscaler',
    label: 'Application Delivery Controllers',
    icon: Server,
    light: true,
    reverse: true,
    title: 'NetScaler ADC & Application Delivery',
    desc: 'Full lifecycle Citrix NetScaler (ADC) services from architecture design to hands-on deployment.',
    features: [
      'High-availability clustering (active-active, active-passive)',
      'SSL/TLS offloading and certificate management',
      'Global Server Load Balancing (GSLB) and multi-site failover',
      'F5 BIG-IP ↔ NetScaler ADC migrations (bidirectional)',
    ],
    tags: ['NetScaler', 'F5 BIG-IP', 'ADC Migration', 'GSLB'],
    metrics: [
      { value: 'SME', label: 'Citrix Recognized Expert' },
      { value: '200+', label: 'NetScaler Deployments' },
      { value: '50+', label: 'ADC Platform Migrations' },
    ],
  },
  {
    id: 'zerotrust',
    label: 'Zero-Trust Architecture',
    icon: Lock,
    light: false,
    reverse: false,
    title: 'Zero-Trust Architecture & IAM',
    desc: 'End-to-end Zero-Trust transformations proven across finance, defense, and government.',
    features: [
      'Identity federation: Okta + Azure AD + NetScaler Gateway',
      'Conditional access policy design and enforcement',
      'Multi-Factor Authentication (MFA) for all access paths',
      'SASE architecture consulting and design',
    ],
    tags: ['Zero-Trust', 'Okta', 'Azure AD', 'MFA'],
    metrics: [
      { value: '94%', label: 'Reduction in Unauthorized Access' },
      { value: '100%', label: 'VPN Elimination (case study)' },
      { value: '30+', label: 'ZTA Implementations' },
    ],
  },
  {
    id: 'cloud',
    label: 'Cloud & Multicloud Security',
    icon: Cloud,
    light: true,
    reverse: true,
    title: 'Multicloud Security Architecture',
    desc: 'Consistent security posture across AWS, Azure, and on-premises with NetScaler as the unified layer.',
    features: [
      'AWS Security architecture (VPC, WAF v2, Shield, GuardDuty)',
      'Azure security design (Application Gateway, Front Door, NSGs)',
      'NetScaler VPX deployment on AWS and Azure Marketplace',
      'Cloud Security Posture Management (CSPM)',
    ],
    tags: ['AWS', 'Azure', 'NetScaler VPX', 'Multicloud'],
    metrics: [
      { value: 'AWS', label: 'Security Specialty Certified' },
      { value: '3', label: 'Cloud Platforms Supported' },
      { value: '40+', label: 'Cloud Security Projects' },
    ],
  },
  {
    id: 'ai',
    label: 'AI & Automation',
    icon: Zap,
    light: false,
    reverse: false,
    title: 'AI-Powered Infrastructure & Automation',
    desc: 'Practical AI-assisted NetScaler administration, WAF policy drafting, and automation with human review.',
    features: [
      'WAF profile drafts from OpenAPI specs (reviewed before apply)',
      'Log analysis assistance and false-positive triage workflows',
      'Configuration drift checks with approval-gated remediation',
      'Scoped copilots (e.g. JPilot) with confirm-before-change guardrails',
    ],
    tags: ['Python', 'LLM', 'NITRO API', 'Automation'],
    metrics: [
      { value: 'Review', label: 'Changes Approved Before Apply' },
      { value: 'Local', label: 'ADC Credentials Stay On-Prem' },
      { value: 'JPilot', label: 'Self-Hosted AI Copilot' },
    ],
  },
]

export default function ServicesPage() {
  const seo = ROUTE_SEO.services

  return (
    <div className="services-page">
      <SeoHead {...seo} jsonLd={jsonLdForRoute('services')} />

      <section className="page-hero">
        <div className="page-hero-bg" />
        <div className="container page-hero-content">
          <span className="section-label reveal">Our Expertise</span>
          <h1 className="reveal reveal-delay-1">
            Expert Security &amp;<br />
            <span className="gradient-text">Delivery Services</span>
          </h1>
          <p className="page-hero-subtitle reveal reveal-delay-2">
            From WAF policy design to AI-driven infrastructure automation —
            every engagement delivered at the principal architect level.
          </p>
        </div>
      </section>

      {services.map((svc) => {
        const Icon = svc.icon
        return (
          <section
            key={svc.id}
            id={svc.id}
            className={`section ${svc.light ? 'section-light' : ''}`}
          >
            <div className="container">
              <div
                className={`grid items-center gap-12 lg:grid-cols-2 ${
                  svc.reverse ? '[&>*:first-child]:lg:order-2' : ''
                }`}
              >
                <div className="reveal">
                  <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-xl bg-[var(--nt-primary)]/20 text-[var(--nt-primary-l)]">
                    <Icon className="h-7 w-7" />
                  </div>
                  <span className="section-label">{svc.label}</span>
                  <h2 className="section-title">{svc.title}</h2>
                  <p className="section-subtitle mb-6">{svc.desc}</p>
                  <div className="mb-6 space-y-2">
                    {svc.features.map((f) => (
                      <div key={f} className="flex items-start gap-2 text-sm">
                        <CheckCircle className="mt-0.5 h-4 w-4 shrink-0 text-[var(--nt-primary-l)]" />
                        <span className={svc.light ? 'text-gray-600' : 'text-[var(--nt-text-muted)]'}>
                          {f}
                        </span>
                      </div>
                    ))}
                  </div>
                  <div className="mb-6 flex flex-wrap gap-2">
                    {svc.tags.map((t) => (
                      <span key={t} className="tag">
                        {t}
                      </span>
                    ))}
                  </div>
                  <Link to="/contact" className="btn btn-primary">
                    Get a Consultation <ArrowRight className="h-4 w-4" />
                  </Link>
                </div>

                <div className="reveal reveal-delay-2">
                  <div className="card overflow-hidden p-0">
                    <div className="flex items-center gap-4 bg-[var(--nt-primary)]/20 p-6">
                      <Icon className="h-8 w-8 text-[var(--nt-primary-l)]" />
                      <h3 className="text-lg">{svc.title}</h3>
                    </div>
                    <div className="grid grid-cols-3 gap-4 p-6">
                      {svc.metrics.map((m) => (
                        <div key={m.label} className="text-center">
                          <div className="text-xl font-bold text-[var(--nt-primary-l)]">{m.value}</div>
                          <div className="mt-1 text-xs text-[var(--nt-text-muted)]">{m.label}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>
        )
      })}

      <section className="section">
        <div className="container">
          <div className="relative overflow-hidden rounded-[var(--nt-radius-lg)] border border-[var(--nt-border)] bg-[var(--nt-card-bg)] p-12 text-center reveal">
            <span className="section-label">Ready to Start?</span>
            <h2 className="mb-4">Not sure which service you need?</h2>
            <p className="mx-auto mb-8 max-w-lg text-[var(--nt-text-muted)]">
              Let&apos;s have a discovery call. We&apos;ll assess your environment and recommend the right approach.
            </p>
            <Link to="/book-demo" className="btn btn-primary">
              Book a Free Discovery Call
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
