# backend/controllers/auth_controller.py

from backend.services.db_connection import get_collection
from config.env import COLLECTION_USERS
from backend.models.user_model import user_schema

def login(email, password):
    users = get_collection(COLLECTION_USERS)
    user = users.find_one({"email": email, "password": password})
    return user  # Retorna dict con rol si existe

def register(email, password, role="cliente"):
    users = get_collection(COLLECTION_USERS)
    if users.find_one({"email": email}):
        return None  # Ya existe
    new_user = user_schema(email, password, role)
    users.insert_one(new_user)
    return new_user
