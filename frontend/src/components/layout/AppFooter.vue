<template>
  <footer class="footer">
    <div class="footer-glow"></div>
    <div class="container">
      <div class="footer-grid">
        <!-- Brand col -->
        <div class="footer-brand">
          <img src="@/assets/nexxus-tech-logo-full-large.svg" alt="Nexxus Tech" class="footer-logo" />
          <p class="footer-desc">
            Empowering people and organizations through consulting, architecture,
            shared knowledge, and AI-driven innovation. Inspiring growth, solving
            complex challenges, and making expertise more accessible.
          </p>
          <div class="footer-social">
            <SocialLinks variant="icons" />
          </div>
        </div>

        <!-- Services col -->
        <nav class="footer-col" aria-label="Services">
          <h4 class="footer-col-title">Services</h4>
          <ul>
            <li><RouterLink to="/services#waf">WAF & API Protection</RouterLink></li>
            <li><RouterLink to="/services#netscaler">NetScaler / ADC</RouterLink></li>
            <li><RouterLink to="/services#zerotrust">Zero-Trust Architecture</RouterLink></li>
            <li><RouterLink to="/services#cloud">Cloud Security</RouterLink></li>
            <li><RouterLink to="/services#ai">AI & Automation</RouterLink></li>
          </ul>
        </nav>

        <!-- Products col -->
        <nav class="footer-col" aria-label="Products">
          <h4 class="footer-col-title">Products</h4>
          <ul>
            <li><RouterLink to="/products#jpilot">JPilot</RouterLink></li>
            <li><RouterLink to="/products">All Products</RouterLink></li>
          </ul>
        </nav>

        <!-- Company col -->
        <nav class="footer-col" aria-label="Company">
          <h4 class="footer-col-title">Company</h4>
          <ul>
            <li><RouterLink to="/about">About Us</RouterLink></li>
            <li><RouterLink to="/faq">FAQ</RouterLink></li>
            <li><RouterLink to="/blog">Blog & Insights</RouterLink></li>
            <li><RouterLink to="/contact">Contact</RouterLink></li>
          </ul>
        </nav>

        <!-- Legal col -->
        <nav class="footer-col" aria-label="Legal">
          <h4 class="footer-col-title">Legal</h4>
          <ul>
            <li>
              <a href="https://jpilot.nexxus-tech.com/legal/privacy">Privacy</a>
            </li>
            <li>
              <a href="https://jpilot.nexxus-tech.com/legal/terms">Terms of Use</a>
            </li>
          </ul>
        </nav>

        <!-- Contact col -->
        <div class="footer-col">
          <h4 class="footer-col-title">Contact</h4>
          <ul class="contact-list">
            <li>
              <i class="pi pi-envelope"></i>
              <a href="mailto:contact@nexxus-tech.com">contact@nexxus-tech.com</a>
            </li>
            <li>
              <i class="pi pi-globe"></i>
              <span>nexxus-tech.com</span>
            </li>
            <li>
              <i class="pi pi-map-marker"></i>
              <span>Colombia · UAE · UK · US</span>
            </li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <p>&copy; {{ new Date().getFullYear() }} Nexxus Tech. All rights reserved.</p>
        <p class="footer-bottom-right">
          Specialized in <span class="highlight">WAF</span> ·
          <span class="highlight">NetScaler</span> ·
          <span class="highlight">Cloud Security</span> ·
          <span class="highlight">AI</span>
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import SocialLinks from '@/components/shared/SocialLinks.vue'
</script>

<style scoped>
.footer {
  background: var(--nt-dark-2);
  border-top: 1px solid var(--nt-border);
  padding: 80px 0 0;
  position: relative;
  overflow: hidden;
}
.footer-glow {
  position: absolute;
  top: -100px; left: 50%;
  transform: translateX(-50%);
  width: 600px; height: 200px;
  background: radial-gradient(ellipse, rgba(91,79,232,0.12) 0%, transparent 70%);
  pointer-events: none;
}
.footer-grid {
  display: grid;
  grid-template-columns: 2fr repeat(4, 1fr) 1.25fr;
  gap: 32px;
  margin-bottom: 60px;
}
.footer-logo { height: 48px; width: auto; margin-bottom: 20px; display: block; }
.footer-desc {
  font-size: 0.9rem;
  color: var(--nt-text-muted);
  line-height: 1.7;
  margin-bottom: 24px;
  max-width: 320px;
}
.footer-social { display: flex; gap: 10px; }
.social-btn {
  width: 40px; height: 40px;
  border-radius: 8px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  display: flex; align-items: center; justify-content: center;
  color: var(--nt-text-muted);
  font-size: 1rem;
  transition: var(--nt-transition);
  text-decoration: none;
}
.social-btn:hover {
  background: var(--nt-primary);
  border-color: var(--nt-primary);
  color: white;
  transform: translateY(-2px);
}
.footer-col-title {
  font-family: var(--font-heading);
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--nt-secondary);
  margin-bottom: 20px;
}
.footer-col ul { list-style: none; display: flex; flex-direction: column; gap: 10px; }
.footer-col ul li a,
.footer-col ul li span {
  font-size: 0.9rem;
  color: var(--nt-text-muted);
  text-decoration: none;
  transition: color 0.2s;
}
.footer-col ul li a:hover { color: var(--nt-white); }
.contact-list { gap: 14px !important; }
.contact-list li {
  display: flex;
  align-items: center;
  gap: 10px;
}
.contact-list .pi {
  color: var(--nt-primary-l);
  font-size: 0.9rem;
  flex-shrink: 0;
}
.footer-bottom {
  border-top: 1px solid rgba(255,255,255,0.06);
  padding: 24px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
  color: var(--nt-text-muted);
  flex-wrap: wrap;
  gap: 8px;
}
.highlight { color: var(--nt-secondary); }

@media (max-width: 1024px) {
  .footer-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 600px) {
  .footer-grid { grid-template-columns: 1fr; gap: 32px; }
  .footer-bottom { flex-direction: column; text-align: center; }
  .footer-bottom-right { display: none; }
}
</style>
