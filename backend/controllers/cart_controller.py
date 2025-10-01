# backend/controllers/cart_controller.py

def calculate_total(cart_items):
    return sum(item["price"] * item["quantity"] for item in cart_items)

def add_to_cart(cart, product, quantity):
    cart.append({
        "product_id": product["_id"],
        "name": product["name"],
        "price": product["price"],
        "quantity": quantity
    })
    return cart
