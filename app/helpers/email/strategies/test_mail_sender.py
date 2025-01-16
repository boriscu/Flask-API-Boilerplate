from flask import render_template
from app.helpers.email.mail_sender import MailSender


class TestMailSender(MailSender):
    def send_template(self, recipients, subject, name):
        data = {"name": name}
        html = render_template("emails/test.html", **data)

        self.send_html(recipients, subject, html)
