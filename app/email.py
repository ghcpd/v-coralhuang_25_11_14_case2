"""Thread-safe email helpers."""

from __future__ import annotations

from threading import Thread
from typing import Iterable, Optional

from flask import current_app
from flask_mail import Message

from app import db, mail
from app.models import EmailLog


def _normalize_recipients(recipients: Iterable[str]) -> list[str]:
    if not recipients:
        raise ValueError("At least one recipient is required")
    return list(recipients)


def send_async_email(app, msg: Message) -> None:
    """Background email sender that owns its application context."""
    # Push an application context inside the thread to safely use extensions.
    with app.app_context():
        log = EmailLog(
            subject=msg.subject,
            sender=msg.sender,
            recipients=",".join(msg.recipients),
            body=msg.body,
        )
        db.session.add(log)
        db.session.commit()

        try:
            mail.send(msg)
            log.mark_sent()
        except Exception as exc:  # pragma: no cover - defensive logging
            log.mark_failed(str(exc))
            raise
        finally:
            db.session.add(log)
            db.session.commit()


def send_email(
    subject: str,
    sender: Optional[str],
    recipients: Iterable[str],
    text_body: str,
    use_async: Optional[bool] = None,
):
    """Dispatch an email synchronously or via a background thread.

    Returns:
        Thread | None: the spawned thread when running asynchronously.
    """

    app = current_app._get_current_object()
    actual_sender = sender or app.config.get("MAIL_DEFAULT_SENDER")
    msg = Message(subject=subject, sender=actual_sender, recipients=_normalize_recipients(recipients))
    msg.body = text_body

    async_enabled = app.config.get("EMAIL_USE_ASYNC", True) if use_async is None else use_async

    if async_enabled:
        thread = Thread(target=send_async_email, args=(app, msg), daemon=True)
        thread.start()
        return thread

    send_async_email(app, msg)
    return None
