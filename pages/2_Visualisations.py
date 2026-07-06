import streamlit as st
import plotly.express as px
import pandas as pd
from components.style import inject_style, metric_card, section_header, styled_divider, PLOTLY_LAYOUT, CHART_COLORS, COLORS
from components.data_loader import load_all_participations, load_swimming
from components.filters import sidebar_filters, apply_filters

st.set_page_config(layout="wide")
inject_style()
st.title("\U0001f4ca Tableau de bord analytique")

filters = sidebar_filters()
df_main = load_all_participations()
filtered_main = apply_filters(df_main, filters)
df_swim = load_swimming()

if filtered_main.empty:
    st.warning("Aucune donnée ne correspond aux filtres.")
    st.stop()

medal_cols = ["Gold", "Silver", "Bronze"]
medal_count = 0
if "medal" in filtered_main.columns:
    medal_df = filtered_main[filtered_main["medal"].isin(medal_cols)].drop_duplicates(subset=["year", "discipline", "event_name", "medal"])
    medal_count = len(medal_df)

section_header("Indicateurs clés")
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    metric_card("\U0001f3c3", f"{len(filtered_main):,}", "Participations")
with c2:
    metric_card("\U0001f30d", f"{filtered_main['noc'].nunique() if 'noc' in filtered_main.columns else 0}", "Pays")
with c3:
    metric_card("\U0001f4c5", f"{filtered_main['year'].nunique() if 'year' in filtered_main.columns else 0}", "Éditions")
with c4:
    metric_card("\U0001f3c6", f"{filtered_main['discipline'].nunique() if 'discipline' in filtered_main.columns else 0}", "Disciplines")
with c5:
    metric_card("\U0001f947", f"{medal_count:,}", "Médailles")

if "medal" in filtered_main.columns and "noc" in filtered_main.columns:
    medals = filtered_main[filtered_main["medal"].isin(medal_cols)].copy().dropna(subset=["noc"])
    medals = medals.drop_duplicates(subset=["year", "discipline", "event_name", "medal"])
    medal_counts = medals["noc"].value_counts()
else:
    medals = pd.DataFrame()
    medal_counts = pd.Series()

LAYOUT = {**PLOTLY_LAYOUT, "title_text": ""}

# === 1. TOP 20 PAYS ===
styled_divider()
section_header("Classement des nations — médailles uniques")
if not medals.empty:
    country_medals = medals.groupby("noc").size().reset_index(name="Total")
    top20 = country_medals.sort_values("Total", ascending=True).tail(20)
    fig = px.bar(top20, x="Total", y="noc", orientation="h",
                 color="Total", color_continuous_scale=["#bae6fd", "#0ea5e9"])
    fig.update_layout(**LAYOUT, coloraxis_showscale=False, height=500)
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, width="stretch")

# === 2. PART DES MÉDAILLES TOP 5 DANS LE TEMPS ===
styled_divider()
section_header("Équilibre des puissances — top 5 pays dans le temps")
if all(c in filtered_main.columns for c in ["year", "noc", "medal"]) and not medals.empty:
    top5 = medals["noc"].value_counts().nlargest(5).index.tolist()
    data_top5 = medals[medals["noc"].isin(top5)]
    share = data_top5.groupby(["year", "noc"]).size().reset_index(name="Count")
    share["Share"] = share.groupby("year")["Count"].transform(lambda x: x / x.sum() * 100)
    fig2 = px.area(share, x="year", y="Share", color="noc", color_discrete_sequence=CHART_COLORS)
    fig2.update_layout(**LAYOUT, yaxis_title="Part (%)", xaxis_title="Année", height=400)
    st.plotly_chart(fig2, width="stretch")

# === 3. CROISSANCE DES PAYS PARTICIPANTS ===
styled_divider()
section_header("Croissance olympique — pays participants par édition")
if all(c in filtered_main.columns for c in ["year", "noc"]):
    winter_years = {1924,1928,1932,1936,1948,1952,1956,1960,1964,1968,1972,1976,1980,1984,1988,1992,1994,1998,2002,2006,2010,2014,2018,2022}
    n_countries = filtered_main.groupby("year")["noc"].nunique().reset_index(name="Pays")
    n_countries["Type"] = n_countries["year"].apply(lambda y: "Hiver" if y in winter_years else "Été")
    fig3 = px.bar(n_countries, x="year", y="Pays", color="Type",
                  color_discrete_map={"Été": "#0ea5e9", "Hiver": "#94a3b8"})
    fig3.update_layout(**LAYOUT, height=400, barmode="stack")
    fig3.update_traces(marker_line_width=0)
    st.plotly_chart(fig3, width="stretch")

# === 4. TOP 20 ATHLÈTES ===
styled_divider()
section_header("Légendes olympiques — top 20 athlètes")
athlete_col = next((c for c in ["as", "Name", "Athlete", "athlete_name"] if c in filtered_main.columns), None)
if athlete_col and "medal" in filtered_main.columns:
    top_ath = (
        filtered_main[filtered_main["medal"].isin(medal_cols)]
        .groupby(athlete_col).size().reset_index(name="Medals")
        .sort_values("Medals", ascending=False).head(20)
    )
    fig5 = px.bar(top_ath, x="Medals", y=athlete_col, orientation="h",
                  color="Medals", color_continuous_scale=["#bae6fd", "#0ea5e9"])
    fig5.update_layout(**LAYOUT, coloraxis_showscale=False, height=500)
    fig5.update_traces(marker_line_width=0)
    st.plotly_chart(fig5, width="stretch")

# === 6. RECORDS NATATION ===
styled_divider()
section_header("Records de natation — tendance par épreuve")
if not df_swim.empty and all(c in df_swim.columns for c in ["Year", "Stroke", "Distance", "Results"]):
    best = df_swim.groupby(["Year", "Stroke", "Distance"])["Results"].min().reset_index()
    c1, c2 = st.columns(2)
    with c1:
        sel_stroke = st.selectbox("Nage", best["Stroke"].unique(), key="vis_stroke")
    with c2:
        sel_dist = st.selectbox("Distance", best[best["Stroke"] == sel_stroke]["Distance"].unique(), key="vis_dist")
    chart_data = best[(best["Stroke"] == sel_stroke) & (best["Distance"] == sel_dist)]
    if not chart_data.empty:
        fig6 = px.line(chart_data, x="Year", y="Results", markers=True,
                       color_discrete_sequence=["#0ea5e9"],
                       title=f"{sel_stroke} — {sel_dist}m")
        fig6.update_layout(**LAYOUT,
                           yaxis_title="Temps (s)", xaxis_title="Année", height=400)
        st.plotly_chart(fig6, width="stretch")
