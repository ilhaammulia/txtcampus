from flask import Flask, send_from_directory, send_file
from src.database import db
from src.error.error_handler import handle_not_found, handle_internal_error, handle_bad_request, handle_forbidden_error, handle_unauthorized_error
from src.error import NotFoundError, InternalServerError, BadRequestError, ForbiddenError, UnauthorizedError
from dotenv import load_dotenv
import os

from src.views.auth_view import auth_blueprint
from src.views.user_view import user_blueprint
from src.views.post_view import post_blueprint

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    db.init_app(app)

    # Static route to serve uploaded profile photos
    @app.route('/files/<path:filepath>', methods=['GET'], endpoint='static_files')
    def uploaded_file(filepath):
        return send_file(os.path.join(os.path.dirname(__file__), "..", filepath))

    # Register blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
    app.register_blueprint(user_blueprint, url_prefix='/api/users')
    app.register_blueprint(post_blueprint, url_prefix='/api/posts')


    # Error handlers for custom exceptions
    app.register_error_handler(NotFoundError, handle_not_found)
    app.register_error_handler(InternalServerError, handle_internal_error)
    app.register_error_handler(BadRequestError, handle_bad_request)
    app.register_error_handler(ForbiddenError, handle_forbidden_error)
    app.register_error_handler(UnauthorizedError, handle_unauthorized_error)

    with app.app_context():
        db.create_all()

    return app
