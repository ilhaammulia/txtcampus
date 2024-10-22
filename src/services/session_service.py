from src.repositories.session_repository import SessionRepository
from src.error import UnauthorizedError

class SessionService:

    @staticmethod
    def create_session(user_id):
        return SessionRepository.create_session(user_id)

    @staticmethod
    def remove_session(token):
        session = SessionRepository.get_session(token)
        if session:
            SessionRepository.remove_session(session.id)

    @staticmethod
    def get_session(token):
        session = SessionRepository.get_session(token)
        if session and not session.is_expired():
            return session
        if session:
            SessionRepository.remove_session(session.id)
        raise UnauthorizedError("Session expired.")
