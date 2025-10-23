from backend.services.db_connection import get_collection
from config.env import COLLECTION_MATERIALES
from bson import ObjectId

# Colección global
collection = get_collection(COLLECTION_MATERIALES)


def _format_material(material):
    """Convierte ObjectId en str para que pueda usarse en frontend o APIs."""
    if not material:
        return None
    material["_id"] = str(material["_id"])
    return material


def get_all_material(limit=100):
    """Obtiene todos los materiales (con límite)."""
    materiales = collection.find().limit(limit)
    return [_format_material(m) for m in materiales]


def get_materiales_por_clasificacion(clasificacion, limit=100):
    """Obtiene materiales filtrados por clasificación."""
    materiales = collection.find({"clasificacion": clasificacion}).limit(limit)
    return [_format_material(m) for m in materiales]


def search_materiales(keyword, limit=100):
    """Busca materiales cuyo nombre o descripción coincida con un keyword (insensible a mayúsculas)."""
    materiales = collection.find({
        "$or": [
            {"descripcion": {"$regex": keyword, "$options": "i"}},
            {"generico": {"$regex": keyword, "$options": "i"}},
            {"clasificacion": {"$regex": keyword, "$options": "i"}},
        ]
    }).limit(limit)
    return [_format_material(m) for m in materiales]


# ✅ FUNCIONES CRUD QUE FALTABAN

def create_material(data):
    """Crea un nuevo material."""
    result = collection.insert_one(data)
    return str(result.inserted_id)


def update_material(material_id, data):
    """Actualiza un material por su ID."""
    collection.update_one({"_id": ObjectId(material_id)}, {"$set": data})
    return True


def delete_material(material_id):
    """Elimina un material por su ID."""
    collection.delete_one({"_id": ObjectId(material_id)})
    return True
