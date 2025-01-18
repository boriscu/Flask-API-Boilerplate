from flask import render_template
from app.helpers.email.mail_sender import MailSender
from config.app_config import AppConfig


class WorkspaceInviteSender(MailSender):
    def send_template(self, user_email: str, token: str, is_registred: bool) -> None:
        subject = "Mentoria: Workspace Invitation"
        recipients = [user_email]

        url = f"{AppConfig.CLIENT_DOMAIN}/workspace-invite?token={token}"

        data = {"url": url}
        html = render_template("emails/workspace_invite_template.html", **data)

        self.send_html(subject=subject, recipients=recipients, html=html)
