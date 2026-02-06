"""
Point d'entrée principal - Jeu de Dames
Architecture professionnelle
"""
import sys
from typing import Optional

from models.board import Board
from models.game_state import GameState
from ai.ai_player import AIPlayer, Difficulty
from interfaces.player import IPlayer


def play_game(white_player: IPlayer, black_player: IPlayer, renderer=None) -> Optional[str]:
    """
    Joue une partie complète
    
    Args:
        white_player: Joueur blanc (humain ou IA)
        black_player: Joueur noir (humain ou IA)
        renderer: Moteur de rendu graphique (optionnel)
    
    Returns:
        Nom du gagnant ou None si abandon
    """
    board = Board.initial_board()
    game_state = GameState(board)
    
    print(f"\n{'='*50}")
    print(f"NOUVELLE PARTIE")
    print(f"Blancs: {white_player.get_name()}")
    print(f"Noirs: {black_player.get_name()}")
    print(f"{'='*50}\n")
    
    move_count = 0
    
    while not game_state.is_game_over():
        move_count += 1
        current_player = white_player if board.current_player.name == 'WHITE' else black_player
        
        print(f"\n--- Tour {move_count} ({board.current_player}) ---")
        
        # Afficher le plateau
        if renderer:
            renderer.render(board)
        else:
            print(board.pretty_print())
        
        # Choisir le coup
        print(f"{current_player.get_name()} réfléchit...")
        
        try:
            if hasattr(current_player, 'wait_for_move'):
                # Joueur humain avec interface graphique
                move = renderer.wait_for_move(board) if renderer else None
                if move is None:
                    print("Abandon !")
                    return None
            else:
                # Joueur IA
                move = current_player.choose_move(board)
                
                # Afficher les stats de l'IA
                if isinstance(current_player, AIPlayer):
                    stats = current_player.get_stats()
                    if stats:
                        print(f"  → Nœuds explorés: {stats.nodes_explored}")
                        print(f"  → Temps: {stats.time_seconds:.3f}s")
        
        except KeyboardInterrupt:
            print("\nPartie interrompue !")
            return None
        except Exception as e:
            print(f"Erreur: {e}")
            return None
        
        print(f"Coup joué: {move}")
        
        # Appliquer le coup
        game_state.apply_move(move)
    
    # Partie terminée
    winner = game_state.get_winner()
    winner_name = white_player.get_name() if winner.name == 'WHITE' else black_player.get_name()
    
    print(f"\n{'='*50}")
    print(f"PARTIE TERMINÉE !")
    print(f"Gagnant: {winner_name}")
    print(f"Nombre de tours: {move_count}")
    print(f"{'='*50}\n")
    
    if renderer:
        renderer.show_message(f"Gagnant: {winner_name}")
    
    return winner_name


def main_menu():
    """Menu principal"""
    print("""
╔════════════════════════════════════════╗
║       JEU DE DAMES - IA                ║
║     Architecture Professionnelle       ║
╚════════════════════════════════════════╝

1. Humain vs IA Facile
2. Humain vs IA Moyen  
3. Humain vs IA Difficile
4. IA vs IA (Démo)
5. Tests de performance
6. Quitter
""")
    
    choice = input("Votre choix: ").strip()
    
    if choice == '1':
        play_vs_ai(Difficulty.EASY)
    elif choice == '2':
        play_vs_ai(Difficulty.MEDIUM)
    elif choice == '3':
        play_vs_ai(Difficulty.HARD)
    elif choice == '4':
        demo_ai_vs_ai()
    elif choice == '5':
        run_performance_tests()
    elif choice == '6':
        print("Au revoir !")
        sys.exit(0)
    else:
        print("Choix invalide !")
        main_menu()


def play_vs_ai(difficulty: Difficulty):
    """Joue contre l'IA"""
    from gui import get_renderer
    
    renderer = get_renderer()
    
    class HumanPlayer(IPlayer):
        def __init__(self, renderer):
            self.renderer = renderer
        
        def choose_move(self, board: Board):
            return self.renderer.wait_for_move(board)
        
        def get_name(self):
            return "Humain"
    
    human = HumanPlayer(renderer)
    ai = AIPlayer(difficulty)
    
    play_game(human, ai, renderer)
    
    renderer.cleanup()


def demo_ai_vs_ai():
    """Démo IA vs IA"""
    ai_easy = AIPlayer(Difficulty.EASY)
    ai_hard = AIPlayer(Difficulty.HARD)
    
    play_game(ai_easy, ai_hard)


def run_performance_tests():
    """Tests de performance de l'IA"""
    from ai.search import choose_move
    from ai.evaluators import MaterialEvaluator, MobilityEvaluator, AdvancedEvaluator
    
    board = Board.initial_board()
    
    print("\n=== TESTS DE PERFORMANCE ===\n")
    
    tests = [
        ("Facile (Minimax depth=2)", 2, MaterialEvaluator(), False),
        ("Moyen (Alpha-Beta depth=4)", 4, MobilityEvaluator(), True),
        ("Difficile (Alpha-Beta depth=5)", 5, AdvancedEvaluator(), True),
    ]
    
    for name, depth, evaluator, use_ab in tests:
        print(f"{name}:")
        move, stats = choose_move(board, depth, evaluator, use_ab)
        print(f"  Nœuds explorés: {stats.nodes_explored}")
        print(f"  Temps: {stats.time_seconds:.3f}s")
        print(f"  Coup choisi: {move}\n")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nAu revoir !")
        sys.exit(0)
