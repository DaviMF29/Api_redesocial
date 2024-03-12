from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO, emit
from routes.post_routes import posts_app
from routes.user_routes import users_app
from routes.message_routes import messages_app
import os

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
jwt = JWTManager(app)
socketio = SocketIO(app)

# Registrar as rotas do Blueprint dos posts
app.register_blueprint(posts_app)
app.register_blueprint(users_app)
app.register_blueprint(messages_app)



if __name__ == "__main__":
    socketio.run(app)
