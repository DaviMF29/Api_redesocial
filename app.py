from flask import Flask
from flask_jwt_extended import JWTManager
from routes.user_routes import users_app
import os

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
jwt = JWTManager(app)

# Registrar as rotas do Blueprint dos posts
app.register_blueprint(users_app)

if __name__ == "__main__":
    app.run()
