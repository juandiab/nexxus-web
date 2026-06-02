import os
from html import escape

import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import APIRouter, HTTPException

from models.contact import ContactRequest, ContactResponse

router = APIRouter()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
CONTACT_TO = os.getenv("CONTACT_TO", "contact@nexxus-tech.com")
CONTACT_FROM = os.getenv("CONTACT_FROM", SMTP_USER or CONTACT_TO)

_BRAND_PRIMARY = "#007BA7"
_BRAND_PRIMARY_LIGHT = "#00A8E0"
_BRAND_DARK = "#1C1C1E"
_BRAND_GREY = "#6B7280"
_BRAND_LIGHT_BG = "#F5F5F7"

SUCCESS_MESSAGE = (
    "Thank you — your message has been received. "
    "A confirmation has been sent to your inbox; we will be in touch within one business day."
)


def _build_team_notification_html(data: ContactRequest) -> str:
    name = escape(data.name)
    email = escape(data.email)
    company = escape(data.company) if data.company else "—"
    service = escape(data.service) if data.service else "—"
    message = escape(data.message)
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <body style="margin:0;padding:0;background:{_BRAND_LIGHT_BG};font-family:'Segoe UI',Arial,sans-serif;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{_BRAND_LIGHT_BG};padding:32px 16px;">
        <tr>
          <td align="center">
            <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;background:#FFFFFF;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">
              <tr>
                <td style="background:linear-gradient(135deg,{_BRAND_DARK} 0%,#2E2E32 100%);padding:28px 32px;">
                  <p style="margin:0 0 6px;font-size:11px;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:{_BRAND_PRIMARY_LIGHT};">Website Enquiry</p>
                  <h1 style="margin:0;font-size:22px;font-weight:700;color:#FFFFFF;">New message from {name}</h1>
                </td>
              </tr>
              <tr>
                <td style="padding:32px;">
                  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:24px;">
                    <tr>
                      <td style="padding:10px 0;border-bottom:1px solid #E5E7EB;width:130px;color:{_BRAND_GREY};font-size:13px;font-weight:600;">Name</td>
                      <td style="padding:10px 0;border-bottom:1px solid #E5E7EB;color:{_BRAND_DARK};font-size:14px;">{name}</td>
                    </tr>
                    <tr>
                      <td style="padding:10px 0;border-bottom:1px solid #E5E7EB;color:{_BRAND_GREY};font-size:13px;font-weight:600;">Email</td>
                      <td style="padding:10px 0;border-bottom:1px solid #E5E7EB;font-size:14px;"><a href="mailto:{email}" style="color:{_BRAND_PRIMARY};text-decoration:none;">{email}</a></td>
                    </tr>
                    <tr>
                      <td style="padding:10px 0;border-bottom:1px solid #E5E7EB;color:{_BRAND_GREY};font-size:13px;font-weight:600;">Company</td>
                      <td style="padding:10px 0;border-bottom:1px solid #E5E7EB;color:{_BRAND_DARK};font-size:14px;">{company}</td>
                    </tr>
                    <tr>
                      <td style="padding:10px 0;color:{_BRAND_GREY};font-size:13px;font-weight:600;">Service</td>
                      <td style="padding:10px 0;color:{_BRAND_DARK};font-size:14px;">{service}</td>
                    </tr>
                  </table>
                  <p style="margin:0 0 8px;font-size:12px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:{_BRAND_GREY};">Message</p>
                  <div style="background:{_BRAND_LIGHT_BG};border-left:4px solid {_BRAND_PRIMARY};border-radius:0 8px 8px 0;padding:16px 20px;color:#374151;font-size:14px;line-height:1.7;white-space:pre-line;">{message}</div>
                  <p style="margin:24px 0 0;font-size:12px;color:#9CA3AF;">Reply directly to this sender — Reply-To is set to their address.</p>
                </td>
              </tr>
            </table>
            <p style="margin:16px 0 0;font-size:11px;color:#9CA3AF;">Sent via nexxus-tech.com contact form</p>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """


def _build_auto_reply_html(data: ContactRequest) -> str:
    first_name = escape(data.name.split()[0] if data.name.strip() else "there")
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <body style="margin:0;padding:0;background:{_BRAND_LIGHT_BG};font-family:'Segoe UI',Arial,sans-serif;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{_BRAND_LIGHT_BG};padding:40px 16px;">
        <tr>
          <td align="center">
            <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;background:#FFFFFF;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">
              <tr>
                <td style="height:4px;background:linear-gradient(90deg,{_BRAND_PRIMARY},{_BRAND_PRIMARY_LIGHT});"></td>
              </tr>
              <tr>
                <td style="padding:40px 40px 24px;text-align:center;">
                  <p style="margin:0 0 8px;font-size:11px;font-weight:700;letter-spacing:0.25em;text-transform:uppercase;color:{_BRAND_PRIMARY};">Nexxus Tech</p>
                  <h1 style="margin:0;font-size:26px;font-weight:700;color:{_BRAND_DARK};line-height:1.3;">Thank you for reaching out</h1>
                </td>
              </tr>
              <tr>
                <td style="padding:0 40px 32px;">
                  <p style="margin:0 0 20px;font-size:16px;line-height:1.75;color:#374151;">Dear {first_name},</p>
                  <p style="margin:0 0 20px;font-size:15px;line-height:1.75;color:#4B5563;">
                    We have received your enquiry and appreciate you taking the time to contact
                    <strong style="color:{_BRAND_DARK};">Nexxus Tech</strong>.
                    A member of our consulting team will review your message and respond within
                    <strong>one business day</strong>.
                  </p>
                  <p style="margin:0 0 28px;font-size:15px;line-height:1.75;color:#4B5563;">
                    Should your matter be urgent, please reply to this email and note the urgency —
                    we prioritise security-related engagements accordingly.
                  </p>
                  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{_BRAND_LIGHT_BG};border-radius:8px;margin-bottom:28px;">
                    <tr>
                      <td style="padding:20px 24px;">
                        <p style="margin:0 0 4px;font-size:11px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:{_BRAND_GREY};">What happens next</p>
                        <p style="margin:0;font-size:14px;line-height:1.6;color:#374151;">
                          1. Your request is assigned to the appropriate specialist<br>
                          2. We may reach out for a brief discovery call if needed<br>
                          3. You receive a tailored response with clear next steps
                        </p>
                      </td>
                    </tr>
                  </table>
                  <p style="margin:0;font-size:15px;line-height:1.75;color:#4B5563;">
                    With regards,<br>
                    <strong style="color:{_BRAND_DARK};">The Nexxus Tech Team</strong><br>
                    <span style="font-size:13px;color:{_BRAND_GREY};">WAF · NetScaler · Cloud Security · AI</span>
                  </p>
                </td>
              </tr>
              <tr>
                <td style="background:{_BRAND_DARK};padding:24px 40px;text-align:center;">
                  <p style="margin:0 0 6px;font-size:13px;color:#E5E5E5;">
                    <a href="mailto:contact@nexxus-tech.com" style="color:{_BRAND_PRIMARY_LIGHT};text-decoration:none;">contact@nexxus-tech.com</a>
                    &nbsp;·&nbsp;
                    <a href="https://nexxus-tech.com" style="color:{_BRAND_PRIMARY_LIGHT};text-decoration:none;">nexxus-tech.com</a>
                  </p>
                  <p style="margin:0;font-size:11px;color:#9CA3AF;">Colombia · UAE · UK · US — Remote engagements worldwide</p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """


