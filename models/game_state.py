"""
État du jeu et règles (logique métier)
"""
from typing import List, Set, Tuple
from .board import Board
from .move import Move, Position
from .types import Player, Piece, CellState


def is_valid_position(row: int, col: int) -> bool:
    """Vérifie si la position est sur le plateau"""
    return 0 <= row < 8 and 0 <= col < 8


def is_playable_square(row: int, col: int) -> bool:
    """Vérifie si la case est jouable (diagonales noires)"""
    return is_valid_position(row, col) and (row + col) % 2 == 1


def get_pawn_directions(player: Player) -> List[Tuple[int, int]]:
    """
    Directions de déplacement des pions
    BLANC monte (row décroît), NOIR descend (row croît)
    """
    if player == Player.WHITE:
        return [(-1, -1), (-1, 1)]  # haut-gauche, haut-droite
    else:
        return [(1, -1), (1, 1)]  # bas-gauche, bas-droite


def get_king_directions() -> List[Tuple[int, int]]:
    """Les dames peuvent se déplacer dans toutes les diagonales"""
    return [(-1, -1), (-1, 1), (1, -1), (1, 1)]


class GameState:
    """Gère l'état du jeu et les règles"""
    
    def __init__(self, board: Board):
        self.board = board
    
    def generate_legal_moves(self, player: Player | None = None) -> List[Move]:
        """
        Génère tous les coups légaux
        RÈGLE IMPORTANTE: Si une capture est possible, elle est obligatoire
        """
        if player is None:
            player = self.board.current_player
        
        captures = self._generate_capture_moves(player)
        if captures:
            return captures  # Capture obligatoire !
        
        return self._generate_simple_moves(player)
    
    def _generate_simple_moves(self, player: Player) -> List[Move]:
        """Génère les coups simples (non-capture)"""
        moves = []
        
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece is None or piece[0] != player:
                    continue
                
                piece_type = piece[1]
                directions = get_pawn_directions(player) if piece_type == Piece.PAWN else get_king_directions()
                
                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc
                    
                    if is_playable_square(new_row, new_col) and self.board.get_piece(new_row, new_col) is None:
                        move = Move(
                            path=[(row, col), (new_row, new_col)],
                            captured_positions=set()
                        )
                        moves.append(move)
        
        return moves
    
    def _generate_capture_moves(self, player: Player) -> List[Move]:
        """Génère tous les coups de capture (avec multi-capture)"""
        captures = []
        
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece is None or piece[0] != player:
                    continue
                
                piece_type = piece[1]
                sequences = self._find_capture_sequences(
                    row, col, player, piece_type, set()
                )
                captures.extend(sequences)
        
        return captures
    
    def _find_capture_sequences(
        self, 
        row: int, 
        col: int, 
        player: Player, 
        piece_type: Piece,
        captured: Set[Position],
        path: List[Position] | None = None
    ) -> List[Move]:
        """
        Trouve récursivement toutes les séquences de capture
        Gère les multi-captures (sauts consécutifs avec la même pièce)
        """
        if path is None:
            path = [(row, col)]
        
        # Directions de capture
        if piece_type == Piece.PAWN:
            directions = get_pawn_directions(player)
        else:  # KING
            directions = get_king_directions()
        
        found_sequences = []
        has_continuation = False
        
        for dr, dc in directions:
            # Position de l'ennemi à capturer
            enemy_row, enemy_col = row + dr, col + dc
            # Position d'atterrissage après capture
            land_row, land_col = row + 2*dr, col + 2*dc
            
            # Vérifications
            if not is_playable_square(land_row, land_col):
                continue
            
            if (enemy_row, enemy_col) in captured:
                continue  # Déjà capturée
            
            enemy_piece = self.board.get_piece(enemy_row, enemy_col)
            if enemy_piece is None or enemy_piece[0] != player.opponent():
                continue  # Pas d'ennemi
            
            if self.board.get_piece(land_row, land_col) is not None:
                continue  # Case occupée
            
            # Capture valide !
            new_captured = captured | {(enemy_row, enemy_col)}
            new_path = path + [(land_row, land_col)]
            
            # Promouvoir le pion en dame si nécessaire
            new_piece_type = piece_type
            if piece_type == Piece.PAWN:
                if (player == Player.WHITE and land_row == 0) or \
                   (player == Player.BLACK and land_row == 7):
                    new_piece_type = Piece.KING
            
            # Chercher des captures supplémentaires
            continuations = self._find_capture_sequences(
                land_row, land_col, player, new_piece_type,
                new_captured, new_path
            )
            
            if continuations:
                found_sequences.extend(continuations)
                has_continuation = True
            else:
                # Pas de continuation, c'est une fin de séquence
                found_sequences.append(Move(
                    path=new_path,
                    captured_positions=new_captured
                ))
        
        return found_sequences
    
    def is_game_over(self) -> bool:
        """Vérifie si le jeu est terminé"""
        return len(self.generate_legal_moves()) == 0
    
    def get_winner(self) -> Player | None:
        """Retourne le gagnant si le jeu est terminé"""
        if not self.is_game_over():
            return None
        return self.board.current_player.opponent()
    
    def apply_move(self, move: Move) -> None:
        """Applique un coup"""
        self.board.apply_move(move)
