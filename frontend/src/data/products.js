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
    mark: 'jpilot',
    logo: JPILOT_LOGOS.dark,
    logoLight: JPILOT_LOGOS.light,
    logoAlt: 'JPilot',
    edition: 'Free Edition',
    label: 'AI-assisted appliance management',
    eyebrow: 'AI-assisted appliance management',
    tagline: 'Operate NetScaler, Cisco, and F5 with confidence',
    subline:
      'Free edition. Bring your own AI keys. Credentials never leave your network.',
    excerpt:
      'JPilot connects your appliance inventory to your own AI provider keys — plan, configure, and troubleshoot with vendor-aware tools.',
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
        title: 'Multi-vendor inventory',
        icon: 'pi pi-sitemap',
        body: 'Register NetScaler ADC, SDX, Cisco IOS/XE, and F5 BIG-IP with encrypted credentials and tags for filtering.',
      },
      {
        title: 'JPilot chat roles',
        icon: 'pi pi-users',
        body: 'Architect, Operator, and Analyst personas with tool-calling bound to the selected appliance — credentials never sent to the LLM.',
      },
      {
        title: 'Bring your own keys',
        icon: 'pi pi-key',
        body: 'Connect OpenAI, Anthropic, Gemini, Azure OpenAI, AWS Bedrock, OpenRouter, or a local endpoint. You choose the provider and pay for inference.',
      },
      {
        title: 'SME engineer skills',
        icon: 'pi pi-book',
        body: 'Architect, Operator, and Analyst workflows, prompts, and memory files are built from NetScaler, Cisco, and F5 SME practice — plus recommended actions in the command menu.',
      },
      {
        title: 'MCP tool server',
        icon: 'pi pi-wrench',
        body: 'Next-Gen API, classic CLI over SSH, NITRO helpers, diagnostics, and SSL CSR generation exposed to the agent.',
      },
      {
        title: 'Enterprise-ready auth',
        icon: 'pi pi-lock',
        body: 'Password login, optional passkeys, account recovery, and admin user management with role-based access.',
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
      landing: 'https://jpilot.nexxus-tech.com',
      blog: '/blog/jpilot-ai-management-platform',
    },
    disclaimer:
      'JPilot is an independent product by Nexxus-Tech SAS. It is not affiliated with, endorsed by, sponsored by, or certified by Cloud Software Group (Citrix / NetScaler), Cisco Systems, F5 Networks, or their affiliates. NetScaler, Citrix, Cisco, F5 BIG-IP, and related names are trademarks of their respective owners and are used here only for identification and interoperability.',
  },
  {
    id: 'cafeina',
    name: 'Cafeina',
    mark: 'cafeina',
    edition: 'macOS',
    label: 'Personal menu bar utility',
    tagline: 'Keep your Mac awake from the menu bar',
    excerpt:
      'A lightweight native macOS utility by Juan Pablo Otalvaro A. Runs locally on your Mac — no personal data collection.',
    tags: ['macOS 13+', 'Menu Bar', 'Privacy-first', 'Open Source'],
    metrics: [
      { value: '13+', label: 'macOS' },
      { value: 'Local', label: 'On-device' },
      { value: '0', label: 'Data collected' },
    ],
    href: '/cafeina',
    repoUrl: 'https://github.com/juandiab/Cafeina',
    support: {
      email: 'support@nexxus-tech.com',
    },
    disclaimer:
      'Cafeina is a personal app by Juan Pablo Otalvaro A. It is not affiliated with Caffeine or any similarly named apps.',
  },
]
