# data/seed_db.py

from backend.services.db_connection import get_collection
from data.generate_products import generate_bulk_products
from config.env import COLLECTION_PRODUCTS, COLLECTION_USERS
from backend.models.user_model import user_schema
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configuración visual
TOTAL = 500_000
BATCH_SIZE = 5000
BAR_LENGTH = 50

def print_progress(current, total, start_time):
    percent = int((current / total) * 100)
    filled = int(BAR_LENGTH * percent // 100)
    empty = BAR_LENGTH - filled

    # Color según avance
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

def seed_products():
    collection = get_collection(COLLECTION_PRODUCTS)
    collection.drop()

    print("🛒 Insertando productos...")
    start = time.time()
    inserted = 0

    for batch in generate_bulk_products(TOTAL, BATCH_SIZE):
        collection.insert_many(batch)
        inserted += BATCH_SIZE
        print_progress(inserted, TOTAL, start)

    print(f"\n✅ Productos insertados: {TOTAL} en {round(time.time() - start, 2)} segundos")

def seed_users():
    collection = get_collection(COLLECTION_USERS)
    collection.drop()

    print("👤 Insertando usuarios...")
    users = [
        user_schema(email=f"user{i}@tienda.com", password="123456", role="cliente")
        for i in range(1, 101)
    ]
    users.append(user_schema(email="admin@tienda.com", password="123456", role="admin"))
    collection.insert_many(users)
    print("✅ Usuarios insertados: 100 clientes + 1 admin")

if __name__ == "__main__":
    seed_users()
    seed_products()
