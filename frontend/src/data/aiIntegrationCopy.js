/** Page-local EN/ES copy for /ai-integration — not site-wide i18n. */
export const AI_INTEGRATION_LOCALE_KEY = 'nexxus-ai-integration-locale'

export const AI_INTEGRATION_SERVICE = {
  en: 'AI Tech for your company',
  es: 'AI Tech en tu empresa',
}

export const AI_INTEGRATION_COPY = {
  en: {
    seo: {
      title: 'AI Tech for your company | Nexxus Tech',
      description:
        'AI automation for small and medium businesses — customer communication on WhatsApp and email, sales follow‑up, internal processes, and a website agent that updates your site in real time. Founder‑led, LatAm and Spain. business@nexxus-tech.com',
    },
    toggle: { en: 'EN', es: 'ES', aria: 'Page language' },
    hero: {
      label: 'AI automation for small and medium businesses',
      h1Before: 'AI Tech for',
      h1Highlight: 'your company',
      subtitle:
        'We automate the work that already costs you hours — answering customers, following up on sales, running the day-to-day, and keeping your website current. Real workflows, a human in charge, results you can measure.',
      positioningLine:
        'You don\'t need to know AI. We guide you through the whole process so you integrate it safely.',
      primaryCta: 'Request a consult',
      secondaryCta: 'Book a 20‑min call',
    },
    useCases: {
      label: 'Where it pays',
      title: 'Four places where it pays for itself',
      subtitle: 'We start where your team already loses hours — not with a demo.',
      items: [
        {
          id: 'customers',
          icon: 'pi pi-comments',
          flowLabel: 'Customers',
          title: 'Customer communication',
          desc: 'First response on WhatsApp, email, and web forms — sorted, answered, and passed to your team when a person needs to step in.',
          bullets: [
            'WhatsApp, email, and form inbox handled',
            'Order and status updates sent for you',
            'Handed to a person when it matters',
          ],
        },
        {
          id: 'sales',
          icon: 'pi pi-chart-line',
          flowLabel: 'Sales',
          title: 'Sales',
          desc: 'Every lead answered and followed up, quotes drafted, reminders sent — so nothing sits in a spreadsheet because someone was busy.',
          bullets: [
            'Leads answered and qualified fast',
            'Quote drafts and follow‑ups',
            'Reminders so no deal goes cold',
          ],
        },
        {
          id: 'operations',
          icon: 'pi pi-cog',
          flowLabel: 'Processes',
          title: 'Internal processes',
          desc: 'The copy‑paste between tools your team does every week — quotes into the system, invoices into the spreadsheet, approvals by email.',
          bullets: [
            'Forms and emails into your systems',
            'Invoices, orders, and approvals routed',
            'Weekly admin done without a person typing',
          ],
        },
        {
          id: 'website',
          icon: 'pi pi-globe',
          flowLabel: 'Web',
          title: 'Your website',
          desc: 'An agent on your site that adds, updates, and removes content in real time — products, prices, hours, promotions — without waiting for a developer.',
          bullets: [
            'Publish or change a page from a message',
            'Products, hours, and offers always current',
            'You approve, it publishes',
          ],
        },
      ],
    },
    audience: {
      label: 'For Whom',
      title: 'For teams of 5 to 100 that already sell and serve customers',
      subtitle:
        'You have customers, orders, and a small team with no spare hours. We don\'t run two‑year transformations — we take one task off your plate, prove it works, then the next. LatAm and Spain, led by the founders.',
      guidanceLine:
        'You don\'t need to know AI. We guide you through the whole process so you integrate it safely.',
      tags: [
        'Owner / founder',
        'Ops lead',
        'Sales team',
        'Customer service',
        '5–100 people',
        'LatAm',
        'Spain',
      ],
    },
    packages: {
      label: 'What We Do',
      title: 'Four ways to start',
      subtitle:
        'Customer communication, sales follow‑up, internal processes, and your website — start with one, grow when it pays.',
      cta: 'Request a consult',
      items: [
        {
          id: 'diagnostic',
          name: 'AI Diagnostic',
          duration: '1–2 weeks',
          icon: 'pi pi-search',
          outcome: 'A short map of where AI pays for itself.',
          bullets: [
            'Process and pain inventory',
            '1–3 automation quick wins',
            'A written plan you can act on, not a slide deck',
          ],
        },
        {
          id: 'pilot',
          name: 'Pilot',
          duration: '4–6 weeks',
          icon: 'pi pi-play',
          outcome: 'One real workflow automated end to end, with a metric.',
          bullets: [
            'One bot, agent, or app your team uses daily',
            'Hours saved, errors avoided, faster response — measured',
            'A person stays in charge',
          ],
        },
        {
          id: 'system',
          name: 'Rollout',
          duration: '2–3 months',
          icon: 'pi pi-sitemap',
          outcome:
            'Several workflows connected — customers, sales, processes, website — and your team running them.',
          bullets: [
            'More than one workflow',
            'Integrations with the tools you already have',
            'Doesn\'t depend on one person (or on us)',
          ],
        },
        {
          id: 'retainer',
          name: 'Monthly plan',
          duration: 'Ongoing',
          icon: 'pi pi-refresh',
          outcome: 'Once it\'s live: new automations, monitoring, and support each month.',
          bullets: [
            'Ongoing improvements, not vague "maintenance"',
            'Agreed monthly scope',
            'Same principals who built it',
          ],
        },
      ],
    },
    process: {
      label: 'How We Work',
      title: 'The path: Diagnose → Pilot → Rollout → Monthly plan',
      subtitle:
        'Start small, measure, then grow. AI takes the repetitive work off your people; it doesn\'t replace them.',
      pipelineCaption:
        'Four steps, one measured path from diagnosis to ongoing support.',
      workflow: {
        caption: 'Real workflows — intake, decision, action, human oversight.',
        nodes: [
          { id: 'intake', label: 'Request' },
          { id: 'decide', label: 'Decide' },
          { id: 'act', label: 'Act' },
          { id: 'human', label: 'Human review' },
        ],
      },
      steps: [
        { name: 'Diagnose', desc: 'Map what your team does by hand and where automation pays.' },
        { name: 'Pilot', desc: 'One workflow live, with a number that proves it.' },
        { name: 'Rollout', desc: 'Connect more flows and tools; your team runs them.' },
        { name: 'Monthly plan', desc: 'New automations, monitoring, and support each month.' },
      ],
      visualTitle: 'A person stays in charge',
      principles: [
        'You don\'t need to be an AI team — we stay with you',
        'Start small, measure, then grow',
        'Your team approves what matters',
        'No black‑box automation — you see what it does',
        'Works with the tools you already use',
        'Your data stays in your accounts',
      ],
    },
    proof: {
      label: 'Who does the work',
      title: 'Founder‑led, remote, 20+ countries',
      subtitle:
        'The same founders who scope your project build it and stay on it. No juniors handed your account after the sale.',
      stats: [
        { value: '15+', label: 'Years of Experience' },
        { value: '20+', label: 'Countries Served' },
        { value: '100+', label: 'Projects Delivered' },
        { value: '100%', label: '100% remote' },
      ],
    },
    cta: {
      label: "Let's Talk",
      title: "Tell us where the work hurts. We'll tell you where AI pays.",
      bodyBefore: 'Reach us at',
      bodyAfter:
        'or use the contact form — we reply within 24 hours on business days and tell you straight if it doesn\'t make sense for you.',
      primaryCta: 'Request a consult',
      secondaryCta: 'Book a 20‑min call',
    },
  },
  es: {
    seo: {
      title: 'AI Tech en tu empresa | Nexxus Tech',
      description:
        'Automatización con IA para PYMEs: comunicación con clientes por WhatsApp y correo, seguimiento comercial, procesos internos y un agente que actualiza tu web en tiempo real. Con los fundadores al frente, LatAm y España. business@nexxus-tech.com',
    },
    toggle: { en: 'EN', es: 'ES', aria: 'Idioma de la página' },
    hero: {
      label: 'Automatización con IA para PYMEs',
      h1Before: 'AI Tech',
      h1Highlight: 'en tu empresa',
      subtitle:
        'Automatizamos el trabajo que ya te cuesta horas: responder a clientes, dar seguimiento a ventas, llevar el día a día y mantener tu web al día. Flujos reales, una persona al mando y resultados que se miden.',
      positioningLine:
        'No necesitas saber de IA. Te guiamos en todo el proceso para que la integres de forma segura.',
      primaryCta: 'Solicitar consulta',
      secondaryCta: 'Agendar una llamada de 20 min',
    },
    useCases: {
      label: 'Dónde paga',
      title: 'Cuatro lugares donde se paga solo',
      subtitle: 'Empezamos donde tu equipo ya pierde horas, no con una demo.',
      items: [
        {
          id: 'customers',
          icon: 'pi pi-comments',
          flowLabel: 'Clientes',
          title: 'Comunicación con clientes',
          desc: 'Primera respuesta en WhatsApp, correo y formularios web: se ordena, se responde y pasa a tu equipo cuando hace falta una persona.',
          bullets: [
            'WhatsApp, correo y formularios atendidos',
            'Avisos de pedido y estado enviados por ti',
            'Pasa a una persona cuando importa',
          ],
        },
        {
          id: 'sales',
          icon: 'pi pi-chart-line',
          flowLabel: 'Ventas',
          title: 'Ventas',
          desc: 'Cada lead respondido y con seguimiento, cotizaciones o presupuestos listos, recordatorios enviados; nada se queda en una hoja porque alguien estaba ocupado.',
          bullets: [
            'Leads respondidos y calificados rápido',
            'Borradores de presupuesto y seguimiento',
            'Recordatorios para que ninguna venta se enfríe',
          ],
        },
        {
          id: 'operations',
          icon: 'pi pi-cog',
          flowLabel: 'Procesos',
          title: 'Procesos internos',
          desc: 'El copiar y pegar entre herramientas que tu equipo hace cada semana: presupuestos al sistema, facturas a la hoja de cálculo, aprobaciones por correo.',
          bullets: [
            'Formularios y correos a tus sistemas',
            'Facturas, pedidos y aprobaciones en su sitio',
            'Tareas semanales sin que nadie las teclee',
          ],
        },
        {
          id: 'website',
          icon: 'pi pi-globe',
          flowLabel: 'Web',
          title: 'Tu sitio web',
          desc: 'Un agente en tu web que publica, cambia y quita contenido en tiempo real: productos, precios, horarios, promociones, sin esperar a un desarrollador.',
          bullets: [
            'Publica o cambia una página desde un mensaje',
            'Productos, horarios y ofertas siempre al día',
            'Tú apruebas, él publica',
          ],
        },
      ],
    },
    audience: {
      label: 'Para quién',
      title: 'Para equipos de 5 a 100 personas que ya venden y atienden clientes',
      subtitle:
        'Tienes clientes, pedidos y un equipo pequeño sin horas de sobra. No hacemos transformaciones de dos años: te quitamos una tarea, demostramos que funciona y vamos a la siguiente. LatAm y España, con los fundadores al frente.',
      guidanceLine:
        'No necesitas saber de IA. Te guiamos en todo el proceso para que la integres de forma segura.',
      tags: [
        'Dueño/a o fundador/a',
        'Responsable de operaciones',
        'Equipo comercial',
        'Atención al cliente',
        '5–100 personas',
        'LatAm',
        'España',
      ],
    },
    packages: {
      label: 'Qué hacemos',
      title: 'Cuatro formas de empezar',
      subtitle:
        'Comunicación con clientes, seguimiento comercial, procesos internos y tu web: empieza por uno y crece cuando se pague.',
      cta: 'Solicitar consulta',
      items: [
        {
          id: 'diagnostic',
          name: 'Diagnóstico IA',
          duration: '1–2 semanas',
          icon: 'pi pi-search',
          outcome: 'Un mapa breve de dónde la IA se paga sola.',
          bullets: [
            'Inventario de procesos y dolores',
            '1–3 quick wins de automatización',
            'Un plan escrito que puedes usar, no una presentación',
          ],
        },
        {
          id: 'pilot',
          name: 'Piloto',
          duration: '4–6 semanas',
          icon: 'pi pi-play',
          outcome: 'Un flujo real automatizado de punta a punta, con una métrica.',
          bullets: [
            'Un bot, agente o app que tu equipo usa a diario',
            'Horas ahorradas, errores evitados, respuesta más rápida: medido',
            'Una persona sigue al mando',
          ],
        },
        {
          id: 'system',
          name: 'Implementación',
          duration: '2–3 meses',
          icon: 'pi pi-sitemap',
          outcome:
            'Varios flujos conectados (clientes, ventas, procesos, web) y tu equipo operándolos.',
          bullets: [
            'Más de un workflow',
            'Integraciones con las herramientas que ya tienes',
            'No depende de una sola persona (ni de nosotros)',
          ],
        },
        {
          id: 'retainer',
          name: 'Acompañamiento mensual',
          duration: 'Continuo',
          icon: 'pi pi-refresh',
          outcome:
            'Cuando ya está en marcha: nuevas automatizaciones, monitoreo y soporte cada mes.',
          bullets: [
            'Mejoras continuas, no un "mantenimiento" vago',
            'Alcance mensual acordado',
            'Los mismos principals que lo construyeron',
          ],
        },
      ],
    },
    process: {
      label: 'Cómo trabajamos',
      title: 'El camino: Diagnóstico → Piloto → Implementación → Acompañamiento',
      subtitle:
        'Empezamos en pequeño, medimos y después crecemos. La IA le quita el trabajo repetitivo a tu gente; no la reemplaza.',
      pipelineCaption:
        'Cuatro pasos, un camino medido del diagnóstico al soporte continuo.',
      workflow: {
        caption: 'Flujos reales — intake, decisión, acción, supervisión humana.',
        nodes: [
          { id: 'intake', label: 'Solicitud' },
          { id: 'decide', label: 'Decide' },
          { id: 'act', label: 'Actúa' },
          { id: 'human', label: 'Revisión humana' },
        ],
      },
      steps: [
        { name: 'Diagnóstico', desc: 'Mapeamos lo que tu equipo hace a mano y dónde paga automatizar.' },
        { name: 'Piloto', desc: 'Un flujo en marcha, con un número que lo demuestra.' },
        { name: 'Implementación', desc: 'Conectamos más flujos y herramientas; tu equipo los opera.' },
        { name: 'Acompañamiento', desc: 'Nuevas automatizaciones, monitoreo y soporte cada mes.' },
      ],
      visualTitle: 'Una persona sigue al mando',
      principles: [
        'No hace falta un equipo de IA: vamos con ustedes',
        'Empezar en pequeño, medir, después crecer',
        'Tu equipo aprueba lo que importa',
        'Sin cajas negras: ves lo que hace',
        'Funciona con las herramientas que ya usas',
        'Tus datos se quedan en tus cuentas',
      ],
    },
    proof: {
      label: 'Quién hace el trabajo',
      title: 'Los fundadores al frente, remoto, 20+ países',
      subtitle:
        'Los mismos fundadores que definen tu proyecto lo construyen y lo siguen. Sin juniors a los que te pasan después de la venta.',
      stats: [
        { value: '15+', label: 'Años de experiencia' },
        { value: '20+', label: 'Países atendidos' },
        { value: '100+', label: 'Proyectos entregados' },
        { value: '100%', label: '100% remoto' },
      ],
    },
    cta: {
      label: 'Hablemos',
      title: 'Cuéntanos dónde duele el trabajo. Te decimos dónde la IA paga.',
      bodyBefore: 'Escríbenos a',
      bodyAfter:
        'o usa el formulario de contacto: respondemos en 24 horas en días hábiles y te decimos claro si no tiene sentido para ti.',
      primaryCta: 'Solicitar consulta',
      secondaryCta: 'Agendar una llamada de 20 min',
    },
  },
}
