import streamlit as st
from components.style import inject_style, metric_card, section_header, styled_divider
from components.data_loader import load_all_participations, get_available_columns
from components.filters import sidebar_filters, apply_filters

st.set_page_config(layout="wide")
inject_style()
st.title("\U0001f50d Exploration des données")

filters = sidebar_filters()
df = load_all_participations()
filtered_df = apply_filters(df, filters)

# Metrics
section_header("Indicateurs")
c1, c2, c3, c4 = st.columns(4)
with c1:
    metric_card("\U0001f4cb", f"{len(filtered_df):,}", "Entrées")
with c2:
    metric_card("\U0001f30d", f"{filtered_df['noc'].nunique() if 'noc' in filtered_df.columns else 0}", "Pays")
with c3:
    metric_card("\U0001f4c5", f"{filtered_df['year'].nunique() if 'year' in filtered_df.columns else 0}", "Années")
with c4:
    metric_card("\U0001f3c6", f"{filtered_df['discipline'].nunique() if 'discipline' in filtered_df.columns else 0}", "Disciplines")

styled_divider()

# Download
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "\U0001f4e5 Télécharger les données filtrées (CSV)",
    csv,
    "filtered_olympic_data.csv",
    "text/csv",
    width="content",
)

# Data
section_header("Données filtrées")
st.dataframe(filtered_df, width="stretch", height=500)

# Stats
with st.expander("\U0001f4ca Résumé statistique"):
    numeric_cols = filtered_df.select_dtypes(include=["float64", "int64"]).columns
    if len(numeric_cols) > 0:
        st.dataframe(filtered_df[numeric_cols].describe(), width="stretch")
    else:
        st.info("Aucune colonne numérique disponible.")
