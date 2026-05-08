import csv
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
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

    # play_game_silent now returns the winner color as 'blanc'/'noir'/'nul'.
    winner_color = play_game_silent(white_player, black_player) or "nul"

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
        self.total_time: float = 0.0

    def run(
        self,
        level_1: Difficulty,
        level_2: Difficulty,
        match_count: int,
        max_workers: int | None = None,
    ) -> List[MatchResult]:
        """Lance matchs """
        start_time = time.perf_counter()
        self.results = []

        if max_workers is None or max_workers <= 1:
            for match_number in range(1, match_count + 1):
                self.results.append(_run_single_match(match_number, level_1, level_2))
        else:
            with ProcessPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(_run_single_match, match_number, level_1, level_2): match_number
                    for match_number in range(1, match_count + 1)
                }

                completed_results: List[MatchResult] = []
                for future in as_completed(futures):
                    completed_results.append(future.result())

            self.results = sorted(completed_results, key=lambda result: result.match_number)

        self.total_time = time.perf_counter() - start_time
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
        print(f"Temps total du tournoi: {self.total_time:.2f} secondes")
        print("=" * 50 + "\n")
    
    def save_summary_csv(self, filename: str = None) -> str:
    
        if not self.results:
            print("Aucun résultat à sauvegarder.")
            return None
        
        if filename is None:
            filename = "tournament_summary.csv"
        
        # Agréger les résultats
        white_lvl = self.results[0].white_lvl
        black_lvl = self.results[0].black_lvl
        
        white_wins = sum(1 for r in self.results if r.winner == "blanc")
        black_wins = sum(1 for r in self.results if r.winner == "noir")
        draws = sum(1 for r in self.results if r.winner == "nul")
        
        # Écrire le CSV (append si existe, sinon créer)
        file_exists = False
        try:
            with open(filename, 'r', encoding='utf-8'):
                file_exists = True
        except FileNotFoundError:
            file_exists = False
        
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [ 'white_level', 'black_level', 
                         'white_wins', 'black_wins', 'draws', 'time_seconds']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow({
                'white_level': white_lvl,
                'black_level': black_lvl,
                'white_wins': white_wins,
                'black_wins': black_wins,
                'draws': draws,
                'time_seconds': f"{self.total_time:.2f}",
            })
        
        return filename
