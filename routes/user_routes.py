from flask import Flask, request, jsonify, Blueprint
from controllers.user_controller import login, create_user_controller, add_follower_controller,edit_data_user_controller

users_app = Blueprint("users_app", __name__)


@users_app.route("/api/login", methods=["POST"])
def login_route():
    data = request.get_json()
    if "username" not in data or "password" not in data:
        return jsonify({"message": "Missing username or password"}), 400

    username = data["username"]
    password = data["password"]

    response, status_code = login(username, password)
    return jsonify(response), status_code

@users_app.route("/api/users", methods=["POST"])
def create_user_route():
    data = request.get_json()
    if "name" not in data or "username" not in data or "email" not in data or "password" not in data:
        return jsonify({"message": "Missing required fields"}), 400

    name = data["name"]
    username = data["username"]
    email = data["email"]
    password = data["password"]

    response, status_code = create_user_controller(name, username, email, password)
    return jsonify(response), status_code

@users_app.route("/api/users/follow/<string:user_id>", methods=["PATCH"])
def add_follower(user_id):
    data = request.get_json()
    friend_id = data["friend_id"]
    response = add_follower_controller(user_id, friend_id)
    return jsonify(response), 200



@users_app.route("/api/users/edit/<string:user_id>", methods=["PATCH"])
def edit_data_user(user_id):
    data = request.get_json()
    print(data)
    if "field" not in data or "change" not in data:
        return jsonify({"message": "Missing field or change"}), 400
    
    field = data["field"]
    change = data["change"]
    response = edit_data_user_controller(user_id, field, change)
    return jsonify(response),200





