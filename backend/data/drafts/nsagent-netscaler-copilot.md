# NSAgent: Open-Source NetScaler Copilot with Memory-Guided AI Tools

Managing NetScaler ADC at scale means juggling **Next-Gen API** endpoints, classic **NITRO**, and **SSH CLI** syntax—often under pressure during incidents or migration projects. **NSAgent** (NetScaler Copilot) is an open-source platform that brings a unified admin UI and an AI assistant together: register appliances, pick your LLM provider, and let Copilot read and change configuration through audited tools—without credentials ever being sent to the model.

Repository: [github.com/juandiab/nsagent](https://github.com/juandiab/nsagent) · Release **v0.02**

> NSAgent is an independent project and is not affiliated with Citrix. NetScaler is a trademark of Citrix Systems, Inc.

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

## Quick start (Docker)

1. Generate a Fernet key and copy `.env.example` to `.env`
2. Set `NSAGENT_ENCRYPTION_KEY`, `JWT_SECRET_KEY`, and admin bootstrap credentials
3. Run `docker compose up --build`
4. Open the UI (default `http://localhost:5173`), add a NetScaler appliance, configure an AI provider, enable **SSH fallback** in MCP settings for diagnostics
5. Use **Copilot** with an appliance selected

Enable Next-Gen API on the ADC (`enable ns nextgenapi`) for API tools; SSH (port 22) is required for classic CLI and diagnostics.

## How this fits Nexxus engagements

We see NSAgent as a practical accelerator for teams we support on **F5-to-NetScaler migrations**, **WAF tuning**, and **multicloud ADC** designs—not a replacement for change control or peer review. The memory files and confirmation gates mirror how we already work: **documented syntax first**, then executed change, then validation (including port and path checks from the appliance perspective).

If you are building internal AI ops tooling, NSAgent is a solid reference implementation: MCP tool surface, orchestration rules, and an MIT-licensed codebase you can extend.

## What's next

The project is active at **v0.02** with room to grow—more StyleBook-style automation, deeper AppFW workflows, and enterprise hardening (TLS, external IdP) are natural follow-ons. Contributions and issues are welcome on GitHub.

*Want help designing AI-assisted NetScaler operations for your environment—or planning a migration with proper guardrails? [Contact Nexxus Tech](/contact).*
