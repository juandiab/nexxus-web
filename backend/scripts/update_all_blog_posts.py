#!/usr/bin/env python3
"""Update blog posts 1-4 (disclaimer/corrections) and add post-quantum article (id 6)."""
import json
from pathlib import Path

DISCLAIMER = (
    "> **Note:** This article is a **concise technical overview** aligned with official "
    "NetScaler documentation—not a substitute for a full design review, test plan, or "
    "runbook. **Nexxus Tech can help you with end-to-end implementation** in your environment.\n"
)

FOOTER = (
    "\n\n---\n\n*This is a quick review to orient your team. For workshops, phased rollout, "
    "production hardening, and operational handover, [contact Nexxus Tech](/contact).*"
)

OWASP_FOOTER_ADD = (
    "\n\n---\n\n*This is a quick review aligned with OWASP Top 10:2025 and Citrix documentation. "
    "Nexxus Tech delivers full WAF programs—profile design, learning/tuning, API schema validation, "
    "and SIEM integration. [Contact us](/contact) for implementation support.*"
)

POSTS = {
    "1": {
        "content_patch": "footer",
        "footer": OWASP_FOOTER_ADD,
        "prepend_disclaimer": True,
    },
    "2": {
        "title": "Building Zero Trust Access with NetScaler Gateway, Okta, and Microsoft Entra ID",
        "excerpt": (
            "A documentation-aligned overview of Zero Trust with NetScaler Gateway as SAML SP, "
            "Microsoft Entra ID or Okta as IdP, Conditional Access, nFactor, and EPA—not a "
            "one-size-fits-all product bundle."
        ),
        "content": DISCLAIMER
        + r"""# Building Zero Trust Access with NetScaler Gateway, Okta, and Microsoft Entra ID

**Zero Trust** is an architecture: verify explicitly, use least privilege, and assume breach. It is **not** a single SKU. In practice, many enterprises combine **NetScaler Gateway** (secure access and reverse proxy), **Microsoft Entra ID** (directory and Conditional Access), and **Okta** (identity orchestration, MFA, or federation)—with clear separation of roles.

References: [Entra ID as SAML IdP](https://docs.netscaler.com/en-us/citrix-adc/current-release/aaa-tm/authentication-methods/saml-authentication/azure-saml-idp), [Okta + Gateway](https://help.okta.com/oie/en-us/content/topics/integrations/citrix-netscaler-radius-int.htm), [EPA in nFactor](https://docs.netscaler.com/en-us/netscaler-gateway/current-release/vpn-user-config/endpoint-policies/epa-as-factor-in-nfactor-authentication.html).

## What each component does

| Component | Role |
|-----------|------|
| **Microsoft Entra ID** | Authoritative directory (often), Conditional Access, device compliance signals |
| **Okta** | IdP/MFA broker, federation hub, or RADIUS bridge to Gateway |
| **NetScaler Gateway** | **SAML SP**, session management, authorization, optional **EPA**, app publishing |

Gateway evaluates the session (`NSC_TMAA` / `NSC_TMAS` cookies). Unauthenticated users are redirected to the IdP; the SP validates the SAML assertion before granting access.

## Identity patterns (choose deliberately)

### Pattern A — Entra ID as SAML IdP (common for Microsoft shops)

1. Register **Citrix ADC SAML Connector** (or equivalent enterprise app) in Entra ID.
2. On NetScaler: create **authentication SAML server** with IdP metadata URL, redirect URL, and SP signing certificate.
3. Bind SAML policy to **Gateway** or—preferably for MFA chains—**AAA virtual server** using **nFactor**.

Okta is optional here unless you federate Entra ↔ Okta for workforce SSO.

### Pattern B — Okta as IdP (SAML or RADIUS)

- **SAML 2.0:** Okta catalog app for Citrix Gateway; configure SAML server/policy on NetScaler ([Okta SAML guide](https://saml-doc.okta.com/SAML_Docs/How-to-Configure-SAML-2.0-for-NetScaler-Gateway.html)).
- **RADIUS:** Okta RADIUS Agent translates Gateway RADIUS to Okta API calls (MFA at login page). Users must complete Okta MFA enrollment before first Gateway login.

**Important:** SAML on Gateway **basic** vs **advanced** authentication policies affects **Citrix Workspace** SP-initiated flows. Full SSO into VDAs often requires **FAS** (Federated Authentication Service) or RADIUS—do not assume SAML alone delivers desktop SSO.

## nFactor and continuous device checks

Use an **authentication virtual server (AAA)** and **nFactor** policy labels instead of a single-factor bind when you need:

- LDAP/AD → MFA → EPA sequence
- Different paths by group (password vs push MFA)
- **Pre-auth EPA** (first step) and **post-auth EPA** (last step) per Citrix docs

EPA actions use `authentication epaAction` and bind to **noschema** policy labels. Failed EPA can **terminate** auth or place users in a **quarantine group** for limited access.

## Entra Conditional Access (identity plane)

In Entra ID, typical policies (orthogonal to Gateway CLI):

- Require **MFA** for external access
- Require **compliant device** (Intune)
- Block **legacy authentication**
- Use **Identity Protection** risk signals

These policies apply at IdP sign-in; Gateway still needs correct **session timeouts**, **split tunneling**, and **authorization policies** for apps.

## Sample SAML server skeleton (lab)

Replace URLs, certs, and metadata with your tenant values:

```
add authentication samlAction entra_saml \
  -samlIdPMetadataUrl "https://login.microsoftonline.com/<tenant>/federationmetadata/2007-06/federationmetadata.xml" \
  -samlRedirectUrl "https://login.microsoftonline.com/<tenant>/saml2" \
  -samlSigningCertName sp_signing_cert \
  -samlIssuerName "https://gateway.example.com/saml/sp"

add authentication policy saml_pol -rule true -action entra_saml

add authentication policylabel mfa_flow -loginSchema LSCHEMA_INT

bind authentication policylabel mfa_flow -policyName saml_pol -priority 100 -gotoPriorityExpression END

bind authentication vserver aaa_vs -policy saml_pol -priority 100 -nextFactor mfa_flow
```

Bind the **AAA vserver** to Gateway as needed; use the **nFactor visualizer** (GUI) for complex trees.

## Zero Trust checklist (realistic)

- [ ] Document user → IdP → Gateway → app data flow
- [ ] Prefer **HTTPS** everywhere; modern TLS ciphers on Gateway VIP
- [ ] Implement **nFactor** when MFA + EPA + multiple IdPs are required
- [ ] Align Entra **Conditional Access** with Gateway session policies
- [ ] Plan **FAS** or RADIUS if Citrix desktop SSO is in scope
- [ ] Centralize audit: Gateway logs + Entra sign-in logs + SIEM
- [ ] Test **fail closed** (IdP down, cert expiry, EPA failure)

## What this article is not

It does not replace a **threat model**, **PKI design**, or **per-application authorization** review. Vendor marketing claims (e.g. fixed percentage risk reduction) vary by environment—measure outcomes in **your** pilot.
"""
        + FOOTER,
        "tags": ["Zero-Trust", "NetScaler Gateway", "Entra ID", "Okta", "SAML", "nFactor"],
        "read_time": 11,
    },
    "3": {
        "title": "Automating NetScaler with NITRO, Python, and AI Assistants",
        "excerpt": (
            "How to use the official NITRO API/SDK, GitOps, and AI assistants responsibly "
            "for NetScaler operations—without trusting hallucinated CLI or unvalidated changes."
        ),
        "content": DISCLAIMER
        + r"""# Automating NetScaler with NITRO, Python, and AI Assistants

Large NetScaler estates accumulate **App Firewall profiles**, **policies**, **certificates**, and **bindings** across sites. Manual change is slow and drift-prone. Automation should use **supported APIs** first; AI is a **copilot**, not the source of truth.

Official references: [NetScaler APIs](https://www.netscaler.com/platform/apis), [NITRO error handling](https://developer-docs.netscaler.com/en-us/adc-nitro-api/current-release/error-and-exception-handling.html), [Next-Gen API](https://developer-docs.netscaler.com/en-us/nextgen-api/getting-started-guide).

## Start with NITRO (and Next-Gen where available)

**NITRO** is NetScaler’s REST configuration API. For Python, use the **NITRO SDK** from your appliance (**Downloads → NITRO API SDK for Python**) or HTTPS REST with session cookies.

```python
from nssrc.com.citrix.netscaler.nitro.service.nitro_service import nitro_service

ns = nitro_service("10.0.0.10", "https")
ns.login("api_user", "password", 3600)
try:
    # Use generated resource types from the SDK for typed operations
    pass
finally:
    ns.logout()
```

**Best practices**

- Use **HTTPS**; validate certificates in production
- Store credentials in a **vault**, not source code
- Check **`errorcode`** in responses (non-zero = failure)
- Use **`save ns config`** (or NITRO save) for persistent changes
- For bulk jobs, understand **`X-NITRO-ONERROR`** continue vs terminate behavior
- Prefer **read-only** service accounts for inventory; separate **change** roles

For greenfield automation, evaluate **Next-Gen API** (application-centric, OpenAPI) alongside classic NITRO.

## What to automate (high value)

| Use case | Approach |
|----------|----------|
| **Inventory & drift** | Scheduled NITRO/Next-Gen GET vs Git-desired state |
| **Certificate expiry** | Monitor `sslcertkey` expirations; alert before outage |
| **WAF tuning** | Export App Firewall logs → SIEM; human-approved relaxations |
| **API protection** | Import OpenAPI spec → REST schema validation on profile (14.1+) |
| **StyleBooks / Terraform / Ansible** | Citrix-supported IaC instead of ad-hoc scripts |

**Do not** let an LLM push unreviewed `set appfw` or `rm` commands to production. Wrong **Action** parameters (`-SQLInjectionAction`, not `-SQLInjection ON`) can block all traffic.

## Where AI helps (safely)

AI assistants (including tools like **JPilot**) are useful when they:

1. **Search documented syntax** (memory files, OpenAPI, NITRO schemas) before suggesting changes
2. **Propose** configs for human review
3. **Execute** only after explicit approval on non-production or change windows
4. **Never embed secrets** in prompts

Example workflow (conceptual):

```python
# 1. Pull current profile (read-only)
# 2. Compare to desired template in Git
# 3. Ask LLM to explain diffs — not to invent CLI
# 4. Apply via pipeline with tests + rollback
```

For **WAF**, pair automation with the **learning feature** and staged `log learn` before `block`.

## What this article does not claim

There is no universal “70% less admin time” guarantee—outcomes depend on maturity, scope, and process. Automation ROI comes from **fewer outages**, **consistent baselines**, and **faster audits**, not from auto-generating profiles from OpenAPI specs without validation.

## Related Nexxus offerings

- JPilot-style **guided change** with approval gates
- **OWASP-aligned WAF** rollout (see our WAF article)
- **NITRO/Next-Gen** pipeline design and CI integration
"""
        + FOOTER,
        "tags": ["NetScaler", "NITRO API", "Python", "Automation", "AI", "DevOps"],
        "read_time": 9,
    },
    "4": {
        "title": "Multicloud Application Delivery with NetScaler on AWS and Azure",
        "excerpt": (
            "How NetScaler VPX on AWS and Azure, NetScaler Console agents, and consistent "
            "ADC policies complement—not replace—each cloud's native security controls."
        ),
        "content": DISCLAIMER
        + r"""# Multicloud Application Delivery with NetScaler on AWS and Azure

Most enterprises run **AWS**, **Azure**, and on-premises together. Each cloud offers native load balancing and WAF (ALB, AWS WAF, Application Gateway, Front Door). **NetScaler ADC** is still valuable when you need **the same delivery and security model everywhere**—especially if teams already standardize on NetScaler for Gateway, GSLB, App Firewall, and observability.

References: [NetScaler Console overview](https://docs.netscaler.com/en-us/netscaler-console-service/overview.html), [Provision VPX on AWS](https://docs.netscaler.com/en-us/netscaler-console-service/hybrid-multi-cloud-deployments/provisioning-vpx-aws.html), [VPX on Azure (Tech Zone)](https://community.citrix.com/tech-zone/build/deployment-guides/netscaler-adc-azure-gslb/).

## Clarify the architecture goal

NetScaler is **not** a magic “single pane” that replaces AWS and Azure security services. Typical goals:

- **Consistent L4–L7** policies (LB, SSL, rewrite, responder, App Firewall)
- **Same Gateway / IdP integration** in every region
- **Central lifecycle management** via **NetScaler Console** (formerly ADM) with **per-site agents**

```
[Users]
   → [Regional NetScaler VPX — AWS or Azure]
         → [App tiers in VPC/VNet]
[NetScaler Console] ←→ [Agent in each site/VPC] ←→ [Managed ADC instances]
```

## AWS: VPX placement

Common pattern (adjust for your security zones):

- Deploy **NetScaler VPX** from **AWS Marketplace** (BYOL or subscription licenses)
- Use **management**, **client**, and **server** subnets (three-subnet model per Citrix guidance)
- Terminate **TLS** on NetScaler; apply **App Firewall** and **rate limiting** before backends
- Optional: ALB in front or behind depending on architecture—document traffic flow to avoid **double NAT** or bypass paths

**NetScaler Console** can **provision** VPX via an **agent** in the VPC with multi-AZ options.

## Azure: VPX placement

- Deploy VPX from **Azure Marketplace** (standalone or HA ARM templates)
- **Azure Front Door** or Application Gateway may sit **in front** for global edge + DDoS; NetScaler often handles **regional** advanced ADC features (GSLB, complex policies, Gateway)
- Same three-subnet discipline applies inside the VNet

## Unified management (what Console actually does)

**NetScaler Console service** provides:

- Inventory and health of MPX/VPX/SDX/Gateway instances
- **Configuration jobs**, certificates, backups (feature-dependent)
- **StyleBooks** for repeatable deployments
- **Agents** that proxy between cloud/on-prem instances and the SaaS console—install an agent **per site/VPC**

It does **not** automatically merge AWS WAF and Azure WAF rules into one policy language—you still coordinate **cloud-native** and **NetScaler** controls explicitly.

## Security layering (honest)

| Layer | AWS example | Azure example | NetScaler role |
|-------|-------------|---------------|----------------|
| Edge DDoS | Shield / CloudFront | Front Door DDoS | Regional ADC, WAF, bot mgmt |
| L7 WAF | AWS WAF on ALB | App Gateway WAF | App Firewall + API schema validation |
| Identity | IAM, Cognito | Entra ID | Gateway + SAML/OIDC to Entra/Okta |
| Network | Security groups | NSGs | Segmentation in VPC/VNet design |

Pick **one primary L7 inspection point** per app path to avoid conflicting breaks.

## Identity across clouds

A consistent pattern:

- **Entra ID** (or Okta) as IdP
- **NetScaler Gateway** VIP per region or global GSLB to regional Gateway
- Same **SAML** server definitions (adjusted for regional URLs/certs)

See our Zero Trust article for SAML/nFactor cautions.

## Multicloud checklist

- [ ] Document traffic flow (no uninspected bypass)
- [ ] Standardize **SSL profiles** and cipher suites (consider **hybrid PQC** on internet-facing VIPs)
- [ ] Deploy **Console agents** per VPC/VNet/site
- [ ] Use **StyleBooks/Git** for baseline configs
- [ ] Align licensing (pooled/flexed vs per-instance marketplace)
- [ ] Run **DR tests** per cloud region

## What we implement for customers

Nexxus designs **landing zones**, **ADC high availability**, **WAF baselines**, and **Console onboarding**—not just marketplace installs.
"""
        + FOOTER,
        "tags": ["Multicloud", "AWS", "Azure", "NetScaler", "NetScaler Console", "VPX"],
        "read_time": 11,
    },
    "6": {
        "title": "NetScaler Hybrid Post-Quantum Cryptography: Quantum-Ready TLS",
        "slug": "netscaler-hybrid-post-quantum-cryptography",
        "excerpt": (
            "NetScaler supports hybrid PQC (X25519_MLKEM768) on the TLS front end with enhanced "
            "SSL profiles—mitigating harvest-now-decrypt-later risk while staying browser-compatible."
        ),
        "content": DISCLAIMER
        + r"""# NetScaler Hybrid Post-Quantum Cryptography: Quantum-Ready TLS

Quantum computers threaten **classical key exchange** (RSA, finite-field DH, and eventually elliptic-curve schemes at scale). Attackers can **record encrypted traffic today** and decrypt later—**harvest now, decrypt later (HNDL)**. Regulators and standards bodies are pushing **post-quantum cryptography (PQC)** migration on aggressive timelines.

**NetScaler** addresses this on the **TLS front end** with **hybrid post-quantum cryptography**: combine a classical algorithm with a **quantum-resistant** key encapsulation so you keep interoperability while improving future security.

Official reference: [Support for Hybrid Post-Quantum Cryptography on the front end](https://docs.netscaler.com/en-us/citrix-adc/current-release/ssl/hybrid-pqc.html).

## What NetScaler implements

| Item | Detail |
|------|--------|
| **Hybrid curve** | **X25519_MLKEM768** (X25519 + ML-KEM-768), aligned with browser support (e.g. TLS 1.3 code point 0x11EC) |
| **Scope** | **Front-end** TLS key exchange on enhanced SSL profiles |
| **Benefit** | HNDL risk reduction while maintaining compatibility with major browsers (Chrome, Firefox, Edge) |
| **Availability** | Hybrid PQC in current **14.1** releases (e.g. **14.1.51+** per Citrix announcements); verify your build release notes |

Hybrid means you do **not** rely on PQC alone—you combine proven classical ECDH with ML-KEM so negotiation stays practical during the transition.

## Prerequisites

1. **Enhanced SSL profile** — hybrid PQC is **not** available on legacy non-enhanced SSL profiles. Migrate configs using Citrix guidance: [Migrate to enhanced SSL profile](https://docs.netscaler.com/en-us/citrix-adc/current-release/ssl/migrate-ssl-profile.html).
2. **TLS 1.3** on front-end entities where required for modern curves (including X25519).
3. **Browser/client support** — confirm clients used by your workforce support hybrid PQC; monitor fallback behavior in pilot.

## Enable hybrid PQC (CLI)

Append the hybrid curve to an existing enhanced SSL profile:

```
bind ssl profile prod_ssl_frontend -eccCurveName X25519_MLKEM768
save ns config
```

To **rebind all ECC curves** with hybrid PQC prioritized first:

```
bind ssl profile prod_ssl_frontend -eccCurveName ALL
save ns config
```

Bind the profile to your **SSL virtual server** or use SSL profile settings at the vserver level per your deployment standard.

### GUI path

1. **Traffic Management → SSL → SSL Profiles**
2. Edit the **enhanced** profile → **Advanced Settings → ECC Curve**
3. Bind **X25519_MLKEM768** or **ALL** (puts hybrid curve at top of preference list)

## What is *not* covered by this single feature

- **Back-end** TLS to origin servers may still use classical curves—plan PQC end-to-end where stacks support it.
- **Certificate signatures** (e.g. RSA/ECDSA cert keys) are separate from **key exchange** hybrid PQC—inventory algorithms across PKI.
- **Data at rest**, **VPN payloads**, and **management channels** need their own crypto roadmaps.
- **Quantum-safe** does not replace **patching**, **WAF**, or **access control**.

## Suggested migration phases

| Phase | Activity |
|-------|----------|
| **Discover** | Inventory VIPs, SSL profiles, cipher suites, and cert algorithms |
| **Lab** | Enable `X25519_MLKEM768` on a non-production enhanced profile; test browsers and API clients |
| **Pilot** | Internet-facing apps with monitoring for handshake failures |
| **Expand** | Roll region-by-region; document fallback if legacy clients fail |
| **Govern** | Map to organizational PQC policy (e.g. NIST migration guidance) |

Citrix public guidance discusses **NIST-aligned** hybrid approaches and phased customer timelines—treat dates as **planning anchors**, not substitutes for your compliance team’s schedule.

## Cipher and ECDH context

NetScaler continues to support **ECDHE** cipher families and curves (P-256, P-384, X25519, etc.) on front-end and back-end entities. Hybrid PQC **adds** a preferred modern key-exchange path; review [ECDHE ciphers](https://docs.netscaler.com/en-us/citrix-adc/current-release/ssl/ciphers-available-on-the-citrix-ADC-appliances/ecdhe-ciphers.html) when tuning full cipher groups.

## Quick validation

- Confirm profile type: **enhanced**
- `show ssl profile prod_ssl_frontend` — ECC curve bindings include **X25519_MLKEM768**
- Client test: TLS 1.3 handshake negotiates hybrid group (browser dev tools or `openssl s_client` with supported build)
- Monitor SSL errors and session establishment rates after enablement

## How Nexxus can help

PQC is a **program**, not a one-line CLI change. We help with **SSL profile migration**, **cipher baselines**, **Gateway and app VIP testing**, and coordination with **Entra/Okta**-facing services so you do not break access during the transition.
"""
        + FOOTER,
        "category": "Security",
        "tags": ["NetScaler", "PQC", "Post-Quantum", "TLS", "SSL", "Cryptography"],
        "date": "2026-06-02",
        "read_time": 8,
            "featured": True,
        "cover_color": "#6B5CE7",
    },
}

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "blog_posts.json"


