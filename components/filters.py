import streamlit as st
from .data_loader import get_countries, get_years, get_disciplines, load_all_participations


def sidebar_filters():
    """Crée la barre latérale avec les filtres."""
    st.sidebar.markdown(
        '<div style="font-size:0.8rem; font-weight:600; color:#64748b; text-transform:uppercase; '
        'letter-spacing:0.05em; margin-bottom:0.5rem;">Filtres</div>',
        unsafe_allow_html=True,
    )

    df = load_all_participations()
    available_columns = df.columns.tolist()

    countries = get_countries()
    years = get_years()
    disciplines = get_disciplines()

    if countries:
        selected_countries = st.sidebar.multiselect("Pays", options=countries, default=[])
    else:
        selected_countries = []

    if years:
        selected_years = st.sidebar.multiselect("Années", options=years, default=[])
    else:
        selected_years = []

    if disciplines:
        selected_disciplines = st.sidebar.multiselect("Disciplines", options=disciplines, default=[])
    else:
        selected_disciplines = []

    if "Medal" in available_columns:
        selected_medals = st.sidebar.multiselect("Médailles", options=["Gold", "Silver", "Bronze"], default=["Gold", "Silver", "Bronze"])
    else:
        selected_medals = []

    if "gender" in available_columns:
        gender_values = sorted(df["gender"].dropna().unique().tolist())
        selected_gender = st.sidebar.selectbox("Genre", options=["All"] + gender_values, index=0)
    else:
        selected_gender = "All"

    return {
        "countries": selected_countries,
        "years": selected_years,
        "disciplines": selected_disciplines,
        "medals": selected_medals,
        "gender": selected_gender,
    }


def apply_filters(df, filters):
    """Applique les filtres à un DataFrame."""
    filtered_df = df.copy()

    if filters["countries"] and "noc" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["noc"].isin(filters["countries"])]

    if filters["years"] and "year" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["year"].isin(filters["years"])]

    if filters["disciplines"] and "discipline" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["discipline"].isin(filters["disciplines"])]

    if filters["medals"] and "medal" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["medal"].isin(filters["medals"])]

    if filters["gender"] != "All" and "gender" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["gender"] == filters["gender"]]

    return filtered_df
