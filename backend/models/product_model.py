# backend/models/product_model.py

def product_schema(name, description, price, stock, category="general"):
    return {
        "name": name,
        "description": description,
        "price": float(price),
        "stock": int(stock),
        "category": category,
        "created_at": datetime.utcnow()
    }
