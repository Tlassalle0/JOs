import streamlit as st
import plotly.express as px
from components.data_loader import load_all_participations
from components.filters import sidebar_filters, apply_filters
from components.predictor import predict_2028, get_top_athletes_prediction

st.set_page_config(layout="wide")
st.title("🔮 Prédictions JO 2028")

filters = sidebar_filters()
df = load_all_participations()
filtered_df = apply_filters(df, filters)

st.markdown("### Méthodologie")
st.info(
    """
    Les prédictions sont basées sur l'analyse des tendances linéaires du nombre de médailles
    par pays au fil des éditions précédentes. Le score combine la prédiction pour 2028
    et la force de la tendance (croissance ou décroissance).
    """
)

if filtered_df.empty:
    st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
else:
    predictions = predict_2028(filtered_df)

    if predictions.empty:
        st.warning("Données insuffisantes pour générer des prédictions (au moins 2 années par pays).")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top 10 des pays prédits pour 2028")
            top10 = predictions.head(10)
            fig = px.bar(top10, x='Score', y='Country', orientation='h',
                         title="Score prédictif", hover_data=['Predicted2028', 'RecentAvg', 'Trend'])
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Tableau des prédictions")
            st.dataframe(predictions, use_container_width=True, height=400)

        st.markdown("---")
        st.subheader("Analyse par pays")
        if 'Country' in predictions.columns:
            selected_country = st.selectbox("Sélectionner un pays", options=predictions['Country'].tolist())
            if selected_country:
                country_data = filtered_df[filtered_df['noc'] == selected_country]
                if 'year' in country_data.columns:
                    medal_by_year = country_data.groupby('year').size().reset_index(name='MedalCount')
                    fig = px.line(medal_by_year, x='year', y='MedalCount', markers=True,
                                  title=f"Évolution des médailles de {selected_country}")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Données d'année non disponibles.")
        else:
            st.info("Pas de pays dans les prédictions.")

    st.markdown("---")
    st.subheader("🏃 Athlètes à suivre en 2028")
    top_athletes = get_top_athletes_prediction(filtered_df, top_n=15)
    if not top_athletes.empty:
        fig = px.bar(top_athletes, x='MedalCount', y='Name', orientation='h',
                     color='Country', title="Athlètes les plus médaillés récemment")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Données insuffisantes pour identifier les athlètes.")

    st.markdown("---")
    if not predictions.empty:
        csv_pred = predictions.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger les prédictions (CSV)",
            data=csv_pred,
            file_name='predictions_2028.csv',
            mime='text/csv'
        )
    else:
        st.info("Aucune prédiction à télécharger.")
