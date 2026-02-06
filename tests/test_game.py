"""
Tests unitaires pour le jeu de Dames
Architecture professionnelle avec pytest
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.board import Board
from models.types import Player, Piece, CellState
from models.game_state import GameState
from ai.evaluators import MaterialEvaluator
from ai.search import minimax, alphabeta, SearchStats


class TestBoardSetup:
    """Tests de configuration du plateau"""
    
    def test_initial_board_dimensions(self):
        """Le plateau doit faire 8x8"""
        board = Board.initial_board()
        assert len(board.grid) == 8
        assert all(len(row) == 8 for row in board.grid)
    
    def test_initial_piece_count(self):
        """Doit avoir 12 pièces par joueur au départ"""
        board = Board.initial_board()
        assert board.count_pieces(Player.WHITE) == 12
        assert board.count_pieces(Player.BLACK) == 12
    
    def test_initial_white_position(self):
        """Les blancs doivent être en bas (rangées 5-7)"""
        board = Board.initial_board()
        white_pieces = board.get_all_pieces(Player.WHITE)
        assert all(row >= 5 for row, col in white_pieces)
    
    def test_initial_black_position(self):
        """Les noirs doivent être en haut (rangées 0-2)"""
        board = Board.initial_board()
        black_pieces = board.get_all_pieces(Player.BLACK)
        assert all(row <= 2 for row, col in black_pieces)


class TestMovement:
    """Tests de déplacement"""
    
    def test_white_pawn_moves_up(self):
        """Un pion blanc doit se déplacer vers le haut"""
        board = Board.initial_board()
        game_state = GameState(board)
        moves = game_state.generate_legal_moves()
        
        # Les pions blancs en rangée 5 peuvent monter en rangée 4
        assert any(move.start[0] == 5 and move.end[0] == 4 for move in moves)
    
    def test_capture_is_mandatory(self):
        """Si une capture est possible, elle est obligatoire"""
        board = Board()
        board.set_piece(3, 3, CellState.WHITE_PAWN)
        board.set_piece(2, 4, CellState.BLACK_PAWN)  # Peut être capturé
        board.current_player = Player.WHITE
        
        game_state = GameState(board)
        moves = game_state.generate_legal_moves()
        
        # Tous les coups doivent être des captures
        assert all(move.is_capture for move in moves)
    
    def test_promotion_to_king(self):
        """Un pion atteignant le bout devient dame"""
        board = Board()
        board.set_piece(1, 1, CellState.WHITE_PAWN)
        board.current_player = Player.WHITE
        
        from models.move import Move
        move = Move(path=[(1, 1), (0, 0)], captured_positions=set())
        board.apply_move(move)
        
        # Vérifier que c'est maintenant une dame
        piece = board.get_piece(0, 0)
        assert piece is not None
        assert piece[1] == Piece.KING


class TestAI:
    """Tests de l'IA"""
    
    def test_material_evaluator(self):
        """L'évaluateur matériel doit calculer correctement"""
        board = Board()
        board.set_piece(0, 0, CellState.WHITE_PAWN)
        board.set_piece(1, 1, CellState.BLACK_KING)
        board.current_player = Player.WHITE
        
        evaluator = MaterialEvaluator()
        score = evaluator.evaluate(board)
        
        # Blancs: 1 pion (+1), Noirs: 1 dame (-5) => score = -4
        assert score == -4.0
    
    def test_minimax_finds_moves(self):
        """Minimax doit trouver des coups"""
        board = Board.initial_board()
        evaluator = MaterialEvaluator()
        stats = SearchStats()
        
        score, move = minimax(board, 2, True, evaluator, stats)
        
        assert move is not None
        assert stats.nodes_explored > 0
    
    def test_alphabeta_finds_moves(self):
        """Alpha-Beta doit trouver des coups"""
        board = Board.initial_board()
        evaluator = MaterialEvaluator()
        stats = SearchStats()
        
        score, move = alphabeta(
            board, 2, float('-inf'), float('inf'), True, evaluator, stats
        )
        
        assert move is not None
        assert stats.nodes_explored > 0
    
    def test_alphabeta_explores_less_than_minimax(self):
        """Alpha-Beta doit explorer moins de nœuds que Minimax"""
        board = Board.initial_board()
        evaluator = MaterialEvaluator()
        
        stats_minimax = SearchStats()
        minimax(board, 2, True, evaluator, stats_minimax)
        
        stats_alphabeta = SearchStats()
        alphabeta(board, 2, float('-inf'), float('inf'), True, evaluator, stats_alphabeta)
        
        # Alpha-Beta doit explorer moins (élagage)
        assert stats_alphabeta.nodes_explored <= stats_minimax.nodes_explored


class TestGameState:
    """Tests de l'état du jeu"""
    
    def test_initial_legal_moves(self):
        """Au départ, il doit y avoir exactement 7 coups légaux pour les blancs"""
        board = Board.initial_board()
        game_state = GameState(board)
        moves = game_state.generate_legal_moves()
        
        assert len(moves) == 7
    
    def test_no_pieces_is_game_over(self):
        """Partie terminée si plus de pièces"""
        board = Board()
        board.current_player = Player.WHITE
        game_state = GameState(board)
        
        assert game_state.is_game_over()
    
    def test_winner_is_opponent(self):
        """Le gagnant est l'adversaire si le joueur actuel ne peut pas jouer"""
        board = Board()
        board.current_player = Player.WHITE
        game_state = GameState(board)
        
        winner = game_state.get_winner()
        assert winner == Player.BLACK


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, '-v'])
