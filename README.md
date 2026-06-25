# Nexxus Tech Website

**Version 0.21** — Full-stack website for **nexxus-tech.com** — WAF · NetScaler · Cloud Security · AI

## Stack
| Layer | Technology |
|---|---|
| Frontend | Vue 3 + PrimeVue 4 + Vite |
| Backend | Python 3.12 + FastAPI |
| Licensing | Python 3.12 + FastAPI + MongoDB 7 |
| Web Server | Nginx stable-alpine (SSL termination + reverse proxy) |
| Runtime | Docker Compose |

---

## Changelog

### v0.21 — 2026-06-25
- **nginx / SC Studio sync** — `www.nexxus-tech.com` now proxies `/licensing/` to the licensing service instead of 301 redirecting to apex, so `POST /licensing/scstudio/register` and `POST /licensing/scstudio/sync` work on both `www` and apex (fixes SC Studio clients that call the `www` URL)
- **nginx** — extended proxy timeouts on the `www` licensing location for large encrypted catalog payloads; all other `www` paths still redirect to `nexxus-tech.com`

### v0.20 — 2026-06-24
- **Book a demo** — embedded Google Calendar scheduler on `/book-demo`; JPbot opens an in-site modal instead of a new tab; Products CTA, navbar, footer, and Services discovery call link to the demo page
- **Scheduling** — `AppointmentScheduler` component; `GOOGLE_APPOINTMENT_SCHEDULE_URL` replaces legacy `calendar.app.google` share link; enquiry pre-fill via query params
- **Performance** — async app CSS via `load-app-css.js` (CSP-safe preload activation; replaces inline `onload` on stylesheet links)
- **Security** — CSP `frame-src https://calendar.google.com` for inline calendar embed
- **SEO** — `/book-demo` route meta, sitemap entry

### v0.19 — 2026-06-24
- **SEO** — shortened meta descriptions; fixed heading hierarchy (`h3` nav/footer columns, industry cards); 1200×630 Open Graph image (`nexxus-tech-og.png`); canonical `www` → apex redirects on HTTP and HTTPS
- **PWA** — `site.webmanifest` and dedicated `apple-touch-icon.png` (180×180)
- **Security** — shared `nginx/security-headers.conf` with strict CSP (`script-src 'self'`; PrimeVue-compatible `style-src-elem` / `style-src-attr`); HSTS unchanged (`max-age=63072000; includeSubDomains; preload`)
- **Performance** — self-hosted variable fonts and PrimeIcons (no Google Fonts / jsDelivr); inlined critical CSS with async main stylesheet load; blog preview skeletons; navbar/logo dimension fixes to reduce CLS; 48×48px tap targets on nav and social icons
- **Frontend** — `coverColorClass()` utility for CSP-safe blog cover colors; homepage eager-loaded for faster LCP; Vite `deferAppCss` build plugin

### v0.18 — 2026-06-22
- **SC Studio license sync** — new `/licensing/scstudio/` API for SC Studio servers to register, pull an encrypted license catalog, and sync on demand
- **Registration** — `POST /licensing/scstudio/register` with `serverName`, `serverFingerprint`, `ipAddress`, `publicIpAddress`; admin approves in **Admin console → SC Studio**
- **Sync** — `POST /licensing/scstudio/sync` with `X-ScStudio-Api-Key` header and `{ "serverId" }` body; returns full `licenses` collection encrypted with the registered `serverFingerprint` (AES-256-GCM + HKDF-SHA256)
- **Admin console** — dedicated **SC Studio** nav section: unified server table (registration + API key), approve/reject, view/copy/regenerate/disable/delete key, one API key per approved server
- **Licensing API v0.8.0** — MongoDB collections `scstudioServers` and `scstudioApiKeys`; API keys stored hashed with Fernet-encrypted copy for admin retrieval
- **nginx** — longer proxy timeouts for SC Studio API paths (`/api/`, `/calibrations/`, `/skill-feedback`) to support large sync payloads

### v0.17 — 2026-06-13
- **Blog admin** — create, edit, delete, and publish posts from `/adminconsole/blogs`; MongoDB-backed store with role-gated API (`admin` or `blog`)
- **Blog AI assistant** — paste a draft to extract title, slug, excerpt, tags, cover color, and polished markdown; separate LLM settings in Settings; server-side markdown sanitization for safe rendering
- **Blog rendering** — line-based markdown parser (handles Python docstrings and nested code fences); improved article typography on `/blog/:slug`
- **Licensing activation** — detects existing deployment licenses on page load; email/license-code recovery to link a license to a new device without re-registering; case-insensitive app name lookup
- **Licensing API v0.7.2** — recovery endpoints (`/activation/recover/*`), license rebind by code, sync rebind when fingerprint changes
- **License update emails** — branded HTML notifications when admins extend, change type, edit, expire, deactivate, or reactivate a license
- **JPbot settings** — admin-configurable LLM provider, model dropdown, and encrypted API key in MongoDB; Book a demo flow refinements
- **Admin console** — Settings view (JPbot + blog assistant), blog panel, JWT role claim handling

