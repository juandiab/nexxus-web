/** Central site metadata — single source of truth for SEO and structured data. */
export const SITE_URL = 'https://nexxus-tech.com'
export const SITE_NAME = 'Nexxus Tech'
export const SITE_TAGLINE = 'WAF · NetScaler · Cloud Security · AI'
export const SITE_EMAIL = 'contact@nexxus-tech.com'
export const SITE_FAVICON = '/nexxus-tech-favicon.png'
export const APPLE_TOUCH_ICON = '/apple-touch-icon.png'
export const SITE_MANIFEST = '/site.webmanifest'
export const SITE_OG_IMAGE = `${SITE_URL}/nexxus-tech-og.png`
export const SITE_OG_IMAGE_WIDTH = 1200
export const SITE_OG_IMAGE_HEIGHT = 630
export const DEFAULT_OG_IMAGE = SITE_OG_IMAGE
export const DEFAULT_OG_IMAGE_ALT =
  'Nexxus Tech — WAF, NetScaler, cloud security, and AI consulting'
/** Google Calendar appointment schedule — inline embed + share link base. */
export const GOOGLE_APPOINTMENT_SCHEDULE_URL =
  'https://calendar.google.com/calendar/appointments/schedules/AcZssZ1XATx8OuwjeatDb843nItYEV0H4cnwGPJCw3yX7rnAjq3dcrlU7JfKXzu8qb2-jqn1bUXGrXMu?gv=true'
/** @deprecated Use GOOGLE_APPOINTMENT_SCHEDULE_URL */
export const JPILOT_DEMO_CALENDAR_URL = GOOGLE_APPOINTMENT_SCHEDULE_URL
export const JPILOT_OG_IMAGE = `${SITE_URL}/jpilot-og.png`
export const JPILOT_OG_IMAGE_ALT =
  'JPilot — self-hosted AI copilot for NetScaler, F5, and Cisco network appliances'

export const ORGANIZATION = {
  name: SITE_NAME,
  legalName: 'Nexxus Tech',
  url: SITE_URL,
  logo: `${SITE_URL}/nexxus-tech-logo-full-large.svg`,
  email: SITE_EMAIL,
  foundingDate: '2010',
  description:
    'Principal-level consulting in Web Application Firewall (WAF), NetScaler ADC, Zero-Trust Architecture, multicloud security, and AI-powered infrastructure automation. 15+ years of experience across 20+ countries.',
  slogan: 'Securing the World\'s Most Critical Applications',
  areaServed: 'Worldwide',
  knowsAbout: [
    'Web Application Firewall',
    'NetScaler ADC',
    'F5 BIG-IP',
    'Zero-Trust Architecture',
    'Multicloud Security',
    'AWS Security',
    'Azure Security',
    'AI Infrastructure Automation',
    'Application Delivery Controllers',
    'API Security',
    'Citrix NetScaler',
    'Okta',
    'Microsoft Entra ID',
  ],
  sameAs: [
    'https://www.linkedin.com/in/jotalvaro/',
    'https://x.com/NexxusTech',
    'https://github.com/juandiab',
  ],
}

export const FOUNDER = {
  name: 'Juan Pablo Otalvaro',
  jobTitle: 'Founder & Principal Cloud & Security Architect',
  url: `${SITE_URL}/about`,
  sameAs: [
    'https://www.linkedin.com/in/jotalvaro/',
    'https://github.com/juandiab',
  ],
  knowsAbout: [
    'NetScaler WAF',
    'Zero-Trust Architecture',
    'AWS Security',
    'LLM Engineering',
    'Multicloud Security',
  ],
}

