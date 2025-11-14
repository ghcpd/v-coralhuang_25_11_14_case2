"""Database models."""
from datetime import datetime

from app import db


class EmailLog(db.Model):
    """Keep a simple audit of emails sent through the system."""

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<EmailLog subject={self.message!r}>"
