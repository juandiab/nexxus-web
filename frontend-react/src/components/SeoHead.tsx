import { Helmet } from 'react-helmet-async'
import {
  SITE_URL,
  SITE_NAME,
  DEFAULT_OG_IMAGE,
  DEFAULT_OG_IMAGE_ALT,
  SITE_OG_IMAGE_WIDTH,
  SITE_OG_IMAGE_HEIGHT,
  SITE_FAVICON,
  APPLE_TOUCH_ICON,
  SITE_MANIFEST,
} from '@/config/site'

export interface SeoOptions {
  title: string
  description: string
  path?: string
  image?: string
  imageAlt?: string
  type?: string
  noindex?: boolean
  jsonLd?: object | object[] | null
}

export function SeoHead({
  title,
  description,
  path = '/',
  image = DEFAULT_OG_IMAGE,
  imageAlt = DEFAULT_OG_IMAGE_ALT,
  type = 'website',
  noindex = false,
  jsonLd = null,
}: SeoOptions) {
  const canonical = path.startsWith('http') ? path : `${SITE_URL}${path}`
  const graph = jsonLd
    ? Array.isArray(jsonLd)
      ? jsonLd
      : [jsonLd]
    : null
  const payload = graph
    ? graph.length === 1
      ? graph[0]
      : { '@context': 'https://schema.org', '@graph': graph }
    : null

  return (
    <Helmet>
      <title>{title}</title>
      <meta name="description" content={description} />
      <meta name="robots" content={noindex ? 'noindex, nofollow' : 'index, follow'} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:type" content={type} />
      <meta property="og:url" content={canonical} />
      <meta property="og:site_name" content={SITE_NAME} />
      <meta property="og:image" content={image} />
      <meta property="og:image:alt" content={imageAlt} />
      <meta property="og:image:width" content={String(SITE_OG_IMAGE_WIDTH)} />
      <meta property="og:image:height" content={String(SITE_OG_IMAGE_HEIGHT)} />
      <meta property="og:locale" content="en_US" />
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={image} />
      <meta name="twitter:image:alt" content={imageAlt} />
      <link rel="canonical" href={canonical} />
      <link rel="manifest" href={SITE_MANIFEST} />
      <link rel="icon" type="image/png" sizes="300x300" href={SITE_FAVICON} />
      <link rel="apple-touch-icon" sizes="180x180" href={APPLE_TOUCH_ICON} />
      {payload && (
        <script type="application/ld+json">{JSON.stringify(payload)}</script>
      )}
    </Helmet>
  )
}
