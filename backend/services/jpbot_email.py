"""HTML email templates for JPbot enquiries."""

from __future__ import annotations

from html import escape

from models.chat import ChatProfile

_BRAND_PRIMARY = "#007BA7"
_BRAND_PRIMARY_LIGHT = "#00A8E0"
_BRAND_DARK = "#1C1C1E"
_BRAND_GREY = "#6B7280"
_BRAND_LIGHT_BG = "#F5F5F7"
_CRITICAL = "#DC2626"
_HIGH = "#EA580C"


def _badge_html(criticality: str) -> str:
    c = criticality.lower()
    if "critical" in c:
        bg, fg = _CRITICAL, "#FFFFFF"
    elif "high" in c:
        bg, fg = _HIGH, "#FFFFFF"
    else:
        bg, fg = _BRAND_PRIMARY, "#FFFFFF"
    label = escape(criticality)
    return (
        f'<span style="display:inline-block;padding:4px 10px;border-radius:6px;'
        f'font-size:11px;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;'
        f'background:{bg};color:{fg};">{label}</span>'
    )


def _row(label: str, value: str, *, last: bool = False) -> str:
    border = "" if last else "border-bottom:1px solid #E5E7EB;"
    return f"""
    <tr>
      <td style="padding:10px 0;{border}width:140px;color:{_BRAND_GREY};font-size:13px;font-weight:600;vertical-align:top;">{escape(label)}</td>
      <td style="padding:10px 0;{border}color:{_BRAND_DARK};font-size:14px;line-height:1.5;">{value}</td>
    </tr>
    """


def _section_title(text: str) -> str:
    return (
        f'<p style="margin:24px 0 10px;font-size:11px;font-weight:700;letter-spacing:0.1em;'
        f'text-transform:uppercase;color:{_BRAND_GREY};">{escape(text)}</p>'
    )


def _bullet_list(items: list[str]) -> str:
    if not items:
        return f'<p style="margin:0;color:#9CA3AF;font-size:14px;">—</p>'
    lis = "".join(
        f'<li style="margin:0 0 8px;color:#374151;font-size:14px;line-height:1.6;">{escape(i)}</li>'
        for i in items
        if i.strip()
    )
    return f'<ul style="margin:0;padding-left:20px;">{lis}</ul>'


def _paragraphs(text: str) -> str:
    if not text.strip():
        return f'<p style="margin:0;color:#9CA3AF;">—</p>'
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    return "".join(
        f'<p style="margin:0 0 14px;color:#374151;font-size:14px;line-height:1.75;">{escape(p)}</p>'
        for p in parts
    )


def _transcript_html(transcript: str) -> str:
    safe = escape(transcript)
    return (
        f'<div style="background:#F9FAFB;border:1px solid #E5E7EB;border-radius:8px;'
        f'padding:14px 16px;font-family:Consolas,\'Courier New\',monospace;font-size:12px;'
        f'line-height:1.6;color:#4B5563;white-space:pre-wrap;max-height:320px;overflow:auto;">{safe}</div>'
    )


