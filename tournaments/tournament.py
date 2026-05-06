"""
Tournoi simple entre deux IA.
"""
from dataclasses import dataclass
from typing import List

from ai.ai_player import AIPlayer, Difficulty
from run import play_game


@dataclass
class MatchResult:
    """Résultat d'un match."""

    match_number: int
    white_lvl: str
    black_lvl: str
    winner: str


class Tournament:
    """Tournoi : joueur 1 blanc, joueur 2 noir."""

    def __init__(self):
        self.results: List[MatchResult] = []

    def run(self, level_1: Difficulty, level_2: Difficulty, match_count: int) -> List[MatchResult]:
        """Lance matchs """
        self.results = []

        white_level = "facile" if level_1 == Difficulty.EASY else "moyen" if level_1 == Difficulty.MEDIUM else "hard"
        black_level = "facile" if level_2 == Difficulty.EASY else "moyen" if level_2 == Difficulty.MEDIUM else "hard"

        for match_number in range(1, match_count + 1):
            white_player = AIPlayer(level_1)
            black_player = AIPlayer(level_2)

            winner_name = play_game(white_player, black_player, renderer=None)
            winner_color = "nul"
            if winner_name == white_player.get_name():
                winner_color = "blanc"
            elif winner_name == black_player.get_name():
                winner_color = "noir"

            self.results.append(
                MatchResult(
                    match_number=match_number,
                    white_lvl=white_level,
                    black_lvl=black_level,
                    winner=winner_color,
                )
            )

        return self.results

    def get_results(self) -> List[MatchResult]:
        """Retourne les résultats enregistrés."""
        return list(self.results)

    def print_results(self) -> None:
        """Affiche les résultats du tournoi."""
        print("\n" + "=" * 50)
        print("RESULTATS DU TOURNOI")
        print("=" * 50)

        white_wins = 0
        black_wins = 0
        draws = 0

        for result in self.results:
            if result.winner == "blanc":
                white_wins += 1
            elif result.winner == "noir":
                black_wins += 1
            else:
                draws += 1

            print(
                f"Match {result.match_number}: {result.white_lvl} (Blanc) vs "
                f"{result.black_lvl} (Noir) | Gagnant: {result.winner}"
            )

        print("-" * 50)
        print(f"Victoires blancs: {white_wins}")
        print(f"Victoires noirs: {black_wins}")
        print(f"Matchs nuls: {draws}")
        print("=" * 50 + "\n")
