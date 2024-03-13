from flask import Blueprint, request, jsonify
from controllers.post_controller import add_comment_controller, update_likes_count_controller, create_post_controller, get_post_by_id_controller,delete_post_controller, delete_all_posts_from_user_id_controller

posts_app = Blueprint("posts_app", __name__)

@posts_app.route("/api/post/comment/<string:post_id>", methods=["PATCH"])
def add_comment_route(post_id):
    data = request.get_json()
    if "comment" not in data or "user_id" not in data:
        return jsonify({"message": "Missing comment field"}), 400

    comment = data["comment"]
    user_id = data["user_id"]

    response, status_code = add_comment_controller(post_id, comment, user_id)
    return jsonify(response), status_code

@posts_app.route("/api/post/like/<post_id>", methods=["PATCH"])
def update_likes_count_route(post_id):
    data = request.get_json()
    if "action" not in data or "user_id" not in data:
        return jsonify({"message": "Missing action or user_id field"}), 400

    action = data["action"]
    user_id = data["user_id"]

    response, status_code = update_likes_count_controller(post_id, action, user_id)
    return jsonify(response), status_code

@posts_app.route("/api/post", methods=["POST"])
def create_post_route():
    data = request.get_json()

    if "user_id" not in data or "username" not in data:
        return jsonify({"message": "Missing required fields"}), 400

    user_id = data["user_id"]
    username = data["username"]
    text = data.get("text")
    image_path = data.get("image_path")

    response, status_code = create_post_controller(user_id, username, text, image_path)
    return jsonify(response), status_code


@posts_app.route("/api/post/<string:post_id>", methods=["GET"])
def get_post_by_id_route(post_id):
    response, status_code = get_post_by_id_controller(post_id)
    return jsonify(response), status_code


@posts_app.route("/api/posts/<string:post_id>",methods=["DELETE"])
def delete_post_by_id_route(post_id):
    response = delete_post_controller(post_id)
    return jsonify(response)

@posts_app.route("/api/post/deleteAllFromUser/<string:user_id>",methods=["DELETE"])
def delete_all_posts_from_user_id(user_id):
    response = delete_all_posts_from_user_id_controller(user_id)
    return jsonify(response)
