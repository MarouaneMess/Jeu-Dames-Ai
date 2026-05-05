"""
Algorithmes de recherche Minimax et Alpha-Beta
"""
from dataclasses import dataclass
from typing import Tuple, List
import time
import random

from models.board import Board
from models.move import Move
from models.game_state import GameState
from interfaces.evaluator import IEvaluator


@dataclass
class SearchStats:
    """Statistiques de recherche"""
    nodes_explored: int = 0
    time_seconds: float = 0.0
    depth_reached: int = 0


def minimax(
    board: Board, 
    depth: int, 
    maximizing: bool, 
    evaluator: IEvaluator, 
    stats: SearchStats,
    last_move: Move | None = None,
    collect_best_moves: bool = False
) -> Tuple[float, Move | None | List[Move]]:
    """
    Algorithme Minimax classique
    Explore tout l'arbre jusqu'à la profondeur donnée
    """
    stats.nodes_explored += 1
    
    game_state = GameState(board)
    legal_moves = game_state.generate_legal_moves()
    
    # Cas terminal
    if depth == 0 or len(legal_moves) == 0:
        score = evaluator.evaluate(board)
        return score if maximizing else -score, (None if not collect_best_moves else [])
    
    best_moves = []
    
    if maximizing:
        max_score = float('-inf')
        for move in legal_moves:
            # Simuler le coup
            child_board = board.clone()
            child_board.apply_move(move)
            
            score, _ = minimax(child_board, depth - 1, False, evaluator, stats, last_move, collect_best_moves=False)
            
            if score > max_score:
                max_score = score
                best_moves = [move]
            elif score == max_score:
                best_moves.append(move)
        
        if collect_best_moves:
            return max_score, best_moves
        else:
            return max_score, best_moves[0] if best_moves else None
    else:
        min_score = float('inf')
        for move in legal_moves:
            child_board = board.clone()
            child_board.apply_move(move)
            
            score, _ = minimax(child_board, depth - 1, True, evaluator, stats, last_move, collect_best_moves=False)
            
            if score < min_score:
                min_score = score
                best_moves = [move]
            elif score == min_score:
                best_moves.append(move)
        
        if collect_best_moves:
            return min_score, best_moves
        else:
            return min_score, best_moves[0] if best_moves else None


def alphabeta(
    board: Board, 
    depth: int, 
    alpha: float, 
    beta: float, 
    maximizing: bool, 
    evaluator: IEvaluator, 
    stats: SearchStats,
    move_ordering: bool = True,
    last_move: Move | None = None,
    collect_best_moves: bool = False
) -> Tuple[float, Move | None | List[Move]]:
    """
    Algorithme Alpha-Beta avec élagage
    Plus efficace que Minimax grâce à l'élagage des branches
    """
    stats.nodes_explored += 1
    
    game_state = GameState(board)
    legal_moves = game_state.generate_legal_moves()
    
    # Cas terminal
    if depth == 0 or len(legal_moves) == 0:
        score = evaluator.evaluate(board)
        return score if maximizing else -score, (None if not collect_best_moves else [])
    
    # Tri des coups (captures en premier)
    if move_ordering:
        legal_moves = _order_moves(board, legal_moves)
    
    best_moves = []
    
    if maximizing:
        max_score = float('-inf')
        for move in legal_moves:
            child_board = board.clone()
            child_board.apply_move(move)
            
            score, _ = alphabeta(child_board, depth - 1, alpha, beta, False, evaluator, stats, move_ordering, last_move, collect_best_moves=False)
            
            if score > max_score:
                max_score = score
                best_moves = [move]
            elif score == max_score:
                best_moves.append(move)
            
            alpha = max(alpha, score)
            if beta <= alpha:
                break  # Coupure Beta
        
        if collect_best_moves:
            return max_score, best_moves
        else:
            return max_score, best_moves[0] if best_moves else None
    else:
        min_score = float('inf')
        for move in legal_moves:
            child_board = board.clone()
            child_board.apply_move(move)
            
            score, _ = alphabeta(child_board, depth - 1, alpha, beta, True, evaluator, stats, move_ordering, last_move, collect_best_moves=False)
            
            if score < min_score:
                min_score = score
                best_moves = [move]
            elif score == min_score:
                best_moves.append(move)
            
            beta = min(beta, score)
            if beta <= alpha:
                break  # Coupure Alpha
        
        if collect_best_moves:
            return min_score, best_moves
        else:
            return min_score, best_moves[0] if best_moves else None


def _order_moves(board: Board, moves: list[Move]) -> list[Move]:
    """
    Trie les coups pour améliorer l'élagage Alpha-Beta
    Ordre: captures > promotions > autres
    """
    def move_priority(move: Move) -> int:
        priority = 0
        
        # Captures en priorité
        if move.is_capture:
            priority += 100 + move.capture_count * 10
        
        # Promotions
        start_row, start_col = move.start
        end_row, end_col = move.end
        piece = board.get_piece(start_row, start_col)
        
        if piece and piece[1].name == 'PAWN':
            if (piece[0].name == 'WHITE' and end_row == 0) or \
               (piece[0].name == 'BLACK' and end_row == 7):
                priority += 50
        
        return -priority  # Négatif car on veut trier décroissant
    
    return sorted(moves, key=move_priority)


def choose_move(
    board: Board,
    depth: int,
    evaluator: IEvaluator,
    use_alphabeta: bool = True,
    last_move: Move | None = None
) -> Tuple[Move, SearchStats]:
    """
    Choisit le meilleur coup avec stats
    
    Args:
        board: Plateau actuel
        depth: Profondeur de recherche
        evaluator: Fonction d'évaluation
        use_alphabeta: True pour Alpha-Beta, False pour Minimax
        last_move: Dernier coup joué (pour éviter les répétitions)
    
    Returns:
        (meilleur_coup, statistiques)
    """
    stats = SearchStats()
    start_time = time.time()
    
    if use_alphabeta:
        _, best_moves = alphabeta(
            board, depth, float('-inf'), float('inf'), True, evaluator, stats, 
            move_ordering=True, last_move=last_move, collect_best_moves=True
        )
    else:
        _, best_moves = minimax(board, depth, True, evaluator, stats, last_move, collect_best_moves=True)
    
    # Choisir aléatoirement parmi tous les meilleurs coups
    # Cela crée de la variabilité sans sacrifier la qualité
    best_move = random.choice(best_moves) if best_moves else None
    
    stats.time_seconds = time.time() - start_time
    stats.depth_reached = depth
    
    return best_move, stats
