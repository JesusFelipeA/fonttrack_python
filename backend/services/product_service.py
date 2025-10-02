from backend.services.db_connection import get_collection
from config.env import COLLECTION_PRODUCTS
from bson import ObjectId

collection = get_collection(COLLECTION_PRODUCTS)

def get_all_products(limit=50):
    products = list(collection.find().sort("_id", -1).limit(limit))
    for p in products:
        p["_id"] = str(p["_id"])  
    return products

def get_product_by_id(product_id):
    return collection.find_one({"_id": ObjectId(product_id)})

def create_product(product_data):
    result = collection.insert_one(product_data)
    return str(result.inserted_id)

def update_product(product_id, update_data):
    result = collection.update_one({"_id": ObjectId(product_id)}, {"$set": update_data})
    return result.modified_count > 0

def delete_product(product_id):
    result = collection.delete_one({"_id": ObjectId(product_id)})
    return result.deleted_count > 0
