from src.models.user import User
from src.database import db

def create_admin():
    username = "admin"
    password = "password"

    if not User.query.filter_by(username=username).first():
        user = User(username=username, name="Universitas Jenderal Achmad Yani Yogyakarta", email_address="admin@admin.com", bio="Akun resmi Unjaya", role="admin")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