### v0.16 — 2026-06-12
- **SC Studio subdomain** — nginx terminates TLS for `scstudio.nexxus-tech.com`; routes UI to `scstudio-frontend:5173` (Vite dev) and API/JPilot paths (`/api/`, `/calibrations/`, `/skill-feedback`, `/health`) to `scstudio-backend-api:8000` on the shared Docker network (no host port publish on scstudio)

### v0.15 — 2026-06-11
- **Products / JPilot videos** — demo clips served from `frontend/public/videos/` (not committed to git); documented filenames, 1080p export, MP4/WebM conversion, and server deploy steps

### v0.14 — 2026-06-11
- **JPilot blog** — article retitled to **AI Management Platform for Network Appliances**; repo and install URLs updated to `github.com/Nexxus-Tech-SAS/jpilot` and `install.nexxus-tech.com/jpilot`; installation steps aligned with current jpilot README (install folder prompt, legal terms, progress bar, license gate)
- **JPilot blog** — slug renamed to `/blog/jpilot-ai-management-platform`; permanent redirect from `/blog/nsagent-open-source-netscaler-copilot`; sitemap and products page link updated

### v0.13 — 2026-06-10
- **JPbot** — new **Book a demo** intake path: contact details → demo focus → Google Calendar booking link with visitor info in the URL; team notified via existing enquiry email
- **JPbot** — company / organization is now required on the contact step (frontend + API validation)
- **Products** — “Book a demo” CTA and JPbot share `JPILOT_DEMO_CALENDAR_URL` (`calendar.app.google/…`)

### v0.12 — 2026-06-10
- **Products hero** — product-launch lockup: “Introducing” eyebrow, centered JPilot logo, **JP**ilot title with cerulean `JP` accent, description as supporting copy, then subline → install block → video

### v0.11 — 2026-06-09
- **Products** — rebuilt `/products` as a JPilot command-first landing: hero with product logo, branded install blocks (macOS / Linux / Windows tabs via `install.nexxus-tech.com`), demo-video placeholders, early-access licensing note, supported-platforms grid, and three-action CTA (no GitHub links)
- **JPilot SEO** — repositioned from “AI Copilot” to “AI management platform”; titles broadened to **Network Appliances**; vendor names kept in descriptions, subline, and platform list; JSON-LD `SoftwareApplication` descriptions updated
- **Products UX** — tighter hero rhythm, uniform section padding, 16:9 max-width video/skeleton containers, readable copy line lengths
- **Footer** — new **Legal** column: Privacy and Terms of Use (`jpilot.nexxus-tech.com/legal/…`)
- **Favicon** — `nexxus-tech-favicon.png` replaces `nexxus-tech-icon.png` site-wide

### v0.10 — 2026-06-05
- **SEO** — per-route meta titles/descriptions, canonical URLs, Open Graph/Twitter cards, and JSON-LD (Organization, Person, Service, FAQPage, SoftwareApplication); `robots.txt` and `sitemap.xml` added
- **FAQ** — new `/faq` page with 10 accordion items; footer link; FAQPage structured data
- **Products** — new `/products` page for JPilot (overview, philosophy, capabilities, roles, platforms, founder note); homepage product showcase; nav and footer **Products** links
- **JPilot** — product narrative from activation letter; `JpilotLogo` component (dark/light SVG variants); platform cards styled like the About vision grid
- **Accessibility** — skip-to-content link, nav landmarks, contact form `aria-*`, team carousel pause/resume control

### v0.09 — 2026-06-04
- **Branding** — new Nexxus Tech wordmark SVG and PNG favicon across the public site, admin console, and activation portal; legacy `logo*.svg` assets removed
- **Home** — hero subtitle reframed with emphasized messaging (accessibility, AI-driven innovation, people-first growth, 20+ countries)
- **Home** — “Why Nexxus Tech” copy refresh; sixth service card updated to **ADC Platform Migrations** (F5 BIG-IP ↔ NetScaler)
- **Services** — NetScaler section expanded for bidirectional ADC migrations, WAF/LTM policy translation, and parallel-run cutovers
- **About** — **Our Vision** section (`/about#vision`): “People First. Technology Amplified.” with AI pull quote
- **About** — **Sebastian Garcia Tabares** added to Meet the Team (Principal Enterprise Networking Architect · CCIE Enterprise)
- **JPbot** — “Chat with JPbot” invite shows once per browser session; auto-dismisses after 5 seconds; no repeat after close (chat still available via the bubble)