def build_team_jpbot_html(
    profile: ChatProfile,
    *,
    situation: str,
    pain_points: list[str],
    urgency: str,
    next_steps: list[str],
    transcript: str,
) -> str:
    name = escape(profile.name)
    email = escape(str(profile.email))
    company = escape(profile.company) if profile.company else "—"
    service = escape(profile.service)
    techs = ", ".join(profile.technologies)
    if profile.technology_other:
        techs = f"{techs}, Other: {escape(profile.technology_other)}" if techs else f"Other: {escape(profile.technology_other)}"
    techs = techs or "—"
    version = escape(profile.platform_version) if profile.platform_version else "—"
    model = escape(profile.platform_model) if profile.platform_model else "—"
    users = escape(profile.users_affected) if profile.users_affected else "—"

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <body style="margin:0;padding:0;background:{_BRAND_LIGHT_BG};font-family:'Segoe UI',Arial,sans-serif;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{_BRAND_LIGHT_BG};padding:32px 16px;">
        <tr><td align="center">
          <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;background:#FFFFFF;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">
            <tr>
              <td style="background:linear-gradient(135deg,{_BRAND_DARK} 0%,#2E2E32 100%);padding:28px 32px;">
                <p style="margin:0 0 8px;font-size:11px;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:{_BRAND_PRIMARY_LIGHT};">JPbot Enquiry</p>
                <h1 style="margin:0 0 12px;font-size:22px;font-weight:700;color:#FFFFFF;">{name}</h1>
                {_badge_html(profile.criticality)}
              </td>
            </tr>
            <tr><td style="padding:32px;">
              {_section_title("Contact")}
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:8px;">
                {_row("Name", name)}
                {_row("Email", f'<a href="mailto:{email}" style="color:{_BRAND_PRIMARY};text-decoration:none;">{email}</a>')}
                {_row("Company", company)}
                {_row("Service interest", service, last=True)}
              </table>

              {_section_title("Technical context")}
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                {_row("Criticality", escape(profile.criticality))}
                {_row("Users affected", users)}
                {_row("Technologies", techs)}
                {_row("Platform version", version)}
                {_row("Platform model", model, last=True)}
              </table>

              {_section_title("Situation")}
              {_paragraphs(situation)}

              {_section_title("Pain points")}
              {_bullet_list(pain_points)}

              {_section_title("Urgency")}
              {_paragraphs(urgency)}

              {_section_title("Suggested next steps")}
              {_bullet_list(next_steps)}

              {_section_title("Conversation transcript")}
              {_transcript_html(transcript)}

              <p style="margin:24px 0 0;font-size:12px;color:#9CA3AF;">Reply directly to the visitor — Reply-To is set to their email.</p>
            </td></tr>
          </table>
          <p style="margin:16px 0 0;font-size:11px;color:#9CA3AF;">Submitted via JPbot · nexxus-tech.com</p>
        </td></tr>
      </table>
    </body>
    </html>
    """


def build_visitor_jpbot_html(
    profile: ChatProfile,
    *,
    visitor_summary: str,
    service: str,
    criticality: str,
) -> str:
    first = escape(profile.name.split()[0] if profile.name.strip() else "there")
    summary_html = _paragraphs(visitor_summary)
    crit_badge = _badge_html(criticality)

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <body style="margin:0;padding:0;background:{_BRAND_LIGHT_BG};font-family:'Segoe UI',Arial,sans-serif;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{_BRAND_LIGHT_BG};padding:40px 16px;">
        <tr><td align="center">
          <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;background:#FFFFFF;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">
            <tr><td style="height:4px;background:linear-gradient(90deg,{_BRAND_PRIMARY},{_BRAND_PRIMARY_LIGHT});"></td></tr>
            <tr><td style="padding:40px 40px 24px;text-align:center;">
              <p style="margin:0 0 8px;font-size:11px;font-weight:700;letter-spacing:0.25em;text-transform:uppercase;color:{_BRAND_PRIMARY};">Nexxus Tech</p>
              <h1 style="margin:0;font-size:24px;font-weight:700;color:{_BRAND_DARK};">We received your enquiry</h1>
            </td></tr>
            <tr><td style="padding:0 40px 32px;">
              <p style="margin:0 0 20px;font-size:16px;line-height:1.75;color:#374151;">Hi {first},</p>
              <p style="margin:0 0 24px;font-size:15px;line-height:1.75;color:#4B5563;">
                Thank you for speaking with <strong>JPbot</strong>. Here is a quick summary of what you shared:
              </p>
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{_BRAND_LIGHT_BG};border-radius:10px;margin-bottom:24px;">
                <tr><td style="padding:20px 24px;">
                  <p style="margin:0 0 10px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:{_BRAND_GREY};">Your request</p>
                  {summary_html}
                  <p style="margin:16px 0 8px;font-size:12px;color:{_BRAND_GREY};"><strong>Service:</strong> {escape(service)}</p>
                  <p style="margin:0;font-size:12px;color:{_BRAND_GREY};"><strong>Priority:</strong> {crit_badge}</p>
                </td></tr>
              </table>
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{_BRAND_LIGHT_BG};border-radius:8px;margin-bottom:24px;">
                <tr><td style="padding:20px 24px;">
                  <p style="margin:0 0 8px;font-size:11px;font-weight:700;text-transform:uppercase;color:{_BRAND_GREY};">What happens next</p>
                  <p style="margin:0;font-size:14px;line-height:1.65;color:#374151;">
                    A Nexxus specialist will review your enquiry and respond within <strong>one business day</strong>
                    (sooner for critical issues). If anything is missing, we may reach out with a brief follow-up.
                  </p>
                </td></tr>
              </table>
              <p style="margin:0;font-size:15px;color:#4B5563;">— The Nexxus Tech Team</p>
            </td></tr>
            <tr><td style="background:{_BRAND_DARK};padding:24px 40px;text-align:center;">
              <p style="margin:0;font-size:13px;color:#E5E5E5;">
                <a href="mailto:contact@nexxus-tech.com" style="color:{_BRAND_PRIMARY_LIGHT};text-decoration:none;">contact@nexxus-tech.com</a>
              </p>
            </td></tr>
          </table>
        </td></tr>
      </table>
    </body>
    </html>
    """


def build_team_plain_text(
    profile: ChatProfile,
    *,
    situation: str,
    pain_points: list[str],
    urgency: str,
    next_steps: list[str],
    transcript: str,
) -> str:
    techs = ", ".join(profile.technologies)
    if profile.technology_other:
        techs = f"{techs}, Other: {profile.technology_other}" if techs else f"Other: {profile.technology_other}"
    lines = [
        f"JPbot enquiry from {profile.name} <{profile.email}>",
        f"Criticality: {profile.criticality}",
        f"Service: {profile.service}",
        f"Users affected: {profile.users_affected or '—'}",
        f"Technologies: {techs or '—'}",
        f"Version: {profile.platform_version or '—'}",
        f"Model: {profile.platform_model or '—'}",
        "",
        "SITUATION",
        situation,
        "",
        "PAIN POINTS",
        *[f"- {p}" for p in pain_points],
        "",
        "URGENCY",
        urgency,
        "",
        "NEXT STEPS",
        *[f"- {s}" for s in next_steps],
        "",
        "TRANSCRIPT",
        transcript,
    ]
    return "\n".join(lines)
