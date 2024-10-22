from datetime import datetime

def get_db():
    from src.app import db
    return db

class BaseModel(get_db().Model):
    __abstract__ = True  # This ensures that BaseModel is not created as a table

    created_at = get_db().Column(get_db().DateTime, default=datetime.utcnow)
    updated_at = get_db().Column(get_db().DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
