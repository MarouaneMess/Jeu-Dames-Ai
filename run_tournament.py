"""
Lancement simple d'un tournoi de dames entre deux IA.
"""
import os
import time

from ai.ai_player import Difficulty
from tournaments.tournament import Tournament


def ask_level(prompt: str) -> Difficulty:
    """Demande un niveau de difficulté."""
    options = {
        "1": Difficulty.EASY,
        "2": Difficulty.MEDIUM,
        "3": Difficulty.HARD,
    }

    while True:
        print(prompt)
        print("1. Facile")
        print("2. Moyen")
        print("3. Difficile")
        choice = input("Votre choix: ").strip().lower()
        if choice in options:
            return options[choice]
        print("Choix invalide, recommencez.\n")


def ask_match_count() -> int:
    """Demande le nombre de matchs à jouer."""
    while True:
        value = input("Nombre de matchs à jouer: ").strip()
        try:
            match_count = int(value)
            if match_count > 0:
                return match_count
        except ValueError:
            pass
        print("Entrez un nombre entier supérieur à 0.\n")


def main() -> None:
    """Menu principal du tournoi."""
    print("\n" + "=" * 60)
    print("TOURNOI SIMPLE")
    print("=" * 60)
    print("Choisissez 2 niveaux au début, puis le nombre de matchs. Les niveaux ne changent pas pendant le tournoi.\n")

    level_one = ask_level("Choisissez le niveau de la première IA:")
    level_two = ask_level("Choisissez le niveau de la deuxième IA:")
    match_count = ask_match_count()
    workers = 15

    tournament = Tournament()
    start = time.perf_counter()
    tournament.run(level_one, level_two, match_count, max_workers=workers)
    elapsed = time.perf_counter() - start
    tournament.print_results()

    print(f"\n{'='*50}")
    print(f"Temps total mesuré: {elapsed:.2f} secondes ")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    main()
