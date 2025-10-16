# backend/controllers/user_controller.py

from backend.services.db_connection import get_collection
from config.env import COLLECTION_USERS
import hashlib
from bson import ObjectId

# Conexión a la colección de usuarios
collection = get_collection(COLLECTION_USERS)


# 🔒 Función para hashear contraseñas
def _hash_password(password: str) -> str:
    """Hashea la contraseña usando SHA256 (lib estándar)."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# 📋 Obtener todos los usuarios
def get_all_users(limit=100):
    users = collection.find({}, {"password": 0}).limit(limit)
    users_list = []
    for user in users:
        user["_id"] = str(user["_id"])
        if "correo" not in user or not user["correo"]:
            if "email" in user and user["email"]:
                user["correo"] = user["email"]
        users_list.append(user)
    return users_list


# ➕ Crear un usuario
def create_user(user_data):
    """Crea un nuevo usuario con contraseña hasheada."""
    try:
        if "password" in user_data and user_data["password"]:
            user_data["password"] = _hash_password(user_data["password"])

        result = collection.insert_one(user_data)
        return str(result.inserted_id)
    except Exception as e:
        raise Exception(f"Error al crear usuario: {e}")


# ✏️ Actualizar un usuario
def update_user(correo, update_data):
    try:
        if "password" in update_data and update_data["password"]:
            update_data["password"] = _hash_password(update_data["password"])

        result = collection.update_one({"correo": correo}, {"$set": update_data})
        return result.modified_count > 0
    except Exception as e:
        raise Exception(f"Error al actualizar usuario: {e}")


def delete_user(correo):
    try:
        result = collection.delete_one({"correo": correo})
        return result.deleted_count > 0
    except Exception as e:
        raise Exception(f"Error al eliminar usuario: {e}")
