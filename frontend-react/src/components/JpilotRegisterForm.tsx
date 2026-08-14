import { useMemo, useState, type FormEvent } from 'react'
import axios from 'axios'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Button } from '@/components/ui/button'
import countries from '@/data/countries.json'

const COMPANY_SIZES = ['1–10', '11–50', '51–200', '201–1000', '1000+'] as const
const USE_TYPES = [
  { value: 'company', label: 'Company' },
  { value: 'consultant', label: 'Consultant' },
  { value: 'personal', label: 'Personal use' },
] as const

type UseType = (typeof USE_TYPES)[number]['value']

interface FormState {
  name: string
  email: string
  use_type: UseType | ''
  country: string
  company: string
  company_size: string
}

interface FormErrors {
  name?: string
  email?: string
  use_type?: string
  country?: string
  company?: string
  company_size?: string
}

export function JpilotRegisterForm({
  onRegistered,
}: {
  onRegistered?: (email: string) => void
}) {
  const [form, setForm] = useState<FormState>({
    name: '',
    email: '',
    use_type: '',
    country: '',
    company: '',
    company_size: '',
  })
  const [errors, setErrors] = useState<FormErrors>({})
  const [submitting, setSubmitting] = useState(false)
  const [errorMessage, setErrorMessage] = useState('')

  const showCompany = form.use_type === 'company' || form.use_type === 'consultant'
  const showCompanySize = form.use_type === 'company'
  const companyRequired = form.use_type === 'company'
  const companyLabel = form.use_type === 'consultant' ? 'Company / organization' : 'Company *'

  const countryOptions = useMemo(
    () => countries.map((country) => ({ name: country.name, code: country.code })),
    [],
  )

  const setUseType = (value: string | null) => {
    const useType = (value ?? '') as FormState['use_type']
    setForm((prev) => ({
      ...prev,
      use_type: useType,
      company: useType === 'personal' ? '' : prev.company,
      company_size: useType === 'company' ? prev.company_size : '',
    }))
  }

  const validate = (): boolean => {
    const next: FormErrors = {}
    if (!form.name.trim()) next.name = 'Name is required'
    if (!form.email.trim() || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(form.email)) {
      next.email = 'Valid email is required'
    }
    if (!form.use_type) next.use_type = 'Use type is required'
    if (!form.country) next.country = 'Country is required'
    if (form.use_type === 'company' && !form.company.trim()) {
      next.company = 'Company is required'
    }
    if (form.use_type === 'company' && !form.company_size) {
      next.company_size = 'Company size is required'
    }
    setErrors(next)
    return Object.keys(next).length === 0
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (!validate()) return
    setSubmitting(true)
    setErrorMessage('')
    try {
      const email = form.email.trim()
      await axios.post('/api/jpilot-interest', {
        name: form.name.trim(),
        email,
        use_type: form.use_type,
        country: form.country,
        company: form.use_type === 'personal' ? '' : form.company.trim(),
        company_size: form.use_type === 'company' ? form.company_size : '',
      })
      onRegistered?.(email)
    } catch (err: unknown) {
      const detail = axios.isAxiosError(err) ? err.response?.data?.detail : null
      setErrorMessage(
        typeof detail === 'string'
          ? detail
          : 'Something went wrong. Please try emailing us directly.',
      )
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5 text-left" noValidate>
      <div className="grid gap-5 sm:grid-cols-2">
        <div className="space-y-2">
          <Label htmlFor="jpilot-name">Name *</Label>
          <Input
            id="jpilot-name"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            placeholder="Jane Smith"
            autoComplete="name"
            className={errors.name ? 'border-red-500' : ''}
            required
          />
          {errors.name && <p className="text-xs text-red-400">{errors.name}</p>}
        </div>
        <div className="space-y-2">
          <Label htmlFor="jpilot-email">Email *</Label>
          <Input
            id="jpilot-email"
            type="email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            placeholder="jane@company.com"
            autoComplete="email"
            className={errors.email ? 'border-red-500' : ''}
            required
          />
          {errors.email && <p className="text-xs text-red-400">{errors.email}</p>}
        </div>
      </div>

      <div className="grid gap-5 sm:grid-cols-2">
        <div className="space-y-2">
          <Label>Use type *</Label>
          <Select value={form.use_type} onValueChange={setUseType}>
            <SelectTrigger className={errors.use_type ? 'border-red-500' : ''}>
              <SelectValue placeholder="Select use type…" />
            </SelectTrigger>
            <SelectContent>
              {USE_TYPES.map((opt) => (
                <SelectItem key={opt.value} value={opt.value}>
                  {opt.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          {errors.use_type && <p className="text-xs text-red-400">{errors.use_type}</p>}
        </div>
        <div className="space-y-2">
          <Label>Country *</Label>
          <Select
            value={form.country}
            onValueChange={(value) => setForm({ ...form, country: value ?? '' })}
          >
            <SelectTrigger className={errors.country ? 'border-red-500' : ''}>
              <SelectValue placeholder="Select country…" />
            </SelectTrigger>
            <SelectContent>
              {countryOptions.map((country) => (
                <SelectItem key={country.code} value={country.name}>
                  {country.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          {errors.country && <p className="text-xs text-red-400">{errors.country}</p>}
        </div>
      </div>

      {showCompany && (
        <div className="grid gap-5 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="jpilot-company">{companyLabel}</Label>
            <Input
              id="jpilot-company"
              value={form.company}
              onChange={(e) => setForm({ ...form, company: e.target.value })}
              placeholder={companyRequired ? 'Acme Corp' : 'Optional'}
              autoComplete="organization"
              className={errors.company ? 'border-red-500' : ''}
              required={companyRequired}
            />
            {errors.company && <p className="text-xs text-red-400">{errors.company}</p>}
          </div>
          {showCompanySize && (
            <div className="space-y-2">
              <Label>Company size *</Label>
              <Select
                value={form.company_size}
                onValueChange={(value) => setForm({ ...form, company_size: value ?? '' })}
              >
                <SelectTrigger className={errors.company_size ? 'border-red-500' : ''}>
                  <SelectValue placeholder="Select company size…" />
                </SelectTrigger>
                <SelectContent>
                  {COMPANY_SIZES.map((size) => (
                    <SelectItem key={size} value={size}>
                      {size}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {errors.company_size && (
                <p className="text-xs text-red-400">{errors.company_size}</p>
              )}
            </div>
          )}
        </div>
      )}

      {errorMessage && (
        <p className="rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-300">
          {errorMessage}
        </p>
      )}

      <Button type="submit" disabled={submitting} className="bg-[var(--nt-primary)]">
        {submitting ? 'Registering…' : 'Register and continue'}
      </Button>
    </form>
  )
}
