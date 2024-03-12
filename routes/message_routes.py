from flask import Blueprint, jsonify, request
from controllers.message_controller import send_message, get_messages

messages_app = Blueprint('messages', __name__)

@messages_app.route('/messages', methods=['POST'])
def handle_message():
    data = request.get_json()
    send_message(data)
    return jsonify({'message': 'Mensagem enviada com sucesso'})

@messages_app.route('/messages/<user_id>', methods=['GET'])
def get_user_messages(user_id):
    messages = get_messages(user_id)

    serialized_messages = [{'sender_id': msg.sender_id, 'message': msg.message} for msg in messages]

    return jsonify(serialized_messages)
