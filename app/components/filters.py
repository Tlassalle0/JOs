import streamlit as st
from .data_loader import get_countries, get_years, get_disciplines, load_all_participations

def sidebar_filters():
    """Crée la barre latérale avec les filtres communs."""
    st.sidebar.header("Filtres")
    
    # Charger les données pour détecter les colonnes disponibles
    df = load_all_participations()
    available_columns = df.columns.tolist()

    # Filtre par pays
    countries = get_countries()
    if countries:
        selected_countries = st.sidebar.multiselect(
            "Pays",
            options=countries,
            default=countries[:5] if len(countries) >= 5 else countries
        )
    else:
        selected_countries = []
        st.sidebar.warning("Pas de données de pays")

    # Filtre par année
    years = get_years()
    if years:
        selected_years = st.sidebar.multiselect(
            "Années",
            options=years,
            default=years[-5:] if len(years) >= 5 else years
        )
    else:
        selected_years = []
        st.sidebar.warning("Pas de données d'années")

    # Filtre par discipline
    disciplines = get_disciplines()
    if disciplines:
        selected_disciplines = st.sidebar.multiselect(
            "Disciplines",
            options=disciplines,
            default=[]
        )
    else:
        selected_disciplines = []
        st.sidebar.warning("Pas de données de disciplines")

    # Filtre par médaille (seulement si colonne présente)
    if 'Medal' in available_columns:
        medals = ['Gold', 'Silver', 'Bronze']
        selected_medals = st.sidebar.multiselect(
            "Médailles",
            options=medals,
            default=medals
        )
    else:
        selected_medals = []
        st.sidebar.info("Filtre médailles indisponible")

    # Filtre par genre (si disponible)
    if 'Gender' in available_columns:
        gender_options = ['M', 'F', 'All']
        selected_gender = st.sidebar.selectbox(
            "Genre",
            options=gender_options,
            index=2
        )
    else:
        selected_gender = 'All'
        st.sidebar.info("Filtre genre indisponible")

    return {
        'countries': selected_countries,
        'years': selected_years,
        'disciplines': selected_disciplines,
        'medals': selected_medals,
        'gender': selected_gender
    }

def apply_filters(df, filters):
    """Applique les filtres à un DataFrame."""
    filtered_df = df.copy()

    if filters['countries'] and 'noc' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['noc'].isin(filters['countries'])]

    if filters['years'] and 'year' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['year'].isin(filters['years'])]

    if filters['disciplines'] and 'discipline' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['discipline'].isin(filters['disciplines'])]

    if filters['medals'] and 'medal' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['medal'].isin(filters['medals'])]

    if filters['gender'] != 'All' and 'gender' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['gender'] == filters['gender']]

    return filtered_df