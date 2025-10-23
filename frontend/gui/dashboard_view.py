# frontend/gui/dashboard_view.py

from frontend.gui.product_window import build_product_frame
from frontend.gui.admin_view import build_admin_frame

def build_dashboard(root, user):
    if user["role"] == "admin":
        build_admin_frame(root)
    else:
        build_product_frame(root)
