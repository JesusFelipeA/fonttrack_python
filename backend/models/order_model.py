# backend/models/order_model.py

def order_schema(user_id, items, total):
    return {
        "user_id": user_id,
        "items": items,  # Lista de dicts: [{product_id, quantity}]
        "total": float(total),
        "status": "pendiente",
        "created_at": datetime.utcnow()
    }
