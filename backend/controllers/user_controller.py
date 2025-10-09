# backend/controllers/user_controller.py

from backend.services.db_connection import get_collection
from config.env import COLLECTION_USERS
import hashlib

collection = get_collection(COLLECTION_USERS)


def _hash_password(password: str) -> str:
    """Hashea la contraseña usando SHA256 (lib estándar)."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_all_users(limit=100):
    """Obtiene todos los usuarios (sin contraseñas)."""
    users = collection.find({}, {"password": 0}).limit(limit)
    return list(users)


def create_user(user_data):
    """Crea un nuevo usuario con contraseña hasheada."""
    if "password" in user_data and user_data["password"]:
        user_data["password"] = _hash_password(user_data["password"])

    result = collection.insert_one(user_data)
    return str(result.inserted_id)


def update_user(email, update_data):
    """Actualiza un usuario por email."""
    if "password" in update_data and update_data["password"]:
        update_data["password"] = _hash_password(update_data["password"])

    result = collection.update_one({"email": email}, {"$set": update_data})
    return result.modified_count > 0


def delete_user(email):
    """Elimina un usuario por su email."""
    result = collection.delete_one({"email": email})
    return result.deleted_count > 0