### v0.08 — 2026-06-04
- **Activation page** — Arabic founder letter (UAE locale) with RTL layout; form UI stays English when Arabic is selected
- **Activation i18n** — locale codes aligned to country flags (US, Colombia, Brazil, UAE); PNG flag assets replace SVGs for broader browser support

### v0.07 — 2026-06-04
- **Activation page** — trilingual founder letter (English, Spanish, Portuguese) with SVG flag language switcher (Windows-compatible); form on the right, letter on the left
- **Activation UX** — deployment details under “Your information”; app fingerprint hidden; activation date shown as DD-MM-YYYY
- **Country field** — PrimeVue AutoComplete with searchable country list; OFAC high-risk jurisdictions excluded from selection
- **Licensing API v0.7.2** — `country` captured and stored at activation
- **Admin console** — extend license dialog defaults to 30 additional days

### v0.06 — 2026-06-04
- **Licensing system enabled** — end-to-end activation, sync, and admin management for on-premises products (e.g. JPilot); see [Licensing system overview](#licensing-system-overview) below
- **Admin console** — standalone Vue app at `/adminconsole`: license list/management, user accounts, passkey sign-in, JWT session
- **Activation flow** — public page at `/licensing/activate`; email verification before a license is issued and bound to a deployment
- **Sync API** — client apps periodically sync to refresh license status, expiration, and encrypted license payload
- **Licensing API v0.7.0** — MongoDB-backed FastAPI service; license CRUD, extend/expire/deactivate, offline license export

### v0.05a — 2026-06-04
- **Fix: licensing 502** — resilient MongoDB startup retries, healthcheck always returns 200, compose waits for MongoDB/licensing healthy before nginx routes traffic; clearer env validation errors in logs

### v0.05 — 2026-06-04
- **Licensing Phase 1** — MongoDB + Python licensing API in Docker Compose, exposed at `/licensing/` via nginx
- **Admin console** — `/adminconsole` login (env-based credentials, JWT); placeholder dashboard for future license management
- **Env** — `ADMIN_CONSOLE_USER`, `ADMIN_CONSOLE_PASSWORD`, `ENCRYPTION_KEY`, `JWT_SECRET_KEY`, `MONGODB_URI` (see `.env.example`)

### v0.04 — 2026-06-03
- **About: Meet the Team carousel** — team profiles rotate in a PrimeVue Carousel with circular autoplay (3s interval), prev/next controls, and dot indicators
- **About: Vanessa Cabrera Figueredo** — Principal Product Experience Designer · AI & Enterprise UX added to the team section
- **Fix: team carousel autoplay** — reliable 3s rotation via controlled page state (PrimeVue built-in autoplay does not start when `circular` is enabled)

### v0.03b — 2026-06-02
- **UI: blog category tags** — high-contrast `tag-on-cover` style on colored card headers and post hero so category labels remain readable on all `cover_color` values (blog grid, home preview, post page)

### v0.03 — 2026-06-02
- **SSL: complete certificate chain** — `ssl_certificate` now serves `fullchain.crt` (leaf + SSL2BUY intermediate + Sectigo/USERTrust cross-cert), resolving the SSL Labs "incomplete chain / grade capped to B" finding
- **SSL: Post-Quantum Cryptography** — enabled `X25519MLKEM768` hybrid key exchange via `ssl_conf_command Curves`; upgraded nginx base image to `stable-alpine` (OpenSSL 3.3+) which includes ML-KEM support
- **Server: GitHub SSH access** — generated Ed25519 deploy key (`github_nexxus`), configured `/root/.ssh/config`, and switched git remote from HTTPS to SSH (`git@github.com:juandiab/nexxus-web.git`)

### v0.02
- Blog articles rewritten from official docs; PQC article added
- OWASP NetScaler WAF article with accurate technical content
- Guided JPilot workflows (LB, AppFW, CSR, auth, Gateway)

### v0.01
- Initial release

---

## Quick Start (Production)

### 1. Configure environment
```bash
cp .env.example .env
# Edit .env with SMTP, AI API key, and licensing variables (required for /licensing/)
```

Generate a valid Fernet `ENCRYPTION_KEY`:
```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### Licensing 502 troubleshooting

If `curl https://nexxus-tech.com/licensing/health` returns **502**:

```bash
docker compose ps
docker compose logs licensing --tail 80
docker compose logs mongodb --tail 30
```

Common causes:
- Missing licensing vars in `.env` (container exits immediately)
- Invalid `ENCRYPTION_KEY` (must be a Fernet key, not a random string)
- `nexxustech-licensing` not running — run `docker compose up -d --build mongodb licensing` and rebuild nginx after pulling

---

## Licensing system overview

Nexxus Tech products can be licensed through this stack. The design keeps sensitive material (license codes, encrypted payloads) out of public docs and admin UI where possible.

| Surface | URL | Purpose |
|---|---|---|
| Activation | `/licensing/activate` | End-user activates or recovers a deployment license (email OTP); shows existing license when fingerprint already registered |
| Sync | `/licensing/sync` | Installed apps report fingerprint + app name; server returns current status, expiration, and an updated encrypted license blob |
| SC Studio register | `/licensing/scstudio/register` | SC Studio server first-time registration (pending until admin approval) |
| SC Studio sync | `/licensing/scstudio/sync` | Approved SC Studio server pulls encrypted full license database (API key auth) |
| Admin console | `/adminconsole` | Operators sign in (password + passkey), manage licenses, SC Studio servers, and platform users |
| Licensing API | `/licensing/` | REST API (health, auth, licenses, activation, sync, scstudio) — proxied by nginx to the `licensing` container |

**Typical flow**

1. **Activate** — The application opens the activation page (or calls the API). If the deployment already has a license, it is shown immediately. Otherwise the user verifies email (or recovers an existing license by email/code) before a license is bound to the fingerprint and application name.
2. **Run** — The app stores its license locally and validates expiration and status.
3. **Sync** — On a schedule (or on demand), the app syncs with the server to pick up admin changes (extended validity, type change, deactivation, forced expiry). Users receive email when admins change their license.
4. **Administer** — From the admin console, operators can extend validity, change license type, force-expire, deactivate, or delete licenses. License changes trigger user notification emails when SMTP is configured.

**SC Studio license database sync**

1. **Register** — SC Studio calls `POST /licensing/scstudio/register` with its `serverName`, `serverFingerprint`, and IP addresses.
2. **Approve** — An admin approves the server under **SC Studio** in the admin console; Nexxus generates a `serverId` and API key (shown once for the operator to paste into SC Studio).
3. **Sync** — SC Studio calls `POST /licensing/scstudio/sync` with header `X-ScStudio-Api-Key` and body `{ "serverId": "..." }`. The response includes `encryptedDatabase`, encrypted with the registered `serverFingerprint` (not the API key). SC Studio decrypts locally and imports the catalog.
4. **Manage** — Admins can view/copy/regenerate/disable keys, reject or delete registrations; each approved server has exactly one API key.

**Admin console capabilities**

- View licenses in a compact table (contact, organization, license type, status, validity)
- Force-expire (blocks auto-renew for free licenses), deactivate/reactivate, extend days, change type, delete
- Email notifications to license holders on extend, type change, edit, expire, deactivate, and reactivate
- Manage admin users (create, deactivate, password reset, passkey management)
- SC Studio server registrations and license-sync API keys (admin only)
- Blog post management and AI assistant settings (admin / blog roles)

**Configuration**

Required env vars are listed under **Licensing** in `.env.example` (`ENCRYPTION_KEY`, `JWT_SECRET_KEY`, `MONGODB_URI`, WebAuthn/ SMTP settings for email). Generate secrets as described in [Quick Start](#1-configure-environment); do not commit `.env`.

**Operations**

```bash
docker compose up -d --build mongodb licensing admin-console nginx
curl -s https://nexxus-tech.com/licensing/health
```

For local development with hot reload, use `docker-compose.dev.yml` (see repo).

### 2. Ensure SSL certs are in place
Same layout as NSAgent — place `cert.crt` (full chain) and `cert.key` in `nginx/ssl/`. See **[nginx/ssl/README.md](nginx/ssl/README.md)** for conversion steps, verification commands, and Docker volume notes.

```bash
chmod 600 nginx/ssl/cert.key
chmod 644 nginx/ssl/cert.crt
docker compose restart nginx   # after cert updates (no image rebuild)
```

### 3. Build and run
```bash
cd website/
docker compose up -d --build
```

The site will be available at:
- **https://nexxus-tech.com** (port 443)
- **http://nexxus-tech.com** → redirects to HTTPS (port 80)

---

## Development

### Frontend only
```bash
cd frontend/
npm install
npm run dev    # http://localhost:5173
```

### Backend only
```bash
cd backend/
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

---

## Project Structure
```
website/
├── docker-compose.yml
├── docker-compose.dev.yml    ← Dev stack with Vite hot reload
├── .env.example              ← Copy to .env and configure
├── nginx/
│   ├── Dockerfile
│   └── nginx.conf            ← SSL + reverse proxy config
├── frontend/
│   ├── Dockerfile
│   ├── src/views/LicensingActivateView.vue
│   └── …                     ← Home, Services, About, Blog, Contact
├── admin-console/            ← Operator UI (/adminconsole)
├── licensing/                ← Licensing + activation + sync API
│   ├── main.py
│   ├── routers/
│   └── services/
├── activation-portal/        ← Standalone activation UI (optional)
└── backend/
    ├── Dockerfile
    ├── main.py               ← FastAPI app
    ├── routers/
    │   ├── contact.py        ← Contact form → email
    │   ├── blog.py           ← Blog API (JSON-backed)
    │   └── chat.py           ← JPbot chat (DeepSeek)
    └── data/
        └── blog_posts.json   ← Add posts here
```

---

## Configuring JPbot (chat widget)

1. Create a [DeepSeek API](https://platform.deepseek.com/) key and set in `.env`:
   ```
   AI_PROVIDER=deepseek
   AI_API_KEY=your-deepseek-api-key-here
   AI_MODEL=deepseek-chat
   ```
2. Restart the backend: `docker compose restart backend`

JPbot collects name, email, company, and service, then discusses the visitor's needs. When ready, they submit an enquiry (same email flow as the contact form). Draft details can pre-fill `/contact` via session storage.

The **“Chat with JPbot”** invite card appears ~2.5s after page load, once per browser session. It auto-closes after 5 seconds if ignored, or when dismissed manually; it does not reappear until a new session. Visitors can always open chat from the floating bubble.

---

## Managing the blog

Articles live in `backend/data/blog_posts.json` as Markdown. Full guide: **[docs/BLOG.md](docs/BLOG.md)**.

**Add a new post:**

```bash
python3 scripts/new-blog-post.py \
  --title "Your Article Title" \
  --category "WAF & Security" \
  --content-file path/to/draft.md
```

Then on the server: `docker compose restart backend` (no frontend rebuild needed).

Copy `backend/data/blog_post.template.json` if you prefer to edit JSON by hand.

---

## Replacing the Logo

Logo files (SVG):
- `frontend/public/nexxus-tech-logo-full-large.svg` — full wordmark (navbar, footer, admin header)
- `frontend/public/nexxus-tech-favicon.png` — favicon (300×300), used site-wide
- `frontend/src/assets/nexxus-tech-logo-full-large.svg` — copy imported by navbar/footer

Replace the public files, sync to `src/assets/`, then rebuild (`docker compose up -d --build frontend`).

---

## JPilot product demo videos

Demo clips on `/products#jpilot` are **self-hosted** under `frontend/public/videos/` and served at `/videos/…`. They are **excluded from git** (too large for GitHub); copy them to the server before rebuilding the frontend image.

### Filenames

| Base name | Section |
|---|---|
| `install` | Hero (user-initiated play; optional `install-poster.jpg`) |
| `section-chat` | Talk to your appliances in plain language |
| `section-roles` | Architect, Operator, Analyst |
| `section-providers` | Your keys, your data, your hardware |
| `section-mcp` | Built on MCP |

For each clip, provide **`{name}.webm`** and **`{name}.mp4`**. `DemoVideo` probes for the `.webm` file to decide whether to show the player or the skeleton placeholder.

### Export settings

- **Resolution:** 1920×1080 (16:9) — displays at up to 720px wide but fullscreen uses full resolution
- **Source:** DaVinci Resolve → `.mov`, then convert for the web

### Convert `.mov` → MP4 + WebM (ffmpeg)

```bash
brew install ffmpeg   # macOS

for f in *.mov; do
  base="${f%.mov}"
  ffmpeg -i "$f" -c:v libx264 -crf 20 -preset slow -an -movflags +faststart "${base}.mp4"
  ffmpeg -i "$f" -c:v libvpx-vp9 -crf 32 -b:v 0 -an "${base}.webm"
done
```

Hero poster still (optional):

```bash
ffmpeg -i install.mov -ss 00:00:02 -vframes 1 -q:v 2 install-poster.jpg
```

### Deploy to production

```bash
rsync -av frontend/public/videos/ user@server:/opt/nexxus-web/frontend/public/videos/
ssh user@server 'cd /opt/nexxus-web && docker compose up -d --build frontend'
```

Until at least `{name}.webm` is present on the server, the products page shows a skeleton placeholder for that slot.
