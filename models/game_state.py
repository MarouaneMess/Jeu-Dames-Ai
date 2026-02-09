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
                
                if piece_type == Piece.PAWN:
                    # Les pions ne se déplacent que d'une case
                    directions = get_pawn_directions(player)
                    for dr, dc in directions:
                        new_row, new_col = row + dr, col + dc
                        
                        if is_playable_square(new_row, new_col) and self.board.get_piece(new_row, new_col) is None:
                            move = Move(
                                path=[(row, col), (new_row, new_col)],
                                captured_positions=set()
                            )
                            moves.append(move)
                else:
                    # Les dames peuvent se déplacer de plusieurs cases en diagonale
                    directions = get_king_directions()
                    for dr, dc in directions:
                        distance = 1
                        while True:
                            new_row = row + dr * distance
                            new_col = col + dc * distance
                            
                            # Vérifier si on sort du plateau
                            if not is_playable_square(new_row, new_col):
                                break
                            
                            # Vérifier si la case est occupée
                            if self.board.get_piece(new_row, new_col) is not None:
                                break
                            
                            # Case valide : ajouter le mouvement
                            move = Move(
                                path=[(row, col), (new_row, new_col)],
                                captured_positions=set()
                            )
                            moves.append(move)
                            
                            # Continuer dans cette direction
                            distance += 1
        
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
        
        found_sequences = []
        
        if piece_type == Piece.PAWN:
            # Les pions capturent comme avant (saut de 2 cases)
            directions = get_pawn_directions(player)
            
            for dr, dc in directions:
                enemy_row, enemy_col = row + dr, col + dc
                land_row, land_col = row + 2*dr, col + 2*dc
                
                if not is_playable_square(land_row, land_col):
                    continue
                
                if (enemy_row, enemy_col) in captured:
                    continue
                
                enemy_piece = self.board.get_piece(enemy_row, enemy_col)
                if enemy_piece is None or enemy_piece[0] != player.opponent():
                    continue
                
                if self.board.get_piece(land_row, land_col) is not None:
                    continue
                
                # Capture valide !
                new_captured = captured | {(enemy_row, enemy_col)}
                new_path = path + [(land_row, land_col)]
                
                # Promouvoir en dame si atteint dernière ligne
                new_piece_type = piece_type
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
                else:
                    found_sequences.append(Move(
                        path=new_path,
                        captured_positions=new_captured
                    ))
        
        else:  # KING - Peut capturer à distance
            directions = get_king_directions()
            
            for dr, dc in directions:
                # Chercher un ennemi dans cette direction
                distance = 1
                enemy_found = None
                enemy_pos = None
                
                while True:
                    check_row = row + dr * distance
                    check_col = col + dc * distance
                    
                    if not is_playable_square(check_row, check_col):
                        break
                    
                    piece_at = self.board.get_piece(check_row, check_col)
                    
                    if piece_at is not None:
                        # On a trouvé une pièce
                        if piece_at[0] == player.opponent() and enemy_found is None:
                            # C'est un ennemi et c'est le premier trouvé
                            if (check_row, check_col) not in captured:
                                enemy_found = piece_at
                                enemy_pos = (check_row, check_col)
                                distance += 1
                                continue
                        # Pièce alliée ou deuxième ennemi : arrêter
                        break
                    
                    # Case vide
                    if enemy_found is not None:
                        # On a déjà trouvé un ennemi, donc on peut atterrir ici
                        land_row, land_col = check_row, check_col
                        
                        new_captured = captured | {enemy_pos}
                        new_path = path + [(land_row, land_col)]
                        
                        # Chercher des captures supplémentaires depuis cette position
                        continuations = self._find_capture_sequences(
                            land_row, land_col, player, piece_type,
                            new_captured, new_path
                        )
                        
                        if continuations:
                            found_sequences.extend(continuations)
                        else:
                            found_sequences.append(Move(
                                path=new_path,
                                captured_positions=new_captured
                            ))
                    
                    distance += 1
        
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
