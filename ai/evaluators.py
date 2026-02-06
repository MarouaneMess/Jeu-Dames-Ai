"""
Fonctions d'évaluation pour le jeu de Dames
Architecture: Classe de base + classes dérivées (évite la duplication) car y en a des focntions qui sont répétées
"""
from interfaces.evaluator import IEvaluator
from models.board import Board
from models.types import Player, Piece
from models.game_state import GameState


class BaseEvaluator(IEvaluator):
    """Classe de base avec fonctions communes"""
    
    PAWN_VALUE = 1.0
    KING_VALUE = 5.0
    MOBILITY_WEIGHT = 0.1
    
    def _calculate_material(self, board: Board) -> float:
        """Calcule le score matériel 
        Score = (valeur des pièces du joueur actuel) - (valeur des pièces de l'adversaire)"""
        current = board.current_player
        score = 0.0
        
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece is None:
                    continue
                
                player, piece_type = piece
                value = self.PAWN_VALUE if piece_type == Piece.PAWN else self.KING_VALUE
                
                if player == current:
                    score += value
                else:
                    score -= value
        
        return score
    
    def _calculate_mobility(self, board: Board) -> float:
        """Calcule le bonus de mobilité (une seule fois)"""
        current = board.current_player
        opponent = current.opponent()
        
        game_state = GameState(board)
        current_moves = len(game_state.generate_legal_moves(current))
        
        board_copy = board.clone()
        board_copy.current_player = opponent
        opponent_game_state = GameState(board_copy)
        opponent_moves = len(opponent_game_state.generate_legal_moves(opponent))
        
        return (current_moves - opponent_moves) * self.MOBILITY_WEIGHT


class MaterialEvaluator(BaseEvaluator):
    """Évaluation basée uniquement sur le matériel"""
    
    def evaluate(self, board: Board) -> float:
        """Score = matériel du joueur actuel - matériel de l'adversaire"""
        return self._calculate_material(board)
    
    def get_name(self) -> str:
        return "Material"


class MobilityEvaluator(BaseEvaluator):
    """Évaluation matériel + mobilité (nombre de coups possibles)"""
    
    def evaluate(self, board: Board) -> float:
        """Score = matériel + bonus mobilité"""
        material = self._calculate_material(board)
        mobility = self._calculate_mobility(board)
        return material + mobility
    
    def get_name(self) -> str:
        return "Material+Mobility"


class AdvancedEvaluator(BaseEvaluator):
    """Évaluation avancée avec stratégie positionnelle"""
    
    PROMOTION_THREAT_WEIGHT = 0.3
    BACK_ROW_WEIGHT = 0.2
    CENTER_WEIGHT = 0.15
    
    def evaluate(self, board: Board) -> float:
        """Score = matériel + mobilité + position"""
        current = board.current_player
        
        # Matériel
        material = self._calculate_material(board)
        
        # Bonus position
        position_bonus = self._calculate_position_bonus(board, current)
        
        # Mobilité
        mobility = self._calculate_mobility(board)
        
        return material + position_bonus + mobility
    
    def _calculate_position_bonus(self, board: Board, current: Player) -> float:
        """Calcule les bonus de position (promotion threat, centre, défense)"""
        bonus = 0.0
        
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece is None:
                    continue
                
                player, piece_type = piece
                if player != current:
                    # Bonus pour l'adversaire (négatif)
                    position_bonus = 0.0
                else:
                    position_bonus = 0.0
                
                # Menace de promotion (pions avancés)
                if piece_type == Piece.PAWN:
                    if player == Player.WHITE:
                        distance_to_promotion = row
                        if distance_to_promotion <= 2:
                            position_bonus += (3 - distance_to_promotion) * self.PROMOTION_THREAT_WEIGHT
                    else:  # BLACK
                        distance_to_promotion = 7 - row
                        if distance_to_promotion <= 2:
                            position_bonus += (3 - distance_to_promotion) * self.PROMOTION_THREAT_WEIGHT
                
                # Contrôle du centre
                if 2 <= row <= 5 and 2 <= col <= 5:
                    position_bonus += self.CENTER_WEIGHT
                
                # Défense de la dernière rangée
                if (player == Player.WHITE and row == 7) or (player == Player.BLACK and row == 0):
                    position_bonus += self.BACK_ROW_WEIGHT
                
                if player == current:
                    bonus += position_bonus
                else:
                    bonus -= position_bonus
        
        return bonus
    
    def get_name(self) -> str:
        return "Advanced"
