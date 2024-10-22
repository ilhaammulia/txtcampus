from src.models.bookmark import Bookmark
from src.app import db

class BookmarkRepository:

    @staticmethod
    def create_bookmark(user_id, post_id):
        bookmark = Bookmark(user_id=user_id, post_id=post_id)
        db.session.add(bookmark)
        db.session.commit()
        return bookmark

    @staticmethod
    def delete_bookmark(bookmark_id):
        bookmark = Bookmark.query.get(bookmark_id)
        db.session.delete(bookmark)
        db.session.commit()
        return True

    @staticmethod
    def get_bookmark(user_id, post_id):
        return Bookmark.query.filter_by(user_id=user_id, post_id=post_id).first()

    @staticmethod
    def get_bookmarks_by_user(user_id):
        return Bookmark.query.filter_by(user_id=user_id).all()
