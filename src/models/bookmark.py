from src.models import BaseModel
from src.database import db

class Bookmark(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    user = db.relationship('User', backref='bookmarks')
    post = db.relationship('Post', backref='bookmarks')

    def __repr__(self):
        return f'<Bookmark by User {self.user_id} for Post {self.post_id}>'
