import uuid
from datetime import datetime
from src.models import BaseModel
from src.database import db

class Post(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_anonym = db.Column(db.Boolean, default=False)
    is_responded = db.Column(db.Boolean, default=False)
    upvotes_count = db.Column(db.Integer, default=0)
    downvotes_count = db.Column(db.Integer, default=0)
    replies_count = db.Column(db.Integer, default=0)
    bookmarks_count = db.Column(db.Integer, default=0)
    engagement_rate = db.Column(db.Float, default=0.0)
    sentimen = db.Column(db.String(50), default="neutral")
    sentimen_score = db.Column(db.Float, default=0.0)

    reply_to = db.Column(db.String(36), db.ForeignKey('post.uuid'), nullable=True)  # Self-reference to uuid
    parent_post = db.relationship('Post', remote_side=[uuid], backref='replies')

    user = db.relationship('User', backref='posts')

    def __repr__(self):
        return f'<Post {self.uuid}>'

    def calculate_engagement(self):
        diff = datetime.utcnow() - self.created_at
        rate = (self.upvotes_count - self.downvotes_count) + self.replies_count + self.bookmarks_count + (int(self.is_responded) * 10)
        rate /= diff.days + 1
        self.engagement_rate = rate

    def calculate_count(self, num, item):
        counts = {
            'upvote': 'upvotes_count',
            'downvote': 'downvotes_count',
            'bookmark': 'bookmarks_count',
            'reply': 'replies_count'
        }
        if item in counts:
            current_value = getattr(self, counts[item])
            if current_value == 0 and num < 0: return
            setattr(self, counts[item], current_value + num)
            self.calculate_engagement()
        db.session.commit()


    @property
    def json(self):
        return {
            'uuid': self.uuid,
            'user': self.user.json if not self.is_anonym else None,
            'content': self.content,
            'is_anonym': self.is_anonym,
            'is_responded': self.is_responded,
            'stats': {
                'upvotes': self.upvotes_count,
                'downvotes': self.downvotes_count,
                'replies': self.replies_count,
                'bookmarks': self.bookmarks_count
            },
            'reply_to': {
                "uuid": self.parent_post.uuid,
                "username": self.parent_post.username if not self.parent_post.is_anonym else None,
            },
            'created_at':self.created_at
        }
