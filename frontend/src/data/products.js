/** JPilot logo variants — dark UI uses the black asset; light sections use the default asset. */
export const JPILOT_LOGOS = {
  dark: '/JPilot-logo-big-black.svg',
  light: '/JPilot-logo-big.svg',
}

/** Product catalog — JPilot command-first product page */
export const products = [
  {
    id: 'jpilot',
    name: 'JPilot',
    logo: JPILOT_LOGOS.dark,
    logoLight: JPILOT_LOGOS.light,
    logoAlt: 'JPilot',
    edition: 'Free Edition',
    label: 'AI Copilot for Network Appliances',
    eyebrow: 'AI copilot for network appliances',
    tagline:
      'AI copilot for NetScaler, F5, and Cisco — self-hosted on your infrastructure, BYO AI keys.',
    subline:
      'Free edition. Bring your own AI keys. Your credentials never leave your network.',
    excerpt:
      'Self-hosted AI copilot for NetScaler, F5, and Cisco. Plain-language CLI and API access, BYO keys.',
    tags: ['NetScaler', 'Cisco', 'F5', 'BYO AI', 'Open Source'],
    metrics: [
      { value: '3', label: 'Agent Roles' },
      { value: 'BYO', label: 'Your AI Keys' },
      { value: 'EA', label: 'Early Access' },
    ],
    repoUrl: 'https://github.com/Nexxus-Tech-SAS/jpilot',
    installation: {
      prerequisite:
        'Docker is the only hard prerequisite. The installer can set up git and Docker for you.',
      afterNote:
        'After install, the setup wizard opens in your browser (admin account, domain, TLS, deploy mode), then JPilot launches automatically.',
      platforms: [
        {
          id: 'windows',
          name: 'Windows',
          shell: 'PowerShell',
          icon: 'pi pi-microsoft',
          command: 'irm https://install.nexxus-tech.com/jpilot/ps1 | iex',
          hint: 'Offers to install Git for Windows + Docker Desktop via winget if missing.',
        },
        {
          id: 'macos',
          name: 'macOS',
          shell: 'Terminal',
          icon: 'pi pi-apple',
          command: 'curl -fsSL https://install.nexxus-tech.com/jpilot | bash',
          hint: 'Offers to install git + Docker Desktop (Homebrew / Xcode CLT) if missing.',
        },
        {
          id: 'linux',
          name: 'Linux',
          shell: 'Terminal · Ubuntu recommended',
          icon: 'pi pi-android',
          command: 'curl -fsSL https://install.nexxus-tech.com/jpilot | bash',
          hint: 'Offers to install git + Docker Engine (apt/dnf/yum/pacman/zypper/apk auto-detected) if missing.',
        },
      ],
      steps: [
        {
          title: 'Run the installer',
          body: 'Paste the command for your platform into PowerShell or a terminal and press Enter.',
        },
        {
          title: 'Complete the setup wizard',
          body: 'Configure admin account, domain, TLS, and deploy mode in the browser wizard.',
        },
        {
          title: 'Save your encryption key',
          body: 'On the Review step, copy the generated NSAGENT_ENCRYPTION_KEY—it is required to restore or migrate your install.',
        },
        {
          title: 'Sign in and connect',
          body: 'Register your appliances and connect your AI provider keys.',
        },
      ],
    },
    capabilities: [
      {
        title: 'Multi-vendor appliances',
        icon: 'pi pi-sitemap',
        body: 'NetScaler ADC (MPX/VPX), NetScaler SDX, Cisco IOS/XE, and F5 BIG-IP—one interface, same guardrails on every stack.',
      },
      {
        title: 'Bring your own AI',
        icon: 'pi pi-key',
        body: 'Connect OpenAI, Anthropic, Gemini, Grok, DeepSeek, OpenRouter, LM Studio, or any OpenAI-compatible endpoint. For enterprise privacy, use AWS Bedrock or Azure OpenAI so inference runs in your AWS or Azure account—your data stays in your company’s cloud, not a shared public API. You hold the keys and pay your provider; JPilot only connects to what you configure.',
      },
      {
        title: 'Role-based agents',
        icon: 'pi pi-users',
        body: 'Architect (design docs), Operator (configure), Analyst (read-first troubleshooting)—tool-calling chat with human approval gates.',
      },
      {
        title: 'Design → operate workflow',
        icon: 'pi pi-arrow-right-arrow-left',
        body: 'Memory-guided MCP tools for Next-Gen API, CLI-over-SSH, diagnostics, and SSL—search real syntax before suggesting or executing work.',
      },
      {
        title: 'Credential isolation',
        icon: 'pi pi-shield',
        body: 'Appliance credentials are encrypted and never sent to the LLM.',
      },
      {
        title: 'Passkey access',
        icon: 'pi pi-lock',
        body: 'Sign in with passkeys (biometrics) for phishing-resistant access to JPilot. Admins can configure passkey policy under Settings → Security—optional, enabled, or enforced for your team.',
      },
    ],
    trust: {
      title: 'You can see exactly what runs',
      lead: 'The installer at install.nexxus-tech.com is a thin, auditable proxy to the open-source bootstrap scripts in our GitHub repo—not a black box.',
      bullets: [
        'On every run: publisher (Nexxus-Tech SAS), exact source repo/branch, and a link to read the script before you pipe it.',
        'Before auto-installing dependencies: names the exact source (winget, your distro package manager, get.docker.com, or Homebrew), warns that Administrator / sudo may be required, and offers a manual-install path.',
        'Scripts are source-available in the jpilot repository.',
      ],
      closing:
        'Built for admins who pipe to shell warily—and want to know who published it and what it pulls.',
    },
    earlyAccess: {
      title: 'Free Edition · Early Access',
      body: 'Early access gives you unlimited use of JPilot in your own environment while we refine the product—run it on your infrastructure, connect your appliances, and use every feature at your pace. It is not positioned as a permanent free tier; it is an honest preview while the product matures. Report issues and follow development in the repo.',
    },
    support: {
      email: 'support@nexxus-tech.com',
      site: 'https://www.nexxus-tech.com',
      siteLabel: 'nexxus-tech.com',
    },
    links: {
      install: 'https://install.nexxus-tech.com/jpilot',
      blog: '/blog/nsagent-open-source-netscaler-copilot',
    },
    disclaimer:
      'JPilot is an independent project and is not affiliated with, endorsed by, or sponsored by Cloud Software Group, Inc., F5, Inc., or Cisco Systems, Inc. NetScaler is a trademark of Cloud Software Group, Inc. BIG-IP and F5 are trademarks of F5, Inc. Cisco and IOS are trademarks of Cisco Systems, Inc.',
  },
]
