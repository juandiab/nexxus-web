# NSAgent: Open-Source NetScaler Copilot with Memory-Guided AI Tools

Managing NetScaler ADC at scale means juggling **Next-Gen API** endpoints, classic **NITRO**, and **SSH CLI** syntax—often under pressure during incidents or migration projects. **NSAgent** (NetScaler Copilot) is an open-source platform that brings a unified admin UI and an AI assistant together: register appliances, pick your LLM provider, and let Copilot read and change configuration through audited tools—without credentials ever being sent to the model.

Repository: [github.com/juandiab/nsagent](https://github.com/juandiab/nsagent) · Release **v0.02**

> NSAgent is an independent project and is not affiliated with Citrix. NetScaler is a trademark of Citrix Systems, Inc.

## Installation

The only prerequisite is **Docker**. The installer downloads the project, generates secrets and a TLS certificate, writes `.env`, launches the stack, and opens JPilot in your browser.

**Prerequisites:** Docker and Docker Compose; NetScaler ADC with **Next-Gen API** enabled (`enable ns nextgenapi`) for API tools; SSH access (port 22) for classic CLI and diagnostics; optional SMTP for password-reset emails.

### Windows

Install [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/) and [Git for Windows](https://git-scm.com/download/win), then run in **PowerShell**:

```powershell
irm https://raw.githubusercontent.com/juandiab/nsagent/main/get.ps1 | iex
```

### macOS

Install [Docker Desktop](https://docs.docker.com/desktop/install/mac-install/) (or let the installer set it up via Homebrew), then run in **Terminal**:

```bash
curl -fsSL https://raw.githubusercontent.com/juandiab/nsagent/main/get.sh | bash
```

### Ubuntu / Linux

Docker Engine is required—the installer offers to install it if missing. Then run:

```bash
curl -fsSL https://raw.githubusercontent.com/juandiab/nsagent/main/get.sh | bash
```

The script checks for Docker, downloads JPilot, and starts the setup wizard. Then:

1. Open **https://localhost:9443** (self-signed certificate—accept the one-time browser warning).
2. Complete the wizard: admin account, domain, and TLS (self-signed or your own cert).
3. On the **Review** step, **save the generated `NSAGENT_ENCRYPTION_KEY`**—required to restore or migrate the install and cannot be recovered.
4. Click **Install JPilot**. The wizard writes `.env` and `nginx/ssl/`, then launches the stack and opens it in your browser.
5. Sign in at **https://\<your-domain\>** with the admin account you created.

Already cloned the repo? Run `./install.sh` (macOS/Linux) or `.\install.ps1` (Windows) from the project root instead of the one-liner.

To reconfigure an existing install (overwrites `.env`):

```bash
./install.sh --reconfigure      # macOS / Linux
.\install.ps1 -Reconfigure      # Windows (PowerShell)
```

The installer generates `NSAGENT_ENCRYPTION_KEY` (Fernet) and `JWT_SECRET_KEY` automatically and derives WebAuthn, CORS, and API URL settings from the domain you choose.

**After first login:**

- **NetScalers** — add your appliance (name, host, API/SSH user and password).
- **AI Providers** — add an LLM provider and set it as default.
- **Settings → MCP** — tool toggles, **SSH fallback** (required for diagnostics and SSL shell), timeouts.
- **Settings → Platform** — optional Brave Search API key for JPilot doc augmentation.
- **Settings → Security** — register an optional passkey after password login.
- **Users** (admin) — create users with email (for password reset) and initial passwords.
- **SSL Certificate Tools** — generate CSR or self-signed cert on an appliance.
- **JPilot** — select an appliance and ask questions or request changes.

For manual `.env` configuration, TLS certificate placement, and advanced setup, see the [NSAgent README on GitHub](https://github.com/juandiab/nsagent#manual-setup-advanced).

## Why another NetScaler tool?

Most teams already use ADM, automation scripts, or ad-hoc CLI sessions. The gap NSAgent targets is **AI-assisted operations with guardrails**:

- **Official syntax in memory** — curated `netscaler_nextgen_api_memory.md` and `netscaler_adc_cli_memory.md` files are searched *before* API or CLI writes, so the assistant is steered toward real endpoints and commands instead of inventing syntax.
- **Tool execution, not chat-only advice** — the orchestrator requires `netscaler_run_cli_command` or `netscaler_run_cli_commands` for changes, with confirmation for destructive operations.
- **Credentials stay on your side** — appliance passwords are encrypted (Fernet) in MongoDB; only the MCP server uses them to talk to NetScaler.

That combination is what makes it useful for **migrations**, **health checks**, and **repeatable LB/AppFW workflows**—the same problems Nexxus Tech helps customers solve in production.

## Architecture at a glance

```
Vue 3 UI  →  FastAPI backend  →  MCP server  →  NetScaler ADC
                ↓
            MongoDB (settings, appliances, users, AI providers)
```

| Component | Role |
|-----------|------|
| **Frontend** (Vue 3 + PrimeVue) | Appliances, AI providers, Copilot chat, user admin |
| **Backend API** (FastAPI) | Auth, CRUD, Copilot orchestration, MCP proxy |
| **MCP server** | Next-Gen API, NITRO helpers, SSH CLI, diagnostics |
| **MongoDB** | Encrypted appliance store and configuration |

Copilot supports **OpenAI**, **Anthropic**, **Gemini**, **Grok**, **LM Studio**, and OpenAI-compatible endpoints—so you can align with your existing AI governance.

## What Copilot can do today

### Inventory and configuration

- List virtual servers from **Next-Gen applications** and classic **`lbvserver`**
- Create applications via Next-Gen API or multi-step LB setup via CLI (service groups, binds, `save ns config`)
- Read-only NITRO and Next-Gen GET/POST/PUT/DELETE with memory search first

### Diagnostics (v0.02)

Built for the “is it the network or NetScaler?” moment:

| Question | Tooling |
|----------|---------|
| Can the appliance reach a host? | `ping`, `ping6`, `traceroute` via `netscaler_run_diagnostic` |
| Is **TCP port** open on a backend? | `netscaler_telnet` or `tcp_port` diagnostic |
| Counters, events, performance | `netscaler_collect_nsconmsg` (read-only) |

**Auto port check:** if your message includes `host:port` (e.g. `192.168.20.36:5173`), the backend can run a telnet check from the appliance and return **open**, **refused**, or **no_response** before the model even picks a tool—saving time in triage.

NetScaler note: port checks use `/usr/bin/telnet` from the shell; the platform does not ship `nc` or GNU `timeout`. Spurious `ERROR: Export failed` after shell commands can be ignored when telnet output is clear.

### Security-minded auth

- Password login for all users; optional **WebAuthn passkeys** after registration in Settings
- Admin user management with roles (`admin` / `user`)
- Destructive CLI/API operations require explicit **`confirmed=true`** after user approval

## How this fits Nexxus engagements

We see NSAgent as a practical accelerator for teams we support on **F5-to-NetScaler migrations**, **WAF tuning**, and **multicloud ADC** designs—not a replacement for change control or peer review. The memory files and confirmation gates mirror how we already work: **documented syntax first**, then executed change, then validation (including port and path checks from the appliance perspective).

If you are building internal AI ops tooling, NSAgent is a solid reference implementation: MCP tool surface, orchestration rules, and an MIT-licensed codebase you can extend.

## What's next

The project is active at **v0.02** with room to grow—more StyleBook-style automation, deeper AppFW workflows, and enterprise hardening (TLS, external IdP) are natural follow-ons. Contributions and issues are welcome on GitHub.

*Want help designing AI-assisted NetScaler operations for your environment—or planning a migration with proper guardrails? [Contact Nexxus Tech](/contact).*
