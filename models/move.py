"""
Représentation d'un coup dans le jeu de Dames
"""
from dataclasses import dataclass
from typing import List, Set, Tuple


Position = Tuple[int, int]


@dataclass
class Move:
    """
    Représente un coup aux Dames
    
    path: Liste des positions (row, col) de départ jusqu'à l'arrivée
          Simple: [départ, arrivée]
          Multi-capture: [départ, après_capture1, après_capture2, ...]
    captured_positions: Ensemble des positions des pièces capturées
    """
    path: List[Position]
    captured_positions: Set[Position]

    @property
    def start(self) -> Position:
        """Position de départ"""
        return self.path[0]

    @property
    def end(self) -> Position:
        """Position d'arrivée"""
        return self.path[-1]

    @property
    def is_capture(self) -> bool:
        """True si ce coup capture des pièces"""
        return len(self.captured_positions) > 0

    @property
    def capture_count(self) -> int:
        """Nombre de pièces capturées"""
        return len(self.captured_positions)

    def __str__(self) -> str:
        if self.is_capture:
            return f"{self.start} -> {self.end} (x{self.capture_count})"
        return f"{self.start} -> {self.end}"

    def __hash__(self) -> int:
        return hash((tuple(self.path), tuple(sorted(self.captured_positions))))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Move):
            return False
        return (self.path == other.path and 
                self.captured_positions == other.captured_positions)
