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
- **Prédictions** : modèles de régression linéaire pour prédire les performances 2028 et identifier les pays et athlètes prometteurs
- **Documentation intégrée** : page À propos avec le manuel d'utilisation

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets)
- Accès au dossier `cleaned_data/` contenant les CSV : `all_participations.csv`, `athletism_completed.csv`, `swimming.csv`

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
streamlit run app/app.py
```

Le navigateur s'ouvre automatiquement sur `http://localhost:8501`. Utilisez la barre latérale pour naviguer entre les pages et appliquer des filtres.

### Pages disponibles

- **Accueil** : présentation du projet et vue d'ensemble des données
- **Exploration** : tableau de données avec filtres et téléchargement CSV
- **Visualisations** : graphiques interactifs par thématique
- **Prédictions** : modèles de prédiction pour 2028, classement des pays et athlètes
- **À propos** : documentation technique et manuel d'installation

## Structure du projet

```
.
├── app/                            # Application Streamlit
│   ├── app.py                      # Configuration et page d'accueil
│   ├── __init__.py
│   ├── components/                 # Modules partagés
│   │   ├── data_loader.py          # Chargement et cache des données
│   │   ├── filters.py              # Filtres communs (sidebar)
│   │   └── predictor.py            # Modèles de prédiction
│   ├── pages/                      # Pages de l'application
│   │   ├── 1_Exploration.py
│   │   ├── 2_Visualisations.py
│   │   ├── 3_Predictions.py
│   │   └── 4_Apropos.py
│   ├── utils/                      # Utilitaires divers (à compléter)
│   └── .streamlit/                 # Configuration Streamlit
│       └── config.toml
├── cleaned_data/                   # Données fournies (CSV)
│   ├── all_participations.csv
│   ├── athletism_completed.csv
│   └── swimming.csv
├── raw_data/                       # Données brutes (optionnel)
├── requirements.txt                # Dépendances Python
├── README.md                       # Ce fichier
└── .gitignore                      # Fichiers ignorés par Git
```

## Livrables

- Dépôt Git avec le code et la documentation
- Jupyter Notebook retraçant la démarche d'analyse
- Application Streamlit déployée localement
- Documentation technique et manuel d'installation (ce README)

## Remarques

- Les données doivent être placées dans le dossier `cleaned_data/` à la racine du projet.
- Certaines visualisations nécessitent des colonnes spécifiques (Country, Year, Medal, Discipline, Age, Name, Gender). Assurez-vous que vos données les contiennent.
- Les modèles de prédiction sont simples (régression linéaire) et peuvent être améliorés.

## Licence

Projet éducatif - YNov Bordeaux
