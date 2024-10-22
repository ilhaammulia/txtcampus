from src.models.user import User
from src.app import db
from src.error import NotFoundError

class UserRepository:

    @staticmethod
    def create_user(username, password, name, email, bio=None):
        user = User(username=username, name=name, email_address=email, bio=bio)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_user_by_email(email_address):
        return User.query.filter_by(email_address=email_address).first()

    @staticmethod
    def get_user_by_username_or_email(identifier):
        user = User.query.filter((User.username == identifier) | (User.email_address == identifier)).first()
        if not user:
            raise NotFoundError("User not found")
        return user
