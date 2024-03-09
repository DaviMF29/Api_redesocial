from models.Notification import Notification
from flask_jwt_extended import create_access_token  #TALVEZ USE PARA AUTENTICAR ROTAS


def create_notification(user_id, type_of_notification, user_receiver_id):
    notification_id = Notification.create_notification(user_id,type_of_notification,user_receiver_id)
    return {"id":notification_id,"message": f"Notification {type_of_notification} created"},201


def get_notifications_by_user_id(user_id):
    notification = Notification.get_notifications(user_id)
    return notification