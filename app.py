import streamlit as st
from components.style import inject_style, metric_card, feature_card
from components.data_loader import load_all_participations, load_athletism, load_swimming

st.set_page_config(
    page_title="YPerf - Performance Olympique 2028",
    page_icon="\U0001f3c5",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_style()

# Hero
st.markdown(
    """<div class="hero-banner">
        <h1>\U0001f3c5 YPerf — Performance Olympique 2028</h1>
        <p>Explorez les performances olympiques historiques et découvrez les tendances
        qui faconneront les Jeux de Los Angeles 2028.</p>
    </div>""",
    unsafe_allow_html=True,
)

# Load data for stats
df = load_all_participations()
df_ath = load_athletism()
df_swim = load_swimming()

# Global metrics
st.markdown('<div class="section-header">Vue d\'ensemble</div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1:
    metric_card("\U0001f3c5", f"{len(df):,}", "Participations")
with c2:
    metric_card("\U0001f30d", f"{df['noc'].nunique() if 'noc' in df.columns else 0}", "Pays")
with c3:
    metric_card("\U0001f4c5", f"{df['year'].nunique() if 'year' in df.columns else 0}", "Éditions")
with c4:
    metric_card("\U0001f3c6", f"{df['discipline'].nunique() if 'discipline' in df.columns else 0}", "Disciplines")

st.markdown("")

# Features
st.markdown('<div class="section-header">Fonctionnalités</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    feature_card(
        "\U0001f50d",
        "Exploration",
        "Parcourez les données historiques des JO avec des filtres interactifs par pays, année, discipline et genre.",
    )
with c2:
    feature_card(
        "\U0001f4ca",
        "Visualisations",
        "Tableaux de bord interactifs : classements pays, évolution temporelle, disciplines, genre et athlètes.",
    )
with c3:
    feature_card(
        "\U0001f52e",
        "Prédictions 2028",
        "Modèle CatBoost pour prédire les temps de natation olympique et identifier les favoris de Los Angeles 2028.",
    )

st.markdown("")

# Datasets
st.markdown('<div class="section-header">Données chargées</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        f"""<div class="metric-card" style="text-align:left;">
            <div class="metric-label">all_participations.csv</div>
            <div class="metric-value" style="font-size:1.2rem;">{len(df):,} lignes</div>
        </div>""",
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f"""<div class="metric-card" style="text-align:left;">
            <div class="metric-label">athletism_completed.csv</div>
            <div class="metric-value" style="font-size:1.2rem;">{len(df_ath):,} lignes</div>
        </div>""",
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        f"""<div class="metric-card" style="text-align:left;">
            <div class="metric-label">swimming.csv</div>
            <div class="metric-value" style="font-size:1.2rem;">{len(df_swim):,} lignes</div>
        </div>""",
        unsafe_allow_html=True,
    )

st.sidebar.success("Sélectionnez une page dans le menu.")
