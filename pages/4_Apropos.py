import streamlit as st
from components.style import inject_style, section_header, styled_divider

st.set_page_config(layout="wide")
inject_style()
st.title("\u2139\ufe0f À propos")

st.markdown(
    """<div class="hero-banner" style="padding:1.5rem 2rem;">
        <h1 style="font-size:1.6rem;">YPerf — Performance Olympique 2028</h1>
        <p>Application de data storytelling développée dans le cadre d'un projet Fil Rouge à Ynov Bordeaux.</p>
    </div>""",
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    section_header("\U0001f4da Documentation technique")
    st.markdown(
        """
        **Structure du projet**
        - `app.py` — Point d'entrée Streamlit
        - `pages/` — Pages de l'application
        - `components/` — Modules partagés (données, filtres, prédiction, style)
        - `scripts/` — Scripts de traitement des données
        - `notebooks/` — Jupyter Notebooks d'analyse
        - `data/` — Données brutes et nettoyées
        - `model/` — Artifacts d'entraînement CatBoost

        **Technologies**
        """
    )
    techs = ["Streamlit", "Pandas", "Plotly", "Scikit-learn", "CatBoost", "NumPy"]
    for tech in techs:
        st.markdown(f'<span class="tech-badge">{tech}</span>', unsafe_allow_html=True)

    st.markdown("")
    st.markdown(
        """
        **Workflow**
        1. Acquisition et nettoyage des données
        2. Analyse exploratoire
        3. Visualisation interactive
        4. Modélisation prédictive
        5. Déploiement Streamlit
        """
    )

with col2:
    section_header("\U0001f6e0\ufe0f Manuel d'installation")
    st.markdown(
        """
        **Prérequis**
        - Python 3.8+
        - pip

        **Installation**
        ```bash
        git clone <repo-url>
        cd JOs
        python -m venv venv
        venv\\Scripts\\activate   # Windows
        pip install -r requirements.txt
        ```

        **Lancement**
        ```bash
        streamlit run app.py
        ```
        """
    )

    st.markdown("")
    section_header("\U0001f4cb Livrables")
    st.markdown(
        """
        - Dépôt Git avec code et documentation
        - Jupyter Notebooks retraçant l'analyse
        - Application Streamlit déployée localement
        - Documentation technique et manuel d'utilisation
        """
    )

styled_divider()

section_header("\U0001f465 Équipe")
st.markdown(
    """<div class="info-box">
    <strong>Projet Fil Rouge — YNov Bordeaux</strong><br>
    Application de data storytelling pour les Jeux Olympiques de Los Angeles 2028.
    </div>""",
    unsafe_allow_html=True,
)
