from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from typing import List

from ai.ai_player import AIPlayer, Difficulty
from run import play_game_silent


@dataclass
class MatchResult:
    """Résultat d'un match."""
    match_number: int
    white_lvl: str
    black_lvl: str
    winner: str


def _difficulty_label(level: Difficulty) -> str:
    if level == Difficulty.EASY:
        return "facile"
    if level == Difficulty.MEDIUM:
        return "moyen"
    return "hard"


def _run_single_match(match_number: int, level_1: Difficulty, level_2: Difficulty) -> MatchResult:
    white_player = AIPlayer(level_1)
    black_player = AIPlayer(level_2)

    winner_name = play_game_silent(white_player, black_player)
    winner_color = "nul"
    if winner_name == white_player.get_name():
        winner_color = "blanc"
    elif winner_name == black_player.get_name():
        winner_color = "noir"

    return MatchResult(
        match_number=match_number,
        white_lvl=_difficulty_label(level_1),
        black_lvl=_difficulty_label(level_2),
        winner=winner_color,
    )


class Tournament:
    """Tournoi : joueur 1 blanc, joueur 2 noir."""

    def __init__(self):
        self.results: List[MatchResult] = []

    def run(
        self,
        level_1: Difficulty,
        level_2: Difficulty,
        match_count: int,
        max_workers: int | None = None,
    ) -> List[MatchResult]:
        """Lance matchs """
        self.results = []

        if max_workers is None or max_workers <= 1:
            for match_number in range(1, match_count + 1):
                self.results.append(_run_single_match(match_number, level_1, level_2))
            return self.results

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(_run_single_match, match_number, level_1, level_2): match_number
                for match_number in range(1, match_count + 1)
            }

            completed_results: List[MatchResult] = []
            for future in as_completed(futures):
                completed_results.append(future.result())

        self.results = sorted(completed_results, key=lambda result: result.match_number)

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
