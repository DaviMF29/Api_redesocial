from models.User import User
import bcrypt
import base64
from flask_jwt_extended import create_access_token

def login(username, password):
    user = User.get_user_by_username_model(username)
    if user and bcrypt.checkpw(password.encode(), base64.b64decode(user["password"])):
        access_token = create_access_token(identity=username)
        return {"access_token": access_token}, 200
    else:
        return {"message": "Invalid username or password"}, 401
    

def create_user_controller(name, username, email, password):
    user = User.get_user_by_email_model(email)
    if user:
        return {"message": "User already created"}, 400
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(10))
    hashed_password_base64 = base64.b64encode(hashed_password).decode()
    user_id = User.create_user_model(name, username, email, hashed_password_base64)
    return {"id": user_id, "message": f"User {username} created"}, 201

def add_follower_controller(user_id, friend_id):                                       
    user = User.get_user_by_id_model(user_id)
    friend = User.get_user_by_id_model(friend_id)
    
    if not user or not friend:
        return {"message": "Some user with this id does not exist"}, 404
    
    user["following"].append(friend_id)
    friend["followers"].append(user_id)
    User.update_user(user_id, user)
    User.update_user(friend_id, friend)
    return {"message": "Friendship initialized"}, 200

