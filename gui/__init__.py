from .tkinter_renderer import TkinterRenderer

__all__ = ['TkinterRenderer', 'get_renderer']


def get_renderer():
    """
    Retourne le renderer Tkinter
    
    Returns:
        Instance de TkinterRenderer
    """
    return TkinterRenderer()
