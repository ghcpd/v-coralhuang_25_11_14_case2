from datetime import datetime
from app import db


class EmailLog(db.Model):
    """Log of emails sent by the application."""
    __tablename__ = 'email_log'
    
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    recipients = db.Column(db.String(500), nullable=False)
    sender = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<EmailLog {self.id}: {self.subject}>'
