from datetime import datetime
from app.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_address = db.Column(db.String(42), unique=True, nullable=False)
    nonce = db.Column(db.Integer, nullable=False) # Random number for login security
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.public_address}>'