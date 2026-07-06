import streamlit as st

st.set_page_config(layout="wide")
st.title("ℹ️ À propos du projet YPerf")

st.markdown(
    """
    ## YPerf - Performance Olympique 2028

    YPerf est une application de data storytelling développée dans le cadre d'un projet
    Fil Rouge. Elle permet d'explorer les performances olympiques historiques et de
    faire des projections pour les Jeux Olympiques de Los Angeles 2028.
    """
)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📚 Documentation technique")
    st.markdown(
        """
        ### Structure du projet
        - `app.py` : Page d'accueil et configuration
        - `pages/` : Pages de l'application (Exploration, Visualisations, Prédictions)
        - `components/` : Modules partagés (chargement données, filtres, prédiction)
        - `utils/` : Fonctions utilitaires (à développer)
        - `cleaned_data/` : Jeux de données nettoyés (fournis)

        ### Technologies utilisées
        - **Streamlit** : Framework pour l'application web interactive
        - **Pandas** : Manipulation des données
        - **Plotly** : Graphiques interactifs
        - **Scikit-learn** : Modèles de prédiction
        - **Statsmodels** : Analyses statistiques (optionnel)

        ### Workflow
        1. Acquisition des données (déjà fournies dans `cleaned_data/`)
        2. Nettoyage et structuration (hors scope de l'appli)
        3. Analyse exploratoire (page Exploration)
        4. Visualisation (page Visualisations)
        5. Modélisation prédictive (page Prédictions)
        """
    )

with col2:
    st.subheader("🛠️ Manuel d'installation")
    st.markdown(
        """
        ### Prérequis
        - Python 3.8 ou supérieur
        - pip (gestionnaire de paquets Python)

        ### Installation
        ```bash
        # Cloner le dépôt Git
        git clone <repo-url>
        cd JOs

        # Créer un environnement virtuel (recommandé)
        python -m venv venv
        venv\\Scripts\\activate  # Windows
        # source venv/bin/activate  # macOS/Linux

        # Installer les dépendances
        pip install -r requirements.txt
        ```

        ### Lancement de l'application
        ```bash
        streamlit run app.py
        ```

        L'application s'ouvre automatiquement dans le navigateur à l'adresse `http://localhost:8501`.
        """
    )

st.markdown("---")

st.subheader("📋 Livrables")
st.markdown(
    """
    - Dépôt Git avec tout le code et la documentation
    - Jupyter Notebook retraçant la démarche et les analyses
    - Application de data storytelling déployée localement
    - Documentation technique du projet et manuel d'installation et d'utilisation
    """
)

st.subheader("👥 Équipe")
st.markdown("Projet Fil Rouge - YNov Bordeaux")
