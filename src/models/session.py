from datetime import datetime, timedelta
from src.database import db
from . import BaseModel
import secrets

class Session(BaseModel):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    expired_at = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref='sessions')

    def __init__(self, user_id, duration_hours=24):
        self.user_id = user_id
        self.token = self.generate_token()  # Automatically generate the token
        self.expired_at = datetime.utcnow() + timedelta(hours=duration_hours)

    @staticmethod
    def generate_token():
        """Generates a cryptographically secure random token."""
        return secrets.token_urlsafe(64)  # Generates a URL-safe 64-character token

    def is_expired(self):
        """Checks if the session token is expired."""
        return datetime.utcnow() > self.expired_at

    @property
    def json(self):
        return {
            'user': self.user.json,
            'token': self.token,
            'expired_at': self.expired_at
        }
