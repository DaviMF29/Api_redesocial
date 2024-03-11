from pymongo import MongoClient
import os
from enum import Enum

client = MongoClient(os.getenv("MONDODB_URI"))
db = client.get_database(os.getenv("MONGODB_DBNAME"))

class NotificationType(Enum):
    FRIEND_REQUEST = "friend_request"
    MESSAGE_RECEIVED = "message_received"
    POST_LIKED = "post_liked"
    POST_COMMENTED = "post_commented"
    LONG_TIME_NO_POST = "user_no_posting"

class Notification:

    @staticmethod
    def create_notification(user_id, type_of_notification, user_receiver_id, sender_id=None, post_id=None):
        if type_of_notification not in NotificationType.__members__:
            return {"message": "Invalid notification type"}, 400

        notifications_collection = db.notification
        new_notification = {
            "user_id": user_id,
            "type_of_notification": type_of_notification,
            "user_receiver_id": user_receiver_id,
            "sender_id": sender_id,
            "post_id": post_id,
            "notifications": [],
        }

        result = notifications_collection.insert_one(new_notification)
        return str(result.inserted_id), 201

    @staticmethod
    def get_notifications(user_id):
        notification_collection = db.notifications
        notification = notification_collection.find({"user_id":user_id})
        return notification
