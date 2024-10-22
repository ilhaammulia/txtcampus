from src.models.vote import Vote
from src.app import db

class VoteRepository:

    @staticmethod
    def create_vote(user_id, post_id, vote_value):
        vote = Vote(user_id=user_id, post_id=post_id, vote=vote_value)
        db.session.add(vote)
        db.session.commit()
        return vote

    @staticmethod
    def update_vote(vote_id, vote_value):
        vote = Vote.query.get(vote_id)
        vote.vote = vote_value
        db.session.commit()
        return vote

    @staticmethod
    def delete_vote(vote_id):
        vote = Vote.query.get(vote_id)
        db.session.delete(vote)
        db.session.commit()
        return True

    @staticmethod
    def get_vote(user_id, post_id):
        return Vote.query.filter_by(user_id=user_id, post_id=post_id).first()

    @staticmethod
    def get_votes_by_post(post_id):
        return Vote.query.filter_by(post_id=post_id).all()
