"""Database models for the email demo application."""

from __future__ import annotations

from datetime import UTC, datetime

from app import db


def _utcnow():
    return datetime.now(UTC)


class EmailLog(db.Model):
    __tablename__ = "email_logs"

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    sender = db.Column(db.String(255), nullable=False)
    recipients = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(32), nullable=False, default="pending")
    error = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=_utcnow)

    def mark_sent(self) -> None:
        self.status = "sent"
        self.error = None

    def mark_failed(self, message: str) -> None:
        self.status = "failed"
        self.error = message

    def __repr__(self) -> str:  # pragma: no cover - debugging helper
        return f"<EmailLog subject={self.subject!r} status={self.status!r}>"
