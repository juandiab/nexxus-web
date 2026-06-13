"""HTML email templates for admin console account emails."""

from __future__ import annotations

from html import escape

_BRAND_PRIMARY = "#007BA7"
_BRAND_PRIMARY_LIGHT = "#00A8E0"
_BRAND_DARK = "#1C1C1E"
_BRAND_GREY = "#6B7280"
_BRAND_LIGHT_BG = "#F5F5F7"


def _otp_box(value: str, *, label: str = "Temporary password") -> str:
    safe = escape(value)
    return f"""
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:20px 0;">
      <tr><td align="center">
        <p style="margin:0 0 10px;font-size:12px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:{_BRAND_GREY};">{escape(label)}</p>
        <div style="display:inline-block;background:#F0F9FF;border:2px dashed {_BRAND_PRIMARY};border-radius:12px;padding:18px 32px;">
          <span style="font-family:Consolas,'Courier New',monospace;font-size:28px;font-weight:700;letter-spacing:0.18em;color:{_BRAND_DARK};">{safe}</span>
        </div>
      </td></tr>
    </table>
    """


def _cta_button(url: str, label: str) -> str:
    safe_url = escape(url)
    safe_label = escape(label)
    return f"""
    <table role="presentation" cellpadding="0" cellspacing="0" style="margin:24px 0;">
      <tr><td align="center">
        <a href="{safe_url}" style="display:inline-block;background:{_BRAND_PRIMARY};color:#FFFFFF;text-decoration:none;font-size:14px;font-weight:600;padding:12px 28px;border-radius:8px;">{safe_label}</a>
      </td></tr>
    </table>
    """


