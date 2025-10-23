import tkinter as tk
from frontend.gui.theme_config import apply_theme
from frontend.gui.auth_view import build_auth_frame
from frontend.gui.dashboard_view import build_dashboard

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.style = apply_theme()
        self.root.title("🛍️ FontTrack Store")
        self.root.geometry("1024x768")
        self.root.configure(bg="#1e1e2f")  # Fondo oscuro estilo FontTrack

        self.show_auth_view()

    def show_auth_view(self):
        self.clear_window()
        build_auth_frame(self.root, self.on_login_success)

    def on_login_success(self, user):
        self.clear_window()
        build_dashboard(self.root, user)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

def launch_app():
    app = MainWindow()
    app.run()
