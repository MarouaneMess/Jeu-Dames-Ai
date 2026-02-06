"""
Plateau de jeu (Board) pour les Dames
"""
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from copy import deepcopy
from .types import CellState, Player, Piece, cell_state_from
from .move import Move, Position


@dataclass
class Board:
    """
    Représente le plateau de jeu 8x8
    
    grid: Grille 8x8 avec des CellState
    current_player: Joueur dont c'est le tour
    """
    grid: List[List[CellState]] = field(default_factory=lambda: [[CellState.EMPTY for _ in range(8)] for _ in range(8)])
    current_player: Player = Player.WHITE

    @staticmethod
    def initial_board() -> "Board":
        """Crée le plateau initial"""
        board = Board()
        # Pièces NOIRES aux rangées 0-2 (en haut)
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:  # Cases jouables uniquement
                    board.grid[row][col] = CellState.BLACK_PAWN
        
        # Pièces BLANCHES aux rangées 5-7 (en bas)
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board.grid[row][col] = CellState.WHITE_PAWN
        
        board.current_player = Player.WHITE
        return board

    def clone(self) -> "Board":
        """Crée une copie profonde du plateau"""
        return Board(
            grid=deepcopy(self.grid),
            current_player=self.current_player
        )

    def get_piece(self, row: int, col: int) -> Optional[Tuple[Player, Piece]]:
        """Retourne (Joueur, Pièce) ou None si vide"""
        cell = self.grid[row][col]
        if cell == CellState.EMPTY:
            return None
        return (cell.player(), cell.piece_type())

    def set_piece(self, row: int, col: int, cell_state: CellState) -> None:
        """Place une pièce"""
        self.grid[row][col] = cell_state

    def remove_piece(self, row: int, col: int) -> None:
        """Retire une pièce"""
        self.grid[row][col] = CellState.EMPTY

    def apply_move(self, move: Move) -> None:
        """
        Applique un coup sur le plateau (modification en place)
        Gère le déplacement et les captures
        """
        start_row, start_col = move.start
        end_row, end_col = move.end
        
        # Récupère la pièce
        piece_cell = self.grid[start_row][start_col]
        
        # Enlève de la position de départ
        self.remove_piece(start_row, start_col)
        
        # Retire les pièces capturées
        for cap_row, cap_col in move.captured_positions:
            self.remove_piece(cap_row, cap_col)
        
        # Promotion (pion devient dame)
        if piece_cell in (CellState.WHITE_PAWN, CellState.BLACK_PAWN):
            if (piece_cell == CellState.WHITE_PAWN and end_row == 0) or \
               (piece_cell == CellState.BLACK_PAWN and end_row == 7):
                piece_cell = CellState.WHITE_KING if piece_cell == CellState.WHITE_PAWN else CellState.BLACK_KING
        
        # Place à la destination
        self.set_piece(end_row, end_col, piece_cell)
        
        # Change de joueur
        self.current_player = self.current_player.opponent()

    def count_pieces(self, player: Player) -> int:
        """Compte les pièces d'un joueur"""
        count = 0
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece[0] == player:
                    count += 1
        return count

    def get_all_pieces(self, player: Player) -> List[Position]:
        """Retourne les positions de toutes les pièces d'un joueur"""
        positions = []
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece[0] == player:
                    positions.append((row, col))
        return positions

    def pretty_print(self) -> str:
        """Représentation textuelle du plateau"""
        lines = ["  0 1 2 3 4 5 6 7", "  +-+-+-+-+-+-+-+-+"]
        
        for row in range(8):
            row_str = f"{row}|" + "|".join(str(self.grid[row][col]) for col in range(8)) + "|"
            lines.append(row_str)
            lines.append("  +-+-+-+-+-+-+-+-+")
        
        lines.append(f"Joueur actuel: {self.current_player}")
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.pretty_print()
