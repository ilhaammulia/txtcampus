from flask import Blueprint, jsonify, request
from src.services.auth_service import AuthService

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['POST'], endpoint='register_user')
def register():
    data = request.get_json()
    user = AuthService.register_user(
        username=data['username'],
        password=data['password'],
        email_address=data['email_address'],
        name=data['name'],
        bio=data.get('bio')
    )
    return jsonify({'success': True, 'message': 'User registered successfully', 'data': user.id}), 201

@auth_blueprint.route('/login', methods=['POST'], endpoint='login_user')
def login():
    data = request.get_json()
    session, user = AuthService.login_user(data['identifier'], data['password'])
    if session:
        return jsonify({'success': True, 'message': 'Login successful', 'data': session.json}), 200
    return jsonify({'success': False, 'message': 'Invalid username or email address, or password'}), 401
