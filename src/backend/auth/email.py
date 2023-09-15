import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = int(os.getenv('SMTP_PORT'))
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SMTP_USER = os.getenv('SMTP_USER')


def get_email_template_dashboard(username: str, token: str):
    email = EmailMessage()
    email['Subject'] = 'Флагман Поддержка'
    email['From'] = os.getenv('SMTP_USER')
    email['To'] = username

    email.set_content(
        '<div>'
        f'<p>Здравствуйте, {username}! </p>'
        f'<p>{os.getenv("BASE_URL")}/profile/refresh?token={token}</p>'
        '</div>',
        subtype='html'
    )
    return email


def send_email_report_dashboard(username: str, token: str):
    email = get_email_template_dashboard(username, token)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)

