# message_controller.py
from models.Message import Message
from app import socketio
from flask import jsonify
def send_message(data):
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    message = data.get('message')
    Message.save_message(sender_id, receiver_id, message)

    socketio.emit('message_response', {'sender_id': sender_id, 'message': message}, room=receiver_id)

    return {"message": "Message sent successfully"}, 200

def get_messages(user_id):
    messages = Message.get_messages(user_id)
    serialized_messages = [{'sender_id': msg.sender_id, 'message': msg.message} for msg in messages]

    return jsonify(serialized_messages), 200
