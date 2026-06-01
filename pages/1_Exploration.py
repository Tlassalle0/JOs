import streamlit as st
from components.data_loader import load_all_participations, get_available_columns
from components.filters import sidebar_filters, apply_filters

st.set_page_config(layout="wide")
st.title("🔍 Exploration des données")

# Afficher les colonnes disponibles
with st.expander("Colonnes disponibles dans les données"):
    cols = get_available_columns()
    st.write(cols)

filters = sidebar_filters()
df = load_all_participations()
filtered_df = apply_filters(df, filters)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total d'entrées", len(filtered_df))
col2.metric("Pays distincts", filtered_df['noc'].nunique() if 'noc' in filtered_df.columns else 0)
col3.metric("Années", len(filtered_df['year'].unique()) if 'year' in filtered_df.columns else 0)
col4.metric("Disciplines", filtered_df['discipline'].nunique() if 'discipline' in filtered_df.columns else 0)

st.markdown("---")

csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Télécharger les données filtrées (CSV)",
    data=csv,
    file_name='filtered_olympic_data.csv',
    mime='text/csv'
)

st.subheader("Données filtrées")
st.dataframe(filtered_df, use_container_width=True, height=600)

if st.checkbox("Afficher le résumé statistique"):
    st.subheader("Résumé statistique")
    numeric_cols = filtered_df.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_cols) > 0:
        st.write(filtered_df[numeric_cols].describe())
    else:
        st.info("Aucune colonne numérique disponible.")
