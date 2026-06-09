import {
  SITE_URL,
  SITE_NAME,
  SITE_EMAIL,
  DEFAULT_OG_IMAGE,
  ORGANIZATION,
  FOUNDER,
  SERVICES,
  SOFTWARE_PRODUCTS,
} from '@/config/site.js'
import { faqs } from '@/data/faqs.js'
import { products, JPILOT_LOGOS } from '@/data/products.js'

const SCHEMA_CONTEXT = 'https://schema.org'

function orgBase() {
  return {
    '@type': 'Organization',
    '@id': `${SITE_URL}/#organization`,
    name: ORGANIZATION.name,
    legalName: ORGANIZATION.legalName,
    url: ORGANIZATION.url,
    logo: {
      '@type': 'ImageObject',
      url: ORGANIZATION.logo,
    },
    email: ORGANIZATION.email,
    description: ORGANIZATION.description,
    slogan: ORGANIZATION.slogan,
    foundingDate: ORGANIZATION.foundingDate,
    areaServed: ORGANIZATION.areaServed,
    knowsAbout: ORGANIZATION.knowsAbout,
    sameAs: ORGANIZATION.sameAs,
    founder: { '@id': `${SITE_URL}/#founder` },
  }
}

export function organizationSchema() {
  return orgBase()
}

export function founderPersonSchema() {
  return {
    '@type': 'Person',
    '@id': `${SITE_URL}/#founder`,
    name: FOUNDER.name,
    jobTitle: FOUNDER.jobTitle,
    url: FOUNDER.url,
    worksFor: { '@id': `${SITE_URL}/#organization` },
    knowsAbout: FOUNDER.knowsAbout,
    sameAs: FOUNDER.sameAs,
  }
}

export function websiteSchema() {
  return {
    '@type': 'WebSite',
    '@id': `${SITE_URL}/#website`,
    name: SITE_NAME,
    url: SITE_URL,
    description: ORGANIZATION.description,
    publisher: { '@id': `${SITE_URL}/#organization` },
    inLanguage: 'en',
  }
}

export function professionalServiceSchema() {
  return {
    '@type': 'ProfessionalService',
    '@id': `${SITE_URL}/#professional-service`,
    name: SITE_NAME,
    url: SITE_URL,
    description: ORGANIZATION.description,
    email: SITE_EMAIL,
    areaServed: ORGANIZATION.areaServed,
    knowsAbout: ORGANIZATION.knowsAbout,
    provider: { '@id': `${SITE_URL}/#organization` },
    hasOfferCatalog: {
      '@type': 'OfferCatalog',
      name: 'Nexxus Tech Consulting Services',
      itemListElement: SERVICES.map((svc, i) => ({
        '@type': 'Offer',
        position: i + 1,
        itemOffered: {
          '@type': 'Service',
          '@id': `${SITE_URL}/services#${svc.id}`,
          name: svc.name,
          description: svc.description,
          url: svc.url,
          provider: { '@id': `${SITE_URL}/#organization` },
        },
      })),
    },
  }
}

export function servicesPageSchema() {
  return SERVICES.map((svc) => ({
    '@type': 'Service',
    '@id': `${SITE_URL}/services#${svc.id}`,
    name: svc.name,
    description: svc.description,
    url: svc.url,
    provider: { '@id': `${SITE_URL}/#organization` },
    areaServed: ORGANIZATION.areaServed,
    serviceType: svc.name,
  }))
}

