from app import mail
from app.email import send_email
from app.models import EmailLog


def test_send_email_logs_and_sends_message(app_ctx):
    with mail.record_messages() as outbox:
        send_email(
            subject="Greetings",
            sender="noreply@example.com",
            recipients=["user@example.com"],
            text_body="Hello from tests!",
            use_async=False,
        )

    assert len(outbox) == 1
    assert outbox[0].subject == "Greetings"
    assert outbox[0].body == "Hello from tests!"

    log = EmailLog.query.one()
    assert log.subject == "Greetings"
    assert log.recipients == "user@example.com"
    assert log.status == "sent"


def test_send_email_async_thread_can_be_joined(app_ctx, monkeypatch):
    sent_subjects: list[str] = []

    def fake_send(message):
        sent_subjects.append(message.subject)

    monkeypatch.setattr("app.email.mail.send", fake_send)

    thread = send_email(
        subject="Async",
        sender=None,
        recipients=["async@example.com"],
        text_body="async body",
        use_async=True,
    )

    assert thread is not None
    thread.join(timeout=5)
    assert not thread.is_alive()

    log = EmailLog.query.one()
    assert log.subject == "Async"
    assert sent_subjects == ["Async"]
