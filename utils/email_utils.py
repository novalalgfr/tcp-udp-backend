# backend/utils/email_utils.py

import smtplib
from email.message import EmailMessage
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS, FRONTEND_URL

def send_verification_email(to_email, token):
    verify_link = f"{FRONTEND_URL}/verify?token={token}"

    msg = EmailMessage()
    msg["Subject"] = "Verifikasi Akun Kamu"
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    msg.set_content(
        f"Halo!\n\nKlik link berikut untuk verifikasi akun kamu:\n{verify_link}\n\n"
        f"Kalau kamu tidak merasa mendaftar, abaikan email ini."
    )

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)