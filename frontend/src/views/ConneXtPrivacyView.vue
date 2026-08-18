<template>
  <div class="privacy-page">
    <section class="page-hero">
      <div class="page-hero-bg"></div>
      <div class="container page-hero-content">
        <span class="section-label reveal">ConneXt</span>
        <h1 class="reveal reveal-delay-1">ConneXt Privacy Policy</h1>
        <p class="page-hero-subtitle reveal reveal-delay-2">
          Effective date: August 18, 2026
        </p>
      </div>
    </section>

    <section class="section privacy-body">
      <div class="container privacy-inner">
        <article class="privacy-prose reveal">
          <p class="lede">
            ConneXt does not create user accounts and does not sell personal data.
            SSH credentials stay in the iOS Keychain on your device. Optional AI
            keys stay on device; prompts go only to the provider you enable.
          </p>

          <h2>Who we are</h2>
          <p>
            ConneXt is a free native SSH terminal for iPhone and iPad developed by
            <strong>Juan Pablo Otalvaro</strong> at <strong>Nexxus-Tech</strong>.
            These pages are published on the Nexxus Tech website so App Store
            reviewers and users have a stable privacy URL.
          </p>

          <h2>No ConneXt accounts</h2>
          <p>
            ConneXt does not require, create, or host user accounts. There is no
            ConneXt sign-in, no ConneXt cloud profile, and no ConneXt user
            directory. We cannot reset a ConneXt password because the app does
            not have one.
          </p>

          <h2>SSH credentials and private keys</h2>
          <p>
            Host details, passwords, and private keys you import are stored in
            the <strong>iOS Keychain on your device</strong>. ConneXt does not
            upload those credentials to Nexxus-Tech or to any Nexxus-Tech server.
          </p>

          <h2>Connections you configure</h2>
          <p>
            SSH sessions go to the servers <strong>you</strong> add — the hosts,
            ports, and identities you configure in the app. Nexxus-Tech does not
            proxy those connections and does not receive session traffic.
          </p>

          <h2>Optional Command Assistant</h2>
          <p>
            Command Assistant is optional. If you enable it, you paste your own
            API key for <strong>OpenAI</strong>, <strong>Gemini</strong>, or
            <strong>Anthropic</strong>. That key stays on your device. Prompts
            you send go only to the provider you turned on — not to Nexxus-Tech.
            If you never enable the assistant, no prompts are sent to an AI
            provider.
          </p>

          <h2>What we do not do</h2>
          <p>
            ConneXt does not sell personal data. It does not include advertising
            SDKs. It does not build a Nexxus-Tech-side profile of your hosts,
            keys, or session content.
          </p>

          <h2>Contact</h2>
          <p>
            Questions about this policy or ConneXt:
            <a href="mailto:support@nexxus-tech.com">support@nexxus-tech.com</a>
          </p>

          <h2>Copyright</h2>
          <p>
            © {{ year }} Nexxus-Tech / Juan Pablo Otalvaro. All rights reserved.
          </p>

          <p class="back-link">
            <RouterLink to="/connext">← Back to ConneXt</RouterLink>
            ·
            <RouterLink to="/connext/support">Support</RouterLink>
          </p>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup>
const year = new Date().getFullYear()
</script>

<style scoped>
.page-hero {
  min-height: 32vh;
  display: flex;
  align-items: center;
  background: var(--nt-dark);
  padding: 120px 0 48px;
  position: relative;
  overflow: hidden;
}
.page-hero-bg {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 50% 60%, rgba(0, 123, 167, 0.14) 0%, transparent 65%);
}
.page-hero-content { position: relative; z-index: 1; max-width: 720px; }
.page-hero h1 {
  font-size: clamp(2rem, 4.5vw, 2.8rem);
  margin-top: 8px;
}
.page-hero-subtitle {
  font-size: 1rem;
  color: var(--nt-text-muted);
  margin-top: 12px;
}

.privacy-body {
  padding: 48px 0 100px;
  background: var(--nt-dark-2);
  border-top: 1px solid var(--nt-border);
}
.privacy-inner { max-width: 720px; }
.privacy-prose h2 {
  font-size: 1.2rem;
  margin: 28px 0 10px;
}
.privacy-prose p {
  color: var(--nt-text-muted);
  line-height: 1.8;
  margin-bottom: 12px;
}
.privacy-prose .lede {
  color: var(--nt-text);
  font-size: 1.08rem;
  font-weight: 600;
  line-height: 1.7;
  margin-bottom: 8px;
  padding: 18px 20px;
  border-left: 3px solid var(--nt-primary);
  background: rgba(0, 123, 167, 0.08);
}
.privacy-prose a {
  color: var(--nt-secondary);
  font-weight: 600;
}
.privacy-prose a:hover { text-decoration: underline; }
.back-link {
  margin-top: 36px !important;
  padding-top: 24px;
  border-top: 1px solid var(--nt-border);
}
</style>
