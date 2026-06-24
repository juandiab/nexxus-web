import {
  SITE_URL,
  SITE_NAME,
  SITE_FAVICON,
  APPLE_TOUCH_ICON,
  SITE_MANIFEST,
  DEFAULT_OG_IMAGE,
  DEFAULT_OG_IMAGE_ALT,
  SITE_OG_IMAGE_WIDTH,
  SITE_OG_IMAGE_HEIGHT,
} from '@/config/site.js'

const MANAGED_ATTR = 'data-seo-managed'

function upsertMeta(attr, key, content) {
  document
    .querySelectorAll(`meta[${attr}="${key}"]:not([${MANAGED_ATTR}])`)
    .forEach((el) => el.remove())

  const selector = `meta[${attr}="${key}"][${MANAGED_ATTR}]`
  let el = document.querySelector(selector)

  if (!content) {
    el?.remove()
    return
  }

  if (!el) {
    el = document.createElement('meta')
    el.setAttribute(attr, key)
    el.setAttribute(MANAGED_ATTR, '')
    document.head.appendChild(el)
  }
  el.setAttribute('content', content)
}

function upsertLink(rel, href, extra = {}) {
  document
    .querySelectorAll(`link[rel="${rel}"]:not([${MANAGED_ATTR}])`)
    .forEach((el) => el.remove())

  const selector = `link[rel="${rel}"][${MANAGED_ATTR}]`
  let el = document.querySelector(selector)

  if (!href) {
    el?.remove()
    return
  }

  if (!el) {
    el = document.createElement('link')
    el.setAttribute('rel', rel)
    el.setAttribute(MANAGED_ATTR, '')
    document.head.appendChild(el)
  }
  el.setAttribute('href', href)
  Object.entries(extra).forEach(([k, v]) => el.setAttribute(k, v))
}

/**
 * Apply page-level SEO metadata and optional JSON-LD graphs.
 * @param {object} options
 * @param {string} options.title
 * @param {string} options.description
 * @param {string} [options.path='/']
 * @param {string} [options.image]
 * @param {string} [options.imageAlt]
 * @param {string} [options.type='website']
 * @param {boolean} [options.noindex]
 * @param {object|object[]} [options.jsonLd]
 */
export function applySeo({
  title,
  description,
  path = '/',
  image = DEFAULT_OG_IMAGE,
  imageAlt = DEFAULT_OG_IMAGE_ALT,
  type = 'website',
  noindex = false,
  jsonLd = null,
}) {
  const canonical = path.startsWith('http') ? path : `${SITE_URL}${path}`

  document.title = title

  upsertMeta('name', 'description', description)
  upsertMeta('name', 'robots', noindex ? 'noindex, nofollow' : 'index, follow')

  upsertMeta('property', 'og:title', title)
  upsertMeta('property', 'og:description', description)
  upsertMeta('property', 'og:type', type)
  upsertMeta('property', 'og:url', canonical)
  upsertMeta('property', 'og:site_name', SITE_NAME)
  upsertMeta('property', 'og:image', image)
  upsertMeta('property', 'og:image:alt', imageAlt)
  upsertMeta('property', 'og:image:width', String(SITE_OG_IMAGE_WIDTH))
  upsertMeta('property', 'og:image:height', String(SITE_OG_IMAGE_HEIGHT))
  upsertMeta('property', 'og:locale', 'en_US')

  upsertMeta('name', 'twitter:card', 'summary_large_image')
  upsertMeta('name', 'twitter:title', title)
  upsertMeta('name', 'twitter:description', description)
  upsertMeta('name', 'twitter:image', image)
  upsertMeta('name', 'twitter:image:alt', imageAlt)

  upsertLink('canonical', canonical)
  upsertLink('manifest', SITE_MANIFEST)
  upsertLink('icon', SITE_FAVICON, { type: 'image/png', sizes: '300x300' })
  upsertLink('apple-touch-icon', APPLE_TOUCH_ICON, { sizes: '180x180' })

  setJsonLd('seo-jsonld', jsonLd)
}

/**
 * Inject or replace a JSON-LD script block.
 * @param {string} id
 * @param {object|object[]|null} data
 */
export function setJsonLd(id, data) {
  const existing = document.getElementById(id)
  if (!data) {
    existing?.remove()
    return
  }

  const graph = Array.isArray(data) ? data : [data]
  const payload = graph.length === 1 ? graph[0] : { '@context': 'https://schema.org', '@graph': graph }

  let script = existing
  if (!script) {
    script = document.createElement('script')
    script.id = id
    script.type = 'application/ld+json'
    document.head.appendChild(script)
  }
  script.textContent = JSON.stringify(payload)
}
