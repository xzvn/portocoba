from html import escape

import resend
from flask import current_app


def send_contact_notification(contact_message):
    api_key = current_app.config.get("RESEND_API_KEY")
    receiver = current_app.config.get("CONTACT_RECEIVER_EMAIL")
    sender = current_app.config.get("RESEND_FROM")

    if not api_key or not receiver:
        raise RuntimeError("Konfigurasi Resend atau email penerima belum lengkap.")

    resend.api_key = api_key
    safe_message = escape(contact_message.message).replace("\n", "<br>")

    params = {
        "from": sender,
        "to": [receiver],
        "reply_to": contact_message.email,
        "subject": f"Pesan portofolio: {contact_message.subject}",
        "html": f"""
            <div style="font-family:Arial,sans-serif;max-width:640px;margin:auto;color:#191c1d">
                <h2>Pesan baru dari website portofolio</h2>
                <p><strong>Nama:</strong> {escape(contact_message.name)}</p>
                <p><strong>Email:</strong> {escape(contact_message.email)}</p>
                <p><strong>Subjek:</strong> {escape(contact_message.subject)}</p>
                <hr style="border:none;border-top:1px solid #e1e3e4">
                <p>{safe_message}</p>
            </div>
        """,
    }
    return resend.Emails.send(params)