def patch_owasp(post: dict, footer: str) -> None:
    disclaimer = DISCLAIMER
    content = post["content"]
    if disclaimer.strip() not in content:
        content = disclaimer + "\n" + content
    if footer.strip() not in content:
        content = content.rstrip() + footer
    post["content"] = content


def main():
    posts = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in posts}

    # Post 1 — disclaimer + footer only
    if "1" in POSTS and "1" in by_id:
        patch_owasp(by_id["1"], POSTS["1"]["footer"])

    # Posts 2–4 — full replace
    for pid in ("2", "3", "4"):
        if pid not in POSTS or pid not in by_id:
            continue
        spec = POSTS[pid]
        post = by_id[pid]
        post["title"] = spec["title"]
        post["excerpt"] = spec["excerpt"]
        post["content"] = spec["content"]
        post["tags"] = spec["tags"]
        post["read_time"] = spec["read_time"]

    # Post 6 — new article
    if "6" in POSTS:
        spec = POSTS["6"]
        new_post = {
            "id": "6",
            "slug": spec["slug"],
            "title": spec["title"],
            "excerpt": spec["excerpt"],
            "content": spec["content"],
            "category": spec["category"],
            "tags": spec["tags"],
            "author": "Juan Pablo Otalvaro",
            "author_role": "Principal Cloud & Security Architect",
            "date": spec["date"],
            "read_time": spec["read_time"],
            "featured": spec["featured"],
            "cover_color": spec["cover_color"],
        }
        # Insert after JPilot (id 5) if present, else append
        if any(p["id"] == "6" for p in posts):
            posts = [new_post if p["id"] == "6" else p for p in posts]
        else:
            inserted = False
            out = []
            for p in posts:
                out.append(p)
                if p["id"] == "5":
                    out.append(new_post)
                    inserted = True
            if not inserted:
                out.append(new_post)
            posts = out

    DATA_FILE.write_text(
        json.dumps(posts, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Updated blog_posts.json ({len(posts)} posts)")


if __name__ == "__main__":
    main()
