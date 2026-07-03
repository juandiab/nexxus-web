import { Link } from 'react-router-dom'
import { ExternalLink, Copy, Check } from 'lucide-react'
import { useState } from 'react'
import Aurora from '@/components/Aurora'
import SpotlightCard from '@/components/SpotlightCard'
import { SeoHead } from '@/components/SeoHead'
import { ROUTE_SEO } from '@/config/site'
import { jsonLdForRoute } from '@/data/structuredData'
import { products } from '@/data/products'
import { buttonVariants } from '@/components/ui/button'
import { cn } from '@/lib/utils'

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
            <p className="mx-auto mt-4 max-w-2xl text-lg text-[var(--nt-text-muted)] reveal reveal-delay-1">
              {product.tagline}
            </p>
            <p className="mt-2 text-sm text-[var(--nt-text-muted)] reveal reveal-delay-1">
              {product.subline}
            </p>
          </div>

          <div id="install" className="mx-auto max-w-2xl reveal reveal-delay-2">
            <InstallBlock />
          </div>

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
            Install JPilot during Early Access and we&apos;ll issue you a free license under our Terms of Use.
            Bring your own AI keys, run it on your own infrastructure.
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
        <div className="container text-center reveal">
          <p className="mx-auto max-w-3xl text-xs text-[var(--nt-text-muted)]">{product.disclaimer}</p>
          <div className="mt-8">
            <Link to="/contact" className="btn btn-primary">
              Get Support
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
