# backend/controllers/product_controller.py
<<<<<<< HEAD

from backend.services.db_connection import get_collection
from config.env import COLLECTION_PRODUCTS

def get_all_products(limit=100):
    products = get_collection(COLLECTION_PRODUCTS)
    return list(products.find().limit(limit))

def get_products_by_category(category, limit=100):
    products = get_collection(COLLECTION_PRODUCTS)
    return list(products.find({"category": category}).limit(limit))

def search_products(keyword, limit=100):
    products = get_collection(COLLECTION_PRODUCTS)
    return list(products.find({"name": {"$regex": keyword, "$options": "i"}}).limit(limit))
=======
from backend.services.db_connection import get_collection
from config.env import COLLECTION_PRODUCTS
from bson import ObjectId

collection = get_collection(COLLECTION_PRODUCTS)

def _format_product(product):
    """Convierte ObjectId en str para que FastAPI lo pueda devolver."""
    if not product:
        return None
    product["_id"] = str(product["_id"])
    return product

def get_all_products(limit=100):
    products = collection.find().limit(limit)
    return [_format_product(p) for p in products]

def get_products_by_category(category, limit=100):
    products = collection.find({"category": category}).limit(limit)
    return [_format_product(p) for p in products]

def search_products(keyword, limit=100):
    products = collection.find({"name": {"$regex": keyword, "$options": "i"}}).limit(limit)
    return [_format_product(p) for p in products]
>>>>>>> 09544df (Crud de productos)
