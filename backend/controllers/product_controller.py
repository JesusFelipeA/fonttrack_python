# backend/controllers/product_controller.py

from backend.services.db_connection import get_collection
from config.env import COLLECTION_PRODUCTS
from bson import ObjectId

# Colección global
collection = get_collection(COLLECTION_PRODUCTS)


def _format_product(product):
    """Convierte ObjectId en str para que pueda usarse en frontend o APIs."""
    if not product:
        return None
    product["_id"] = str(product["_id"])
    return product


def get_all_products(limit=100):
    """Obtiene todos los productos (con límite)."""
    products = collection.find().limit(limit)
    return [_format_product(p) for p in products]


def get_products_by_category(category, limit=100):
    """Obtiene productos filtrados por categoría."""
    products = collection.find({"category": category}).limit(limit)
    return [_format_product(p) for p in products]


def search_products(keyword, limit=100):
    """Busca productos cuyo nombre coincida con un keyword (insensible a mayúsculas)."""
    products = collection.find({"name": {"$regex": keyword, "$options": "i"}}).limit(limit)
    return [_format_product(p) for p in products]
