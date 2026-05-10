# 🎮 Jeu de Dames avec IA 

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Tests](https://img.shields.io/badge/Tests-14%2F14-success)
![Architecture](https://img.shields.io/badge/Architecture-Professionnelle-purple)
![GUI](https://img.shields.io/badge/GUI-Tkinter-green)

## 🚀 Démarrage Rapide

```bash
# Lancer le jeu
python run.py

```
Exemples utiles:

```bash
# Lancer les benchmarks d'évaluateurs (génére CSV + PNG sous docs/benchmarks)
python scripts/benchmark_evaluators.py

# Résumer les tournois et générer le tableau de bord
python scripts/summarize_tournaments.py

# Lancer un tournoi automatisé (génére résultats sous tournaments/)
python run_tournament.py
```

---

## 📋 Ce Projet

Un jeu de Dames complet avec:
- ✅ **3 niveaux d'IA** (Easy/Medium/Hard)
- ✅ **Interface Tkinter** (simple et rapide)
- ✅ **Architecture Clean** (models, ai, gui, interfaces)
- ✅ **14 tests unitaires** (100% pass)
- ✅ **Algorithmes IA** (Minimax, Alpha-Beta)

---

## 🏗️ Architecture

```
Jeu-Dames-Ai/
├── models/          # Logique métier (Board, Move, GameState)
├── ai/              # Intelligence artificielle (Minimax, Alpha-Beta)
├── gui/             # Interface graphique (Tkinter)
├── interfaces/      # Abstractions (IPlayer, IEvaluator, IRenderer)
├── scripts/         # Scripts d'analyse (benchmarks, résumés)
├── tournaments/     # Résultats et utilitaires de tournoi
├── tests/           # Tests unitaires (14 tests)
├── docs/            # Documentation et résultats (benchmarks, rapports)
├── run.py           # 👈 DÉMARRER ICI (menu interactif)
└── run_tournament.py # Lancer tournois automatisés
```

---


## 🖼️ Interface Graphique

### Tkinter (Inclus dans Python)

- Automatique sur toutes les versions
- Interface fonctionnelle et réactive
- Damier avec cases jouables
- Sélection au clic
- Affichage des coups légaux
- Panneau d'informations

---

## ✅ Tests

```bash
# Lancer les tests
python tests/test_game.py
```


**14 tests unitaires:**
- Setup du plateau (4)
- Déplacement des pièces (3)
- IA et évaluation (4)
- État du jeu (3)

---

## 📚 Documentation

- **[docs/rapport](docs/rapport)** - Rapport complet
- **[tests/test_game.py](tests/test_game.py)** - Tests unitaires

---

## 🎮 Règles du Jeu

✅ Plateau 8×8, cases diagonales noires  
✅ Pions: déplacement diagonal avant  
✅ Dames: déplacement diagonal toutes directions  
✅ **Capture obligatoire** (règle officielle)  
✅ **Multi-capture** avec la même pièce  
✅ **Promotion** automatique (pion → dame)  

---

## 🧠 Algorithmes IA

### Minimax (Facile)
- Exploration exhaustive
- Profondeur 1
- ~8 nœuds

### Alpha-Beta (Moyen/Difficile)
- Élagage des branches
- Profondeur 3-5
- 2× plus rapide que Minimax
- Tri des coups (captures en premier)

### Évaluations
1. **Matériel** - Pion=1, Dame=5
2. **Mobilité** - Matériel + bonus coups
3. **Avancé** - + position, promotion, centre

---

## 💻 Technologies

- **Python 3.11+** (type hints, clean code)
- **Tkinter** (interface graphique built-in)
- **pytest** (tests unitaires)
- **Architecture SOLID** (Clean Architecture)


---

##  Conclusion

Ce projet démontre une **maîtrise complète** des concepts suivants:

- ✅ Architecture logicielle professionnelle
- ✅ Algorithmes de recherche en IA (Minimax, Alpha-Beta)
- ✅ Programmation orientée objet 
- ✅ Interfaces graphiques (Tkinter)
- ✅ Tests unitaires (pytest)
- ✅ Documentation technique

Le code est **propre, testable, maintenable et extensible**.

---

**Auteurs:** Messafri Marouane / Nekiche Adel  
**Date:** Mai 2026  
**Version:** 1.0 
