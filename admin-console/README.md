# Admin Leads module

Consulting lead tracking at `/adminconsole/leads` (admin role required). Public `/ai-integration` enquiries and contact/JPbot submissions land here as `source=web_form` leads.

Edit/create lead form uses PrimeVue `Select` with `option-label` / `option-value` so dropdowns show labels (e.g. “New”, “Web form”) instead of raw option objects.

## Leads bot API key

JP generates a key in **Admin → Leads keys** (`/adminconsole/leads-api-keys`), then gives the raw key to the Leads bot operator. The bot sends it on every ingestion request:

```
X-Nexxus-Leads-Key: <raw_key>
```

Keys are shown once at creation or rotation. Revoke compromised keys from the same page.

## Leads bot contract

Leads bot drafts proposals offline; update `proposal_status` when sent.

Authenticated API for automation:

- `GET /api/admin/leads` — list (filters: `q`, `status`, `source`, `locale`, `include_archived`)
- `GET /api/admin/leads/{id}` — detail with timeline, `last_api_sync_at`, `last_api_agent`, `proposals[]`
- `POST /api/admin/leads` — create manual lead
- `PUT /api/admin/leads/{id}` — full update
- `PATCH /api/admin/leads/{id}` — partial update (e.g. `research_summary`, `proposal_status`)
- `POST /api/admin/leads/{id}/notes` — append timestamped note
- `DELETE /api/admin/leads/{id}` — archive (soft delete)
- `GET /api/admin/leads/export.csv` — CSV export
- `GET /api/admin/leads/{id}/proposals/{proposalId}/file` — download proposal PDF (admin JWT)

### Leads API keys (admin JWT)

- `GET /api/admin/leads-api-keys` — list keys
- `POST /api/admin/leads-api-keys` — create (`name`, `agent`: `leads` | `chief-of-staff`)
- `POST /api/admin/leads-api-keys/{id}/revoke`
- `POST /api/admin/leads-api-keys/{id}/rotate` — new raw key once

MongoDB collections: `leads`, `leadsApiKeys` (hashed keys only).

Public forms (`POST /api/contact`, JPbot `POST /api/chat/submit`) create leads with `source=web_form`, `status=new`.

Service ingestion API (`/api/v1/leads`): see [backend/README.md](../backend/README.md).
