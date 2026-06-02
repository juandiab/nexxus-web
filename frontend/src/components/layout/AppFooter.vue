<template>
  <footer class="footer">
    <div class="footer-glow"></div>
    <div class="container">
      <div class="footer-grid">
        <!-- Brand col -->
        <div class="footer-brand">
          <img src="@/assets/logo-white.svg" alt="Nexxus Tech" class="footer-logo" />
          <p class="footer-desc">
            Principal-level consulting in WAF, Application Delivery Controllers,
            Zero-Trust Architecture, and AI-driven security automation.
            Deployed across 54+ countries.
          </p>
          <div class="footer-social">
            <a href="#" class="social-btn" aria-label="LinkedIn" title="LinkedIn (coming soon)">
              <i class="pi pi-linkedin"></i>
            </a>
            <a href="#" class="social-btn" aria-label="Twitter" title="Twitter/X (coming soon)">
              <i class="pi pi-twitter"></i>
            </a>
            <a href="#" class="social-btn" aria-label="GitHub" title="GitHub (coming soon)">
              <i class="pi pi-github"></i>
            </a>
          </div>
        </div>

        <!-- Services col -->
        <div class="footer-col">
          <h4 class="footer-col-title">Services</h4>
          <ul>
            <li><RouterLink to="/services#waf">WAF & API Protection</RouterLink></li>
            <li><RouterLink to="/services#netscaler">NetScaler / ADC</RouterLink></li>
            <li><RouterLink to="/services#zerotrust">Zero-Trust Architecture</RouterLink></li>
            <li><RouterLink to="/services#cloud">Cloud Security</RouterLink></li>
            <li><RouterLink to="/services#ai">AI & Automation</RouterLink></li>
          </ul>
        </div>

        <!-- Company col -->
        <div class="footer-col">
          <h4 class="footer-col-title">Company</h4>
          <ul>
            <li><RouterLink to="/about">About Us</RouterLink></li>
            <li><RouterLink to="/blog">Blog & Insights</RouterLink></li>
            <li><RouterLink to="/contact">Contact</RouterLink></li>
          </ul>
        </div>

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
  background: radial-gradient(ellipse, rgba(0,123,167,0.12) 0%, transparent 70%);
  pointer-events: none;
}
.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1.5fr;
  gap: 48px;
  margin-bottom: 60px;
}
.footer-logo { height: 40px; margin-bottom: 20px; display: block; }
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
