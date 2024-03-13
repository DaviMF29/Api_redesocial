from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO, emit
from routes.post_routes import posts_app
from routes.user_routes import users_app
import os
from pymongo import MongoClient


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
jwt = JWTManager(app)
socketio = SocketIO(app)

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database(os.getenv("MONGODB_DBNAME"))
# Registrar as rotas do Blueprint dos posts
app.register_blueprint(posts_app)
app.register_blueprint(users_app)

@socketio.on('message')
def handle_message(data):
    messages_collection = db.messages
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    message = data.get('message')
    time = data.get('time')

    # Salva a mensagem no banco de dados
    messages_collection.insert_one({
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'message': message,
        'time':time
    })

    # Emite uma mensagem de confirmação para o remetente
    emit('message_response', {'sender_id': sender_id, 'message': message}, room=sender_id)

    # Emite a mensagem para o destinatário
    emit('message_response', {'sender_id': sender_id, 'message': message}, room=receiver_id)

@app.route('/messages/send', methods=['POST'])
def send_message():
    messages_collection = db.messages

    data = request.get_json()
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    message = data.get('message')
    time = data.get('time')

    
    if not sender_id or not receiver_id or not message:
        return jsonify({'error': 'Missing required fields'}), 400

    # Salva a mensagem no banco de dados
    messages_collection.insert_one({
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'message': message,
        'time':time
    })

    # Emite um evento 'message' para enviar a mensagem para o destinatário
    socketio.emit('message', {'sender_id': sender_id, 'message': message}, room=receiver_id)

    return jsonify({'message': 'Message sent successfully'}), 200

if __name__ == "__main__":
    socketio.run(app)
