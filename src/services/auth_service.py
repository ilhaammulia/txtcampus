import base64
from src.repositories.user_repository import UserRepository
from src.repositories.session_repository import SessionRepository
from src.error import BadRequestError

class AuthService:

    @staticmethod
    def register_user(username, password, email_address, name, bio=None):
        if username and UserRepository.get_user_by_username(username):
            raise BadRequestError("Username is already taken")

        if email_address and UserRepository.get_user_by_email(email_address):
            raise BadRequestError("Email address is already in use")

        return UserRepository.create_user(username, password, name, email_address, bio)

    @staticmethod
    def login_user(identifier, password):
        user = UserRepository.get_user_by_username_or_email(identifier)
        if user and user.check_password(password):
            session = SessionRepository.create_session(user.id)
            return session, user
        return None, None
