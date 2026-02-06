"""
Joueur IA avec trois niveaux de difficulté
"""
from enum import Enum
from interfaces.player import IPlayer
from models.board import Board
from models.move import Move
from .evaluators import MaterialEvaluator, MobilityEvaluator, AdvancedEvaluator
from .search import choose_move, SearchStats


class Difficulty(Enum):
    """Niveaux de difficulté de l'IA"""
    EASY = 1
    MEDIUM = 2
    HARD = 3


class AIPlayer(IPlayer):
    """Joueur contrôlé par l'IA"""
    
    def __init__(self, difficulty: Difficulty):
        self.difficulty = difficulty
        self.last_stats: SearchStats | None = None
        
        # Configuration selon la difficulté
        if difficulty == Difficulty.EASY:
            self.depth = 2
            self.evaluator = MaterialEvaluator()
            self.use_alphabeta = False  # Minimax simple
        elif difficulty == Difficulty.MEDIUM:
            self.depth = 4
            self.evaluator = MobilityEvaluator()
            self.use_alphabeta = True  # Alpha-Beta
        else:  # HARD
            self.depth = 7
            self.evaluator = AdvancedEvaluator()
            self.use_alphabeta = True  # Alpha-Beta
    
    def choose_move(self, board: Board) -> Move:
        """Choisit le meilleur coup"""
        move, stats = choose_move(
            board, 
            self.depth, 
            self.evaluator, 
            self.use_alphabeta
        )
        self.last_stats = stats
        return move
    
    def get_name(self) -> str:
        """Nom du joueur IA"""
        return f"IA {self.difficulty.name.capitalize()}"
    
    def get_stats(self) -> SearchStats | None:
        """Retourne les stats de la dernière recherche"""
        return self.last_stats
