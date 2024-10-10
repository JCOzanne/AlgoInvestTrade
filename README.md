![logo AlgoTrade&Invest](https://user.oc-static.com/upload/2020/09/18/1600429119334_P6.png)

## Projet
Algo Invest & Trade est une société financière spécialisée dans l'investissement.
Elle souhaite optimiser ses stratégies d'investissement à l'aide d'algorithmes.
Ce projet permet le calcul de la meilleure combinaisons d'actions dans lesquelles 
investir en fonction de leur prix et de leur rendement avec la contrainte d'un budget maximal.

### structure du projet

Le projet est composé des fichiers :
- bruteforce.py 
- optimized.py  
Et du dossier data/ comprenant :
- dataset1.csv (fichier contenant 1001 actions/prix/rendement)
- dataset2.csv (fichier contenant 1000 actions/prix/rendement)
- dataset_brute_force.csv (fichier contenant 20 actions/prix/rendement)

### Fonctionnalités

Le fichier bruteforce.py lit les fichiers d'actions et cherche la combinaison d'actions
réalisant le meilleur profit en analysant toutes les combinaisons possibles.
Il affiche le temps d'exécution.
Le fichier optimized.py lit les fichiers d'actions en utilisant la programmation dynamique
(algorithme du sac à dos).
Il affiche le temps d'exécution.

### Installation

1. Cloner le dépôt :
`$ git clone https://github.com/JCOzanne/AlgoInvestTrade`  

2. Créer et activer l'environnement virtuel
- sur windows :  
`cd AlgoInvestTrade`  
`python -m venv env`  
`~env\scripts\activate`  

- sur MacOS / Linux  
`cd AlgoInvestTrade`  
`python3 -m venv env`  
`$ source/env/bin/activate`

3. Lancer le programme  
- sur windows :  
`python bruteforce.py (ou optimized.py)  nom_du_fichier`  
exemple : `python optimized.py dataset1`
- sur Mac OS / Linux :  
`python3 bruteforce.py (ou optimized.py)  nom_du_fichier`


