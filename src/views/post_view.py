from flask import Blueprint, jsonify, request, g
from src.middlewares.auth import auth_required
from src.services.post_service import PostService

post_blueprint = Blueprint('post', __name__)

@post_blueprint.route('/', methods=['GET'], endpoint='get_posts')
@auth_required
def get_posts():
    page = int(request.args.get('page', 1) or 1)
    per_page = int(request.args.get('per_page', 5) or 5)

    user_id = g.current_user.id or None
    username = g.current_user.username or None

    query = request.args.get('username')

    try:
        if query:
            posts = PostService.get_all_posts_by_user(query, page, per_page)
        else:
            posts = PostService.get_all_posts(page, per_page)
        data = []
        for post in posts:
            data.append({
                **post.json,
                'is_upvoted': any(vote.user_id == user_id and vote.vote == 1 for vote in post.votes),
                'is_downvoted': any(vote.user_id == user_id and vote.vote == -1 for vote in post.votes),
                'is_bookmarked': any(bookmark.user_id == user_id for bookmark in post.bookmarks),
                'is_replied': any(reply.reply_to and reply.json['reply_to']['username'] == username for reply in post.replies),
                'sentimen': post.sentimen if g.current_user.role == 'admin' else None,
                'sentimen_score': post.sentimen_score if g.current_user.role == 'admin' else None,
            })
        return jsonify({'success': True, 'message': None, 'data': {'posts': data, 'pagination': {'page': posts.page, 'per_page': posts.per_page, 'total_items': posts.total, 'total_pages': posts.pages}}})
    except:
        return jsonify({'success': True, 'message': None, 'data': {'posts': [], 'pagination': {'page': page, 'per_page': per_page, 'total_items': 0, 'total_pages': 0}}})

@post_blueprint.route('/search', methods=['GET'], endpoint='search')
@auth_required
def search():
    page = int(request.args.get('page', 1) or 1)
    per_page = int(request.args.get('per_page', 5) or 5)

    query = request.args.get('search', '')
    search_type = request.args.get('search_type', 'posts')

    try:
        data = PostService.search(query, search_type, page, per_page)
        return jsonify({'success': True, 'message': None, 'data': {'items': [item.json for item in data.items], 'pagination': {'page': data.page, 'per_page': data.per_page, 'total_items': data.total, 'total_pages': data.pages}}})
    except:
        return jsonify({'success': True, 'message': None, 'data': {'items': [], 'pagination': {'page': page, 'per_page': per_page, 'total_items': 0, 'total_pages': 0}}})

@post_blueprint.route('/<string:uuid>', methods=['GET'], endpoint='get_post')
@auth_required
def get_post(uuid):
    post = PostService.get_post_by_uuid(uuid)
    user_id = g.current_user.id or None
    username = g.current_user.username or None
    if post:
        post = {
            **post.json,
            'is_upvoted': any(vote.user_id == user_id and vote.vote == 1 for vote in post.votes),
            'is_downvoted': any(vote.user_id == user_id and vote.vote == -1 for vote in post.votes),
            'is_bookmarked': any(bookmark.user_id == user_id for bookmark in post.bookmarks),
            'is_replied': any(reply.reply_to and reply.json['reply_to']['username'] == username for reply in post.replies),
            'sentimen': post.sentimen if g.current_user.role == 'admin' else None,
            'sentimen_score': post.sentimen_score if g.current_user.role == 'admin' else None,
        }
        return jsonify({'success': True, 'message': None, 'data': post})
    return jsonify({'success': False, 'message': 'Post not found', 'data': None}), 404