export const SERVICES = [
  {
    id: 'waf',
    name: 'Web Application Firewall & API Protection',
    description:
      'Enterprise-grade WAF deployment, policy design, and continuous tuning for Citrix NetScaler ADC and F5 BIG-IP. OWASP Top 10 mitigation, bot management, and API gateway security.',
    url: `${SITE_URL}/services#waf`,
  },
  {
    id: 'netscaler',
    name: 'NetScaler ADC & Application Delivery',
    description:
      'Full lifecycle Citrix NetScaler (ADC) services — high availability, SSL offload, GSLB, content switching, F5 BIG-IP migrations, and performance optimization.',
    url: `${SITE_URL}/services#netscaler`,
  },
  {
    id: 'zerotrust',
    name: 'Zero-Trust Architecture & IAM',
    description:
      'End-to-end Zero-Trust transformations combining NetScaler Gateway, Okta, Azure AD, and DUO for finance, defense, and government deployments.',
    url: `${SITE_URL}/services#zerotrust`,
  },
  {
    id: 'cloud',
    name: 'Multicloud Security Architecture',
    description:
      'Consistent security posture across AWS, Azure, and on-premises with NetScaler as the unified application delivery and security layer.',
    url: `${SITE_URL}/services#cloud`,
  },
  {
    id: 'ai',
    name: 'AI-Powered Infrastructure & Automation',
    description:
      'AI-assisted NetScaler administration, WAF policy drafting, configuration drift detection, and LLM-driven security operations with human review guardrails.',
    url: `${SITE_URL}/services#ai`,
  },
]

export const SOFTWARE_PRODUCTS = [
  {
    name: 'JPilot',
    alternateName: 'NSAgent',
    description:
      'Self-hosted AI management platform for network appliances — chat to plan, configure, and troubleshoot NetScaler, F5, and Cisco. BYO AI keys.',
    url: 'https://nexxus-tech.com/products#jpilot',
    downloadUrl: 'https://install.nexxus-tech.com/jpilot',
    applicationCategory: 'BusinessApplication',
    operatingSystem: 'Docker, Linux, Windows, macOS',
    offers: { price: '0', priceCurrency: 'USD' },
  },
  {
    name: 'Cafeina',
    description:
      'Personal macOS menu bar utility that keeps your Mac awake while enabled. Runs locally with no personal data collection.',
    url: 'https://nexxus-tech.com/cafeina',
    downloadUrl: 'https://github.com/juandiab/Cafeina',
    applicationCategory: 'UtilitiesApplication',
    operatingSystem: 'macOS 13 or later',
    offers: { price: '0', priceCurrency: 'USD' },
  },
  {
    name: 'ConneXt',
    description:
      'Free native SSH terminal for iPhone and iPad. Liquid Glass navigation, split terminals, reusable imported keys, and an optional Command Assistant. No subscription, no in-app purchases.',
    url: 'https://nexxus-tech.com/connext',
    downloadUrl: 'https://apps.apple.com/app/connext',
    applicationCategory: 'DeveloperApplication',
    operatingSystem: 'iOS, iPadOS',
    offers: { price: '0', priceCurrency: 'USD' },
  },
]

/** Static blog slugs for sitemap generation (mirrors backend/data/blog_posts.json). */
export const BLOG_SLUGS = [
  'deploying-my-first-apple-watch-app',
  'build-a-terminal-llm-helper-for-ubuntu-in-python',
  'jpilot-ai-management-platform',
  'netscaler-hybrid-post-quantum-cryptography',
  'netscaler-waf-top10-owasp-2024',
  'zero-trust-architecture-netscaler-okta-azure-ad',
  'ai-powered-netscaler-administration-automation',
  'multicloud-security-aws-azure-netscaler',
]

