"""
Interface pour les joueurs (humain ou IA)
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.board import Board
    from models.move import Move


class IPlayer(ABC):
    """Interface abstraite pour un joueur"""
    
    @abstractmethod
    def choose_move(self, board: 'Board') -> 'Move':
        """Choisir un coup à jouer"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Obtenir le nom du joueur"""
        pass
