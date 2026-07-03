<template>
  <section class="logo-test">
    <header class="logo-test__intro">
      <p class="logo-test__kicker">Logo & loader preview</p>
      <h1>Nexus marks</h1>
      <p>
        The neon mark and loaders below. Connection rings are live in the
        <strong>top-left navbar</strong> on this page.
      </p>
    </header>

    <article class="logo-test__option">
      <div class="logo-test__option-head">
        <p class="logo-test__option-label">Neon mark</p>
        <h2>Static logo</h2>
        <p>Outline hex, vertex nodes, N pillars, diagonal bridge, center nucleus.</p>
      </div>

      <div class="logo-test__compare" aria-label="Reference image vs CSS mark">
        <div class="logo-test__compare-item">
          <img
            src="@/assets/logo-neon-reference.png"
            alt="Reference neon Nexxus mark"
            class="logo-test__reference-img"
          />
          <span>Reference image</span>
        </div>
        <div class="logo-test__compare-item">
          <NxNeonMark size="lg" />
          <span>CSS static mark</span>
        </div>
      </div>

      <div class="logo-test__variants" aria-label="Neon mark colour previews">
        <div class="logo-test__variant logo-test__variant--cyan">
          <NxNeonMark size="md" />
          <span>Brand cyan</span>
        </div>
        <div class="logo-test__variant logo-test__variant--white">
          <NxNeonMark size="md" class="logo-test__mark--white" />
          <span>White on dark</span>
        </div>
        <div class="logo-test__variant logo-test__variant--dark">
          <NxNeonMark size="md" class="logo-test__mark--dark" />
          <span>Dark on light</span>
        </div>
      </div>
    </article>

    <article class="logo-test__option logo-test__option--rings">
      <div class="logo-test__option-head">
        <p class="logo-test__option-label">Loader</p>
        <h2>Connection rings</h2>
        <p>Rotating connection rings around a central hub.</p>
      </div>

      <div class="logo-test__grid">
        <div class="logo-test__stage" aria-label="Connection rings loader preview">
          <NxConnectionRings size="lg" />
        </div>

        <div class="logo-test__variants" aria-label="Connection rings colour previews">
          <div class="logo-test__variant logo-test__variant--cyan">
            <NxConnectionRings size="md" />
            <span>Brand cyan</span>
          </div>
          <div class="logo-test__variant logo-test__variant--white">
            <NxConnectionRings size="md" class="logo-test__mark--white" />
            <span>White on dark</span>
          </div>
          <div class="logo-test__variant logo-test__variant--dark">
            <NxConnectionRings size="md" class="logo-test__mark--dark" />
            <span>Dark on light</span>
          </div>
        </div>
      </div>
    </article>

    <article class="logo-test__option logo-test__option--core">
      <div class="logo-test__option-head">
        <p class="logo-test__option-label">Loader</p>
        <h2>Nexus Core</h2>
        <p>Hex hub, diagonal signal, and linked side nodes.</p>
      </div>

      <div class="logo-test__grid">
        <div class="logo-test__stage" aria-label="Nexus Core loader preview">
          <div class="ld-nexxus"><i></i><i></i><i></i></div>
        </div>

        <div class="logo-test__variants" aria-label="Nexus Core colour previews">
          <div class="logo-test__variant logo-test__variant--cyan">
            <div class="ld-nexxus"><i></i><i></i><i></i></div>
            <span>Brand cyan</span>
          </div>
          <div class="logo-test__variant logo-test__variant--white">
            <div class="ld-nexxus"><i></i><i></i><i></i></div>
            <span>White on dark</span>
          </div>
          <div class="logo-test__variant logo-test__variant--dark">
            <div class="ld-nexxus"><i></i><i></i><i></i></div>
            <span>Dark on light</span>
          </div>
        </div>
      </div>
    </article>

    <article class="logo-test__option logo-test__option--term">
      <div class="logo-test__option-head">
        <p class="logo-test__option-label">Wordmark</p>
        <h2>Term-OS cursor</h2>
        <p>
          JetBrains Mono wordmark with blinking terminal cursor — used in the
          navbar logo on this page.
        </p>
      </div>

      <div class="logo-test__grid">
        <div class="logo-test__stage" aria-label="Term-OS reference loader">
          <div class="ld-cursor">ZX-OS</div>
        </div>

        <div class="logo-test__variants" aria-label="Term-OS wordmark previews">
          <div class="logo-test__variant logo-test__variant--cyan">
            <span class="logo-test__wordmark ld-cursor logo-test__wordmark--split">
              <span class="logo-test__wordmark-nexxus">NEXXUS</span><span class="logo-test__wordmark-tech"> TECH</span>
            </span>
            <span>Navbar colours</span>
          </div>
          <div class="logo-test__variant logo-test__variant--white">
            <div class="ld-cursor logo-test__mark--white">ZX-OS</div>
            <span>White on dark</span>
          </div>
          <div class="logo-test__variant logo-test__variant--dark">
            <div class="ld-cursor logo-test__mark--dark">ZX-OS</div>
            <span>Dark on light</span>
          </div>
        </div>
      </div>
    </article>
  </section>
