import { Link } from 'react-router-dom'
import { ExternalLink } from 'lucide-react'

const footerLinks = {
  services: [
    { to: '/services#waf', label: 'WAF & API Protection' },
    { to: '/services#netscaler', label: 'NetScaler / ADC' },
    { to: '/services#zerotrust', label: 'Zero-Trust Architecture' },
    { to: '/services#cloud', label: 'Cloud Security' },
    { to: '/services#ai', label: 'AI & Automation' },
  ],
  products: [
    { to: '/products#jpilot', label: 'JPilot' },
    { to: '/products', label: 'All Products' },
  ],
  company: [
    { to: '/about', label: 'About Us' },
    { to: '/faq', label: 'FAQ' },
    { to: '/blog', label: 'Blog & Insights' },
    { to: '/book-demo', label: 'Book a Demo' },
    { to: '/contact', label: 'Contact' },
  ],
}

export default function AppFooter() {
  return (
    <footer className="relative border-t border-[var(--nt-border)] bg-[var(--nt-dark-2)] pt-16 pb-8">
      <div className="pointer-events-none absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-[var(--nt-primary)] to-transparent opacity-40" />
      <div className="container">
        <div className="grid gap-10 md:grid-cols-2 lg:grid-cols-6">
          <div className="lg:col-span-2">
            <img
              src="/nexxus-tech-logo-full-large.svg"
              alt="Nexxus Tech"
              className="mb-4 h-10 w-auto"
            />
            <p className="mb-6 max-w-sm text-sm leading-relaxed text-[var(--nt-text-muted)]">
              Empowering people and organizations through consulting, architecture,
              shared knowledge, and AI-driven innovation.
            </p>
            <div className="flex gap-3">
              <a
                href="https://www.linkedin.com/in/jotalvaro/"
                target="_blank"
                rel="noopener noreferrer"
                className="flex h-10 w-10 items-center justify-center rounded-lg border border-[var(--nt-border)] text-[var(--nt-secondary)] transition-colors hover:border-[var(--nt-primary)] hover:text-[var(--nt-primary-l)]"
                aria-label="LinkedIn"
              >
                <ExternalLink className="h-4 w-4" />
              </a>
              <a
                href="https://github.com/juandiab"
                target="_blank"
                rel="noopener noreferrer"
                className="flex h-10 w-10 items-center justify-center rounded-lg border border-[var(--nt-border)] text-[var(--nt-secondary)] transition-colors hover:border-[var(--nt-primary)] hover:text-[var(--nt-primary-l)]"
                aria-label="GitHub"
              >
                <ExternalLink className="h-4 w-4" />
              </a>
            </div>
          </div>

          <FooterCol title="Services" links={footerLinks.services} />
          <FooterCol title="Products" links={footerLinks.products} />
          <FooterCol title="Company" links={footerLinks.company} />

          <div>
            <h3 className="mb-4 font-[family-name:var(--font-heading)] text-xs font-bold tracking-widest text-white uppercase">
              Contact
            </h3>
            <ul className="space-y-3 text-sm text-[var(--nt-text-muted)]">
              <li>
                <a href="mailto:contact@nexxus-tech.com" className="hover:text-[var(--nt-secondary)]">
                  contact@nexxus-tech.com
                </a>
              </li>
              <li>nexxus-tech.com</li>
              <li>Colombia · UAE · UK · US</li>
            </ul>
          </div>
        </div>

        <div className="mt-12 flex flex-col items-center justify-between gap-4 border-t border-[var(--nt-border)] pt-8 text-sm text-[var(--nt-text-muted)] md:flex-row">
          <p>© {new Date().getFullYear()} Nexxus Tech. All rights reserved.</p>
          <div className="flex gap-6">
            <a href="https://jpilot.nexxus-tech.com/legal/privacy">Privacy</a>
            <a href="https://jpilot.nexxus-tech.com/legal/terms">Terms of Use</a>
          </div>
        </div>
      </div>
    </footer>
  )
}

function FooterCol({
  title,
  links,
}: {
  title: string
  links: { to: string; label: string }[]
}) {
  return (
    <nav aria-label={title}>
      <h3 className="mb-4 font-[family-name:var(--font-heading)] text-xs font-bold tracking-widest text-white uppercase">
        {title}
      </h3>
      <ul className="space-y-2.5">
        {links.map((link) => (
          <li key={link.to}>
            <Link
              to={link.to}
              className="text-sm text-[var(--nt-text-muted)] transition-colors hover:text-[var(--nt-secondary)]"
            >
              {link.label}
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  )
}