def _build_auto_reply_plain(data: ContactRequest) -> str:
    first_name = data.name.split()[0] if data.name.strip() else "there"
    return f"""Dear {first_name},

Thank you for contacting Nexxus Tech. We have received your enquiry and a member of our consulting team will review it and respond within one business day.

What happens next:
1. Your request is assigned to the appropriate specialist
2. We may reach out for a brief discovery call if needed
3. You receive a tailored response with clear next steps

If your matter is urgent, please reply to this email and note the urgency — we prioritise security-related engagements accordingly.

With regards,
The Nexxus Tech Team
contact@nexxus-tech.com
https://nexxus-tech.com

—
WAF · NetScaler · Cloud Security · AI
"""


async def _send_email(
    *,
    to: str,
    subject: str,
    html: str,
    plain: str | None = None,
    reply_to: str | None = None,
) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Nexxus Tech <{CONTACT_FROM}>"
    msg["To"] = to
    if reply_to:
        msg["Reply-To"] = reply_to
    if plain:
        msg.attach(MIMEText(plain, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))

    await aiosmtplib.send(
        msg,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        start_tls=True,
        username=SMTP_USER,
        password=SMTP_PASS,
    )


@router.post("/contact", response_model=ContactResponse)
async def send_contact(data: ContactRequest):
    if not SMTP_USER or not SMTP_PASS:
        print(f"[CONTACT] (dev) Team notification → {CONTACT_TO}")
        print(f"[CONTACT] (dev) Auto-reply → {data.email}")
        print(f"[CONTACT] From: {data.name} <{data.email}> | {data.message[:80]}...")
        return ContactResponse(success=True, message=SUCCESS_MESSAGE)

    try:
        await _send_email(
            to=CONTACT_TO,
            subject=f"[Nexxus Tech] New enquiry from {data.name}",
            html=_build_team_notification_html(data),
            reply_to=data.email,
        )
        await _send_email(
            to=data.email,
            subject="Thank you for contacting Nexxus Tech",
            html=_build_auto_reply_html(data),
            plain=_build_auto_reply_plain(data),
            reply_to=CONTACT_TO,
        )
        return ContactResponse(success=True, message=SUCCESS_MESSAGE)
    except Exception as exc:
        print(f"[CONTACT ERROR] {exc}")
        raise HTTPException(
            status_code=500,
            detail="Failed to send message. Please try again or email contact@nexxus-tech.com directly.",
        )
