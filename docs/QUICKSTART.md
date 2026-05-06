# 🚀 QUICKSTART - Jeu de Dames

## Installation Rapide

### Option 2: Python 3.14 (Tkinter automatique)

```bash
# 1. Installer pytest 
pip install pytest

# 2. Lancer le jeu (utilise Tkinter)
python run.py
```

---

## Utilisation

### Menu Principal

```bash
python run.py
```

**Options disponibles:**
1. **Humain vs IA Facile** - Jouez contre une IA simple
2. **Humain vs IA Moyen** - IA plus forte avec Alpha-Beta
3. **Humain vs IA Difficile** - IA experte avec évaluation avancée
4. **IA vs IA (Démo)** - Regardez deux IA jouer
5. **Tests de performance** - Benchmarks des algorithmes

### Interface Graphique

**Tkinter**


## Tests

```bash
# Lancer tous les tests
pytest tests/ -v

# Tests avec détails
pytest tests/test_game.py -v


**Résultat attendu:** 13 tests passent ✅

---

## Structure du Projet

```
projet/
├── models/         # Logique du jeu (Board, Move, GameState)
├── ai/            # Intelligence artificielle (3 niveaux)
├── gui/           # Interface graphique (Pygame + Tkinter)
├── interfaces/    # Abstractions (IPlayer, IEvaluator, IRenderer)
├── tests/         # Tests unitaires (13 tests)
├── run.py         # Point d'entrée principal 👈 DÉMARRER ICI
└── RAPPORT.md     # Documentation complète
```

---

## Niveaux d'IA

| Niveau | Algorithme | Profondeur | Temps | Qualité |
|--------|-----------|-----------|-------|---------|
| **Facile** | Minimax | 2 | 0.01s | ⭐ |
| **Moyen** | Alpha-Beta | 4 | 0.15s | ⭐⭐⭐ |
| **Difficile** | Alpha-Beta | 5 | 0.30s | ⭐⭐⭐⭐⭐ |

---

## Règles du Jeu

✅ Les pions se déplacent en diagonale vers l'avant  
✅ Les dames se déplacent en diagonale dans toutes les directions  
✅ **Capture obligatoire** - Si vous pouvez capturer, vous devez  
✅ **Multi-capture** - Continuez à capturer avec la même pièce  
✅ **Promotion** - Un pion atteignant le bout devient dame  
✅ **Victoire** - L'adversaire n'a plus de pièces ou de coups  

---

## Commandes Utiles

```bash
# Lancer le jeu
python run.py

# Tests
pytest tests/ -v

# Voir la structure
tree /F                    # Windows
find . -name "*.py"        # Linux/Mac

# Performance IA
python run.py
# Puis choisir option 5
```


## Liens Utiles

- **RAPPORT.md** - Documentation complète (architecture, algorithmes, tests)
- **tests/test_game.py** - Exemples d'utilisation du code
- **models/game_state.py** - Règles du jeu implémentées
- **ai/search.py** - Algorithmes Minimax et Alpha-Beta

---

