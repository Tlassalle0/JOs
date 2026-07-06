import streamlit as st
from .data_loader import get_countries, get_years, get_disciplines, load_all_participations

def sidebar_filters():
    """Crée la barre latérale avec les filtres communs."""
    st.sidebar.header("Filtres")
    
    df = load_all_participations()
    available_columns = df.columns.tolist()

    countries = get_countries()
    years = get_years()
    disciplines = get_disciplines()

    # Définir les valeurs par défaut basées sur la fréquence d'apparition
    default_countries = []
    default_years = []
    if 'noc' in df.columns and len(countries) > 0:
        # Top 5 pays les plus fréquents
        top_countries = df['noc'].value_counts().nlargest(5).index.tolist()
        default_countries = [c for c in top_countries if c in countries]
    if 'year' in df.columns and len(years) > 0:
        # Top 5 années les plus fréquentes, triées par ordre croissant
        top_years = df['year'].value_counts().nlargest(5).index.tolist()
        default_years = sorted([y for y in top_years if y in years])

    # Filtre par pays
    if countries:
        selected_countries = st.sidebar.multiselect(
            "Pays",
            options=countries,
            default=default_countries
        )
    else:
        selected_countries = []
        st.sidebar.warning("Pas de données de pays")

    # Filtre par année
    if years:
        selected_years = st.sidebar.multiselect(
            "Années",
            options=years,
            default=default_years
        )
    else:
        selected_years = []
        st.sidebar.warning("Pas de données d'années")

    # Filtre par discipline
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