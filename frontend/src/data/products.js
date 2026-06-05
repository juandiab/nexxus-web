import { ACTIVATION_LETTERS } from './activation-i18n.js'

const letter = ACTIVATION_LETTERS.en

/** JPilot logo variants — dark UI uses the black asset; light sections use the default asset. */
export const JPILOT_LOGOS = {
  dark: '/JPilot-logo-big-black.svg',
  light: '/JPilot-logo-big.svg',
}

/** Product catalog — JPilot narrative inspired by the activation letter; technical reference: github.com/juandiab/nsagent README */
export const products = [
  {
    id: 'jpilot',
    name: 'JPilot',
    logo: JPILOT_LOGOS.dark,
    logoLight: JPILOT_LOGOS.light,
    logoAlt: 'JPilot',
    repoName: 'nsagent',
    version: 'v0.33',
    label: 'AI-Assisted Appliance Management',
    tagline: 'A bridge between people, knowledge, and technology',
    icon: 'pi pi-bolt',
    iconBg: 'linear-gradient(135deg,#007BA7,#00A8E0)',
    desc: 'JPilot is for the engineers, architects, and administrators who have invested years mastering NetScaler, ADC platforms, and complex network technologies. It connects to your appliances with memory-guided tools and human approval gates—so AI amplifies your judgment instead of replacing it. More than software, it is an extension of a simple belief: technology should help people learn, grow, and achieve what once seemed reserved for only a few specialists.',
    excerpt:
      'AI-assisted management that empowers engineers—amplifying judgment, making expertise more accessible, and helping teams grow stronger.',
    visionPrinciples: [
      {
        title: 'Empower people',
        body: 'Every product we build starts with a simple idea: technology should empower people, not replace them.',
      },
      {
        title: 'Make knowledge accessible',
        body: 'Complex ADC and network platforms demanded countless hours of study and real-world experience. JPilot helps make that knowledge more accessible—so more people can learn, grow, and move forward with confidence.',
      },
      {
        title: 'Teams that grow',
        body: 'The most rewarding outcomes are not only working systems, but teams that come out better prepared, more confident, and more capable of facing what comes next.',
      },
      {
        title: 'AI amplifies creativity',
        body: 'Artificial Intelligence does not replace human creativity; it amplifies it. The best tools enhance our capabilities—but judgment, experience, creativity, and purpose still come from people.',
      },
    ],
    capabilities: [
      'Connect NetScaler, Cisco, and F5 appliances with encrypted credentials that never reach the language model',
      'Architect, Operator, and Analyst roles—for design, controlled change, and read-first troubleshooting',
      'Memory-guided tools that search real API and CLI syntax before suggesting or executing work',
      'Confirm-before-change guardrails so automation supports human review, not blind trust',
      'Bring your own AI provider—you choose the model and hold the keys',
      'Open-source core you can run on your own infrastructure with Docker',
    ],
    roles: [
      {
        name: 'Architect',
        icon: 'pi pi-compass',
        desc: 'Plan and document before you touch production—structured discovery and formal design outputs that help teams understand the why, not just the how.',
      },
      {
        name: 'Operator',
        icon: 'pi pi-cog',
        desc: 'Turn approved designs into configuration—with tools that respect syntax, memory gates, and explicit confirmation before destructive change.',
      },
      {
        name: 'Analyst',
        icon: 'pi pi-search',
        desc: 'Troubleshoot with read-first diagnostics—reachability, port checks, and appliance health—so engineers spend less time guessing and more time deciding.',
      },
    ],
    platforms: [
      { name: 'NetScaler ADC', detail: 'MPX, VPX', status: 'Available' },
      { name: 'NetScaler SDX', detail: 'Platform & VPX lifecycle', status: 'Beta' },
      { name: 'Cisco IOS/XE', detail: 'Enterprise switching', status: 'Beta' },
      { name: 'F5 BIG-IP', detail: 'TMSH operations', status: 'Beta' },
    ],
    tags: ['NetScaler', 'Cisco', 'F5', 'AI Copilot', 'Open Source'],
    metrics: [
      { value: 'People', label: 'Come First' },
      { value: 'Amplify', label: 'Human Judgment' },
      { value: 'Open', label: 'Source Core' },
    ],
    founderNote: {
      closing: letter.closing,
      author: letter.author,
      role: letter.role,
      company: letter.company,
      quote:
        'More than software, we strive to build tools that serve as a bridge between people, knowledge, and technology—so you can learn, grow, and continue developing your full potential.',
    },
    links: {
      github: 'https://github.com/juandiab/nsagent',
      readme: 'https://github.com/juandiab/nsagent/blob/main/README.md',
      blog: '/blog/nsagent-open-source-netscaler-copilot',
    },
    disclaimer:
      'JPilot is an independent project and is not affiliated with, endorsed by, or sponsored by Citrix Systems, Inc. NetScaler is a trademark of Citrix Systems, Inc.',
  },
]
