from backend.services.db_connection import get_collection
from config.env import COLLECTION_FALLAS
from bson import ObjectId

collection = get_collection(COLLECTION_FALLAS)

def _format_falla(falla):
    if not falla:
        return None
    falla["_id"] = str(falla["_id"])
    if "lugar_id" in falla and isinstance(falla["lugar_id"], ObjectId):
        falla["lugar_id"] = str(falla["lugar_id"])
    return falla

def get_all_fallas(limit=100):
    fallas = collection.find().limit(limit)
    return [_format_falla(f) for f in fallas]

def get_falla_by_id(id):
    falla = collection.find_one({"_id": ObjectId(id)})
    return _format_falla(falla)

def create_falla(data):
    result = collection.insert_one(data)
    return str(result.inserted_id)

def update_falla(id, data):
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    return result.modified_count > 0

def delete_falla(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0
