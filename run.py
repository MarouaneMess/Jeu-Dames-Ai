import sys
from typing import Optional

from models.board import Board
from models.game_state import GameState
from ai.ai_player import AIPlayer, Difficulty
from interfaces.player import IPlayer


"""focntion pricipale pour lancer une partie """
def play_game(white_player: IPlayer, black_player: IPlayer, renderer=None, silence: bool = True) -> Optional[str]:
    board = Board.initial_board()
    game_state = GameState(board)

    if not silence: 
        print(f"\n{'='*50}")
        print(f"NOUVELLE PARTIE")
        print(f"Blancs: {white_player.get_name()}")
        print(f"Noirs: {black_player.get_name()}")
        print(f"{'='*50}\n")

    move_count = 0
    position_counts = {}

    def _state_key(b: Board):
        return (
            tuple(tuple(cell.value for cell in row) for row in b.grid),
            b.current_player
        )
    
    position_counts[_state_key(board)] = 1

    while not game_state.is_game_over():
        move_count += 1
        current_player = white_player if board.current_player.name == 'WHITE' else black_player

        if not silence:
            print(f"\n--- Tour {move_count} ({board.current_player}) ---")

        # Afficher le plateau
        if renderer:
            renderer.render(board)
        elif not silence:
            print(board.pretty_print())

        # Choisir le coup
        if not silence:
            print(f"{current_player.get_name()} réfléchit...")

        try:
            if hasattr(current_player, 'wait_for_move'):
                # Joueur humain avec interface graphique
                move = renderer.wait_for_move(board) if renderer else None
                if move is None:
                    print("Aucun coup reçu. Fin de la partie.")
                    return None
            else:
                # Joueur IA
                move = current_player.choose_move(board)

                # Afficher les stats de l'IA
                if not silence and isinstance(current_player, AIPlayer) and current_player.get_stats():
                    stats = current_player.get_stats()
                    print(f"Stats de recherche: Profondeur={stats.depth}, Noeuds explorés={stats.nodes_explored}, Temps={stats.time:.3f}s")
        except KeyboardInterrupt:
            print("Partie interrompue par l'utilisateur.")
            return None

        except Exception as e:
            print(f"Erreur: {e}")
            return None
        if not silence:
            print(f"Coup choisi: {move}")

        # Appliquer le coup
        game_state.apply_move(move)
        
        # Vérifier la règle des 20 coups sans capture (nul)
        if game_state.is_draw_by_twenty_moves():
            if renderer:
                renderer.show_message("Match nul (20 coups sans capture) !")
            
            print(f"\n{'='*50}")
            print("20 coups sans capture. Match nul.")
            print(f"PARTIE TERMINÉE !")
            print(f"Temps de la partie: {game_state.get_time():.2f} secondes")
            print(f"{'='*50}\n")
            return "nul"

        # Vérifier les positions répétées (pour un match nul)
        state_key = _state_key(board)
        position_counts[state_key] = position_counts.get(state_key, 0) + 1
        if position_counts[state_key] >= 5:
            if renderer:
                renderer.show_message("Match nul par répétition de position 5 fois !")

            print(f"\n{'='*50}")
            print("Position répétée 5 fois. Match nul.")
            print(f"PARTIE TERMINÉE !")
            print(f"Temps de la partie: {game_state.get_time():.2f} secondes")
            print(f"{'='*50}\n")

            return "nul"
        
    # Partie terminée
    winner = game_state.get_winner()
    winner_name = white_player.get_name() if winner.name == 'WHITE' else black_player.get_name()
    winner_color = "Blanc" if winner.name == 'WHITE' else "Noir"
    if renderer:
        renderer.show_message(f"Victoire de {winner_name} ({winner_color}) !")

    print(f"\n{'='*50}")
    print(f"PARTIE TERMINÉE !")
    print(f"Gagnant: {winner_name} | Couleur: {winner_color}")
    print(f"Nombre de tours: {move_count}")
    print(f"Temps de la partie: {game_state.get_time():.2f} secondes")
    print(f"{'='*50}\n")

    # Retourner la couleur gagnante en minuscule ('blanc'/'noir') pour faciliter
    # l'identification lorsque les deux IA ont le même nom.
    return winner_color.lower()

"""focntions pour lancer des partie avec gui, affichage console ou non"""
def play_game_gui( white_player: IPlayer, black_player: IPlayer) -> Optional[str]:
    from gui import get_renderer
    renderer = get_renderer()
    try:
        return play_game(white_player, black_player, renderer=renderer, silence=True)
    finally:
        renderer.cleanup()

