import { useEffect, useState } from 'react'
import { Link, NavLink } from 'react-router-dom'
import { Menu } from 'lucide-react'
import { buttonVariants } from '@/components/ui/button'
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from '@/components/ui/sheet'
import { cn } from '@/lib/utils'

const links = [
  { to: '/', label: 'Home' },
  { to: '/services', label: 'Services' },
  { to: '/products', label: 'Products' },
  { to: '/about', label: 'About' },
  { to: '/blog', label: 'Blog' },
  { to: '/book-demo', label: 'Book a Demo' },
]

export default function NavBar() {
  const [scrolled, setScrolled] = useState(false)
  const [open, setOpen] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40)
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? 'bg-[rgba(28,28,30,0.95)] backdrop-blur-md shadow-[0_1px_0_rgba(0,123,167,0.15)]'
          : 'bg-transparent'
      }`}
    >
      <div className="container flex h-[72px] items-center justify-between">
        <Link to="/" className="flex items-center" onClick={() => setOpen(false)}>
          <img
            src="/nexxus-tech-logo-full-large.svg"
            alt="Nexxus Tech"
            className="h-[52px] w-auto max-w-full"
            width={324}
            height={52}
            decoding="async"
          />
        </Link>

        <nav className="hidden items-center gap-1 lg:flex" aria-label="Main navigation">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `inline-flex min-h-12 min-w-12 items-center justify-center rounded-md px-4 py-2 font-[family-name:var(--font-heading)] text-[0.85rem] font-semibold tracking-wider uppercase transition-colors ${
                  isActive
                    ? 'text-white'
                    : 'text-white/75 hover:text-white'
                }`
              }
            >
              {link.label}
            </NavLink>
          ))}
          <Link
            to="/contact"
            className={cn(
              buttonVariants({ variant: 'default' }),
              'ml-2 bg-[var(--nt-primary)] hover:bg-[var(--nt-primary-l)]'
            )}
          >
            Get in Touch
          </Link>
        </nav>

        <Sheet open={open} onOpenChange={setOpen}>
          <SheetTrigger
            className={cn(buttonVariants({ variant: 'ghost', size: 'icon' }), 'lg:hidden')}
            aria-label="Toggle menu"
          >
            <Menu className="h-6 w-6 text-white" />
          </SheetTrigger>
          <SheetContent side="right" className="border-[var(--nt-border)] bg-[var(--nt-dark)]">
            <SheetHeader>
              <SheetTitle className="text-white">Menu</SheetTitle>
            </SheetHeader>
            <nav className="mt-8 flex flex-col gap-2" aria-label="Mobile navigation">
              {links.map((link) => (
                <Link
                  key={link.to}
                  to={link.to}
                  onClick={() => setOpen(false)}
                  className="rounded-md px-4 py-3 font-[family-name:var(--font-heading)] text-sm font-semibold tracking-wider text-white/80 uppercase hover:bg-white/5 hover:text-white"
                >
                  {link.label}
                </Link>
              ))}
              <Link
                to="/contact"
                onClick={() => setOpen(false)}
                className={cn(
                  buttonVariants({ variant: 'default' }),
                  'mt-4 w-full bg-[var(--nt-primary)] text-center'
                )}
              >
                Get in Touch
              </Link>
            </nav>
          </SheetContent>
        </Sheet>
      </div>
    </header>
  )
}
