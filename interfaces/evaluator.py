"""
Interface pour les fonctions d'évaluation
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.board import Board


class IEvaluator(ABC):
    """Interface abstraite pour une fonction d'évaluation"""
    
    @abstractmethod
    def evaluate(self, board: 'Board') -> float:
        """
        Évaluer une position du jeu
        
        Returns:
            Score positif si favorable au joueur actuel, négatif sinon
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Obtenir le nom de l'évaluateur"""
        pass
