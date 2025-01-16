from flask import render_template

from config.app_config import AppConfig

from app.helpers.email.mail_sender import MailSender


class UserVerificationSender(MailSender):
    def send_template(self, user_email, token):
        subject = "Mentoria: Account Verification"
        recipients = [user_email]
        url = f"{AppConfig.CLIENT_DOMAIN}/user-confirmation?token={token}"

        data = {"url": url}
        html = render_template("emails/user_verification_template.html", **data)

        self.send_html(subject=subject, recipients=recipients, html=html)
