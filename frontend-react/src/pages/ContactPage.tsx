import type { ReactNode, ComponentType, FormEvent } from 'react'
import { useState } from 'react'
import axios from 'axios'
import { Mail, Globe, MapPin, Clock, Send, Loader2 } from 'lucide-react'
import { SeoHead } from '@/components/SeoHead'
import { ROUTE_SEO } from '@/config/site'
import { jsonLdForRoute } from '@/data/structuredData'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Button } from '@/components/ui/button'

const expertise = [
  'WAF Policy Design', 'NetScaler ADC', 'F5 BIG-IP',
  'Zero-Trust', 'Okta / Azure AD', 'AWS Security',
  'Multicloud Security', 'AI Automation', 'Citrix Cloud',
  'DaaS / CVAD', 'GSLB', 'API Security',
]

const serviceOptions = [
  'WAF & API Protection',
  'NetScaler / ADC',
  'Zero-Trust Architecture',
  'Multicloud Security',
  'AI & Automation',
  'Citrix Virtual Apps & Desktops',
  'Other / Discovery Call',
]

interface FormState {
  name: string
  email: string
  company: string
  service: string
  message: string
}

interface FormErrors {
  name?: string
  email?: string
  message?: string
}

export default function ContactPage() {
  const seo = ROUTE_SEO.contact
  const [form, setForm] = useState<FormState>({
    name: '', email: '', company: '', service: '', message: '',
  })
  const [errors, setErrors] = useState<FormErrors>({})
  const [submitting, setSubmitting] = useState(false)
  const [submitStatus, setSubmitStatus] = useState<'success' | 'error' | ''>('')
  const [errorMessage, setErrorMessage] = useState('')

  const validate = (): boolean => {
    const next: FormErrors = {}
    if (!form.name.trim()) next.name = 'Name is required'
    if (!form.email.trim() || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(form.email)) {
      next.email = 'Valid email is required'
    }
    if (!form.message.trim() || form.message.length < 10) {
      next.message = 'Please provide a message (at least 10 characters)'
    }
    setErrors(next)
    return Object.keys(next).length === 0
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (!validate()) return
    setSubmitting(true)
    setSubmitStatus('')
    try {
      await axios.post('/api/contact', form)
      setSubmitStatus('success')
      setForm({ name: '', email: '', company: '', service: '', message: '' })
    } catch (err: unknown) {
      setSubmitStatus('error')
      const detail = axios.isAxiosError(err) ? err.response?.data?.detail : null
      setErrorMessage(
        typeof detail === 'string'
          ? detail
          : 'Something went wrong. Please try emailing us directly.'
      )
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="contact-page">
      <SeoHead {...seo} jsonLd={jsonLdForRoute('contact')} />

      <section className="page-hero">
        <div className="page-hero-bg" />
        <div className="container page-hero-content">
          <span className="section-label reveal">Get in Touch</span>
          <h1 className="reveal reveal-delay-1">
            Let&apos;s Start a<br />
            <span className="gradient-text">Conversation</span>
          </h1>
          <p className="page-hero-subtitle reveal reveal-delay-2">
            Whether you need a WAF assessment, a Zero-Trust roadmap, or just want to
            explore what&apos;s possible — we&apos;re here.
          </p>
        </div>
      </section>

      <section className="section bg-[var(--nt-dark-2)]">
        <div className="container grid gap-16 lg:grid-cols-[1fr_420px]">
          <div className="reveal">
            <h2 className="mb-2 text-2xl">Send Us a Message</h2>
            <p className="mb-8 text-sm text-[var(--nt-text-muted)]">
              We respond within 24 hours on business days.
            </p>

            <form onSubmit={handleSubmit} className="space-y-5">
              <div className="grid gap-5 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="name">Full Name *</Label>
                  <Input
                    id="name"
                    value={form.name}
                    onChange={(e) => setForm({ ...form, name: e.target.value })}
                    placeholder="John Smith"
                    className={errors.name ? 'border-red-500' : ''}
                    required
                  />
                  {errors.name && <p className="text-xs text-red-400">{errors.name}</p>}
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">Email Address *</Label>
                  <Input
                    id="email"
                    type="email"
                    value={form.email}
                    onChange={(e) => setForm({ ...form, email: e.target.value })}
                    placeholder="john@company.com"
                    className={errors.email ? 'border-red-500' : ''}
                    required
                  />
                  {errors.email && <p className="text-xs text-red-400">{errors.email}</p>}
                </div>
              </div>

              <div className="grid gap-5 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="company">Company / Organization</Label>
                  <Input
                    id="company"
                    value={form.company}
                    onChange={(e) => setForm({ ...form, company: e.target.value })}
                    placeholder="Acme Corp"
                  />
                </div>
                <div className="space-y-2">
                  <Label>Service Interest</Label>
                  <Select
                    value={form.service}
                    onValueChange={(v) => setForm({ ...form, service: v ?? '' })}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select a service..." />
                    </SelectTrigger>
                    <SelectContent>
                      {serviceOptions.map((opt) => (
                        <SelectItem key={opt} value={opt}>
                          {opt}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="message">Message *</Label>
                <Textarea
                  id="message"
                  rows={6}
                  value={form.message}
                  onChange={(e) => setForm({ ...form, message: e.target.value })}
                  placeholder="Tell us about your project, environment, or challenge..."
                  className={errors.message ? 'border-red-500' : ''}
                  required
                />
                {errors.message && <p className="text-xs text-red-400">{errors.message}</p>}
              </div>

              {submitStatus === 'success' && (
                <div className="rounded-lg border border-green-500/30 bg-green-500/10 p-4 text-sm text-green-400" role="status">
                  Message sent! We&apos;ll be in touch within 24 hours.
                </div>
              )}
              {submitStatus === 'error' && (
                <div className="rounded-lg border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-400" role="alert">
                  {errorMessage}
                </div>
              )}

              <Button
                type="submit"
                disabled={submitting}
                className="bg-[var(--nt-primary)] hover:bg-[var(--nt-primary-l)]"
              >
                {submitting ? (
                  <><Loader2 className="h-4 w-4 animate-spin" /> Sending...</>
                ) : (
                  <><Send className="h-4 w-4" /> Send Message</>
                )}
              </Button>
            </form>
          </div>

          <div className="space-y-6 reveal reveal-delay-2">
            <div className="card">
              <h3 className="mb-6 text-lg">Contact Information</h3>
              <div className="space-y-5">
                <InfoItem icon={Mail} label="Email">
                  <a href="mailto:contact@nexxus-tech.com">contact@nexxus-tech.com</a>
                </InfoItem>
                <InfoItem icon={Globe} label="Website">
                  nexxus-tech.com
                </InfoItem>
                <InfoItem icon={MapPin} label="Global Presence">
                  Colombia · UAE · UK · US
                </InfoItem>
              </div>
            </div>

            <div className="card flex gap-4">
              <Clock className="h-6 w-6 shrink-0 text-[var(--nt-primary-l)]" />
              <div>
                <strong className="text-white">Quick Response</strong>
                <p className="mt-1 text-sm text-[var(--nt-text-muted)]">
                  We typically respond within 24 hours on business days.
                </p>
              </div>
            </div>

            <div className="card">
              <span className="mb-3 block text-xs font-bold tracking-widest text-[var(--nt-text-muted)] uppercase">
                Areas of Engagement
              </span>
              <div className="flex flex-wrap gap-2">
                {expertise.map((item) => (
                  <span key={item} className="tag">
                    {item}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

function InfoItem({
  icon: Icon,
  label,
  children,
}: {
  icon: ComponentType<{ className?: string }>
  label: string
  children: ReactNode
}) {
  return (
    <div className="flex gap-4">
      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-[var(--nt-primary)]/20 text-[var(--nt-primary-l)]">
        <Icon className="h-4 w-4" />
      </div>
      <div>
        <span className="block text-xs font-bold tracking-widest text-[var(--nt-text-muted)] uppercase">
          {label}
        </span>
        <span className="text-sm">{children}</span>
      </div>
    </div>
  )
}
