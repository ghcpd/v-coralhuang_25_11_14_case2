# app/email.py (buggy)
from flask import current_app
from flask_mail import Message
from threading import Thread
from app import mail, db
from app.models import EmailLog

def send_async_email(app, msg):
    # ❌ Bug: No app_context pushed → current_app invalid here
    log = EmailLog(message=msg.subject)
    db.session.add(log)
    db.session.commit()

    mail.send(msg)

def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body

    # ❌ Bug: passes proxy, not real app object
    Thread(target=send_async_email, args=(current_app, msg)).start()
