# backend/models/user_model.py
from datetime import datetime

def user_schema(email, password, role="cliente"):
    return {
        "email": email,
        "password": password,  # En producción: usar hash
        "role": role,          # "admin" o "cliente"
        "created_at": datetime.utcnow()
    }
