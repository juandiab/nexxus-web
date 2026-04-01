import os
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


def _build_html(data: ContactRequest) -> str:
    return f"""
    <html><body style="font-family:Arial,sans-serif;background:#f4f4f4;padding:20px">
      <div style="max-width:600px;margin:auto;background:white;border-radius:8px;padding:32px;border-top:4px solid #5B4FE8">
        <h2 style="color:#0C1929;margin-top:0">New Contact from Nexxus Tech Website</h2>
        <table style="width:100%;border-collapse:collapse">
          <tr><td style="padding:8px 0;color:#666;width:120px"><strong>Name</strong></td><td style="padding:8px 0">{data.name}</td></tr>
          <tr><td style="padding:8px 0;color:#666"><strong>Email</strong></td><td style="padding:8px 0">{data.email}</td></tr>
          <tr><td style="padding:8px 0;color:#666"><strong>Company</strong></td><td style="padding:8px 0">{data.company or "—"}</td></tr>
          <tr><td style="padding:8px 0;color:#666"><strong>Service</strong></td><td style="padding:8px 0">{data.service or "—"}</td></tr>
        </table>
        <hr style="border:none;border-top:1px solid #eee;margin:16px 0">
        <p style="color:#333;white-space:pre-line">{data.message}</p>
        <p style="font-size:12px;color:#999;margin-top:24px">Sent via nexxus-tech.com contact form</p>
      </div>
    </body></html>
    """


@router.post("/contact", response_model=ContactResponse)
async def send_contact(data: ContactRequest):
    if not SMTP_USER or not SMTP_PASS:
        # Dev mode — just log and return success
        print(f"[CONTACT] From: {data.email} | {data.name} | {data.message[:80]}")
        return ContactResponse(success=True, message="Message received. We'll be in touch soon!")

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"[Nexxus Tech] New enquiry from {data.name}"
        msg["From"] = SMTP_USER
        msg["To"] = CONTACT_TO
        msg["Reply-To"] = data.email
        msg.attach(MIMEText(_build_html(data), "html"))

        await aiosmtplib.send(
            msg,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            start_tls=True,
            username=SMTP_USER,
            password=SMTP_PASS,
        )
        return ContactResponse(success=True, message="Message received. We'll be in touch soon!")
    except Exception as exc:
        print(f"[CONTACT ERROR] {exc}")
        raise HTTPException(status_code=500, detail="Failed to send message. Please try again or email us directly.")
