# backend/controllers/user_controller.py

from backend.services.db_connection import get_collection
from config.env import COLLECTION_USERS

def get_all_users():
    users = get_collection(COLLECTION_USERS)
    return list(users.find({}, {"password": 0}))  # Oculta contraseñas

def delete_user(email):
    users = get_collection(COLLECTION_USERS)
    return users.delete_one({"email": email})
