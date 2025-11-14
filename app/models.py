from datetime import datetime
from app import db

class EmailLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EmailLog id={self.id} message={self.message!r}>"
