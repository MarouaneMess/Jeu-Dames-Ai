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
        self.last_move: Move | None = None  # Dernier coup joué par cette IA
        
        # Configuration selon la difficulté
        if difficulty == Difficulty.EASY:
            self.depth = 1
            self.evaluator = MaterialEvaluator()
            self.use_alphabeta = False  # Minimax simple
        elif difficulty == Difficulty.MEDIUM:
            self.depth = 3
            self.evaluator = MobilityEvaluator()
            self.use_alphabeta = True  # Alpha-Beta
        else:  # HARD
            self.depth = 6
            self.evaluator = AdvancedEvaluator()
            self.use_alphabeta = True  # Alpha-Beta
    
    def choose_move(self, board: Board) -> Move:
        """Choisit le meilleur coup"""
        move, stats = choose_move(
            board, 
            self.depth, 
            self.evaluator, 
            self.use_alphabeta,
            last_move=self.last_move
        )
        self.last_stats = stats
        self.last_move = move  # Mémoriser pour la prochaine fois
        return move
    
    def get_name(self) -> str:
        """Nom du joueur IA"""
        names = {
            Difficulty.EASY: "IA Facile",
            Difficulty.MEDIUM: "IA Moyen",
            Difficulty.HARD: "IA Difficile",
        }
        return names[self.difficulty]
    
    def get_stats(self) -> SearchStats | None:
        """Retourne les stats de la dernière recherche"""
        return self.last_stats
