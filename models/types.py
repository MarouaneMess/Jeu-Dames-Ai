"""
Types et énumérations pour le jeu de Dames
"""
from enum import Enum, auto


class Player(Enum):
    """Joueurs du jeu"""
    WHITE = auto()
    BLACK = auto()

    def opponent(self) -> 'Player':
        """Retourne l'adversaire"""
        return Player.BLACK if self == Player.WHITE else Player.WHITE
    
    def __str__(self) -> str:
        return "Blancs" if self == Player.WHITE else "Noirs"


class Piece(Enum):
    """Types de pièces"""
    PAWN = auto()
    KING = auto()

    def __str__(self) -> str:
        return "Pion" if self == Piece.PAWN else "Dame"


class CellState(Enum):
    """État d'une case du plateau"""
    EMPTY = 0
    WHITE_PAWN = 1
    WHITE_KING = 2
    BLACK_PAWN = 3
    BLACK_KING = 4

    def player(self) -> Player | None:
        """Retourne le joueur propriétaire de la pièce"""
        if self == CellState.EMPTY:
            return None
        return Player.WHITE if self in (CellState.WHITE_PAWN, CellState.WHITE_KING) else Player.BLACK

    def piece_type(self) -> Piece | None:
        """Retourne le type de pièce"""
        if self == CellState.EMPTY:
            return None
        return Piece.PAWN if self in (CellState.WHITE_PAWN, CellState.BLACK_PAWN) else Piece.KING

    def __str__(self) -> str:
        return {
            CellState.EMPTY: ".",
            CellState.WHITE_PAWN: "w",
            CellState.WHITE_KING: "W",
            CellState.BLACK_PAWN: "b",
            CellState.BLACK_KING: "B",
        }[self]


def cell_state_from(player: Player, piece_type: Piece) -> CellState:
    """Crée un CellState à partir du joueur et du type de pièce"""
    if player == Player.WHITE:
        return CellState.WHITE_PAWN if piece_type == Piece.PAWN else CellState.WHITE_KING
    else:
        return CellState.BLACK_PAWN if piece_type == Piece.PAWN else CellState.BLACK_KING
