from datetime import datetime
from src.database import db

class BaseModel(db.Model):
    __abstract__ = True  # This ensures that BaseModel is not created as a table

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
