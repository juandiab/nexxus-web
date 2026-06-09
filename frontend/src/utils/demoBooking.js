import { JPILOT_DEMO_CALENDAR_URL } from '@/config/site.js'

/** Build a Google Calendar booking URL with visitor details as query parameters. */
export function buildDemoBookingUrl(profile) {
  const url = new URL(JPILOT_DEMO_CALENDAR_URL)
  const trimmedName = profile.name.trim()
  const [firstName, ...rest] = trimmedName.split(/\s+/)
  const lastName = rest.join(' ')

  const details = [
    profile.demo_notes?.trim(),
    profile.technologies?.length
      ? `Technologies: ${profile.technologies.join(', ')}`
      : '',
    profile.company ? `Company: ${profile.company}` : '',
  ]
    .filter(Boolean)
    .join('\n')

  const params = {
    name: trimmedName,
    firstName,
    lastName,
    email: profile.email.trim(),
    company: profile.company?.trim() || '',
    service: profile.service || '',
    topic: profile.demo_notes?.trim() || profile.service || 'JPilot demo',
    details,
    enquiry: profile.enquiry_type || 'Book a demo',
  }

  Object.entries(params).forEach(([key, value]) => {
    if (value) url.searchParams.set(key, value)
  })

  return url.toString()
}

/** Plain-text summary for enquiry email and clipboard fallback. */
export function buildDemoBookingSummary(profile) {
  const lines = [
    'Demo booking request (via JPbot)',
    `Name: ${profile.name}`,
    `Email: ${profile.email}`,
  ]
  if (profile.company) lines.push(`Company: ${profile.company}`)
  lines.push(`Interest: ${profile.service}`)
  if (profile.technologies?.length) {
    lines.push(`Technologies: ${profile.technologies.join(', ')}`)
  }
  if (profile.demo_notes?.trim()) {
    lines.push(`Notes: ${profile.demo_notes.trim()}`)
  }
  return lines.join('\n')
}