export function aboutTeamPersonSchemas() {
  const members = [
    {
      name: 'Juan Pablo Otalvaro',
      jobTitle: 'Founder & Principal Cloud & Security Architect',
      description:
        'Principal Cloud & Security Architect with 15+ years leading multicloud security transformations across 50+ countries. Citrix SME, AWS Security Specialty certified.',
      knowsAbout: ['WAF', 'Zero-Trust', 'NetScaler', 'AWS Security', 'LLM Engineering'],
    },
    {
      name: 'Jhonny León',
      jobTitle: 'Principal Engineer · Telecom & Cloud Solutions Architect',
      description:
        'Telecom & Cloud Solutions Architect with 15+ years in SS7/Diameter signaling, Oracle STP/vPIC, and OCI deployments for Tier-1 operators.',
      knowsAbout: ['SS7', 'Diameter', 'OCI', 'Telecom Core', 'vPIC'],
    },
    {
      name: 'Vanessa Cabrera Figueredo',
      jobTitle: 'Principal Product Experience Designer · AI & Enterprise UX',
      description:
        'Product Experience Designer with 10+ years specializing in AI-driven UX, fintech, healthtech, and enterprise platforms.',
      knowsAbout: ['Product Experience Design', 'AI-Driven UX', 'Fintech', 'Design Systems'],
    },
    {
      name: 'Sebastian Garcia Tabares',
      jobTitle: 'Principal Enterprise Networking Architect · CCIE Enterprise',
      description:
        'Enterprise Networking Architect with 15+ years in Cisco DNA, SD-Access, SD-WAN, and technical pre-sales for global organizations.',
      knowsAbout: ['Cisco DNA', 'SD-Access', 'SD-WAN', 'CCIE Enterprise', 'Cybersecurity'],
    },
  ]

  return members.map((m, i) => ({
    '@type': 'Person',
    '@id': `${SITE_URL}/about#team-${i + 1}`,
    name: m.name,
    jobTitle: m.jobTitle,
    description: m.description,
    knowsAbout: m.knowsAbout,
    worksFor: { '@id': `${SITE_URL}/#organization` },
    url: `${SITE_URL}/about`,
  }))
}

export function softwareApplicationSchemas() {
  return SOFTWARE_PRODUCTS.map((product) => ({
    '@type': 'SoftwareApplication',
    '@id': `${SITE_URL}/products#${product.name.toLowerCase()}`,
    name: product.name,
    alternateName: product.alternateName,
    description: product.description,
    url: product.url,
    downloadUrl: product.downloadUrl,
    applicationCategory: product.applicationCategory,
    operatingSystem: product.operatingSystem,
    author: { '@id': `${SITE_URL}/#organization` },
    offers: {
      '@type': 'Offer',
      price: product.offers.price,
      priceCurrency: product.offers.priceCurrency,
    },
  }))
}

export function productsPageSchema() {
  return {
    '@type': 'CollectionPage',
    '@id': `${SITE_URL}/products#productspage`,
    name: 'Nexxus Tech Products',
    description:
      'Software products built by Nexxus Tech practitioners, including JPilot NetScaler AI copilot.',
    url: `${SITE_URL}/products`,
    publisher: { '@id': `${SITE_URL}/#organization` },
    hasPart: products.map((p) => ({
      '@type': 'SoftwareApplication',
      '@id': `${SITE_URL}/products#${p.id}`,
      name: p.name,
      description:
        'Self-hosted AI management platform for NetScaler, F5, and Cisco — chat to plan, configure, and troubleshoot. BYO AI keys.',
      image: `${SITE_URL}${JPILOT_LOGOS.dark}`,
      url: `${SITE_URL}/products#${p.id}`,
      downloadUrl: p.links.install,
      applicationCategory: 'BusinessApplication',
      operatingSystem: 'Docker, Linux, Windows, macOS',
      author: { '@id': `${SITE_URL}/#organization` },
    })),
  }
}

export function breadcrumbSchema(items) {
  return {
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: item.name,
      item: item.url.startsWith('http') ? item.url : `${SITE_URL}${item.url}`,
    })),
  }
}

export function blogPostingSchema(post) {
  const postUrl = `${SITE_URL}/blog/${post.slug}`
  return {
    '@type': 'BlogPosting',
    '@id': `${postUrl}#article`,
    headline: post.title,
    description: post.excerpt,
    url: postUrl,
    datePublished: post.date,
    dateModified: post.date,
    author: {
      '@type': 'Person',
      name: post.author,
      jobTitle: post.author_role,
      worksFor: { '@id': `${SITE_URL}/#organization` },
    },
    publisher: { '@id': `${SITE_URL}/#organization` },
    mainEntityOfPage: { '@type': 'WebPage', '@id': postUrl },
    articleSection: post.category,
    keywords: post.tags?.join(', '),
    inLanguage: 'en',
    image: DEFAULT_OG_IMAGE,
  }
}

export function blogListSchema() {
  return {
    '@type': 'Blog',
    '@id': `${SITE_URL}/blog#blog`,
    name: 'Nexxus Tech Blog & Insights',
    description:
      'Technical articles on NetScaler WAF, Zero-Trust, multicloud security, and AI-powered ADC automation.',
    url: `${SITE_URL}/blog`,
    publisher: { '@id': `${SITE_URL}/#organization` },
    inLanguage: 'en',
  }
}

