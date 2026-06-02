#!/usr/bin/env python3
"""Rewrite OWASP / NetScaler WAF blog post (id 1) with accurate technical content."""
import json
from pathlib import Path

CONTENT = r"""# Protecting Against the OWASP Top 10 with NetScaler Web App Firewall

The **NetScaler Web App Firewall** (App Firewall, `appfw`) is the application-security layer on NetScaler ADC. It combines **security checks** (deep inspection of requests and responses), **signatures** (known attack patterns), and optional **adaptive learning** to reduce false positives. It is not a substitute for secure coding—but it is a strong control at the edge when configured using Citrix best practices.

This guide maps the current **[OWASP Top 10:2025](https://owasp.org/Top10/2025/en/)** to what NetScaler can realistically enforce in production, with **correct CLI examples** and a staged rollout model aligned with the [NetScaler Web App Firewall security recommendations](https://docs.netscaler.com/en-us/netscaler-adc-secure-deployment/other-features/netscaler-web-app-firewall-security-recommendations).

> NetScaler is a trademark of Cloud Software Group. OWASP Top 10 is maintained by the OWASP Foundation.

## Understand what a WAF can and cannot fix

| OWASP Top 10:2025 | Primarily addressed by App Firewall? | How NetScaler helps |
|-------------------|--------------------------------------|---------------------|
| **A01 – Broken Access Control** | Partially | `startURL` / `denyURL`, forceful-browsing controls; **not** a replacement for application authorization logic |
| **A02 – Security Misconfiguration** | Partially | Default-deny policies, RFC profiles (`APPFW_RFC_BLOCK`), hardened global settings |
| **A03 – Software Supply Chain Failures** | No | Requires SDLC, dependency scanning, artifact signing—not edge WAF |
| **A04 – Cryptographic Failures** | Partially | SSL/TLS on ADC, HSTS, cipher control; app-level crypto must still be correct |
| **A05 – Injection** | Yes | HTML/JSON **SQL injection**, **command injection**, XSS checks, signatures |
| **A06 – Insecure Design** | No | Threat modeling and architecture—WAF mitigates abuse, not design flaws |
| **A07 – Authentication Failures** | Partially | Bot management, rate limits; primary auth remains on the app/IdP |
| **A08 – Software or Data Integrity Failures** | Partially | CSRF form tagging, cookie consistency, response-side checks where enabled |
| **A09 – Logging & Alerting Failures** | Partially | `log` / `stats` actions, verbose WAF logs, SIEM export—**alerting** must be designed |
| **A10 – Mishandling of Exceptional Conditions** | Partially | Block verbose errors to clients; custom error objects on the profile |

**Takeaway:** enable App Firewall for **injection, XSS, protocol abuse, and API schema violations**; pair it with **secure development**, **access control in code**, and **operational monitoring**.

## How NetScaler App Firewall is structured

Three objects work together:

1. **Profile** (`appfw profile`) — which security checks run and what actions apply (`block`, `log`, `learn`, `stats`, or `none`).
2. **Policy** (`appfw policy`) — which traffic is inspected (hostname, URL, content type, etc.).
3. **Binding** — attach the policy to **Global**, a **CS virtual server**, or other supported bind points so traffic actually hits the profile.

Signatures are configured in a **signatures object** and **associated with the profile**—they are not toggled with invalid `-SQLInjection ON` style parameters.

## Staged rollout (recommended by Citrix)

Do not enable every check on day one. Use tiers:

**Tier 1 — Baseline**

- Buffer overflow, **HTML SQL injection**, **HTML cross-site scripting**
- **Start URL** (anti–forceful browsing) where the app has defined entry points
- **Field format** checks for predictable form fields
- Actions: start with `log stats learn`, move to `block` after tuning

**Tier 2 — Signatures**

- Attach a signatures object; enable **only categories relevant to your stack** (1,300+ rules exist—enabling all increases false positives and CPU use).

**Tier 3 — Advanced (sessionized checks)**

- CSRF form tagging, cookie consistency, field consistency on forms that need it—these use more memory/CPU because the appliance sessionizes clients.

Use the **learning feature** in staging (or carefully on production) to generate relaxations for legitimate traffic before you enforce blocking.

## Correct CLI examples

### Create and tune a profile

```
add appfw profile prod_waf -defaults basic
set appfw profile prod_waf -type HTML
set appfw profile prod_waf -SQLInjectionAction block log learn stats
set appfw profile prod_waf -crossSiteScriptingAction block log learn stats
set appfw profile prod_waf -bufferOverflowAction block log stats
set appfw profile prod_waf -startURLAction block log learn stats
set appfw profile prod_waf -fieldFormatAction block log learn stats
set appfw profile prod_waf -VerboseLogLevel pattern
save ns config
```

**Common mistakes to avoid**

- `-SQLInjection ON` and `-crossSiteScripting ON` are **not valid**—use `-SQLInjectionAction` and `-crossSiteScriptingAction` with one or more actions (`block`, `log`, `learn`, `stats`, `none`).
- Creating a profile with only `-type HTML` on `add`—use `-defaults basic|advanced|core` on `add`, then `set -type HTML` (or `HTML XML`).

Official example from Citrix documentation:

```
set appfw profile pr-basic -crossSiteScriptingAction block -SQLInjectionAction block
```

### Policy, bind, and default deny

```
add appfw policy prod_waf_pol "HTTP.REQ.HOSTNAME.EQ(\"www.example.com\")" prod_waf
bind appfw global prod_waf_pol 100

set appfw settings -defaultProfile appfw_block
set appfw settings -sessionCookieName "ns_waf_sid_prod"
save ns config
```

For a **catch-all deny** policy evaluated last, see Citrix secure deployment: `default_deny_profile` / `default_deny_policy` bound at global priority **after** your allow policies.

Deploy in **two-arm mode** when possible so traffic cannot bypass the ADC.

## JSON, REST, and OpenAPI (API security)

Modern APIs need more than HTML checks. NetScaler supports:

- **JSON SQL injection** and **JSON XSS** security checks on App Firewall profiles
- **REST API schema validation** by importing **OpenAPI (Swagger 2.0, OAS 3.x)** and binding the spec to the profile—traffic that does not match the schema can be **blocked or logged** (`restAction`)
- **gRPC** validation via **ProtoBuf** specs (`grpcAction`)

Workflow: import the API specification → assign to the profile → enable **REST API Schema Validation** under Security Checks → bind the profile to the virtual server. Use **relaxation rules** for known false positives.

Reference: [API specification validation](https://docs.netscaler.com/en-us/citrix-adc/current-release/api-security/api_schema_validation).

## Bot management (separate from App Firewall)

**Bot Management** is a distinct feature set (bot profiles, signatures, policies) bound to a **load balancing virtual server**, not configured with a one-line `add bot policy ... -rule true` shortcut.

Typical flow:

1. Create a **bot profile** and enable the detection categories you need (fingerprinting, device detection, etc.).
2. Create **bot policies** that reference the profile and match traffic expressions.
3. **Bind** bot policies to the `lb vserver` with appropriate priority.

Use bot management for **automated abuse**, credential stuffing, and scrapers—alongside App Firewall for payload attacks.

## Rate limiting (Responder—not the WAF profile)

Per-IP or per-URL **rate limiting** is implemented with **limit identifiers**, **stream selectors**, and **Responder** (or other advanced policies)—not by toggling a checkbox inside the App Firewall profile.

Example pattern:

```
add ns limitIdentifier api_rate -threshold 100 -timeSlice 1000 -mode request_rate
add responder action api_throttle respondwith "\"429 Too Many Requests\""
add responder policy api_rate_pol "sys.check_limit(\"api_rate\")" api_throttle
bind lb vserver web_vs -policyName api_rate_pol -priority 110
save ns config
```

Use rate limiting for **A07 (authentication abuse)** and flood scenarios; use App Firewall for **payload and protocol violations**.

## Production checklist (accurate)

- [ ] Enable App Firewall globally and bind policies to the correct **CS/LB/global** bind point
- [ ] Start with **basic** profile defaults; tighten in tiers
- [ ] Use **`learn`** before full **`block`** on XSS/SQLi-heavy sites
- [ ] Keep **`APPFW_RFC_BLOCK`** as the RFC profile unless you have a documented reason to change it
- [ ] Configure **`appfw_block`** default profile for unmatched traffic
- [ ] Associate **signatures** selectively—not “enable everything”
- [ ] Bind **startURL** / **denyURL** for forceful browsing (A01 partial control)
- [ ] For APIs: **OpenAPI import** + REST schema validation + JSON security checks
- [ ] Add **bot policies** on the vserver for automated threats
- [ ] Add **Responder rate limits** for auth/login and expensive endpoints
- [ ] Enable **verbose WAF logging** during tuning; forward logs to SIEM with **alerting** (A09)
- [ ] Run `save ns config` after changes

## Conclusion

NetScaler Web App Firewall is one of the most capable ADC-integrated WAF platforms—when it is configured with **realistic expectations**, **correct action parameters**, and a **staged rollout**. Map OWASP risks to the right control: App Firewall for injection and protocol abuse, bot management for automated clients, rate limiting for floods, and secure development for access control and design.

*Nexxus Tech designs and tunes NetScaler WAF deployments for production—including OWASP-aligned profiles, API schema validation, and false-positive reduction. [Contact us](/contact) for a review of your environment.*"""

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "blog_posts.json"

def main():
    posts = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    for post in posts:
        if post.get("id") == "1":
            post["title"] = "Protecting Against the OWASP Top 10 with NetScaler Web App Firewall"
            post["excerpt"] = (
                "Accurate guide to NetScaler Web App Firewall and OWASP Top 10:2025—"
                "correct appfw CLI, staged rollout, signatures, OpenAPI schema validation, "
                "bot management, and Responder rate limiting."
            )
            post["content"] = CONTENT.strip()
            post["tags"] = [
                "NetScaler",
                "Web App Firewall",
                "OWASP",
                "WAF",
                "API Security",
                "Security",
            ]
            post["read_time"] = 10
            break
    else:
        raise SystemExit("Post id 1 not found")
    DATA_FILE.write_text(
        json.dumps(posts, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print("Updated OWASP WAF blog post")


if __name__ == "__main__":
    main()
