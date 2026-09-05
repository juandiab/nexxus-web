# Nexxus Tech Backend

FastAPI service for nexxus-tech.com public API and admin-authenticated routes.

## Leads ingestion API

Service-authenticated routes for the Leads bot / Chief of Staff. Human admin CRUD remains at `/api/admin/leads` (JWT).

> Leads bot drafts proposals offline; update `proposal_status` when sent.

### API key setup (JP)

1. Sign in to admin console → **Leads keys** (`/adminconsole/leads-api-keys`)
2. Create a key (name + agent: `leads` or `chief-of-staff`)
3. Copy the raw key **once** — it is not stored in plaintext
4. Configure the bot with header `X-Nexxus-Leads-Key: <key>`

Optional break-glass: set `LEADS_API_KEY` in server `.env` if no Mongo keys exist yet.

### Base URL

```
https://nexxus-tech.com/api/v1/leads
```

### Auth headers

```
X-Nexxus-Leads-Key: nxlead_your-key-here
X-Nexxus-Agent: leads
```

Or: `Authorization: Bearer nxlead_your-key-here`

### Admin key management (JWT)

```
GET    /api/admin/leads-api-keys
POST   /api/admin/leads-api-keys
POST   /api/admin/leads-api-keys/{id}/revoke
POST   /api/admin/leads-api-keys/{id}/rotate
```

### Ingestion endpoints

```
POST   /api/v1/leads
PATCH  /api/v1/leads/{id}
GET    /api/v1/leads/{id}
GET    /api/v1/leads?company=&email=&status=&page=&limit=
POST   /api/v1/leads/{id}/proposals
GET    /api/admin/leads/{id}/proposals/{proposalId}/file   (admin JWT)
```

### curl examples

Create lead (new → 201):

```bash
curl -sS -X POST 'https://nexxus-tech.com/api/v1/leads' \
  -H 'Content-Type: application/json' \
  -H 'X-Nexxus-Leads-Key: nxlead_REPLACE_WITH_YOUR_KEY' \
  -H 'X-Nexxus-Agent: leads' \
  -d '{
    "company_name": "Acme Corp",
    "contact_email": "ceo@acme.example",
    "contact_name": "Jane Doe",
    "locale": "en",
    "research_summary": "Manufacturing SME; AI angles: predictive maintenance, doc QA.",
    "idempotency_key": "research-acme-2026-09-05"
  }'
```

Patch research / status:

```bash
curl -sS -X PATCH 'https://nexxus-tech.com/api/v1/leads/LEAD_UUID' \
  -H 'Content-Type: application/json' \
  -H 'X-Nexxus-Leads-Key: nxlead_REPLACE_WITH_YOUR_KEY' \
  -d '{"status": "proposal_draft", "note": "Draft ready for JP review."}'
```

Upload draft proposal PDF:

```bash
curl -sS -X POST 'https://nexxus-tech.com/api/v1/leads/LEAD_UUID/proposals' \
  -H 'X-Nexxus-Leads-Key: nxlead_REPLACE_WITH_YOUR_KEY' \
  -H 'X-Nexxus-Agent: chief-of-staff' \
  -F 'file=@/path/to/proposal.pdf;type=application/pdf' \
  -F 'kind=draft' \
  -F 'language=en' \
  -F 'email_subject=AI Integration Proposal — Acme Corp' \
  -F 'notes=First draft for JP review'
```

Search leads:

```bash
curl -sS 'https://nexxus-tech.com/api/v1/leads?email=ceo@acme.example&page=1&limit=20' \
  -H 'X-Nexxus-Leads-Key: nxlead_REPLACE_WITH_YOUR_KEY'
```

Unauthenticated request (expect 401):

```bash
curl -sS -o /dev/null -w '%{http_code}\n' 'https://nexxus-tech.com/api/v1/leads'
```

### Mongo collections

| Collection | Purpose |
|------------|---------|
| `leads` | Lead pipeline + embedded proposal metadata |
| `leadsApiKeys` | Hashed bot API keys (`key_hash`, `key_prefix`, never raw key) |

### PDF storage

Container path: `/app/data/lead-proposals/{lead_id}/{proposal_id}.pdf`  
Host mount: `./backend/data` (via docker-compose `backend` service volume)