export function contactPageSchema() {
  return {
    '@type': 'ContactPage',
    '@id': `${SITE_URL}/contact#contactpage`,
    name: 'Contact Nexxus Tech',
    description:
      'Contact Nexxus Tech for WAF, NetScaler, Zero-Trust, multicloud security, and AI automation consulting.',
    url: `${SITE_URL}/contact`,
    mainEntity: { '@id': `${SITE_URL}/#organization` },
  }
}

export function faqPageSchema() {
  return {
    '@type': 'FAQPage',
    '@id': `${SITE_URL}/faq#faqpage`,
    name: 'Nexxus Tech Frequently Asked Questions',
    url: `${SITE_URL}/faq`,
    mainEntity: faqs.map((faq) => ({
      '@type': 'Question',
      name: faq.title,
      acceptedAnswer: {
        '@type': 'Answer',
        text: faq.description,
      },
    })),
  }
}

/** Build the JSON-LD graph for a named route. */
export function jsonLdForRoute(routeName, extra = {}) {
  const base = [
    { '@context': SCHEMA_CONTEXT, ...organizationSchema() },
    { '@context': SCHEMA_CONTEXT, ...founderPersonSchema() },
    { '@context': SCHEMA_CONTEXT, ...websiteSchema() },
  ]

  switch (routeName) {
    case 'home':
      return [
        ...base,
        { '@context': SCHEMA_CONTEXT, ...professionalServiceSchema() },
        ...softwareApplicationSchemas().map((s) => ({ '@context': SCHEMA_CONTEXT, ...s })),
        {
          '@context': SCHEMA_CONTEXT,
          ...breadcrumbSchema([{ name: 'Home', url: '/' }]),
        },
      ]
    case 'services':
      return [
        ...base,
        ...servicesPageSchema().map((s) => ({ '@context': SCHEMA_CONTEXT, ...s })),
        {
          '@context': SCHEMA_CONTEXT,
          ...breadcrumbSchema([
            { name: 'Home', url: '/' },
            { name: 'Services', url: '/services' },
          ]),
        },
      ]
    case 'products':
      return [
        ...base,
        { '@context': SCHEMA_CONTEXT, ...productsPageSchema() },
        ...softwareApplicationSchemas().map((s) => ({ '@context': SCHEMA_CONTEXT, ...s })),
        {
          '@context': SCHEMA_CONTEXT,
          ...breadcrumbSchema([
            { name: 'Home', url: '/' },
            { name: 'Products', url: '/products' },
          ]),
        },
      ]
    case 'about':
      return [
        ...base,
        ...aboutTeamPersonSchemas().map((s) => ({ '@context': SCHEMA_CONTEXT, ...s })),
        {
          '@context': SCHEMA_CONTEXT,
          ...breadcrumbSchema([
            { name: 'Home', url: '/' },
            { name: 'About', url: '/about' },
          ]),
        },
      ]
    case 'blog':
      return [
        ...base,
        { '@context': SCHEMA_CONTEXT, ...blogListSchema() },
        {
          '@context': SCHEMA_CONTEXT,
          ...breadcrumbSchema([
            { name: 'Home', url: '/' },
            { name: 'Blog', url: '/blog' },
          ]),
        },
      ]
    case 'contact':
      return [
        ...base,
        { '@context': SCHEMA_CONTEXT, ...contactPageSchema() },
        {
          '@context': SCHEMA_CONTEXT,
          ...breadcrumbSchema([
            { name: 'Home', url: '/' },
            { name: 'Contact', url: '/contact' },
          ]),
        },
      ]
    case 'faq':
      return [
        ...base,
        { '@context': SCHEMA_CONTEXT, ...faqPageSchema() },
        {
          '@context': SCHEMA_CONTEXT,
          ...breadcrumbSchema([
            { name: 'Home', url: '/' },
            { name: 'FAQ', url: '/faq' },
          ]),
        },
      ]
    case 'blog-post':
      if (!extra.post) return base
      return [
        ...base,
        { '@context': SCHEMA_CONTEXT, ...blogPostingSchema(extra.post) },
        {
          '@context': SCHEMA_CONTEXT,
          ...breadcrumbSchema([
            { name: 'Home', url: '/' },
            { name: 'Blog', url: '/blog' },
            { name: extra.post.title, url: `/blog/${extra.post.slug}` },
          ]),
        },
      ]
    default:
      return base
  }
}
