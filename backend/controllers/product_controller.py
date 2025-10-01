# backend/controllers/product_controller.py

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
