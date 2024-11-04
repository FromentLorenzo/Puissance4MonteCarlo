# Puissance4MonteCarlo

Notre projet consiste à développer une intelligence artificielle pour le jeu de Puissance 4 en Python, en combinant les approches de Monte Carlo Tree Search (MCTS) et de Q-learning.

Le MCTS est particulièrement efficace pour évaluer les coups lorsque la partie est déjà avancée, car il peut anticiper les mouvements jusqu’à 10-15 coups à l’avance. Cependant, au début du jeu, MCTS peut manquer de direction et se retrouver dans des positions désavantageuses, car il n’a pas encore accumulé assez d’informations pour choisir les meilleurs mouvements.

C’est ici que le Q-learning devient un complément idéal. En permettant à l’IA d’apprendre des récompenses associées aux différentes positions et actions, le Q-learning aide l’algorithme à prendre des décisions plus éclairées dès le début de la partie. Cette synergie entre MCTS et Q-learning permet de construire une IA performante, capable d'optimiser sa stratégie à la fois dans les premiers coups et dans les phases avancées de jeu.

## Prérecquis 

Notre projet nécessite Python 3, Numpy et Pygame.

## Comment utiliser notre projet ?

Pour lancer une partie contre notre agent hybride :  
`python game_with_hybrid.py`   
Pour créer et remplir notre Q-table :   
`python q_learning_mcts_agent.py`  
Pour obtenir des statistiques entre deux agents :  
`python statistics.py`  
`python statistics_hybrid.py`  

## Statistiques

**Q-learning vs MCTS**

| Temps par coup du MCTS (s) | Victoires du Q-learning | Egalité | Victoires du MCTS |
|-----------------|-----------------|-----------------|-----------------|
| 0.01  | 70 | 1 | 29 |
| 0.05  | 62 | 0 | 38 |
| 0.1   | 53 | 1 | 46 |
| 0.5   | 42 | 1 | 57 |
| 1     | 33 | 0 | 67 |
| 2     | 24 | 1 | 75 |
| 5     | 19 | 0 | 81 |

**Hybrid vs MCTS**

| Temps par coup du MCTS (s) | Victoires de l'hybride | Egalité | Victoires du MCTS |
|-----------------|-----------------|-----------------|-----------------|
| 0.01  | 59 | 1 | 40 |
| 0.05  | 57 | 0 | 43 |
| 0.1   | 56 | 1 | 43 |
| 0.5   | 53 | 0 | 47 |
| 1     | 52 | 0 | 48 |
| 2     | 49 | 2 | 49 |
| 5     | 50 | 1 | 49 |

### Sources

Connect 4 Display using Pygame :  
https://www.askpython.com/python/examples/connect-four-game  
Connect 4 MCTS (Monte Carlo Tree Search) implementation :  
https://www.harrycodes.com/blog/monte-carlo-tree-search#monte-carlo-tree-search-mcts  
