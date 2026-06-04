from __future__ import annotations

import logging
import secrets
import string
from email.message import EmailMessage

import aiosmtplib

from config import settings
from services.email_templates import (
    build_license_activation_html,
    build_license_activation_plain,
    build_password_reset_html,
    build_password_reset_plain,
    build_welcome_credentials_html,
    build_welcome_credentials_plain,
)

logger = logging.getLogger(__name__)


def generate_temporary_password(length: int = 14) -> str:
    alphabet = string.ascii_letters + string.digits
    while True:
        password = "".join(secrets.choice(alphabet) for _ in range(length))
        if any(c.islower() for c in password) and any(c.isupper() for c in password) and any(
            c.isdigit() for c in password
        ):
            return password


async def send_email(*, to_address: str, subject: str, body: str, html_body: str | None = None) -> None:
    if not settings.smtp_host or not settings.smtp_user or not settings.smtp_pass:
        if settings.email_log_only:
            logger.warning(
                "SMTP not configured; email not sent to %s.\nSubject: %s\n%s",
                to_address,
                subject,
                body,
            )
            if html_body:
                logger.debug("HTML body omitted from log (length %s)", len(html_body))
            return
        raise RuntimeError("SMTP is not configured")

    message = EmailMessage()
    message["From"] = settings.smtp_from or settings.smtp_user
    message["To"] = to_address
    message["Subject"] = subject
    message.set_content(body)
    if html_body:
        message.add_alternative(html_body, subtype="html")

    await aiosmtplib.send(
        message,
        hostname=settings.smtp_host,
        port=settings.smtp_port,
        username=settings.smtp_user,
        password=settings.smtp_pass,
        start_tls=True,
    )


async def send_welcome_credentials_email(
    *,
    to_address: str,
    display_name: str,
    username: str,
    temporary_password: str,
) -> None:
    login_url = f"{settings.admin_console_url.rstrip('/')}/login"
    plain = build_welcome_credentials_plain(
        display_name=display_name,
        username=username,
        temporary_password=temporary_password,
        login_url=login_url,
    )
    html = build_welcome_credentials_html(
        display_name=display_name,
        username=username,
        temporary_password=temporary_password,
        login_url=login_url,
    )
    await send_email(
        to_address=to_address,
        subject="Your Nexxus Tech admin console account",
        body=plain,
        html_body=html,
    )


async def send_password_reset_email(
    *,
    to_address: str,
    display_name: str,
    username: str,
    temporary_password: str,
) -> None:
    login_url = f"{settings.admin_console_url.rstrip('/')}/login"
    plain = build_password_reset_plain(
        display_name=display_name,
        username=username,
        temporary_password=temporary_password,
        login_url=login_url,
    )
    html = build_password_reset_html(
        display_name=display_name,
        username=username,
        temporary_password=temporary_password,
        login_url=login_url,
    )
    await send_email(
        to_address=to_address,
        subject="Nexxus Tech admin console — password reset",
        body=plain,
        html_body=html,
    )


async def send_license_activation_email(
    *,
    to_address: str,
    name: str,
    company: str,
    application: str,
    license_code: str,
    otp_code: str,
    license_type: str,
    validity_days: int,
    expiration_date=None,
) -> None:
    plain = build_license_activation_plain(
        name=name,
        company=company,
        application=application,
        license_code=license_code,
        otp_code=otp_code,
        license_type=license_type,
        validity_days=validity_days,
    )
    html = build_license_activation_html(
        name=name,
        company=company,
        application=application,
        license_code=license_code,
        otp_code=otp_code,
        license_type=license_type,
        validity_days=validity_days,
    )
    await send_email(
        to_address=to_address,
        subject=f"Your {application} license — Nexxus Tech",
        body=plain,
        html_body=html,
    )
