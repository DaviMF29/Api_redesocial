from models.Post import Post
from flask_jwt_extended import create_access_token  #TALVEZ USE PARA AUTENTICAR ROTAS
from flask import request
from werkzeug.utils import secure_filename
import os

def create_post_controller(user_id, username, text, image_path=None):
    if image_path is None and "image" in request.files:
        image = request.files["image"]
        image_path = save_image(image)
    
    post_id = Post.create_post_model(user_id, username, text, image_path)
    return {"id": str(post_id), "message": f"Post created"}, 201


def get_post_by_id_controller(post_id):                   #importar o método direto de um model quebraria o modelo MVC (!?)
    post = Post.get_post_by_id_model(post_id)
    return post

def get_all_posts_by_user_id_controller(user_id):
    posts = Post.get_posts_by_user_id_model(user_id)
    if not posts:
        return {"message": "No posts from this user"}, 404

    post_data = [{
        "post_id": str(post["_id"]),
        "user_id": post["user_id"],
        "username": post["username"],
        "text": post["text"]
    } for post in posts]

    return post_data, 200


def add_comment_controller(post_id, comment, user_id):
    post = Post.get_post_by_id_model(post_id)
    if not post:
        return {"message": "This post does not exist"}, 404

    post["comments"].append({"comment": comment, "user_id": user_id})
    Post.update_post(post_id, post)
    return {"message": "Comment added successfully"}, 200

def update_likes_count_controller(post_id, action, user_id):
    post = Post.get_post_by_id_model(post_id)
    if not post:
        return {"message": "Post not found"}, 404

    likes = post.get('likes', [])
    if user_id in likes and action == 'increment':
        return {"message": "User already liked this post"}, 400
    
    if user_id not in likes and action == 'decrement':
        return {"message": "User not liked this post"}, 400

    if action == 'increment':
        post["likes_count"] += 1
        post["likes"].append(user_id)
    elif action == 'decrement':
        post["likes_count"] -= 1
        post["likes"].remove(user_id)
    else:
        return {"message": "Invalid action"}, 400

    Post.update_post(post_id, post)
    return {"message": "Like updated successfully"}, 200




#-----------------------------------------------------------------------------#



def save_image(image):
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    filename = secure_filename(image.filename)
    image_path = os.path.join("uploads", filename)
    image.save(image_path)
    
    return image_path