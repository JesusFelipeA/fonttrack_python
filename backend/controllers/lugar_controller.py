from backend.services.db_connection import get_collection
from config.env import COLLECTION_LUGARES
from bson import ObjectId

collection = get_collection(COLLECTION_LUGARES)

def _format_lugar(lugar):
    if not lugar:
        return None
    lugar["_id"] = str(lugar["_id"])
    return lugar

def get_all_lugares(limit=100):
    lugares = collection.find().limit(limit)
    return [_format_lugar(l) for l in lugares]

def get_lugar_by_id(id):
    lugar = collection.find_one({"_id": ObjectId(id)})
    return _format_lugar(lugar)

def create_lugar(data):
    result = collection.insert_one(data)
    return str(result.inserted_id)

def update_lugar(id, data):
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    return result.modified_count > 0

def delete_lugar(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0
