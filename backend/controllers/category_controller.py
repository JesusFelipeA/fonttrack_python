from backend.services.db_connection import get_collection
from config.env import COLLECTION_CATEGORIES
from bson import ObjectId

# Colección global
collection = get_collection(COLLECTION_CATEGORIES)

def _format_category(category):
    """Convierte ObjectId en str para frontend."""
    if not category:
        return None
    category["_id"] = str(category["_id"])
    return category

def get_all_categories(limit=100):
    categories = collection.find().limit(limit)
    return [_format_category(c) for c in categories]

def get_category_by_id(category_id):
    category = collection.find_one({"_id": ObjectId(category_id)})
    return _format_category(category)

def create_category(data):
    """Crea una nueva categoría."""
    result = collection.insert_one({
        "name": data["name"],
        "description": data.get("description", "")
    })
    return str(result.inserted_id) if result.inserted_id else None

def update_category(category_id, data):
    """Actualiza una categoría existente."""
    result = collection.update_one(
        {"_id": ObjectId(category_id)},
        {"$set": {
            "name": data["name"],
            "description": data.get("description", "")
        }}
    )
    return result.modified_count > 0

def delete_category(category_id):
    """Elimina una categoría."""
    result = collection.delete_one({"_id": ObjectId(category_id)})
    return result.deleted_count > 0
