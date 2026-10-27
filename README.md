# 🚚 Optimisation de tournées de livraison — Théorie des graphes (VRP / CVRPTW)

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)
![NetworkX](https://img.shields.io/badge/NetworkX-graphes-2C7BB6)
![Domaine](https://img.shields.io/badge/Recherche%20opérationnelle-Optimisation%20combinatoire-success)

Projet de **recherche opérationnelle** autour du **problème de tournées de véhicules** (*Vehicle Routing Problem*, VRP), modélisé par la **théorie des graphes**. L'objectif : organiser la livraison d'un ensemble de clients par une flotte de camions, en minimisant le temps de parcours tout en respectant la **capacité** des véhicules et les **fenêtres horaires** de disponibilité des clients.

Le dépôt contient deux réalisations complémentaires : une **démonstration interactive** (`code.py`) qui construit des tournées avec des heuristiques simples et les affiche sous forme de graphe, et un **notebook de recherche complet** (`Livrable final.ipynb`) qui va jusqu'à une métaheuristique avancée validée sur des instances standard du domaine.

---

## 📑 Sommaire

1. [Le problème en bref](#-le-problème-en-bref)
2. [Contexte du projet](#-contexte-du-projet)
3. [Modélisation par les graphes](#-modélisation-par-les-graphes)
4. [Contenu du dépôt](#-contenu-du-dépôt)
5. [La démonstration interactive (`code.py`)](#-la-démonstration-interactive-codepy)
6. [Le notebook de recherche (`Livrable final.ipynb`)](#-le-notebook-de-recherche-livrable-finalipynb)
7. [Prérequis et installation](#-prérequis-et-installation)
8. [Utilisation](#-utilisation)
9. [Pistes d'amélioration](#-pistes-damélioration)
10. [Auteurs](#-auteurs)

---

## 📦 Le problème en bref

Imaginez un entrepôt (le **dépôt**) et une liste de **clients** à livrer, chacun situé à un endroit précis, réclamant une certaine quantité de marchandise et n'étant disponible que sur un créneau horaire. On dispose d'une flotte de **camions** de capacité limitée. La question : **quelles tournées faire emprunter aux camions** pour servir tous les clients, revenir au dépôt, et dépenser le moins de temps possible ?

Ce problème, appelé **CVRPTW** (*Capacitated Vehicle Routing Problem with Time Windows*), combine trois contraintes :

- **C** — *Capacitated* : un camion ne peut pas transporter plus que sa capacité ;
- **TW** — *Time Windows* : chaque client doit être livré pendant son créneau (un camion peut arriver en avance et attendre) ;
- et bien sûr le **retour au dépôt** à la fin de chaque tournée.

C'est un problème **NP-difficile** : il généralise le célèbre problème du voyageur de commerce. Au-delà de quelques dizaines de clients, il devient impossible de trouver la solution exacte en un temps raisonnable, d'où l'emploi d'**heuristiques** et de **métaheuristiques** qui cherchent de très bonnes solutions, à défaut de la meilleure.

---

## 🌍 Contexte du projet

Le projet répond à un scénario fictif inspiré d'un **appel à manifestation d'intérêt de l'ADEME** : une structure, « CesiCDP », cherche à optimiser des tournées de livraison pour réduire les kilomètres parcourus, donc la consommation de carburant et les émissions de gaz à effet de serre. Les applications réelles sont nombreuses : distribution de courrier et de colis, ramassage des ordures, maintenance de réseaux…

La démarche complète (modéliser, prouver la complexité, résoudre de façon approchée, valider statistiquement) est détaillée dans le rapport `Recapitulatif_Projet_CesiCDP_VRP.docx` et mise en œuvre dans le notebook.

---

## 🔗 Modélisation par les graphes

Le problème se représente naturellement par un **graphe orienté et pondéré** :

- chaque **sommet** est un lieu : le dépôt (sommet de départ et d'arrivée) ou un client ;
- chaque **arc** entre deux lieux porte un **poids** : le temps de trajet, calculé à partir des distances et de la vitesse des camions ;
- on y ajoute les données propres à chaque client (demande, fenêtre horaire, temps de service) et aux camions (capacité, vitesse).

Une **tournée** est alors un cycle partant du dépôt, passant par un sous-ensemble de clients, et y revenant. Résoudre le problème, c'est trouver l'ensemble de cycles (un par camion) qui couvre tous les clients au moindre coût, sans violer les contraintes. Le rapport formalise tout cela sous forme d'un **programme linéaire en nombres entiers (PLNE)** et démontre la NP-difficulté du problème par réduction depuis le voyageur de commerce.

---

## 📁 Contenu du dépôt

```
Theorie-Graphes-livraisons-de-clients/
├── code.py                                 # Démonstration interactive autonome (heuristiques + visualisation)
├── code.ipynb                              # Version notebook du même code
├── Livrable final.ipynb                    # Notebook de recherche complet (modélisation + métaheuristique ALNS)
├── Recapitulatif_Projet_CesiCDP_VRP.docx   # Rapport : contexte, modélisation, complexité, plan d'actions
├── images/                                 # Illustrations des algorithmes et des états de résolution
├── Python_3_-_Environnement/               # Notebooks de cours (support)
└── Python_3_-_Fonctionnalites_avancees/    # Notebooks de cours (support)
```

Deux niveaux de lecture coexistent donc : `code.py` pour **voir rapidement le principe en action**, et `Livrable final.ipynb` pour **la démarche de recherche aboutie**.

---

## 🖥 La démonstration interactive (`code.py`)

C'est le point d'entrée le plus simple pour découvrir le projet. Le script construit des tournées avec deux **heuristiques gloutonnes** et les affiche dans une fenêtre interactive (Matplotlib + NetworkX) où l'on passe d'un état à l'autre avec des boutons **← Précédent** et **Suivant →**.

Les trois états affichés sont :

1. **État 0 — Aucun algorithme** : les clients reliés dans l'ordre brut, comme point de départ.
2. **État 1 — Voisins proches + Horaires** : à partir du dépôt, on rejoint à chaque étape le client le plus « proche » en tenant compte du temps de trajet et des fenêtres horaires (heuristique du plus proche voisin).
3. **État 2 — Capacité + Horaires** : on découpe le parcours en plusieurs tournées de camions en respectant la capacité et les créneaux, ce qui fait apparaître plusieurs cycles de couleurs différentes.

Le graphe affiche, pour chaque sommet, la fenêtre horaire, la demande et le temps de service ; et pour chaque arc, le temps de trajet. Le terminal récapitule en parallèle le nombre de camions utilisés et le temps nécessaire pour parcourir tous les clients.

Le script peut générer des **instances aléatoires** (nombre de clients au choix) ou utiliser un petit **jeu de données d'exemple** intégré.

---

## 📓 Le notebook de recherche (`Livrable final.ipynb`)

Le notebook va nettement plus loin que la démonstration et déroule toute la démarche scientifique du projet :

- **modélisation mathématique** complète du CVRP et du CVRPTW sous forme de PLNE ;
- **preuve de complexité** (NP-difficulté par réduction depuis le voyageur de commerce) ;
- une **métaheuristique ALNS** (*Adaptive Large Neighbourhood Search*, recherche à grand voisinage adaptative) avec acceptation par **recuit simulé**, qui détruit puis répare des portions de solution pour s'échapper des optima locaux ;
- une **validation expérimentale** sur des **instances standard du domaine** (bibliothèque VRPLIB), en comparant les résultats aux meilleures solutions connues.

> C'est la pièce maîtresse pour un lecteur qui veut juger de la profondeur technique du projet.

---

## 🛠 Prérequis et installation

- **Python 3** (3.9 ou plus récent recommandé).
- Pour la démonstration `code.py` : **Matplotlib** et **NetworkX**.
- Pour le notebook : **Jupyter**, plus **NumPy** et la bibliothèque **vrplib** (chargement des instances standard). D'autres bibliothèques d'optimisation peuvent être utilisées selon les sections (voir le notebook).

### Installation

```bash
# 1. Récupérer le projet
git clone https://github.com/hugorako947/Theorie-Graphes-livraisons-de-clients.git
cd Theorie-Graphes-livraisons-de-clients

# 2. (Recommandé) créer un environnement virtuel
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows

# 3. Installer les dépendances de la démonstration
pip install matplotlib networkx

# 4. (Pour le notebook) installer Jupyter et les dépendances supplémentaires
pip install jupyter numpy vrplib
```

---

## ▶ Utilisation

### Lancer la démonstration interactive

```bash
python code.py
```

Le script pose d'abord quelques questions **dans le terminal** :

1. **`Instances aléatoires (o/n) ? :`**
   - `o` : des clients sont placés au hasard — il faut alors indiquer le **nombre de clients** ;
   - `n` : le jeu de données d'exemple intégré (4 clients) est utilisé.
2. La fenêtre de visualisation s'ouvre ensuite. Utilisez les boutons **← Précédent** et **Suivant →** pour parcourir les états (ordre brut → plus proche voisin → découpage par capacité) et observer comment les tournées se construisent.

> [!NOTE]
> La fenêtre interactive s'appuie sur Matplotlib. Dans un environnement sans affichage graphique (serveur distant, certains conteneurs), il faut un *backend* graphique disponible pour voir la fenêtre.

### Ouvrir le notebook de recherche

```bash
jupyter notebook "Livrable final.ipynb"
```

Exécutez les cellules dans l'ordre (menu **Run** → **Run All Cells**, ou cellule par cellule) pour suivre le fil : contexte, modélisation, complexité, implémentation de la métaheuristique, puis résultats expérimentaux.

> [!IMPORTANT]
> Le notebook télécharge une fois les instances de test (et leurs meilleures solutions connues) depuis un dépôt de référence. Une **connexion internet** est donc nécessaire au premier lancement des sections de validation.

---

## 💡 Pistes d'amélioration

- Fournir un fichier `requirements.txt` listant toutes les dépendances pour une installation en une commande.
- Unifier la démonstration `code.py` et le notebook, pour que la visualisation interactive affiche aussi les solutions de la métaheuristique ALNS, et pas seulement celles des heuristiques gloutonnes.
- Prendre en compte le **trafic par tranche horaire** (temps de trajet variables selon l'heure de départ), évoqué comme extension dans le rapport.
- Ajouter des mesures de performance (temps de calcul, écart aux meilleures solutions connues) directement dans la visualisation.

---

## 👥 Auteurs

Projet réalisé en équipe dans le cadre d'un module de recherche opérationnelle / théorie des graphes :

- **Hugo Rakotonanahary** — [@hugorako947](https://github.com/hugorako947)
- Saad
- Daoud

Le rapport complet (contexte ADEME, modélisation PLNE, preuve de complexité, choix des algorithmes et plan d'actions) est disponible dans `Recapitulatif_Projet_CesiCDP_VRP.docx`.
