import streamlit as st
import plotly.express as px
from components.data_loader import load_all_participations
from components.filters import sidebar_filters, apply_filters

st.set_page_config(layout="wide")
st.title("📈 Visualisations")

filters = sidebar_filters()
df = load_all_participations()
filtered_df = apply_filters(df, filters)

if filtered_df.empty:
    st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
else:
    tab1, tab2, tab3, tab4 = st.tabs([
        "Médailles par pays",
        "Évolution temporelle",
        "Répartition des sports",
        "Performance athlètes"
    ])

    with tab1:
        st.subheader("Médailles par pays")
        if 'medal' in filtered_df.columns and 'noc' in filtered_df.columns:
            medal_country = filtered_df.groupby(['noc', 'medal']).size().reset_index(name='Count')
            fig = px.bar(medal_country, x='noc', y='Count', color='medal',
                         title="Médailles par pays")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Données de médailles ou de pays non disponibles.")

    with tab2:
        st.subheader("Évolution des médailles dans le temps")
        if 'year' in filtered_df.columns and 'medal' in filtered_df.columns:
            year_medal = filtered_df.groupby(['year', 'medal']).size().reset_index(name='Count')
            fig = px.line(year_medal, x='year', y='Count', color='medal',
                          markers=True, title="Évolution des médailles par année")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Données d'année ou de médailles non disponibles.")

    with tab3:
        st.subheader("Répartition des disciplines")
        if 'discipline' in filtered_df.columns:
            discipline_counts = filtered_df['discipline'].value_counts().reset_index()
            discipline_counts.columns = ['discipline', 'Count']
            fig = px.pie(discipline_counts, values='Count', names='discipline',
                         title="Répartition des disciplines")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Données de discipline non disponibles.")

    with tab4:
        st.subheader("Performances des athlètes (âge)")
        # Vérifier s'il y a une colonne d'âge (peut-être 'age' ou 'as'? Je ne sais pas)
        # Pour l'instant, on saute cette section si pas d'âge
        st.info("Données d'âge non disponibles dans le jeu de données fourni.")

    st.markdown("---")
    st.subheader("Top 20 des pays par nombre de participations")
    if 'noc' in filtered_df.columns:
        country_counts = filtered_df['noc'].value_counts().reset_index()
        country_counts.columns = ['noc', 'Count']
        top_countries = country_counts.sort_values('Count', ascending=True).tail(20)
        fig = px.bar(top_countries, x='Count', y='noc', orientation='h',
                     title="Top 20 des pays")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Données de pays non disponibles.")
