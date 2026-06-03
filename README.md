# Nexxus Tech Website

**Version 0.04** — Full-stack website for **nexxus-tech.com** — WAF · NetScaler · Cloud Security · AI

## Stack
| Layer | Technology |
|---|---|
| Frontend | Vue 3 + PrimeVue 4 + Vite |
| Backend | Python 3.12 + FastAPI |
| Web Server | Nginx stable-alpine (SSL termination + reverse proxy) |
| Runtime | Docker Compose |

---

## Changelog

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
# Edit .env with your SMTP credentials and AI API key
```

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
├── .env.example              ← Copy to .env and configure
├── nginx/
│   ├── Dockerfile
│   └── nginx.conf            ← SSL + reverse proxy config
├── frontend/
│   ├── Dockerfile            ← Multi-stage: build + serve
│   ├── src/
│   │   ├── views/            ← Home, Services, About, Blog, Contact
│   │   ├── components/       ← NavBar, Footer, ChatWidget
│   │   └── assets/           ← SVG logos (transparent bg)
│   └── package.json
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

Logo files are SVG with transparent backgrounds:
- `frontend/src/assets/logo.svg` — full logo (for light backgrounds)
- `frontend/src/assets/logo-white.svg` — full logo (for dark backgrounds)
- `frontend/src/assets/logo-icon.svg` — icon only (used as favicon)

Replace any of these files and rebuild the frontend (`docker compose up -d --build frontend`).
