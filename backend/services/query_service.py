# backend/services/query_service.py

from backend.services.db_connection import get_collection
from config.env import COLLECTION_PRODUCTS

def get_paginated_products(page=1, limit=50):
    skip = (page - 1) * limit
    products = get_collection(COLLECTION_PRODUCTS)
    return list(products.find().skip(skip).limit(limit))

def filter_by_category(category, page=1, limit=50):
    skip = (page - 1) * limit
    products = get_collection(COLLECTION_PRODUCTS)
    return list(products.find({"category": category}).skip(skip).limit(limit))

def search_by_name(keyword, page=1, limit=50):
    skip = (page - 1) * limit
    products = get_collection(COLLECTION_PRODUCTS)
    return list(products.find({"name": {"$regex": keyword, "$options": "i"}}).skip(skip).limit(limit))
