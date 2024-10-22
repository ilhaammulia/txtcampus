from src.models import BaseModel
from src.database import db

class Vote(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    vote = db.Column(db.Integer, nullable=False)  # -1 for downvote, +1 for upvote

    user = db.relationship('User', backref='votes')
    post = db.relationship('Post', backref='votes')

    def __repr__(self):
        return f'<Vote {self.vote} for Post {self.post_id}>'

    @property
    def json(self):
        return {
            'user': self.user.json,
            'post': self.post.json,
        }