def _account_email_shell(*, eyebrow: str, title: str, body_html: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <body style="margin:0;padding:0;background:{_BRAND_LIGHT_BG};font-family:'Segoe UI',Arial,sans-serif;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{_BRAND_LIGHT_BG};padding:40px 16px;">
        <tr><td align="center">
          <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;background:#FFFFFF;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">
            <tr>
              <td style="background:linear-gradient(135deg,{_BRAND_DARK} 0%,#2E2E32 100%);padding:28px 32px;">
                <p style="margin:0 0 8px;font-size:11px;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:{_BRAND_PRIMARY_LIGHT};">{escape(eyebrow)}</p>
                <h1 style="margin:0;font-size:22px;font-weight:700;color:#FFFFFF;">{escape(title)}</h1>
              </td>
            </tr>
            <tr><td style="padding:32px;color:#374151;font-size:15px;line-height:1.7;">
              {body_html}
            </td></tr>
          </table>
          <p style="margin:16px 0 0;font-size:11px;color:#9CA3AF;">Nexxus Tech Admin Console · nexxus-tech.com</p>
        </td></tr>
      </table>
    </body>
    </html>
    """


def build_welcome_credentials_html(
    *,
    display_name: str,
    username: str,
    temporary_password: str,
    login_url: str,
) -> str:
    name = escape(display_name)
    user = escape(username)
    body = f"""
      <p style="margin:0 0 16px;">Hello {name},</p>
      <p style="margin:0 0 16px;">An administrator created an admin console account for you. Use the credentials below to sign in.</p>
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 8px;background:#F9FAFB;border:1px solid #E5E7EB;border-radius:8px;">
        <tr><td style="padding:14px 18px;font-size:14px;">
          <strong style="color:{_BRAND_DARK};">Username:</strong> {user}
        </td></tr>
      </table>
      {_otp_box(temporary_password)}
      {_cta_button(login_url, "Sign in to Admin Console")}
      <p style="margin:0;font-size:13px;color:{_BRAND_GREY};">
        On your first sign-in you will set a new password and register a passkey.
        After that, only your passkey can be used to sign in.
      </p>
    """
    return _account_email_shell(
        eyebrow="Account created",
        title="Welcome to Nexxus Tech Admin",
        body_html=body,
    )


def build_password_reset_html(
    *,
    display_name: str,
    username: str,
    temporary_password: str,
    login_url: str,
) -> str:
    name = escape(display_name)
    user = escape(username)
    body = f"""
      <p style="margin:0 0 16px;">Hello {name},</p>
      <p style="margin:0 0 16px;">An administrator requested a password reset for your admin console account (<strong>{user}</strong>).</p>
      <p style="margin:0 0 8px;">Use this temporary password to sign in:</p>
      {_otp_box(temporary_password, label="New temporary password")}
      {_cta_button(login_url, "Sign in now")}
      <p style="margin:0;font-size:13px;color:{_BRAND_GREY};">
        Existing passkeys were removed. After signing in, set a new password and register a passkey again.
        If you did not expect this email, contact your administrator immediately.
      </p>
    """
    return _account_email_shell(
        eyebrow="Password reset",
        title="Your password was reset",
        body_html=body,
    )


def build_welcome_credentials_plain(
    *,
    display_name: str,
    username: str,
    temporary_password: str,
    login_url: str,
) -> str:
    return (
        f"Hello {display_name},\n\n"
        f"An administrator created an admin console account for you.\n\n"
        f"Username: {username}\n"
        f"Temporary password: {temporary_password}\n\n"
        f"Sign in at: {login_url}\n\n"
        "On your first sign-in you will set a new password and register a passkey.\n"
    )


def build_password_reset_plain(
    *,
    display_name: str,
    username: str,
    temporary_password: str,
    login_url: str,
) -> str:
    return (
        f"Hello {display_name},\n\n"
        f"A password reset was requested for your admin console account ({username}).\n\n"
        f"New temporary password: {temporary_password}\n\n"
        f"Sign in at: {login_url}\n\n"
        "Existing passkeys were removed. Set a new password and register a passkey after signing in.\n"
    )


def _row(label: str, value: str, *, last: bool = False) -> str:
    border = "" if last else "border-bottom:1px solid #E5E7EB;"
    return f"""
    <tr>
      <td style="padding:10px 0;{border}width:140px;color:{_BRAND_GREY};font-size:13px;font-weight:600;vertical-align:top;">{escape(label)}</td>
      <td style="padding:10px 0;{border}color:{_BRAND_DARK};font-size:14px;line-height:1.5;">{value}</td>
    </tr>
    """


def build_license_activation_html(
    *,
    name: str,
    application: str,
    license_code: str,
    otp_code: str,
    license_type: str,
    validity_days: int,
    company: str = "",
) -> str:
    first = escape(name.split()[0] if name.strip() else "there")
    app = escape(application)
    company_row = _row("Company", escape(company)) if company.strip() else ""
    type_label = escape(license_type.replace("_", " ").title())
    details_rows = (
        _row("Application", app)
        + _row("License type", type_label)
        + _row("Validity", f"{validity_days} days after email confirmation")
        + (company_row if company_row else "")
        + _row("Confirmation", "Required on activation page", last=True)
    )

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
              <h1 style="margin:0;font-size:24px;font-weight:700;color:{_BRAND_DARK};">Confirm your license activation</h1>
            </td></tr>
            <tr><td style="padding:0 40px 32px;">
              <p style="margin:0 0 20px;font-size:16px;line-height:1.75;color:#374151;">Hi {first},</p>
              <p style="margin:0 0 24px;font-size:15px;line-height:1.75;color:#4B5563;">
                Thank you for activating <strong>{app}</strong>. Your email contains two codes:
                a <strong>6-digit verification code</strong> for the activation page, and your
                <strong>license code</strong> for the application.
              </p>
              {_otp_box(otp_code, label="Email verification code (6 digits)")}
              {_otp_box(license_code, label="License code (for your application)")}
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{_BRAND_LIGHT_BG};border-radius:10px;margin-bottom:24px;">
                <tr><td style="padding:20px 24px;">
                  <p style="margin:0 0 12px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:{_BRAND_GREY};">License details</p>
                  <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                    {details_rows}
                  </table>
                </tr></td>
              </table>
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{_BRAND_LIGHT_BG};border-radius:8px;margin-bottom:24px;">
                <tr><td style="padding:20px 24px;">
                  <p style="margin:0 0 8px;font-size:11px;font-weight:700;text-transform:uppercase;color:{_BRAND_GREY};">What happens next</p>
                  <p style="margin:0;font-size:14px;line-height:1.65;color:#374151;">
                    Enter the 6-digit verification code on the activation page. Once confirmed, your license will be saved and ready to use in your application.
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


def build_license_activation_plain(
    *,
    name: str,
    application: str,
    license_code: str,
    otp_code: str,
    license_type: str,
    validity_days: int,
    company: str = "",
) -> str:
    lines = [
        f"Hi {name},",
        "",
        f"Thank you for activating {application}.",
        "",
        f"Email verification code (6 digits): {otp_code}",
        "",
        f"License code (for your application): {license_code}",
        "",
        "License details",
        f"Application: {application}",
        f"License type: {license_type.replace('_', ' ').title()}",
        f"Validity: {validity_days} days after email confirmation",
    ]
    if company.strip():
        lines.append(f"Company: {company}")
    lines.extend(
        [
            "",
            "Enter the verification code on the activation page to confirm your email.",
            "",
            "— The Nexxus Tech Team",
            "contact@nexxus-tech.com",
        ]
    )
    return "\n".join(lines)


def _format_display_date(value) -> str:
    if value is None:
        return "—"
    if isinstance(value, str):
        text = value.replace("Z", "+00:00")
        try:
            from datetime import datetime

            value = datetime.fromisoformat(text)
        except ValueError:
            return value
    try:
        from utils.time import ensure_utc_aware

        aware = ensure_utc_aware(value)
        return aware.strftime("%B %d, %Y")
    except (TypeError, ValueError):
        return str(value)


def _license_email_shell(*, eyebrow: str, title: str, body_html: str) -> str:
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
              <h1 style="margin:0;font-size:24px;font-weight:700;color:{_BRAND_DARK};">{escape(title)}</h1>
              <p style="margin:12px 0 0;font-size:13px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:{_BRAND_GREY};">{escape(eyebrow)}</p>
            </td></tr>
            <tr><td style="padding:0 40px 32px;">
              {body_html}
            </td></tr>
            <tr><td style="background:{_BRAND_DARK};padding:24px 40px;text-align:center;">
              <p style="margin:0;font-size:13px;color:#E5E5E5;">
                Questions? <a href="mailto:contact@nexxus-tech.com" style="color:{_BRAND_PRIMARY_LIGHT};text-decoration:none;">contact@nexxus-tech.com</a>
              </p>
            </td></tr>
          </table>
        </td></tr>
      </table>
    </body>
    </html>
    """


def _license_code_box(license_code: str) -> str:
    if not license_code:
        return ""
    return _otp_box(license_code, label="Your license code")


def _license_details_table(
    *,
    application: str,
    license_type: str,
    expiration_date,
    status_label: str,
    validity_days: int | None = None,
) -> str:
    type_label = escape(license_type.replace("_", " ").title())
    rows = (
        _row("Application", escape(application))
        + _row("License type", type_label)
        + (_row("Validity", f"{validity_days} days") if validity_days else "")
        + _row("Expires", escape(_format_display_date(expiration_date)))
        + _row("Status", escape(status_label), last=True)
    )
    return f"""
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{_BRAND_LIGHT_BG};border-radius:10px;margin:24px 0;">
      <tr><td style="padding:20px 24px;">
        <p style="margin:0 0 12px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:{_BRAND_GREY};">Updated license details</p>
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
          {rows}
        </table>
      </td></tr>
    </table>
    """


_CHANGE_COPY = {
    "extended": {
        "eyebrow": "License extended",
        "title": "Your license validity has been extended",
        "lead": "Good news — an administrator extended your license. Your application will continue working until the new expiration date below.",
    },
    "type_changed": {
        "eyebrow": "License updated",
        "title": "Your license type has changed",
        "lead": "An administrator updated your license type and validity. Review the details below and sync your application if needed.",
    },
    "updated": {
        "eyebrow": "License updated",
        "title": "Your license details were updated",
        "lead": "An administrator updated your license. Review the details below and sync your application if needed.",
    },
    "expired": {
        "eyebrow": "License expired",
        "title": "Your license has expired",
        "lead": "An administrator marked your license as expired. Contact support if you believe this was a mistake or need a renewal.",
    },
    "deactivated": {
        "eyebrow": "License deactivated",
        "title": "Your license has been deactivated",
        "lead": "An administrator deactivated your license. Your application will no longer sync until the license is reactivated.",
    },
    "reactivated": {
        "eyebrow": "License reactivated",
        "title": "Your license is active again",
        "lead": "Good news — your license was reactivated. You can sync your application again using the details below.",
    },
}


def build_license_update_html(
    *,
    name: str,
    application: str,
    license_code: str,
    license_type: str,
    expiration_date,
    status_label: str,
    change: str,
    validity_days: int | None = None,
    days_added: int | None = None,
) -> str:
    copy = _CHANGE_COPY.get(change, _CHANGE_COPY["updated"])
    first = escape(name.split()[0] if name.strip() else "there")
    app = escape(application)
    lead = copy["lead"]
    if change == "extended" and days_added:
        lead = (
            f"Good news — an administrator added {days_added} days to your license. "
            f"It is now valid until {_format_display_date(expiration_date)}."
        )

    body = f"""
      <p style="margin:0 0 20px;font-size:16px;line-height:1.75;color:#374151;">Hi {first},</p>
      <p style="margin:0 0 8px;font-size:15px;line-height:1.75;color:#4B5563;">{escape(lead)}</p>
      <p style="margin:0 0 8px;font-size:15px;line-height:1.75;color:#4B5563;">
        Application: <strong>{app}</strong>
      </p>
      {_license_code_box(license_code)}
      {_license_details_table(
          application=application,
          license_type=license_type,
          expiration_date=expiration_date,
          status_label=status_label,
          validity_days=validity_days,
      )}
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F0F9FF;border:1px solid #BAE6FD;border-radius:8px;margin-bottom:24px;">
        <tr><td style="padding:18px 22px;">
          <p style="margin:0;font-size:14px;line-height:1.65;color:#374151;">
            Open your application and sync the license to pick up the latest expiration date and status.
            If you use an offline license file, download a fresh copy from the activation page.
          </p>
        </td></tr>
      </table>
      <p style="margin:0;font-size:15px;color:#4B5563;">— The Nexxus Tech Team</p>
    """
    return _license_email_shell(
        eyebrow=copy["eyebrow"],
        title=copy["title"],
        body_html=body,
    )


def build_license_update_plain(
    *,
    name: str,
    application: str,
    license_code: str,
    license_type: str,
    expiration_date,
    status_label: str,
    change: str,
    validity_days: int | None = None,
    days_added: int | None = None,
) -> str:
    copy = _CHANGE_COPY.get(change, _CHANGE_COPY["updated"])
    lead = copy["lead"]
    if change == "extended" and days_added:
        lead = (
            f"An administrator added {days_added} days to your license. "
            f"It is now valid until {_format_display_date(expiration_date)}."
        )

    lines = [
        f"Hi {name},",
        "",
        lead,
        "",
        f"Application: {application}",
        f"License type: {license_type.replace('_', ' ').title()}",
    ]
    if validity_days:
        lines.append(f"Validity: {validity_days} days")
    lines.extend(
        [
            f"Expires: {_format_display_date(expiration_date)}",
            f"Status: {status_label}",
        ]
    )
    if license_code:
        lines.extend(["", f"License code: {license_code}"])
    lines.extend(
        [
            "",
            "Sync your application to pick up the latest expiration date and status.",
            "",
            "— The Nexxus Tech Team",
            "contact@nexxus-tech.com",
        ]
    )
    return "\n".join(lines)