</template>

<script setup>
import NxNeonMark from '@/components/shared/NxNeonMark.vue'
import NxConnectionRings from '@/components/shared/NxConnectionRings.vue'
</script>

<style scoped>
.logo-test {
  min-height: 100vh;
  padding: clamp(120px, 14vw, 160px) 24px 72px;
  background:
    radial-gradient(circle at 70% 25%, rgba(0, 168, 224, .18), transparent 34%),
    linear-gradient(135deg, #151517 0%, #252528 52%, #111113 100%);
  color: var(--nt-white);
}

.logo-test__intro {
  width: min(1120px, 100%);
  margin: 0 auto clamp(48px, 6vw, 72px);
}

.logo-test__kicker {
  margin: 0 0 14px;
  color: var(--nt-secondary);
  font-family: var(--font-heading);
  font-size: .78rem;
  font-weight: 800;
  letter-spacing: .18em;
  text-transform: uppercase;
}

.logo-test h1 {
  margin: 0 0 18px;
  font-size: clamp(3rem, 9vw, 7rem);
  line-height: .9;
  letter-spacing: 0;
  text-wrap: balance;
}

.logo-test__intro p {
  max-width: 58ch;
  margin: 0;
  color: var(--nt-text-light);
  font-size: clamp(1rem, 1.6vw, 1.2rem);
}

.logo-test__intro strong {
  color: var(--nt-primary-l);
}

.logo-test__option {
  width: min(1120px, 100%);
  margin: 0 auto;
  padding-top: clamp(40px, 6vw, 72px);
  border-top: 1px solid rgba(255, 255, 255, .1);
}

.logo-test__option + .logo-test__option {
  margin-top: clamp(40px, 6vw, 72px);
}

.logo-test__option-head {
  margin-bottom: clamp(32px, 5vw, 48px);
}

.logo-test__option-label {
  margin: 0 0 10px;
  color: var(--nt-secondary);
  font-family: var(--font-heading);
  font-size: .72rem;
  font-weight: 800;
  letter-spacing: .16em;
  text-transform: uppercase;
}

.logo-test__option h2 {
  margin: 0 0 12px;
  font-size: clamp(1.75rem, 4vw, 2.5rem);
  line-height: 1;
  letter-spacing: 0;
}

.logo-test__option-head p:last-child {
  max-width: 58ch;
  margin: 0;
  color: var(--nt-text-light);
  font-size: clamp(.95rem, 1.4vw, 1.05rem);
}

.logo-test__compare {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1px;
  margin-bottom: 1px;
  border: 1px solid rgba(255, 255, 255, .12);
  background: rgba(255, 255, 255, .12);
}

.logo-test__compare-item {
  display: grid;
  place-items: center;
  gap: 20px;
  min-height: 320px;
  padding: 32px;
  background:
    linear-gradient(90deg, rgba(255,255,255,.04) 1px, transparent 1px),
    linear-gradient(0deg, rgba(255,255,255,.04) 1px, transparent 1px),
    rgba(17, 17, 19, .72);
  background-size: 28px 28px;
}

.logo-test__compare-item span {
  font-family: var(--font-heading);
  font-size: .72rem;
  font-weight: 800;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--nt-text-light);
}

.logo-test__reference-img {
  width: 132px;
  height: auto;
  border-radius: 4px;
}

.logo-test__grid {
  display: grid;
  grid-template-columns: minmax(280px, 460px) minmax(0, 1fr);
  gap: 1px;
  border: 1px solid rgba(255, 255, 255, .12);
  background: rgba(255, 255, 255, .12);
}

.logo-test__stage {
  display: grid;
  place-items: center;
  min-height: min(62vw, 460px);
  padding: 28px;
  background:
    linear-gradient(90deg, rgba(255,255,255,.05) 1px, transparent 1px),
    linear-gradient(0deg, rgba(255,255,255,.05) 1px, transparent 1px),
    rgba(17, 17, 19, .72);
  background-size: 28px 28px;
  color: var(--nt-primary-l);
}

