from ttkbootstrap import Style

def apply_theme(theme_name="cyborg"):
    """
    Aplica el tema visual a la interfaz.
    Puedes cambiar el tema por: 'darkly', 'flatly', 'journal', 'cyborg', etc.
    """
    style = Style(theme=theme_name)
    return style
