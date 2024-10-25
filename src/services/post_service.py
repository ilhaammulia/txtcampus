from src.repositories.user_repository import UserRepository
from src.repositories.post_repository import PostRepository
from src.repositories.vote_repository import VoteRepository
from src.repositories.bookmark_repository import BookmarkRepository
from src.error import NotFoundError

class PostService:

    @staticmethod
    def search(query, type, page=1, per_page=5):
        if type == 'posts':
            return PostRepository.search_posts(query, page, per_page)
        return UserRepository.search_users(query, page, per_page)

    @staticmethod
    def create_post(user_id, content, is_anonym=False, reply_to=None):
        parent = PostRepository.get_post_by_uuid(reply_to)
        if reply_to and not parent:
            NotFoundError("Post not found")
        if parent: parent.calculate_count(1, 'reply')
        return PostRepository.create_post(user_id, content, is_anonym, reply_to)

    @staticmethod
    def get_all_posts(page=1, per_page=5):
        return PostRepository.get_all_posts(page, per_page)

    @staticmethod
    def get_all_replies(uuid, page=1, per_page=5):
        return PostRepository.get_all_replies(uuid, page, per_page)

    @staticmethod
    def get_post_by_uuid(uuid):
        return PostRepository.get_post_by_uuid(uuid)

    @staticmethod
    def delete_post(uuid):
        post = PostService.get_post_by_uuid(uuid)
        if not post:
            NotFoundError("Post not found")
        if post.parent_post:
            post.parent_post.calculate_count(-1, 'reply')
        return PostRepository.delete_post(post.id)

    @staticmethod
    def vote_post(user_id, post_uuid, vote_value):
        post = PostService.get_post_by_uuid(post_uuid)
        if not post:
            NotFoundError("Post not found")

        vote = VoteRepository.get_vote(user_id, post.id)
        if vote and vote.vote == vote_value:
            post.calculate_count(-1, 'upvote' if vote.vote == 1 else 'downvote')
            return VoteRepository.delete_vote(vote.id)
        elif vote:
            post.calculate_count(-1, 'upvote' if vote.vote == 1 else 'downvote')
            post.calculate_count(1, 'upvote' if vote_value == 1 else 'downvote')
            return VoteRepository.update_vote(vote.id, vote_value)
        else:
            post.calculate_count(1, 'upvote' if vote_value == 1 else 'downvote')
            return VoteRepository.create_vote(user_id, post.id, vote_value)

    @staticmethod
    def bookmark_post(user_id, post_uuid):
        post = PostService.get_post_by_uuid(post_uuid)
        if not post:
            NotFoundError("Post not found")

        bookmark = BookmarkRepository.get_bookmark(user_id, post.id)
        if bookmark:
            post.calculate_count(-1, 'bookmark')
            return BookmarkRepository.delete_bookmark(bookmark.id)
        post.calculate_count(1, 'bookmark')
        return BookmarkRepository.create_bookmark(user_id, post.id)
