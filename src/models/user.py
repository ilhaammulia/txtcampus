from src.models import BaseModel
from src.database import db
import bcrypt

class User(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email_address = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.Text)
    profile_photo = db.Column(db.String(200), default='public/images/profile-placeholder.png')
    role = db.Column(db.String(10), nullable=False, default='user')

    def set_password(self, password):
        """Hashes the password using bcrypt and stores the hash."""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        """Checks if the provided password matches the stored bcrypt hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def __repr__(self):
        return f'<User {self.username}>'

    @property
    def json(self):
        return {
            'username': self.username,
            'name': self.name,
            'bio': self.bio,
            'profile_photo': self.profile_photo,
        }