.logo-test__stage .ld-nexxus {
  transform: scale(2.7);
}

.logo-test__variants {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1px;
  background: rgba(255, 255, 255, .12);
}

.logo-test__variant {
  display: grid;
  place-items: center;
  min-height: 190px;
  gap: 22px;
  padding: 28px;
  background: #19191c;
  color: var(--nt-primary-l);
}

.logo-test__variant span {
  color: currentColor;
  font-family: var(--font-heading);
  font-size: .78rem;
  font-weight: 800;
  letter-spacing: .12em;
  text-transform: uppercase;
}

.logo-test__variant--white {
  color: var(--nt-white);
}

.logo-test__variant--dark {
  background: var(--nt-light-bg);
  color: var(--nt-dark);
}

.logo-test__mark--white {
  color: var(--nt-white);
}

.logo-test__mark--dark {
  color: var(--nt-dark);
}

.logo-test__wordmark--split {
  display: inline-flex;
  align-items: baseline;
}

.logo-test__wordmark-nexxus {
  color: var(--nt-white);
}

.logo-test__wordmark-tech {
  color: var(--nt-primary);
}

.logo-test__option--term .ld-cursor::after {
  color: var(--nt-primary-l);
}

/* Nexus Core — ld-nexxus */
.logo-test__option--core .ld-nexxus {
  --ink: currentColor;
  position: relative;
  width: 56px;
  height: 56px;
  color: var(--ink);
}

.logo-test__option--core .ld-nexxus,
.logo-test__option--core .ld-nexxus i,
.logo-test__option--core .ld-nexxus i::before,
.logo-test__option--core .ld-nexxus i::after {
  box-sizing: border-box;
}

.logo-test__option--core .ld-nexxus i {
  position: absolute;
  display: block;
}

.logo-test__option--core .ld-nexxus i:nth-child(1) {
  left: 10px;
  top: 17px;
  width: 36px;
  height: 22px;
  border-left: 2px solid var(--ink);
  border-right: 2px solid var(--ink);
  animation: nexxus-core 2.4s ease-in-out infinite;
}

.logo-test__option--core .ld-nexxus i:nth-child(1)::before,
.logo-test__option--core .ld-nexxus i:nth-child(1)::after {
  content: "";
  position: absolute;
  inset: 0;
  border-left: 2px solid var(--ink);
  border-right: 2px solid var(--ink);
}

.logo-test__option--core .ld-nexxus i:nth-child(1)::before {
  transform: rotate(60deg);
}

.logo-test__option--core .ld-nexxus i:nth-child(1)::after {
  transform: rotate(-60deg);
}

.logo-test__option--core .ld-nexxus i:nth-child(2) {
  left: 27px;
  top: 11px;
  width: 2px;
  height: 34px;
  border-radius: 999px;
  background: var(--ink);
  transform: rotate(39deg);
  transform-origin: center;
  animation: nexxus-link 1.4s ease-in-out infinite;
}

.logo-test__option--core .ld-nexxus i:nth-child(3) {
  left: 6px;
  top: 26px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--ink);
  box-shadow: 44px 0 0 var(--ink);
  animation: nexxus-nodes 1.4s ease-in-out infinite;
}

.logo-test__option--core .ld-nexxus i:nth-child(3)::before {
  content: "";
  position: absolute;
  left: 6px;
  top: 2px;
  width: 44px;
  height: 2px;
  background: var(--ink);
  opacity: .22;
}

@keyframes nexxus-core {
  0%, 100% { transform: scale(.96); opacity: .72; }
  50% { transform: scale(1); opacity: 1; }
}

@keyframes nexxus-link {
  0%, 100% { opacity: .42; }
  50% { opacity: 1; }
}

@keyframes nexxus-nodes {
  0%, 100% { transform: scale(.9); opacity: .55; }
  50% { transform: scale(1); opacity: .95; }
}

@media (max-width: 820px) {
  .logo-test__compare,
  .logo-test__variants,
  .logo-test__grid {
    grid-template-columns: 1fr;
  }

  .logo-test__stage {
    min-height: 340px;
  }

  .logo-test__stage .ld-nexxus {
    transform: scale(2.15);
  }
}

@media (prefers-reduced-motion: reduce) {
  .logo-test__option--core .ld-nexxus i {
    animation: none !important;
  }
}
</style>
