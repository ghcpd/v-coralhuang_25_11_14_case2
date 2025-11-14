"""Tests covering the email helper under deterministic conditions."""

from app import mail
from app.email import send_email
from app.models import EmailLog


def test_send_email_records_log_and_message(app):
    assert app.config["EMAIL_ASYNC"] is False

    with mail.record_messages() as outbox:
        thread = send_email(
            "Test Subject",
            "noreply@example.com",
            ["user@example.com"],
            "Hello world body",
        )

    assert thread is None
    assert len(outbox) == 1

    log_entries = EmailLog.query.all()
    assert len(log_entries) == 1
    assert log_entries[0].message == "Test Subject"
