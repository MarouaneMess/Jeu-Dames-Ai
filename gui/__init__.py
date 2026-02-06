"""
Interface graphique avec Tkinter
Simple et compatible avec toutes les versions Python
"""
from .tkinter_renderer import TkinterRenderer

__all__ = ['TkinterRenderer', 'get_renderer']


def get_renderer():
    """
    Retourne le renderer Tkinter
    
    Returns:
        Instance de TkinterRenderer
    """
    return TkinterRenderer()
