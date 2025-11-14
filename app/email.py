# app/email.py (buggy)
from flask import current_app
from flask_mail import Message
from threading import Thread
from app import mail, db
from app.models import EmailLog

def send_async_email(app, msg):
    # ensure this thread has app context and a fresh db session
    with app.app_context():
        # create a log entry in a safe way
        log = EmailLog(message=msg.subject)
        db.session.add(log)
        db.session.commit()

        mail.send(msg)

def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body

    app = current_app._get_current_object()
    # If the app is in testing or explicitly set to synchronous sends, do it inline
    if app.config.get("TESTING") or not app.config.get("EMAIL_SEND_ASYNC", True):
        # run synchronously (same behavior as async function but blocking)
        send_async_email(app, msg)
    else:
        Thread(target=send_async_email, args=(app, msg), daemon=True).start()
