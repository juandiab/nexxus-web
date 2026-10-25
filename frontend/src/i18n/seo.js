import { AI_INTEGRATION_COPY } from '@/data/aiIntegrationCopy.js'

/**
 * Spanish document titles and descriptions.
 * English values stay in ROUTE_SEO and are passed through unchanged.
 * Paths, images, and JSON-LD are never replaced here.
 */
export const SEO_ES = {
  home: {
    title: 'Nexxus Tech — WAF · NetScaler · Seguridad en la nube · IA',
    description:
      'Consultoría de nivel principal en WAF, NetScaler ADC, Zero Trust, seguridad multicloud y automatización con IA. Más de 15 años en más de 20 países.',
  },
  services: {
    title: 'Servicios de seguridad y entrega — Nexxus Tech',
    description:
      'Protección WAF y API, NetScaler ADC, arquitectura Zero Trust, seguridad multicloud y automatización con IA. Cada proyecto lo lidera un arquitecto principal.',
  },
  products: {
    title: 'JPilot — Plataforma de gestión con IA para equipos de red',
    description:
      'Plataforma de IA autoalojada para NetScaler, F5 y Cisco. Planifique, configure y diagnostique por chat: sus claves, su red. Edición gratuita.',
  },
  about: {
    title: 'Quiénes somos — Nexxus Tech',
    description:
      'Arquitectos principales en WAF, NetScaler, Zero Trust, telecom y diseño de productos con IA. Equipo remoto en Colombia, EAU, Reino Unido, España y EE. UU.',
  },
  blog: {
    title: 'Blog y perspectivas — Nexxus Tech',
    description:
      'Perspectivas sobre WAF en NetScaler, Zero Trust, seguridad multicloud, criptografía poscuántica y automatización de ADC con IA, escritas por profesionales.',
  },
  contact: {
    title: 'Contacto — Nexxus Tech',
    description:
      'Contacte a Nexxus Tech para evaluaciones de WAF, hojas de ruta Zero Trust, migraciones de NetScaler y automatización con IA. Remoto, respuesta en 24 horas.',
  },
  'book-demo': {
    title: 'Agende una demo — Nexxus Tech',
    description:
      'Agende un recorrido en vivo de JPilot o de nuestros servicios con un arquitecto principal de Nexxus. Elija el horario que le convenga. Remoto.',
  },
  faq: {
    title: 'Preguntas frecuentes — Nexxus Tech',
    description:
      'Preguntas sobre consultoría en WAF y NetScaler, seguridad OWASP, trabajo remoto, llamadas de descubrimiento y JPilot, el copiloto de IA para equipos de red.',
  },
  'licensing-activate': {
    title: 'Activación de licencia — Nexxus Tech',
    description: 'Active su licencia de software de Nexxus Tech.',
  },
  cafeina: {
    title: 'Cafeina — Utilidad de la barra de menús para macOS',
    description:
      'Cafeina es una aplicación personal de la barra de menús de macOS que mantiene el Mac despierto mientras está activa. macOS 13 o posterior, sin recolección de datos personales.',
  },
  'cafeina-privacy': {
    title: 'Política de privacidad de Cafeina',
    description:
      'Cafeina no recopila, almacena, transmite ni vende datos personales. Sin analítica, rastreo, cuentas ni SDK de publicidad.',
  },
  connext: {
    title: 'ConneXt — Terminal SSH gratuita para iPhone y iPad',
    description:
      'ConneXt es un cliente SSH nativo y gratuito para iOS y iPadOS, de Nexxus-Tech. Navegación Liquid Glass, terminales divididas, claves reutilizables y Command Assistant opcional. Sin suscripción.',
  },
  'connext-privacy': {
    title: 'Política de privacidad de ConneXt',
    description:
      'ConneXt no crea cuentas de usuario ni vende datos personales. Las credenciales SSH permanecen en el llavero de iOS. Las claves de IA opcionales se quedan en el dispositivo; los prompts van solo al proveedor que usted active.',
  },
  'connext-support': {
    title: 'Soporte de ConneXt',
    description:
      'Ayuda con ConneXt, la terminal SSH nativa y gratuita para iPhone y iPad. Requisitos, cómo contactarnos y qué es la aplicación.',
  },
  privacy: {
    title: 'Política de privacidad de ConneXt',
    description:
      'ConneXt no crea cuentas de usuario ni vende datos personales. Las credenciales SSH permanecen en el llavero de iOS. Las claves de IA opcionales se quedan en el dispositivo; los prompts van solo al proveedor que usted active.',
  },
  support: {
    title: 'Soporte de ConneXt',
    description:
      'Ayuda con ConneXt, la terminal SSH nativa y gratuita para iPhone y iPad. Requisitos, cómo contactarnos y qué es la aplicación.',
  },
  'logo-test': {
    title: 'Vista previa del logotipo — Nexxus Tech',
    description:
      'Consultoría de nivel principal en WAF, NetScaler ADC, Zero Trust, seguridad multicloud y automatización con IA. Más de 15 años en más de 20 países.',
  },
}

export function localizedSeo(routeName, seo, currentLocale) {
  if (!seo || currentLocale !== 'es') return seo
  if (routeName === 'ai-integration') {
    return {
      ...seo,
      title: AI_INTEGRATION_COPY.es.seo.title,
      description: AI_INTEGRATION_COPY.es.seo.description,
    }
  }
  const translated = SEO_ES[routeName]
  if (!translated) return seo
  return {
    ...seo,
    title: translated.title,
    description: translated.description,
  }
}
