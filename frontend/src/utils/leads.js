/**
 * Lead capture hooks for public marketing forms.
 *
 * Production path: POST /api/contact creates a Mongo lead via backend
 * `create_web_form_lead` (source=web_form, status=new) when the contact
 * handler runs — no separate client call required.
 *
 * Optional direct API (admin sibling / future public route):
 *   POST /api/leads/web  → WebFormLeadInput (not exposed yet)
 *
 * Query params from /ai-integration CTAs:
 *   service  — pre-selects ContactView service dropdown
 *   locale   — en | es, forwarded as ContactRequest.locale
 *   source   — page id (e.g. ai-integration) appended to lead notes
 *   package  — diagnostic | pilot | system | retainer (optional)
 */

export const LEAD_SOURCE_WEB_FORM = 'web_form'

/** Build contact route query for AI Integration CTAs. */
export function aiIntegrationContactQuery(locale, packageId = null) {
  const service =
    locale === 'es' ? 'Consultoría de Integración de IA' : 'AI Integration Consulting'
  const query = {
    service,
    locale,
    source: 'ai-integration',
  }
  if (packageId) query.package = packageId
  return query
}
