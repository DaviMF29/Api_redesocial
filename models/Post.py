from pymongo import MongoClient
from bson import ObjectId
import os

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database(os.getenv("MONGODB_DBNAME"))

class Post:
    @staticmethod
    def create_post_model(user_id, username, text=None, image_path=None):
        posts_collection = db.posts
        new_post = {
            "user_id": user_id,
            "username": username,
            "text": text,
            "image_path": image_path,
            "comments": [],
            "likes_count": 0,
            "likes": []
        }
        result = posts_collection.insert_one(new_post)
        return str(result.inserted_id)


    @staticmethod
    def get_post_by_id_model(post_id):
        posts_collection = db.posts
        post = posts_collection.find_one({"_id": ObjectId(post_id)})
        return post
    
    @staticmethod 
    def get_posts_by_user_id_model(user_id):
        posts_collection = db.posts
        post = posts_collection.find({"user_id":user_id})
        return post
    
    @staticmethod
    def update_post(post_id, updated_fields):
        posts_collection = db.posts
        result = posts_collection.update_one({"_id": ObjectId(post_id)}, {"$set": updated_fields})
        return result
