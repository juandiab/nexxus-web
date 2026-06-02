# Nexxus Tech Website

Full-stack website for **nexxus-tech.com** — WAF · NetScaler · Cloud Security · AI

## Stack
| Layer | Technology |
|---|---|
| Frontend | Vue 3 + PrimeVue 4 + Vite |
| Backend | Python 3.12 + FastAPI |
| Web Server | Nginx (SSL termination + reverse proxy) |
| Runtime | Docker Compose |

---

## Quick Start (Production)

### 1. Configure environment
```bash
cp .env.example .env
# Edit .env with your SMTP credentials and AI API key
```

### 2. Ensure SSL certs are in place
Your wildcard certificate is already at `../SSL_Cert/`:
- `wildcard.nexxus-tech.com.crt` — domain certificate
- `wildcard.nexxus-tech.com.key` — private key
- `ca-chain.crt` — CA chain

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
