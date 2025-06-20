import smtplib
from email.mime.text import MIMEText
from config.config import Config


class EmailService:
    @staticmethod
    def send_email(to_email, subject, html_content):
        try:
            message = EmailService._build_message(to_email, subject, html_content)
            EmailService._send_message(to_email, message)
            print(f"Email sent to {to_email}")
            return True
        except Exception as e:
            print(f"Email failed: {e}")
            return False

    @staticmethod
    def _build_message(to_email, subject, content):
        msg = MIMEText(content, "html")
        msg["From"] = Config.SMTP_SENDER
        msg["To"] = to_email
        msg["Subject"] = subject
        return msg

    @staticmethod
    def _send_message(to_email, message):
        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
            server.sendmail(Config.SMTP_SENDER, [to_email], message.as_string())
