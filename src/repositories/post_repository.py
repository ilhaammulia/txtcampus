from src.models.post import Post
from src.app import db

class PostRepository:

    @staticmethod
    def create_post(user_id, content, is_anonym=False, reply_to=None):
        new_post = Post(user_id=user_id, content=content, is_anonym=is_anonym, reply_to=reply_to)
        db.session.add(new_post)
        db.session.commit()
        return new_post

    @staticmethod
    def get_all_posts(page=1, per_page=5):
        return Post.query.filter_by(reply_to=None).order_by(Post.engagement_rate.desc(), Post.created_at.desc()).paginate(page=page, per_page=per_page)

    @staticmethod
    def get_all_replies(uuid, page=1, per_page=5):
        return Post.query.filter_by(reply_to=uuid).order_by(Post.engagement_rate.desc(), Post.created_at.desc()).paginate(page=page, per_page=per_page)

    @staticmethod
    def get_post_by_uuid(uuid):
        return Post.query.filter_by(uuid=uuid).first()

    @staticmethod
    def search_posts(query, page=1, per_page=5):
        return Post.query.filter(Post.content.like(f'%{query}%')).filter_by(reply_to=None).order_by(Post.engagement_rate.desc(), Post.created_at.desc()).paginate(page=page, per_page=per_page)

    @staticmethod
    def delete_post(post_id):
        post = Post.query.get(post_id)
        if post:
            db.session.delete(post)
            db.session.commit()
            return True
        return False
