from flask import render_template

from config.app_config import AppConfig

from app.helpers.email.mail_sender import MailSender


class PasswordResetSender(MailSender):
    def send_template(self, user_email, token):
        subject = "Mentoria: Password reset"
        recipients = [user_email]
        url = f"{AppConfig.CLIENT_DOMAIN}/password-reset?token={token}"

        data = {"url": url}
        html = render_template("emails/password_reset_template.html", **data)

        self.send_html(subject=subject, recipients=recipients, html=html)
