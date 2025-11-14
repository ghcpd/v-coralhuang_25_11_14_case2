"""Email helpers for sending messages asynchronously."""
from threading import Thread

from flask import current_app
from flask_mail import Message

from app import db, mail
from app.models import EmailLog


def send_async_email(app, msg):
    """Send an email while operating inside the supplied application context."""
    with app.app_context():
        try:
            log_entry = EmailLog(message=msg.subject)
            db.session.add(log_entry)
            db.session.commit()
            mail.send(msg)
        finally:
            db.session.remove()


def send_email(subject, sender, recipients, text_body):
    """Create a message and dispatch it (possibly on a background thread)."""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body

    app = current_app._get_current_object()
    if app.config.get("EMAIL_ASYNC", True):
        thread = Thread(target=send_async_email, args=(app, msg), daemon=True)
        thread.start()
        return thread

    send_async_email(app, msg)
    return None
