# YPerf - Performance Olympique 2028

Application de data storytelling pour explorer les performances olympiques historiques et faire des prédictions pour les Jeux Olympiques de Los Angeles 2028.

## Sommaire

- [Description](#description)
- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [Livrables](#livrables)
- [Licence](#licence)

## Description

YPerf est une start-up fictive qui anticipe les tendances et performances sportives mondiales en vue des Jeux Olympiques de 2028. L'application permet d'analyser les résultats des JO précédents par sport, pays et genre, de visualiser l'évolution des performances et d'identifier les athlètes et pays en progression.

## Fonctionnalités

- **Exploration** : navigation interactive dans les données avec filtres (pays, années, disciplines, médailles, genre)
- **Visualisations** : graphiques interactifs (barres, lignes, camemberts, boîtes à moustaches) pour analyser les tendances
- **Prédictions** : modèle de régression linéaire pour prédire les médailles par pays et identifier les athlètes prometteurs
- **Prédictions Natation** : modèle CatBoost pour prédire les temps de natation (nécessite le modèle entraîné)
- **Documentation intégrée** : page À propos avec le manuel d'utilisation

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets)
- Accès au dossier `data/2-cleaned_data/` contenant les CSV : `all_participations.csv`, `athletism_completed.csv`, `swimming.csv`
- Pour la prédiction en natation : `catboost` (facultatif si vous n'utilisez pas cette page)

## Installation

1. Cloner le dépôt (ou extraire l'archive) :
   ```bash
   cd JOs
   ```

2. (Optionnel) Créer un environnement virtuel :
   ```bash
   python -m venv venv
   # Sur Windows :
   venv\Scripts\activate
   # Sur macOS/Linux :
   source venv/bin/activate
   ```

3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

Lancer l'application Streamlit :

```bash
streamlit run app.py
```

Le navigateur s'ouvre automatiquement sur `http://localhost:8501`. Utilisez la barre latérale pour naviguer entre les pages et appliquer des filtres.

### Pages disponibles

- **Accueil** : présentation du projet et vue d'ensemble des données
- **Visualisations** : tableau de bord analytique avec onglets (Pays, Temporel, Disciplines, Genre, Athlètes, Natation, Athlétisme, Prédictions, Exploration)
- **Prédictions** : modèle de régression linéaire pour les médailles par pays et analyse des athlètes
- **Natation** : prédiction des temps de natation avec CatBoost (modèle à entraîner séparément)
- **À propos** : documentation technique et manuel d'installation

## Structure du projet

```
.
├── app.py                          # Point d'entrée Streamlit
├── components/                     # Modules partagés
│   ├── data_loader.py              # Chargement et cache des données
│   ├── filters.py                  # Filtres sidebar
│   ├── predictor.py                # Modèle de prédiction médailles
│   └── swimming_predictor.py       # Modèle CatBoost natation
├── pages/                          # Pages Streamlit
│   ├── 1_Exploration.py
│   ├── 2_Visualisations.py
│   ├── 3_Predictions.py
│   ├── 4_Apropos.py
│   └── 5_Swimming.py
├── scripts/                        # Scripts de traitement des données
│   ├── complete_athletism.py       # Complète les données d'athlétisme
│   └── list_event.py               # Liste les événements d'athlétisme
├── notebooks/                      # Jupyter Notebooks
│   ├── clean.ipynb                 # Nettoyage des données
│   ├── swimming_data.ipynb         # Visualisation natation
│   └── swimming_prediction.ipynb   # Entraînement modèle CatBoost
├── data/
│   ├── 1-raw_data/                 # Données brutes
│   └── 2-cleaned_data/             # Données nettoyées (CSV)
├── model/                          # Artifacts d'entraînement
│   ├── swimming_model.cbm          # Modèle CatBoost (à générer)
│   └── catboost_info/
├── .streamlit/config.toml          # Configuration Streamlit
├── requirements.txt                # Dépendances Python
├── README.md
└── .gitignore
```

## Livrables

- Dépôt Git avec le code et la documentation
- Jupyter Notebook retraçant la démarche d'analyse
- Application Streamlit déployée localement
- Documentation technique et manuel d'installation (ce README)

## Remarques

- Les données doivent être placées dans le dossier `data/2-cleaned_data/` à la racine du projet.
- Certaines visualisations nécessitent des colonnes spécifiques (Country, Year, Medal, Discipline, Age, Name, Gender). Assurez-vous que vos données les contiennent.
- Les modèles de prédiction pour les médailles utilisent une régression linéaire simple et peuvent être améliorés.
- Le modèle de prédiction de natation (CatBoost) doit être entraîné au préalable en exécutant le notebook `notebooks/swimming_prediction.ipynb` et en sauvegardant le modèle sous `model/swimming_model.cbm`.

## Licence

Projet éducatif - Ynov Lyon
