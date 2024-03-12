from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONDODB_URI"))
db = client.get_database(os.getenv("MONGODB_DBNAME"))
class Message:
    @staticmethod
    def save_message(sender_id, receiver_id, message):
        messages_collection = db.messages
        messages_collection.insert_one({
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "message": message
        })

    @staticmethod
    def get_messages(user_id):
        messages_collection = db.messages
        messages = messages_collection.find({
            "$or": [{"sender_id": user_id}, {"receiver_id": user_id}]
        })
        return list(messages)
