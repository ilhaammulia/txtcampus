import os
from src.app import db
from flask import current_app
from werkzeug.utils import secure_filename
from src.repositories.user_repository import UserRepository
from src.error import BadRequestError, NotFoundError, BadRequestError

class UserService:

    @staticmethod
    def get_user_by_username(username):
        return UserRepository.get_user_by_username(username)

    @staticmethod
    def update_user_profile(user_id, username=None, email_address=None, name=None, bio=None, profile_photo=None):
        user = UserRepository.get_user_by_id(user_id)

        if username and username != user.username:
            if UserRepository.get_user_by_username(username):
                raise BadRequestError("Username is already taken")

        if email_address and email_address != user.email_address:
            if UserRepository.get_user_by_email(email_address):
                raise BadRequestError("Email address is already in use")

        if username:
            user.username = username
        if email_address:
            user.email_address = email_address
        if name:
            user.name = name
        if bio:
            user.bio = bio

        if profile_photo:
            UserService.remove_profile_photo(user.profile_photo)
            user.profile_photo = UserService.save_profile_photo(profile_photo, user.id)

        db.session.commit()
        return user

    @staticmethod
    def save_profile_photo(file, user_id):
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)

        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, str(user_id), 'profiles', filename)
        os.makedirs(os.path.join(upload_folder, str(user_id), 'profiles'), exist_ok=True)

        file.save(file_path)

        return file_path

    @staticmethod
    def remove_profile_photo(photo_path):
        if not photo_path: return

        try:
            if os.path.exists(photo_path):
                os.remove(photo_path)
        except Exception as e:
            print(f"Error deleting old profile photo: {e}")
