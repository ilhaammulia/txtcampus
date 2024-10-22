from src.models.session import Session
from src.database import db

class SessionRepository:

    @staticmethod
    def create_session(user_id):
        session = Session(user_id)
        db.session.add(session)
        db.session.commit()
        return session

    @staticmethod
    def remove_session(session_id):
        session = Session.query.get(session_id)
        db.session.delete(session)
        db.session.commit()

    @staticmethod
    def get_session(token):
        session = Session.query.filter_by(token=token).first()
        return session
