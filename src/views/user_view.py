from flask import Blueprint, jsonify, request, g
from src.services.user_service import UserService
from src.middlewares.auth import auth_required

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/profile', methods=['POST'], endpoint='update_profile')
@auth_required
def update_profile():
    data = request.form
    username = data.get('username')
    email_address = data.get('email_address')
    name = data.get('name')
    bio = data.get('bio')

    # Handle profile photo upload
    profile_photo = request.files.get('profile_photo')

    user = UserService.update_user_profile(
        user_id=g.current_user.id,
        username=username,
        email_address=email_address,
        name=name,
        bio=bio,
        profile_photo=profile_photo
    )

    return jsonify({'success': True, 'message': 'Profile updated successfully', 'data': user.username}), 200

@user_blueprint.route('/', methods=['GET'], endpoint='get_profile')
@auth_required
def get_profile():
    user = UserService.get_user_by_username(g.current_user.username)
    if user:
        return jsonify({'success': True, 'message': None, 'data': user.json})
    return jsonify({'success': False, 'message': 'User not found', 'data': None}), 404


@user_blueprint.route('/<string:username>', methods=['GET'], endpoint='get_user')
@auth_required
def get_user(username):
    user = UserService.get_user_by_username(username)
    if user:
        return jsonify({'success': True, 'message': None, 'data': user.json})
    return jsonify({'success': False, 'message': 'User not found', 'data': None}), 404
