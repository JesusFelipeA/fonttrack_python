# frontend/gui/cart_view.py

import ttkbootstrap as ttk
from backend.controllers.cart_controller import calculate_total

def build_cart_frame(root, cart_items):
    frame = ttk.Frame(root, padding=30)
    frame.pack(fill="both", expand=True)

    ttk.Label(
        frame, 
        text="🛒 Carrito de compras", 
        font=("Segoe UI", 18, "bold"),
        anchor="center"
    ).pack(pady=(0, 20))

    if not cart_items:
        ttk.Label(frame, text="El carrito está vacío.", font=("Segoe UI", 12, "italic")).pack(pady=10)
    else:
        for item in cart_items:
            item_frame = ttk.Frame(frame, padding=5, bootstyle="secondary")
            item_frame.pack(fill="x", pady=4, padx=10)
            ttk.Label(
                item_frame, 
                text=f"{item['name']}", 
                font=("Segoe UI", 12, "bold"),
                anchor="w"
            ).pack(side="left", padx=(0, 10))
            ttk.Label(
                item_frame, 
                text=f"x{item['quantity']}", 
                font=("Segoe UI", 12),
                anchor="w"
            ).pack(side="left", padx=(0, 10))
            ttk.Label(
                item_frame, 
                text=f"${item['price'] * item['quantity']:.2f}", 
                font=("Segoe UI", 12),
                anchor="w"
            ).pack(side="right")

    total = calculate_total(cart_items)
    ttk.Label(
        frame, 
        text=f"Total: ${total:.2f}", 
        font=("Segoe UI", 14, "bold"),
        anchor="center"
    ).pack(pady=20)
