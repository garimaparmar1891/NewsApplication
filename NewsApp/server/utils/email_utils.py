import smtplib
from email.mime.text import MIMEText
from config.config import Config
from typing import cast


class ConfigValidator:
    @staticmethod
    def validate():
        required = [
            Config.SMTP_SENDER,
            Config.SMTP_SERVER,
            Config.SMTP_PORT,
            Config.SMTP_USERNAME,
            Config.SMTP_PASSWORD,
        ]
        if any(v is None for v in required):
            raise ValueError("SMTP configuration is incomplete. Please check your config.")


class EmailMessageBuilder:
    @staticmethod
    def build(to_email, subject, content):
        msg = MIMEText(content, "html")
        msg["From"] = cast(str, Config.SMTP_SENDER)
        msg["To"] = to_email
        msg["Subject"] = subject
        return msg


class EmailSender:
    @staticmethod
    def send(to_email, message):
        with smtplib.SMTP(cast(str, Config.SMTP_SERVER), cast(int, Config.SMTP_PORT)) as server:
            server.starttls()
            server.login(cast(str, Config.SMTP_USERNAME), cast(str, Config.SMTP_PASSWORD))
            server.sendmail(cast(str, Config.SMTP_SENDER), [to_email], message.as_string())


class EmailService:
    @staticmethod
    def send_email(to_email, subject, html_content):
        try:
            ConfigValidator.validate()
            message = EmailMessageBuilder.build(to_email, subject, html_content)
            EmailSender.send(to_email, message)
            print(f"Email sent to {to_email}")
            return True
        except Exception as e:
            print(f"Email failed: {e}")
            return False
