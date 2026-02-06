"""
Interfaces abstraites pour le jeu de Dames
Architecture SOLID - Inversion de dépendances
"""

from .player import IPlayer
from .evaluator import IEvaluator
from .renderer import IRenderer

__all__ = ['IPlayer', 'IEvaluator', 'IRenderer']
