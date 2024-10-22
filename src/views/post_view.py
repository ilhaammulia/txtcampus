from flask import Blueprint, jsonify, request, g
from src.middlewares.auth import auth_required
from src.services.post_service import PostService

post_blueprint = Blueprint('post', __name__)

@post_blueprint.route('/', methods=['GET'], endpoint='get_posts')
@auth_required
def get_posts():
    page = int(request.args.get('page', 1) or 1)
    per_page = int(request.args.get('per_page', 5) or 5)

    posts = PostService.get_all_posts(page, per_page)
    return jsonify({'success': True, 'message': None, 'data': {'posts': [post.json for post in posts.items], 'pagination': {'page': posts.page, 'per_page': posts.per_page, 'total_items': posts.total, 'total_pages': posts.pages}}})

@post_blueprint.route('/<string:uuid>', methods=['GET'], endpoint='get_post')
@auth_required
def get_post(uuid):
    post = PostService.get_post_by_uuid(uuid)
    if post:
        return jsonify({'success': True, 'message': None, 'data': post.json})
    return jsonify({'success': False, 'message': 'Post not found', 'data': None}), 404

@post_blueprint.route('/', methods=['POST'], endpoint='create_post')
@auth_required
def create_post():
    data = request.get_json()
    new_post = PostService.create_post(user_id=g.current_user.id, content=data['content'], is_anonym=data.get('is_anonym', False), reply_to=data.get('reply_to'))
    return jsonify({'success': True, 'message': 'Post created successfully', 'data': new_post.json}), 201

@post_blueprint.route('/<string:uuid>/replies', methods=['GET'], endpoint='get_replies')
@auth_required
def get_replies(uuid):
    page = int(request.args.get('page', 1) or 1)
    per_page = int(request.args.get('per_page', 5) or 5)

    posts = PostService.get_all_replies(uuid, page, per_page)
    return jsonify({'success': True, 'message': None, 'data': {'replies': [post.json for post in posts.items], 'pagination': {'page': posts.page, 'per_page': posts.per_page, 'total_items': posts.total, 'total_pages': posts.pages}}})

@post_blueprint.route('/<string:uuid>', methods=['DELETE'], endpoint='delete_post')
@auth_required
def delete_post(uuid):
    success = PostService.delete_post(uuid)
    if success:
        return jsonify({'success': True, 'message': 'Post deleted successfully', 'data': None})
    return jsonify({'success': False, 'message': 'Post not found', 'data': None}), 404

@post_blueprint.route('/<string:uuid>/votes', methods=['POST'], endpoint='vote_post')
@auth_required
def vote_post(uuid):
    data = request.get_json()
    vote = PostService.vote_post(g.current_user.id, uuid, data['vote'])
    if vote:
        return jsonify({'success': True, 'message': 'Post voted successfully', 'data': None}), 200
    return jsonify({'success': False, 'message': 'Vote failed', 'data': None}), 400

@post_blueprint.route('/<string:uuid>/bookmarks', methods=['POST'], endpoint='bookmark_post')
@auth_required
def bookmark_post(uuid):
    bookmark = PostService.bookmark_post(g.current_user.id, uuid)
    if bookmark:
        return jsonify({'success': True, 'message': 'Post bookmarked successfully', 'data': None}), 200
    return jsonify({'success': False, 'message': 'Bookmark failed', 'data': None}), 400

@post_blueprint.route('/<string:uuid>/replies', methods=['POST'], endpoint='reply_post')
@auth_required
def reply_post(uuid):
    data = request.get_json()
    new_post = PostService.create_post(user_id=g.current_user.id, content=data['content'], is_anonym=data.get('is_anonym', False), reply_to=uuid)
    return jsonify({'success': True, 'message': None, 'data': {'message': 'Post created successfully', 'uuid': new_post.uuid}}), 201