@post_blueprint.route('/', methods=['POST'], endpoint='create_post')
@auth_required
def create_post():
    data = request.get_json()
    user_id = g.current_user.id or None
    username = g.current_user.username or None
    is_official = data.get('is_official') if g.current_user.role == 'admin' else False

    new_post = PostService.create_post(user_id=g.current_user.id, content=data['content'], is_anonym=data.get('is_anonym', False), reply_to=data.get('reply_to'), is_official=is_official)
    new_post = {
        **new_post.json,
        'is_upvoted': any(vote.user_id == user_id and vote.vote == 1 for vote in new_post.votes),
        'is_downvoted': any(vote.user_id == user_id and vote.vote == -1 for vote in new_post.votes),
        'is_bookmarked': any(bookmark.user_id == user_id for bookmark in new_post.bookmarks),
        'is_replied': any(reply.reply_to and reply.json['reply_to']['username'] == username for reply in new_post.replies),
        'sentimen': new_post.sentimen if g.current_user.role == 'admin' else None,
        'sentimen_score': new_post.sentimen_score if g.current_user.role == 'admin' else None,
    }
    return jsonify({'success': True, 'message': 'Post created successfully', 'data': new_post}), 201

@post_blueprint.route('/<string:uuid>/replies', methods=['GET'], endpoint='get_replies')
@auth_required
def get_replies(uuid):
    page = int(request.args.get('page', 1) or 1)
    per_page = int(request.args.get('per_page', 5) or 5)
    user_id = g.current_user.id or None
    username = g.current_user.username or None
    try:
        posts = PostService.get_all_replies(uuid, page, per_page)
        data = []
        for post in posts:
            data.append({
                **post.json,
                'is_upvoted': any(vote.user_id == user_id and vote.vote == 1 for vote in post.votes),
                'is_downvoted': any(vote.user_id == user_id and vote.vote == -1 for vote in post.votes),
                'is_bookmarked': any(bookmark.user_id == user_id for bookmark in post.bookmarks),
                'is_replied': any(reply.reply_to and reply.json['reply_to']['username'] == username for reply in post.replies),
                'sentimen': post.sentimen if g.current_user.role == 'admin' else None,
                'sentimen_score': post.sentimen_score if g.current_user.role == 'admin' else None,
            })
        return jsonify({'success': True, 'message': None, 'data': {'posts': data, 'pagination': {'page': posts.page, 'per_page': posts.per_page, 'total_items': posts.total, 'total_pages': posts.pages}}})
    except:
        return jsonify({'success': True, 'message': None, 'data': {'replies': [], 'pagination': {'page': page, 'per_page': per_page, 'total_items': 0, 'total_pages': 0}}})

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

@post_blueprint.route('/<string:username>/bookmarks', methods=['GET'], endpoint='bookmark_get')
@auth_required
def get_bookmarks(username):
    page = int(request.args.get('page', 1) or 1)
    per_page = int(request.args.get('per_page', 5) or 5)
    user_id = g.current_user.id or None
    current_username = g.current_user.username or None
    try:
        if username != username:
            raise Exception
        posts = PostService.get_bookmarks(current_username, page, per_page)
        data = []
        for post in posts:
            data.append({
                **post.json,
                'is_upvoted': any(vote.user_id == user_id and vote.vote == 1 for vote in post.votes),
                'is_downvoted': any(vote.user_id == user_id and vote.vote == -1 for vote in post.votes),
                'is_bookmarked': any(bookmark.user_id == user_id for bookmark in post.bookmarks),
                'is_replied': any(reply.reply_to and reply.json['reply_to']['username'] == username for reply in post.replies),
                'sentimen': post.sentimen if g.current_user.role == 'admin' else None,
                'sentimen_score': post.sentimen_score if g.current_user.role == 'admin' else None,
            })
        return jsonify({'success': True, 'message': None, 'data': {'posts': data, 'pagination': {'page': posts.page, 'per_page': posts.per_page, 'total_items': posts.total, 'total_pages': posts.pages}}})
    except Exception as err:
        return jsonify({'success': True, 'message': None, 'data': {'posts': [], 'pagination': {'page': page, 'per_page': per_page, 'total_items': 0, 'total_pages': 0}}})

@post_blueprint.route('/<string:uuid>/replies', methods=['POST'], endpoint='reply_post')
@auth_required
def reply_post(uuid):
    data = request.get_json()
    new_post = PostService.create_post(user_id=g.current_user.id, content=data['content'], is_anonym=data.get('is_anonym', False), reply_to=uuid)
    return jsonify({'success': True, 'message': None, 'data': {'message': 'Post created successfully', 'uuid': new_post.uuid}}), 201
