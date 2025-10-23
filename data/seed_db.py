# data/seed_db.py

from backend.services.db_connection import get_collection
import time
import sys
import os
from bson import ObjectId
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configuración
BAR_LENGTH = 50

COLLECTION_LUGARES = "lugares"
COLLECTION_MATERIALES = "materiales"
COLLECTION_FALLAS = "fallas"
COLLECTION_USUARIOS = "usuarios"


# ----------------- FUNCIONES AUXILIARES -----------------
def print_progress(current, total, start_time):
    percent = int((current / total) * 100)
    filled = int(BAR_LENGTH * percent // 100)
    empty = BAR_LENGTH - filled

    # Color visual
    if percent < 30:
        color = "\033[91m"  # rojo
    elif percent < 70:
        color = "\033[93m"  # amarillo
    else:
        color = "\033[92m"  # verde

    bar = f"{color}{'█' * filled}{'░' * empty}\033[0m"
    elapsed = time.time() - start_time
    sys.stdout.write(f"\r{bar} {percent}% - {int(elapsed)}s transcurridos")
    sys.stdout.flush()


# ----------------- DATOS DE EJEMPLO -----------------

def get_lugares():
    return [
        {
            "_id": ObjectId(),
            "nombre": "BONAFONT, CEDIS Toluca Vesta Park",
            "estado": "estado de mexico",
            "created_at": datetime(2025, 6, 5, 16, 14, 47),
            "updated_at": datetime(2025, 6, 5, 16, 14, 51)
        }
    ]


def get_materiales(lugar_id):
    return [
        {
            "_id": ObjectId(),
            "clave_material": "TV13AER",
            "descripcion": "AEROSOL ROJO",
            "generico": "AEROSOL",
            "clasificacion": "CARROCERIA Y PINTURA",
            "existencia": 1,
            "costo_promedio": 121.15,
            "lugar_id": lugar_id,
            "created_at": datetime(2025, 7, 14, 10, 7, 53),
            "updated_at": datetime(2025, 8, 18, 0, 40, 29)
        },
        {
            "_id": ObjectId(),
            "clave_material": "TV13AEV",
            "descripcion": "AEROSOL VERDE",
            "generico": "AEROSOL",
            "clasificacion": "CARROCERIA Y PINTURA",
            "existencia": 0,
            "costo_promedio": 30.40,
            "lugar_id": lugar_id,
            "created_at": datetime(2025, 7, 14, 10, 7, 53),
            "updated_at": datetime(2025, 8, 12, 22, 1, 5)
        }
    ]


def get_usuarios():
    return [
        {
            "_id": ObjectId(),
            "nombre": "gustavo cid",
            "correo": "al222310413@bonafont.com",
            "rol": "admin",
            "password": "123456",  
            "created_at": datetime(2025, 6, 5, 16, 14, 47)
        },
        {
            "_id": ObjectId(),
            "nombre": "Daniela",
            "correo": "al222311245@bonafont.com",
            "rol": "usuario",
            "password": "123456",
            "created_at": datetime(2025, 6, 6, 12, 0, 0)
        }
    ]


def get_fallas(lugar_id, usuarios, materiales):
    return [
        {
            "_id": ObjectId(),
            "lugar_id": lugar_id,
            "usuario_reporta": {
                "id": usuarios[1]["_id"],
                "nombre": usuarios[1]["nombre"],
                "correo": usuarios[1]["correo"]
            },
            "usuario_revisa": {
                "id": usuarios[0]["_id"],
                "nombre": usuarios[0]["nombre"],
                "correo": usuarios[0]["correo"]
            },
            "vehiculo": {
                "eco": "ECO123",
                "placas": "ABC123",
                "marca": "Toyota",
                "anio": "2017",
                "km": "56799"
            },
            "fecha": datetime(2025, 8, 11),
            "nombre_conductor": "Jaime",
            "descripcion": "Motor no arranca",
            "observaciones": "Cambio de batería",
            "reviso_por": "gustavo",
            "materiales_usados": [
                {
                    "id_material": materiales[0]["_id"],
                    "nombre": materiales[0]["descripcion"],
                    "cantidad": 1
                }
            ],
            "autorizado_por": "Jesus Felipe Aviles",
            "correo_destino": "al222310413@bonafont.com",
            "created_at": datetime(2025, 8, 12, 22, 14, 24),
            "updated_at": datetime(2025, 8, 12, 22, 14, 24)
        }
    ]


# ----------------- FUNCIONES DE SEED -----------------

def seed_lugares():
    col = get_collection(COLLECTION_LUGARES)
    col.drop()
    lugares = get_lugares()
    col.insert_many(lugares)
    print("🏢 Lugares insertados:", len(lugares))
    return lugares


def seed_materiales(lugar):
    col = get_collection(COLLECTION_MATERIALES)
    col.drop()
    materiales = get_materiales(lugar["_id"])
    col.insert_many(materiales)
    print("🧱 Materiales insertados:", len(materiales))
    return materiales


def seed_usuarios():
    col = get_collection(COLLECTION_USUARIOS)
    col.drop()
    usuarios = get_usuarios()
    col.insert_many(usuarios)
    print("👤 Usuarios insertados:", len(usuarios))
    return usuarios


def seed_fallas(lugar, usuarios, materiales):
    col = get_collection(COLLECTION_FALLAS)
    col.drop()
    fallas = get_fallas(lugar["_id"], usuarios, materiales)
    col.insert_many(fallas)
    print("⚙️ Fallas insertadas:", len(fallas))
    return fallas


# ----------------- EJECUCIÓN -----------------
if __name__ == "__main__":
    print("🚀 Iniciando carga de base MongoDB...")

    start = time.time()
    lugares = seed_lugares()
    materiales = seed_materiales(lugares[0])
    usuarios = seed_usuarios()
    fallas = seed_fallas(lugares[0], usuarios, materiales)

    print(f"\n✅ Base cargada correctamente en {round(time.time() - start, 2)}s")