def play_game_console(white_player: IPlayer, black_player: IPlayer) -> Optional[str]:
    return play_game(white_player, black_player, renderer=None, silence=False)

""" pour les tournois"""
def play_game_silent(white_player: IPlayer, black_player: IPlayer) -> Optional[str]:
    return play_game(white_player, black_player, renderer=None, silence=True)

"""focntion pour une partie humain vs ia"""
def human_vs_ai(ai_difficulty: Difficulty):
    class HumanPlayer(IPlayer):
        def get_name(self):
            return "Joueur Humain"
        def choose_move(self, board):
            return None  # Le coup sera choisi via l'interface graphique
        def wait_for_move(self):
            pass  # Méthode pour attendre le coup du joueur humain via l'interface graphique

    human_player = HumanPlayer()
    ai_player = AIPlayer(ai_difficulty)
    return play_game_gui(human_player, ai_player)

"""focntion pour les performances"""
def performance_tests():
    from ai.search import choose_move
    from ai.evaluators import MaterialEvaluator, MobilityEvaluator, AdvancedEvaluator

    board = Board.initial_board()
    print("TEST DE PERFORMANCES  :")
    tests = [
        ("Facile (Minimax, profondeur 1)",1,MaterialEvaluator(), False),
        ("Moyen (Alpha-Beta, profondeur 3)",3,MobilityEvaluator(), True),
        ("Difficile (Alpha-Beta, profondeur 5)",5,MobilityEvaluator(), True),
    ]
    for name, depth, evaluator, use_ab in tests:
        print(f"\n{name} :")
        move, stats = choose_move(board, depth, evaluator,use_ab)
        print(f"Noeuds explorés : {stats.nodes_explored}")
        print(f"Temps : {stats.time_seconds:.3f} secondes")
        print(f"Coup choisi : {move}")

"""focntoion pour le menu pricipal"""
def main_menu():
    """"menu pricipal"""
    while True:
        print ("""
╔════════════════════════════════════════════════════╗
║                                                    ║
║                JEU DE DAMES                        ║
║                                                    ║
╠════════════════════════════════════════════════════╣
║                                                    ║
║   [1]  Humain vs IA Facile                         ║
║   [2]  Humain vs IA Moyen                          ║
║   [3]  Humain vs IA Difficile                      ║
║                                                    ║
║   [4]  IA Facile vs IA Facile                      ║
║   [5]  IA Moyen vs IA Moyen                        ║
║   [6]  IA Difficile vs IA Difficile                ║
║                                                    ║
║   [7]  IA Facile vs IA Moyen                       ║
║   [8]  IA Facile vs IA Difficile                   ║
║   [9]  IA Moyen vs IA Difficile                    ║
║                                                    ║
║   [10]  Tests de performance                       ║
║                                                    ║
║   [11]  Quitter                                    ║
║                                                    ║
╚════════════════════════════════════════════════════╝
           """)
    

        choice = input("Votre choix: ").strip()

        if choice == '1':
            human_vs_ai(Difficulty.EASY)
        elif choice == '2':
            human_vs_ai(Difficulty.MEDIUM)
        elif choice == '3':
            human_vs_ai(Difficulty.HARD)
        elif choice == '4':
            play_game_gui(AIPlayer(Difficulty.EASY), AIPlayer(Difficulty.EASY))
        elif choice == '5':
            play_game_gui(AIPlayer(Difficulty.MEDIUM), AIPlayer(Difficulty.MEDIUM))
        elif choice == '6':
            play_game_gui(AIPlayer(Difficulty.HARD), AIPlayer(Difficulty.HARD))
        elif choice == '7':
            play_game_gui(AIPlayer(Difficulty.EASY), AIPlayer(Difficulty.MEDIUM))
        elif choice == '8':
            play_game_gui(AIPlayer(Difficulty.EASY), AIPlayer(Difficulty.HARD))
        elif choice == '9':
            play_game_gui(AIPlayer(Difficulty.MEDIUM), AIPlayer(Difficulty.HARD))
        elif choice == '10':
            performance_tests()
        elif choice == '11':
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")


if __name__ == "__main__":
    try :
        main_menu()
    except KeyboardInterrupt:
        print("\nProgramme interrompu par l'utilisateur. Au revoir !")
        sys.exit(0)