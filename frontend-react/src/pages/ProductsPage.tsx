import { Link } from 'react-router-dom'
import { ExternalLink, Copy, Check, X } from 'lucide-react'
import { useEffect, useState } from 'react'
import Aurora from '@/components/Aurora'
import SpotlightCard from '@/components/SpotlightCard'
import { SeoHead } from '@/components/SeoHead'
import { ROUTE_SEO } from '@/config/site'
import { jsonLdForRoute } from '@/data/structuredData'
import { products } from '@/data/products'
import { buttonVariants } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import { JpilotRegisterForm } from '@/components/JpilotRegisterForm'
import { isJpilotRegistered, markJpilotRegistered } from '@/utils/jpilotRegistration'

const JPILOT_REDIRECT = 'https://jpilot.nexxus-tech.com'

const product = products[0]

function InstallBlock() {
  const [activePlatform, setActivePlatform] = useState(product.installation.platforms[0].id)
  const [copied, setCopied] = useState(false)
  const platform = product.installation.platforms.find((p) => p.id === activePlatform)!

  const copyCommand = async () => {
    await navigator.clipboard.writeText(platform.command)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="rounded-[var(--nt-radius-lg)] border border-[var(--nt-border)] bg-[var(--nt-card-bg)] p-6">
      <p className="mb-4 text-sm text-[var(--nt-text-muted)]">{product.installation.prerequisite}</p>
      <div className="mb-4 flex flex-wrap gap-2">
        {product.installation.platforms.map((p) => (
          <button
            key={p.id}
            type="button"
            onClick={() => setActivePlatform(p.id)}
            className={`rounded-lg px-4 py-2 text-sm font-semibold transition-colors ${
              activePlatform === p.id
                ? 'bg-[var(--nt-primary)] text-white'
                : 'bg-white/5 text-[var(--nt-text-muted)] hover:text-white'
            }`}
          >
            {p.name}
          </button>
        ))}
      </div>
      <div className="relative mb-3 rounded-lg bg-[var(--nt-dark)] p-4 font-mono text-sm text-[var(--nt-secondary-l)]">
        <code className="block pr-10 break-all">{platform.command}</code>
        <button
          type="button"
          onClick={copyCommand}
          className="absolute top-3 right-3 text-[var(--nt-text-muted)] hover:text-white"
          aria-label="Copy command"
        >
          {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
        </button>
      </div>
      <p className="text-xs text-[var(--nt-text-muted)]">{platform.hint}</p>
    </div>
  )
}

export default function ProductsPage() {
  const seo = ROUTE_SEO.products
  const [registered, setRegistered] = useState(false)
  const [lightbox, setLightbox] = useState<{ src: string; alt: string } | null>(null)

  useEffect(() => {
    if (!lightbox) return
    const onKeydown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') setLightbox(null)
    }
    document.addEventListener('keydown', onKeydown)
    const previousOverflow = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    return () => {
      document.removeEventListener('keydown', onKeydown)
      document.body.style.overflow = previousOverflow
    }
  }, [lightbox])

  useEffect(() => {
    setRegistered(isJpilotRegistered())
  }, [])

  const onRegistered = (email: string) => {
    markJpilotRegistered(email)
    setRegistered(true)
    window.setTimeout(() => {
      window.location.assign(JPILOT_REDIRECT)
    }, 800)
  }

  return (
    <div id="jpilot" className="products-page">
      <SeoHead
        title={seo.title}
        description={seo.description}
        path={seo.path}
        image={seo.image}
        imageAlt={seo.imageAlt}
        jsonLd={jsonLdForRoute('products')}
      />

      <section className="relative overflow-hidden pt-28 pb-20">
        <div className="absolute inset-0 z-0">
          <Aurora colorStops={['#00A8E0', '#007BA7', '#4DB8E0']} amplitude={1} blend={0.5} />
        </div>
        <div className="absolute inset-0 z-[1] bg-gradient-to-b from-[var(--nt-dark)]/60 to-[var(--nt-dark)]" />

        <div className="container relative z-[2]">
          <div className="mb-12 text-center">
            <p className="mb-4 text-sm tracking-widest text-[var(--nt-text-muted)] uppercase reveal">
              Introducing
            </p>
            <img
              src="/JPilot-logo-big-black.svg"
              alt="JPilot"
              className="mx-auto mb-4 h-20 w-20 reveal"
              width={88}
              height={88}
            />
            <h1 className="reveal">
              <span className="text-[var(--nt-primary-l)]">JP</span>ilot
            </h1>
            <p className="mt-2 text-sm tracking-wide text-white/60 reveal">{product.label}</p>
            <p className="mx-auto mt-4 max-w-2xl text-lg text-[var(--nt-text-muted)] reveal reveal-delay-1">
              {product.tagline}
            </p>
            <p className="mx-auto mt-3 max-w-2xl text-sm text-[var(--nt-text-muted)] reveal reveal-delay-1">
              {product.excerpt}
            </p>
            <p className="mt-2 text-sm text-[var(--nt-text-muted)] reveal reveal-delay-1">
              {product.subline}
            </p>
            <div className="mt-6 flex flex-wrap justify-center gap-4 reveal reveal-delay-1">
              {registered ? (
                <a
                  href={JPILOT_REDIRECT}
                  className={cn(buttonVariants({ variant: 'default' }), 'bg-[var(--nt-primary)]')}
                >
                  Open JPilot
                </a>
              ) : (
                <a href="#register" className={cn(buttonVariants({ variant: 'default' }), 'bg-[var(--nt-primary)]')}>
                  Register for access
                </a>
              )}
              <a href={registered ? '#install' : '#register'} className={buttonVariants({ variant: 'outline' })}>
                {registered ? 'Install JPilot' : 'Get install access'}
              </a>
            </div>
          </div>

          <div className="mx-auto mb-10 max-w-3xl reveal reveal-delay-2">
            <video
              controls
              preload="metadata"
              poster="/videos/install-poster.jpg"
              className="aspect-video w-full rounded-[var(--nt-radius)] bg-[var(--nt-dark-3)]"
            >
              <source src="/videos/install.webm" type="video/webm" />
              <source src="/videos/install.mp4" type="video/mp4" />
            </video>
          </div>

          {registered && (
            <div id="install" className="mx-auto max-w-2xl reveal reveal-delay-2">
              <InstallBlock />
            </div>
          )}

          <div className="mt-8 flex flex-wrap justify-center gap-4 reveal reveal-delay-3">
            <a
              href={product.repoUrl}
              target="_blank"
              rel="noopener noreferrer"
              className={cn(buttonVariants({ variant: 'default' }), 'bg-[var(--nt-primary)]')}
            >
              <ExternalLink className="h-4 w-4" /> View on GitHub
            </a>
            <a
              href={product.links.install}
              target="_blank"
              rel="noopener noreferrer"
              className={buttonVariants({ variant: 'outline' })}
            >
              <ExternalLink className="h-4 w-4" /> Install Guide
            </a>
          </div>
        </div>
      </section>

      <section className="section section-light">
        <div className="container text-center reveal">
          <h2 className="mb-4 text-[var(--nt-light-text)]">Early adopters get a free license</h2>
          <p className="mx-auto max-w-2xl text-gray-600">
            The Free edition lets your team explore JPilot with your own AI provider keys, on your own
            infrastructure. Install during Early Access and we&apos;ll issue a free license under our Terms of Use.
          </p>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="mb-12 text-center reveal">
            <span className="section-label">Capabilities</span>
            <h2 className="section-title">What JPilot Does</h2>
          </div>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {product.capabilities.map((cap, i) => (
              <SpotlightCard
                key={cap.title}
                className={`card reveal reveal-delay-${(i % 3) + 1}`}
                spotlightColor="rgba(0, 168, 224, 0.12)"
              >
                <h3 className="mb-3 text-lg">{cap.title}</h3>
                <p className="text-sm text-[var(--nt-text-muted)]">{cap.body}</p>
              </SpotlightCard>
            ))}
          </div>
        </div>
      </section>

      <section className="section section-dark">
        <div className="container">
          <div className="grid gap-12 lg:grid-cols-2 reveal">
            <div>
              <span className="section-label">Trust &amp; Transparency</span>
              <h2 className="section-title mb-4">{product.trust.title}</h2>
              <p className="mb-6 text-[var(--nt-text-muted)]">{product.trust.lead}</p>
              <ul className="space-y-3">
                {product.trust.bullets.map((b) => (
                  <li key={b} className="flex gap-2 text-sm text-[var(--nt-text-muted)]">
                    <Check className="mt-0.5 h-4 w-4 shrink-0 text-[var(--nt-primary-l)]" />
                    {b}
                  </li>
                ))}
              </ul>
            </div>
            <div className="card">
              <h3 className="mb-3">{product.earlyAccess.title}</h3>
              <p className="text-sm text-[var(--nt-text-muted)]">{product.earlyAccess.body}</p>
            </div>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container grid items-stretch gap-10 lg:grid-cols-2">
          <div className="reveal flex flex-col justify-center">
            <span className="section-label">Operations</span>
            <h2 className="section-title">From design to execution</h2>
            <p className="text-[var(--nt-text-muted)]">
              Start in Architect for structured discovery and formal design documents, then hand off to
              Operator for implementation — without leaving the conversation.
            </p>
          </div>
          <button
            type="button"
            className="reveal reveal-delay-1 h-full min-h-[240px] w-full cursor-zoom-in overflow-hidden rounded-[var(--nt-radius)] p-0 transition-[filter,transform] duration-200 hover:brightness-110 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--nt-primary-l)]"
            aria-label="View larger: JPilot design-to-execution workflow"
            onClick={() =>
              setLightbox({
                src: '/jpilot/feature-design.png',
                alt: 'JPilot design-to-execution workflow',
              })
            }
          >
            <img
              src="/jpilot/feature-design.png"
              alt="JPilot design-to-execution workflow"
              className="h-full min-h-[240px] w-full rounded-[var(--nt-radius)] object-cover"
              width={720}
              height={480}
            />
          </button>
        </div>
      </section>

      <section id="register" className="section">
        <div className="container mx-auto max-w-2xl reveal">
          {registered ? (
            <>
              <div className="mb-8 text-center">
                <h2 className="section-title">You&apos;re registered</h2>
                <p className="text-[var(--nt-text-muted)]">
                  Install JPilot with one command, then continue to the platform.
                </p>
              </div>
              <InstallBlock />
              <div className="mt-6 text-center">
                <a
                  href={JPILOT_REDIRECT}
                  className={cn(buttonVariants({ variant: 'default' }), 'bg-[var(--nt-primary)]')}
                >
                  Open JPilot
                </a>
              </div>
            </>
          ) : (
            <>
              <div className="mb-8 text-center">
                <h2 className="section-title">Register for JPilot access</h2>
                <p className="text-[var(--nt-text-muted)]">
                  Leave your details to unlock the install command and continue to the platform.
                </p>
              </div>
              <JpilotRegisterForm onRegistered={onRegistered} />
            </>
          )}
        </div>
      </section>

      <section className="section">
        <div className="container text-center reveal">
          <p className="mx-auto max-w-3xl text-xs text-[var(--nt-text-muted)]">{product.disclaimer}</p>
          <div className="mt-8">
            <Link to="/contact" className="btn btn-primary">
              Get Support
            </Link>
          </div>
        </div>
      </section>

      {lightbox && (
        <div
          className="fixed inset-0 z-[10050] flex cursor-zoom-out items-center justify-center bg-[rgba(5,8,18,0.88)] px-12 py-7 backdrop-blur-sm"
          role="dialog"
          aria-modal="true"
          aria-label={lightbox.alt}
          onClick={() => setLightbox(null)}
        >
          <button
            type="button"
            className="absolute top-4 right-4 flex h-10 w-10 cursor-pointer items-center justify-center rounded-[10px] bg-white/10 text-slate-200 hover:bg-white/20 hover:text-white"
            aria-label="Close image"
            onClick={() => setLightbox(null)}
          >
            <X className="h-4 w-4" />
          </button>
          <img
            src={lightbox.src}
            alt={lightbox.alt}
            className="max-h-[88dvh] max-w-[min(1280px,100%)] cursor-default rounded-xl object-contain shadow-[0_24px_80px_rgba(0,0,0,0.5)]"
            onClick={(event) => event.stopPropagation()}
          />
        </div>
      )}
    </div>
  )
}
