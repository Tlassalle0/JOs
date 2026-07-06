import streamlit as st

st.set_page_config(
    page_title="YPerf - Performance Olympique 2028",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏅 YPerf - Performance Olympique 2028")
st.markdown("---")
st.markdown(
    """
    ## Bienvenue dans l'application de data storytelling YPerf

    YPerf est une start-up qui anticipe les tendances et performances sportives mondiales
    en vue des Jeux Olympiques de 2028 à Los Angeles.

    ### Fonctionnalités principales :
    - **Exploration** : parcourez les données historiques des JO
    - **Visualisations** : graphiques interactifs des performances
    - **Prédictions** : modèles pour projet les nations et athlètes à suivre en 2028

    Utilisez le menu dans la barre latérale pour naviguer entre les pages.
    """
)

st.markdown("---")
st.markdown("### Données chargées :")
st.write("- all_participations.csv")
st.write("- athletism_completed.csv")
st.write("- swimming.csv")

st.sidebar.success(" Sélectionnez une page dans le menu ci-dessus.")
