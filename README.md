# 🎮 Jeu de Dames avec IA - Architecture Professionnelle

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Tests](https://img.shields.io/badge/Tests-14%2F14-success)
![Architecture](https://img.shields.io/badge/Architecture-Professionnelle-purple)
![GUI](https://img.shields.io/badge/GUI-Tkinter-green)

## 🚀 Démarrage Rapide

```bash
# Lancer le jeu
python run.py

# Tests
pytest tests/ -v
```

**👉 Voir [QUICKSTART.md](QUICKSTART.md) pour le guide complet**

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
projet/
├── models/         # Logique métier (Board, Move, GameState)
├── ai/            # Intelligence artificielle (3 niveaux)
├── gui/           # Interface graphique (Tkinter)
├── interfaces/    # Abstractions (IPlayer, IEvaluator, IRenderer)
├── tests/         # Tests unitaires (14 tests)
├── run.py         # 👈 DÉMARRER ICI
├── demo.py        # Démonstration rapide
├── RAPPORT.md     # Documentation complète
└── QUICKSTART.md  # Guide de démarrage
```

---

## 🎯 Niveaux d'IA

| Niveau | Algorithme | Profondeur | Nœuds | Temps |
|--------|-----------|-----------|-------|-------|
| **Facile** | Minimax | 2 | ~57 | 0.004s |
| **Moyen** | Alpha-Beta | 4 | ~518 | 0.076s |
| **Difficile** | Alpha-Beta | 5 | ~2181 | 0.338s |

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
pytest tests/ -v

# Démonstration
python demo.py
```

**14 tests unitaires:**
- Setup du plateau (4)
- Déplacement des pièces (3)
- IA et évaluation (4)
- État du jeu (3)

---

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Guide de démarrage rapide
- **[RAPPORT.md](RAPPORT.md)** - Documentation technique complète
- **[tests/test_game.py](tests/test_game.py)** - Exemples d'utilisation

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
- Profondeur 2
- ~57 nœuds

### Alpha-Beta (Moyen/Difficile)
- Élagage des branches
- Profondeur 4-5
- 2× plus rapide que Minimax
- Tri des coups (captures en premier)

### Évaluations
1. **Matériel** - Pion=1, Dame=5
2. **Mobilité** - Matériel + bonus coups
3. **Avancé** - + position, promotion, centre

---

## 💻 Technologies

- **Python 3.8+** (type hints, clean code)
- **Tkinter** (interface graphique built-in)
- **pytest** (tests unitaires)
- **Architecture SOLID** (Clean Architecture)

---

## 🏆 Points Forts

✅ **Architecture professionnelle** - Séparation models/ai/gui/interfaces  
✅ **Code propre** - Type hints, docstrings, nommage clair  
✅ **Tests complets** - 14 tests unitaires, 100% pass  
✅ **IA performante** - Alpha-Beta avec optimisations  
✅ **Interface simple** - Tkinter, aucune dépendance externe  
✅ **Extensible** - Interfaces abstraites, Open/Closed principle  

---

## � Conclusion

Ce projet démontre une **maîtrise complète** des concepts suivants:

- ✅ Architecture logicielle professionnelle
- ✅ Algorithmes de recherche en IA (Minimax, Alpha-Beta)
- ✅ Programmation orientée objet (SOLID)
- ✅ Interfaces graphiques (Tkinter)
- ✅ Tests unitaires (pytest)
- ✅ Documentation technique

Le code est **propre, testable, maintenable et extensible**.

---

**Auteur:** Projet L3 S2 AI  
**Date:** Février 2026  
**Version:** 2.0 
