"""
Interface pour le rendu graphique
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.board import Board
    from models.move import Move


class IRenderer(ABC):
    """Interface abstraite pour un moteur de rendu"""
    
    @abstractmethod
    def render(self, board: 'Board') -> None:
        """Afficher le plateau de jeu"""
        pass
    
    @abstractmethod
    def wait_for_move(self, board: 'Board') -> 'Move':
        """Attendre qu'un joueur humain choisisse un coup"""
        pass
    
    @abstractmethod
    def show_message(self, message: str) -> None:
        """Afficher un message"""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Nettoyer les ressources"""
        pass
