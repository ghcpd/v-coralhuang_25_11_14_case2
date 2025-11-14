from flask import current_app
from flask_mail import Message
from threading import Thread
from app import mail, db
from app.models import EmailLog
import time


def send_async_email(app, msg, recipients, sender):
    """
    Send email asynchronously within a background thread.
    
    This function must be called within a background thread via Thread().
    It pushes an app context and performs database operations safely.
    
    Args:
        app: The Flask application instance (real object, not proxy)
        msg: The Message object to send
        recipients: List of recipient email addresses
        sender: Sender email address
    """
    with app.app_context():
        try:
            # Small delay to ensure main thread has finished its work
            time.sleep(0.01)
            
            # Log the email send attempt
            log = EmailLog(
                subject=msg.subject,
                recipients=','.join(recipients),
                sender=sender,
                body=msg.body
            )
            db.session.add(log)
            db.session.commit()
            
            # Send the email
            mail.send(msg)
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error sending email: {e}")
        finally:
            db.session.close()


def send_email(subject, sender, recipients, text_body):
    """
    Send email asynchronously by spawning a background thread.
    
    This function queues the email send task to a background thread,
    allowing the request handler to return immediately.
    
    Args:
        subject: Email subject
        sender: Sender email address
        recipients: List of recipient email addresses
        text_body: Email body text
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body

    # Pass the real app instance (not the proxy) to the thread
    app = current_app._get_current_object()
    thread = Thread(
        target=send_async_email,
        args=(app, msg, recipients, sender)
    )
    thread.daemon = False  # Don't let thread prevent app shutdown
    thread.start()
    return thread
