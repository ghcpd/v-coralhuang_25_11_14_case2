# app/email.py (fixed)
from flask import current_app
from flask_mail import Message
from threading import Thread
from app import mail, db

from app.models import EmailLog


def send_async_email(app, msg):
    """
    Run in a background thread, with a pushed app context, and a clean DB session.
    """
    # push a real app context into the thread
    with app.app_context():
        try:
            log = EmailLog(message=msg.subject)
            db.session.add(log)
            db.session.commit()

            mail.send(msg)
        finally:
            # remove the session to avoid leaking connections in the thread
            db.session.remove()


def send_email(subject, sender, recipients, text_body, app=None):
    """Send an email; run async in a background Thread unless the app config
    disables threading or we are running tests (TESTING True).

    The function returns the started Thread if one was created, otherwise None.
    """
    if app is None:
        # use the real application object from the proxy
        app = current_app._get_current_object()

    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body

    if app.config.get('MAIL_USE_THREADING', True) and not app.config.get('TESTING', False):
        thread = Thread(target=send_async_email, args=(app, msg))
        thread.start()
        return thread

    # run synchronously in test mode or when threading is disabled
    send_async_email(app, msg)
    return None
