from __future__ import annotations

from html import escape

import resend
from flask import current_app


def send_contact_notification(contact_message):
    """
    Mengirim notifikasi email dari formulir kontak menggunakan Resend.
    """

    api_key = current_app.config.get("RESEND_API_KEY", "").strip()
    sender = current_app.config.get("RESEND_FROM", "").strip()
    receiver = current_app.config.get(
        "CONTACT_RECEIVER_EMAIL",
        "",
    ).strip()

    if not api_key:
        raise RuntimeError("RESEND_API_KEY belum diatur.")

    if not sender:
        raise RuntimeError("RESEND_FROM belum diatur.")

    if not receiver:
        raise RuntimeError(
            "CONTACT_RECEIVER_EMAIL belum diatur."
        )

    name = escape(contact_message.name)
    email = escape(contact_message.email)
    subject = escape(contact_message.subject)
    message = escape(contact_message.message).replace(
        "\n",
        "<br>",
    )

    email_html = f"""
    <!doctype html>
    <html lang="id">
      <body style="
        margin: 0;
        padding: 30px;
        background: #fff5f5;
        font-family: Arial, sans-serif;
        color: #2b1618;
      ">
        <div style="
          max-width: 640px;
          margin: 0 auto;
          overflow: hidden;
          border: 1px solid #fecaca;
          border-radius: 18px;
          background: #ffffff;
          box-shadow: 0 18px 45px rgba(127, 29, 29, 0.12);
        ">
          <div style="
            padding: 26px 30px;
            color: #ffffff;
            background: linear-gradient(
              135deg,
              #450a0a,
              #991b1b
            );
          ">
            <p style="
              margin: 0 0 8px;
              color: #fecaca;
              font-size: 12px;
              font-weight: bold;
              letter-spacing: 1.5px;
            ">
              PORTFOLIO NELVIN
            </p>

            <h1 style="
              margin: 0;
              font-size: 25px;
            ">
              Pesan baru dari website
            </h1>
          </div>

          <div style="padding: 30px;">
            <table style="
              width: 100%;
              border-collapse: collapse;
            ">
              <tr>
                <td style="
                  width: 110px;
                  padding: 9px 0;
                  color: #7f5a5d;
                ">
                  Nama
                </td>

                <td style="
                  padding: 9px 0;
                  font-weight: bold;
                ">
                  {name}
                </td>
              </tr>

              <tr>
                <td style="
                  padding: 9px 0;
                  color: #7f5a5d;
                ">
                  Email
                </td>

                <td style="padding: 9px 0;">
                  {email}
                </td>
              </tr>

              <tr>
                <td style="
                  padding: 9px 0;
                  color: #7f5a5d;
                ">
                  Subjek
                </td>

                <td style="
                  padding: 9px 0;
                  font-weight: bold;
                ">
                  {subject}
                </td>
              </tr>
            </table>

            <div style="
              margin-top: 24px;
              padding: 20px;
              border-left: 5px solid #b91c1c;
              border-radius: 10px;
              background: #fff1f2;
              line-height: 1.7;
            ">
              {message}
            </div>
          </div>
        </div>
      </body>
    </html>
    """

    email_text = (
        "Pesan baru dari website portfolio\n\n"
        f"Nama: {contact_message.name}\n"
        f"Email: {contact_message.email}\n"
        f"Subjek: {contact_message.subject}\n\n"
        f"Pesan:\n{contact_message.message}"
    )

    resend.api_key = api_key

    params: resend.Emails.SendParams = {
        "from": sender,
        "to": [receiver],
        "subject": (
            f"Portfolio Nelvin: "
            f"{contact_message.subject}"
        ),
        "html": email_html,
        "text": email_text,
        "reply_to": contact_message.email,
    }

    return resend.Emails.send(params)