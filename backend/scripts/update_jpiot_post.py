#!/usr/bin/env python3
"""Update JPilot blog post in blog_posts.json."""
import json
from pathlib import Path

CONTENT = r"""# JPilot: NetScaler AI Copilot with Memory-Guided Tools

Managing NetScaler ADC at scale means juggling **Next-Gen API** endpoints, classic **NITRO**, and **SSH CLI** syntax—often under pressure during incidents or migration projects. **JPilot** is Nexxus Tech's name for an open-source NetScaler copilot platform: a unified admin UI plus an AI assistant that registers appliances, connects to your chosen LLM provider, and reads or changes configuration through audited tools—**without credentials ever being sent to the model**.

The current open-source foundation is available on GitHub ([juandiab/nsagent](https://github.com/juandiab/nsagent), release **v0.02**). We use the **JPilot** name in product and roadmap discussions to keep branding distinct from third-party trademarks.

> JPilot / this open-source stack is an independent project and is not affiliated with Citrix. NetScaler is a trademark of Citrix Systems, Inc.

## Why another NetScaler tool?

Most teams already use ADM, automation scripts, or ad-hoc CLI sessions. The gap JPilot targets is **AI-assisted operations with guardrails**:

- **Official syntax in memory** — curated memory files for Next-Gen API and ADC CLI are searched *before* writes, so the assistant is steered toward real endpoints and commands instead of inventing syntax.
- **Tool execution, not chat-only advice** — the orchestrator runs CLI or API tools for changes, with confirmation for destructive operations.
- **Credentials stay on your side** — appliance passwords are encrypted (Fernet) in the database; only the MCP server uses them to talk to NetScaler.

That combination supports **migrations**, **health checks**, and **repeatable LB/AppFW workflows**—the same problems Nexxus Tech helps customers solve in production.

## NetScaler Next-Gen API: why it matters now

If you have not enabled **Next-Gen API** on your ADCs yet, you are leaving the best path for modern automation on the table. Citrix introduced it as the **forward-looking management plane** for NetScaler—REST-first, documented with **OpenAPI**, and oriented around **applications** rather than dozens of low-level NITRO objects stitched together by hand.

### What you gain as a customer

| Advantage | What it means in practice |
|-----------|-------------------------|
| **REST & JSON your teams already know** | Standard HTTP verbs and JSON payloads fit naturally into Python, Ansible, Terraform pipelines, and internal portals—no proprietary client required for basic integration. |
| **Application-centric model** | Configure **applications** and their components the way delivery teams think—virtual servers, services, and bindings as a coherent unit—not as a scavenger hunt across `lbvserver`, `service`, and `lbmonitor` unless you need classic granularity. |
| **OpenAPI documentation** | Machine-readable specs enable accurate client generation, contract testing, and **AI assistants that cite real endpoints**—JPilot's memory files are aligned to this model so suggestions map to callable APIs. |
| **Faster time-to-value for DevOps** | Platform and SRE teams onboard quicker than mastering the full NITRO catalog; greenfield apps and migrations can start on Next-Gen while legacy objects remain reachable via NITRO or CLI. |
| **Safer automation at scale** | Predictable resource URLs and schemas reduce scripting errors; combined with JPilot's **read-first** and **confirm-before-change** flows, you get automation speed without blind bulk edits. |
| **Coexistence with NITRO & CLI** | Nothing forces a big-bang cutover—Next-Gen, NITRO, and SSH CLI run side by side. JPilot uses **Next-Gen for application lifecycle** where available and falls back to CLI/NITRO for diagnostics and edge cases. |

### Enable it in minutes

On each appliance (Next-Gen API requires the **SSL default profile**—enable it first if `enable ns nextgenapi` reports an error):

```
set ssl parameter -defaultProfile ENABLED
enable ns nextgenapi
save ns config
show ns nextgenapi
```

You should see **Next-Gen API State: STARTED**. After that, JPilot and your own pipelines can list and manage **Next-Gen applications**, issue GET/POST/PUT/DELETE against documented endpoints, and keep classic **`lbvserver`** inventory in view for hybrid estates.

Official docs: [NetScaler Next-Gen API getting started](https://developer-docs.netscaler.com/en-us/nextgen-api/getting-started-guide).

**Bottom line for decision-makers:** teams modernizing ADC operations—or running **F5-to-NetScaler** and **multicloud** programs—should treat Next-Gen API as the default integration surface for new work. JPilot is built to **lead with Next-Gen**, steer the assistant with curated API memory, and only drop to NITRO or shell when the task demands it. That is how you attract faster migrations, fewer operational surprises, and AI copilots that actually execute—not hallucinate—your changes.

## Keeping confidential information secure

Sensitive data is a blocker for many AI rollouts. JPilot is designed so **confidential information does not need to leave your control plane**:

- **Local agents** — run inference and tool execution inside your network; the model sees only what you allow through scoped tools and redacted context.
- **Enterprise APIs** — route requests through your approved AI gateway (private endpoints, DLP, logging, and policy) so traffic never hits public SaaS by default.
- **Secrets never in the prompt** — ADC credentials and connection strings stay in encrypted storage and MCP; they are not embedded in chat history sent to the LLM.
- **Human approval for change** — destructive CLI/API operations require explicit confirmation after review.

Whether you deploy fully on-premises or hybrid, you choose **where the brain runs** and **what context crosses the boundary**—aligned with zero-trust and regulated environments.

## Architecture at a glance

```
Vue 3 UI  →  FastAPI backend  →  MCP server  →  NetScaler ADC
                ↓
            MongoDB (settings, appliances, users, AI providers)
```

| Component | Role |
|-----------|------|
| **Frontend** (Vue 3 + PrimeVue) | Appliances, AI providers, copilot chat, user admin |
| **Backend API** (FastAPI) | Auth, CRUD, orchestration, MCP proxy |
| **MCP server** | Next-Gen API, NITRO helpers, SSH CLI, diagnostics |
| **MongoDB** | Encrypted appliance store and configuration |

JPilot supports **OpenAI**, **Anthropic**, **Gemini**, **Grok**, **LM Studio**, and OpenAI-compatible endpoints—so you can align with existing AI governance and enterprise API policies.

## What JPilot can do today

### Inventory and configuration

- List virtual servers from **Next-Gen applications** and classic **`lbvserver`**
- Create applications via Next-Gen API or multi-step LB setup via CLI (service groups, binds, `save ns config`)
- Read-only NITRO and Next-Gen GET/POST/PUT/DELETE with memory search first

### Guided workflows — ask in plain language

JPilot is built for **conversational delivery**: you describe the outcome, it consults best practices and implementation guides in memory, asks for anything still missing, shows you the plan, and **only pushes configuration after you confirm and approve**.

**Load balancing for Microsoft Outlook / Exchange**

> *"Can you configure LB for Outlook? Here is the VIP and here are the backend servers."*

JPilot searches **best-practice and implementation guidance** (health monitors, persistence, SSL/offload, port expectations), then asks targeted follow-ups—endpoints, subnets, certificate needs, and any remaining design choices. When you are satisfied, it applies the approved config via Next-Gen API or CLI and runs `save ns config` where required.

**Protect applications — or aim for A+**

> *"Protect this application"* or *"Make it A+"*

JPilot reviews **AppFW** profiles, signatures, TLS settings, and exposure, recommends hardening (and optional WAF tuning), and can implement changes once you sign off—so security uplift is guided, not guessed.

**Generate a new CSR**

> *"Generate a new CSR for `www.example.com`"* (or a list of SANs)

JPilot walks through key size, binding context, and certificate request details, then produces the CSR workflow on the appliance you select.

**Authentication for specific websites**

Configure user-facing auth on virtual servers using the method your IdP supports:

- **SAML** (metadata, ACS URLs, attribute maps)
- **LDAP** / **Active Directory**
- **RADIUS**
- **n-factor** (step-up and combined policies)
- **TACACS** (administrative or delegated scenarios)

You name the site or vserver; JPilot asks for server endpoints, groups, and policy intent, then builds and applies the bind chain after approval.

**NetScaler Gateway — simplified setup**

Provide **Gateway server information** (VIP, certificates, authentication servers, session policies). JPilot translates that into a structured Gateway configuration—virtual server, policies, and integrations—without forcing you through every low-level screen first. Review the proposed config, confirm, and deploy.

Across all of these flows, the pattern is the same: **memory-backed guidance → clarifying questions → proposed config → your approval → push**.

### Diagnostics

Built for the “is it the network or NetScaler?” moment:

| Question | Tooling |
|----------|---------|
| Can the appliance reach a host? | `ping`, `ping6`, `traceroute` via diagnostics |
| Is **TCP port** open on a backend? | Telnet / TCP port check from the appliance |
| Counters, events, performance | Read-only counter collection |

**Auto port check:** messages that include `host:port` can trigger a telnet check from the appliance and return **open**, **refused**, or **no_response** before the model picks a tool—speeding up triage.

### Security-minded auth

- Password login; optional **WebAuthn passkeys**
- Admin user management with roles (`admin` / `user`)
- Destructive operations require explicit **`confirmed=true`** after user approval

## Quick start (Docker)

1. Generate a Fernet key and copy `.env.example` to `.env`
2. Set encryption key, `JWT_SECRET_KEY`, and admin bootstrap credentials
3. Run `docker compose up --build`
4. Open the UI, add a NetScaler appliance, configure an AI provider, enable **SSH fallback** for diagnostics
5. Use the copilot with an appliance selected

Enable Next-Gen API on the ADC (`enable ns nextgenapi`) for API tools; SSH (port 22) is required for classic CLI and diagnostics.

## Roadmap

The following capabilities are planned for JPilot beyond today's v0.02 foundation.

### Multi-agent roles

Specialized copilots with distinct prompts, tools, and guardrails—the right expert for each task:

- **Administrator** — Day-to-day operations: inventory, bindings, saves, and controlled changes with approval workflows.
- **Troubleshooter** — Incident diagnostics: reachability, port checks, counters, and guided root-cause paths from the appliance.
- **Designer** — Greenfield and migration design: LB patterns, GSLB, and AppFW layouts grounded in memory-backed syntax before execution.
- **Security Advisor** — Hardening and policy review: AppFW, SSL/TLS, auth profiles, and exposure checks with read-first recommendations.

### Load balancing for scalability

Run multiple JPilot backend instances behind a load balancer for horizontal scale, session affinity, and high availability as adoption grows across teams and regions.

### Cloud SaaS with on-prem agent

Optional **managed JPilot cloud** for UI, orchestration, and integrations, paired with a lightweight **on-premises agent** that stores ADC credentials and runs tools inside your network—the data plane stays in your DC while you consume SaaS convenience.

### Slack and Microsoft Teams

**ChatOps** in the channels your NOC and application teams already use: ask questions, trigger approved diagnostics, and receive structured summaries without opening the full admin UI.

Contributions and feedback are welcome on the [GitHub repository](https://github.com/juandiab/nsagent) as these features land.

## How this fits Nexxus engagements

We see JPilot as a practical accelerator for **F5-to-NetScaler migrations**, **WAF tuning**, and **multicloud ADC** designs—not a replacement for change control or peer review. Memory files, confirmation gates, and local/enterprise AI boundaries mirror how we already work: **documented syntax first**, then executed change, then validation.

If you are planning AI-assisted NetScaler operations with proper guardrails, we can help you pilot JPilot in your environment.

*Want a working session on JPilot, private AI endpoints, or migration guardrails? [Contact Nexxus Tech](/contact).*"""

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "blog_posts.json"

def main():
    posts = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    for post in posts:
        if post.get("id") == "5":
            post["title"] = "JPilot: NetScaler AI Copilot with Memory-Guided Tools"
            post["excerpt"] = (
                "JPilot is Nexxus Tech's NetScaler AI copilot—built on Next-Gen API "
                "(REST, OpenAPI, application-centric automation), memory-guided tools, "
                "secure local/enterprise AI, and a roadmap for multi-agent roles, "
                "scale-out, SaaS + on-prem agent, and Slack/Teams."
            )
            post["content"] = CONTENT.strip()
            post["tags"] = [
                "JPilot",
                "NetScaler",
                "Next-Gen API",
                "AI",
                "MCP",
                "Automation",
                "Roadmap",
            ]
            post["read_time"] = 9
            break
    else:
        raise SystemExit("Post id 5 not found")
    DATA_FILE.write_text(
        json.dumps(posts, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print("Updated JPilot blog post")


if __name__ == "__main__":
    main()
