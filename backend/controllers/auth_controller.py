from backend.services.db_connection import get_collection
from config.env import COLLECTION_USERS
import hashlib

def _hash_password(password: str) -> str:
    """Hashea la contraseña usando SHA256."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

# ========================================
# CRUD DE USUARIOS
# ========================================
def get_all_users():
    users = get_collection(COLLECTION_USERS)
    data = list(users.find())
    for u in data:
        u["_id"] = str(u["_id"])
        u.pop("password", None)
    return data

def create_user(data):
    users = get_collection(COLLECTION_USERS)
    correo = data.get("correo")
    role = data.get("role", "user")
    password = data.get("password")

    if not correo or not password:
        raise ValueError("El correo y la contraseña son obligatorios.")

    if users.find_one({"correo": correo}):
        raise ValueError("El correo ya está registrado.")

    hashed = _hash_password(password)
    new_user = {
        "correo": correo,
        "role": role,
        "password": hashed
    }
    users.insert_one(new_user)
    return new_user

def update_user(correo, data):
    users = get_collection(COLLECTION_USERS)
    if not users.find_one({"correo": correo}):
        raise ValueError("Usuario no encontrado.")

    update_data = {}
    if "correo" in data:
        update_data["correo"] = data["correo"]
    if "role" in data:
        update_data["role"] = data["role"]
    if "password" in data and data["password"]:
        update_data["password"] = _hash_password(data["password"])

    users.update_one({"correo": correo}, {"$set": update_data})
    return True

def delete_user(correo):
    users = get_collection(COLLECTION_USERS)
    users.delete_one({"correo": correo})
    return True

# ========================================
# AUTENTICACIÓN
# ========================================

def login(correo: str, password: str):
    """Verifica las credenciales del usuario y actualiza contraseñas antiguas sin hash."""
    users = get_collection(COLLECTION_USERS)
    user = users.find_one({"correo": correo})
    if not user:
        raise ValueError("Usuario no encontrado.")

    hashed = _hash_password(password)
    stored_password = user.get("password")

    # ✅ Aceptar contraseñas antiguas sin hash
    if stored_password == password:
        # Actualizar automáticamente a hash
        users.update_one({"_id": user["_id"]}, {"$set": {"password": hashed}})
        stored_password = hashed

    # ❌ Si no coincide ni en texto plano ni en hash
    if stored_password != hashed:
        raise ValueError("Contraseña incorrecta.")

    # Limpieza antes de devolver
    user["_id"] = str(user["_id"])
    user.pop("password", None)
    return user


def register(correo: str, password: str, role: str = "user"):
    """Registra un nuevo usuario (siempre guarda contraseña hasheada)."""
    data = {
        "correo": correo,
        "password": _hash_password(password),
        "role": role
    }
    return create_user(data)