export const ROUTE_SEO = {
  home: {
    title: 'Nexxus Tech — WAF · NetScaler · Cloud Security · AI',
    description:
      'Principal-level consulting in WAF, NetScaler ADC, Zero-Trust, multicloud security, and AI automation. 15+ years across 20+ countries.',
    path: '/',
  },
  services: {
    title: 'Security & Delivery Services — Nexxus Tech',
    description:
      'Expert WAF & API protection, NetScaler ADC, Zero-Trust architecture, multicloud security, and AI automation — every engagement led by a principal architect.',
    path: '/services',
  },
  products: {
    title: 'JPilot — AI Management Platform for Network Appliances',
    description:
      'Self-hosted AI platform for NetScaler, F5, and Cisco. Chat to plan, configure, and troubleshoot — your keys, your network. Free edition.',
    path: '/products',
    image: JPILOT_OG_IMAGE,
    imageAlt: JPILOT_OG_IMAGE_ALT,
  },
  about: {
    title: 'About Us — Nexxus Tech',
    description:
      'Principal architects in WAF, NetScaler, Zero-Trust, telecom, and AI product design. Remote-first team across Colombia, UAE, UK, and US.',
    path: '/about',
  },
  blog: {
    title: 'Blog & Insights — Nexxus Tech',
    description:
      'Insights on NetScaler WAF, Zero-Trust, multicloud security, post-quantum crypto, and AI-powered ADC automation from global practitioners.',
    path: '/blog',
  },
  contact: {
    title: 'Contact — Nexxus Tech',
    description:
      'Contact Nexxus Tech for WAF assessments, Zero-Trust roadmaps, NetScaler migrations, and AI automation. Remote worldwide, reply within 24h.',
    path: '/contact',
  },
  bookDemo: {
    title: 'Book a Demo — Nexxus Tech',
    description:
      'Schedule a live JPilot or services walkthrough with a Nexxus principal architect. Pick a time that works for you — remote worldwide.',
    path: '/book-demo',
  },
  faq: {
    title: 'FAQ — Nexxus Tech',
    description:
      'FAQs on WAF and NetScaler consulting, OWASP security, remote delivery, discovery calls, and the JPilot AI copilot for network appliances.',
    path: '/faq',
  },
  licensingActivate: {
    title: 'License Activation — Nexxus Tech',
    description: 'Activate your Nexxus Tech software license.',
    path: '/licensing/activate',
    noindex: true,
  },
  cafeina: {
    title: 'Cafeina — macOS Menu Bar Utility',
    description:
      'Cafeina is a personal macOS menu bar app that keeps your Mac awake while enabled. macOS 13+, no personal data collection.',
    path: '/cafeina',
  },
  cafeinaPrivacy: {
    title: 'Cafeina Privacy Policy',
    description:
      'Cafeina does not collect, store, transmit, or sell personal data. No analytics, tracking, accounts, or advertising SDKs.',
    path: '/cafeina/privacy',
  },
  connext: {
    title: 'ConneXt — Free SSH Terminal for iPhone & iPad',
    description:
      'ConneXt is a free native SSH client for iOS and iPadOS by Nexxus-Tech. Liquid Glass navigation, split terminals, reusable keys, optional Command Assistant. No subscription.',
    path: '/connext',
  },
  connextPrivacy: {
    title: 'ConneXt Privacy Policy',
    description:
      'ConneXt does not create user accounts or sell personal data. SSH credentials stay in iOS Keychain. Optional AI keys stay on device; prompts go only to the provider you enable.',
    path: '/connext/privacy',
  },
  connextSupport: {
    title: 'ConneXt Support',
    description:
      'Get help with ConneXt, the free native SSH terminal for iPhone and iPad. Requirements, how to reach us, and what the app is.',
    path: '/connext/support',
  },
  privacy: {
    title: 'ConneXt Privacy Policy',
    description:
      'ConneXt does not create user accounts or sell personal data. SSH credentials stay in iOS Keychain. Optional AI keys stay on device; prompts go only to the provider you enable.',
    path: '/privacy',
  },
  support: {
    title: 'ConneXt Support',
    description:
      'Get help with ConneXt, the free native SSH terminal for iPhone and iPad. Requirements, how to reach us, and what the app is.',
    path: '/support',
  },
}
