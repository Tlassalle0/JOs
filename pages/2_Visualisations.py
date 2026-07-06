import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from components.data_loader import load_all_participations, load_athletism, load_swimming
from components.filters import sidebar_filters, apply_filters

st.set_page_config(layout="wide")
st.title("📊 YPerf - Tableau de bord analytique")

filters = sidebar_filters()
df_main = load_all_participations()
filtered_main = apply_filters(df_main, filters)

# Charger aussi les données détaillées si disponibles
df_ath = load_athletism()
df_swim = load_swimming()
# Appliquer filtres approximatifs (on ne peut pas filter facilement ces df car pas tous les mêmes colonnes)

if filtered_main.empty:
    st.warning("Aucune donnée ne correspond aux filtres.")
else:
    # ========== MÉTRIQUES GLOBALES ==========
    st.subheader("📌 Indicateurs clés")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Participations", f"{len(filtered_main):,}")
    c2.metric("Pays", filtered_main['noc'].nunique() if 'noc' in filtered_main.columns else 0)
    c3.metric("Années", filtered_main['year'].nunique() if 'year' in filtered_main.columns else 0)
    c4.metric("Disciplines", filtered_main['discipline'].nunique() if 'discipline' in filtered_main.columns else 0)
    if 'medal' in filtered_main.columns:
        c5.metric("Médailles", (filtered_main['medal'].notna() & filtered_main['medal'].isin(['Gold','Silver','Bronze'])).sum())
    st.markdown("---")

    # Pré-calculations pour les graphiques
    medal_cols = ['Gold', 'Silver', 'Bronze']
    if 'medal' in filtered_main.columns and 'noc' in filtered_main.columns:
        medals = filtered_main[filtered_main['medal'].isin(medal_cols)].copy()
        # Nettoyer les NaN dans 'noc'
        medals = medals.dropna(subset=['noc'])
        medal_counts = medals['noc'].value_counts()
    else:
        medals = pd.DataFrame()
        medal_counts = pd.Series()

    # ========== ONGLETS PRINCIPAUX ==========
    tabs = st.tabs([
        "🌍 Pays", 
        "📅 Temporel", 
        "🏟️ Disciplines", 
        "♂️ Genre",
        "🏃 Athlètes",
        "🏊 Natation",
        "🏋️ Athlétisme",
        "📈 Prédictions"
    ])

    # --- TAB 1: PAYS ---
    with tabs[0]:
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Classement pays (medailles)")
            if 'medal' in filtered_main.columns and 'noc' in filtered_main.columns:
                medals = filtered_main[filtered_main['medal'].isin(['Gold','Silver','Bronze'])]
                country_medals = medals.groupby('noc').size().reset_index(name='Total')
                top20 = country_medals.sort_values('Total', ascending=True).tail(20)
                fig = px.bar(top20, x='Total', y='noc', orientation='h', color='Total', title="Top 20 pays")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Données manquantes")

        with col_b:
            st.subheader("Part de marché par année (top 5)")
            if all(col in filtered_main.columns for col in ['year','noc','medal']):
                # Top 5 pays tous temps
                top5 = medals['noc'].value_counts().nlargest(5).index.tolist()
                data_top5 = medals[medals['noc'].isin(top5)]
                share = data_top5.groupby(['year','noc']).size().reset_index(name='Count')
                share['Share'] = share.groupby('year')['Count'].transform(lambda x: x / x.sum() * 100)
                share = share[['year','noc','Share']]
                fig2 = px.area(share, x='year', y='Share', color='noc', title="Part des médailles par année (top 5)")
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("Données incomplètes")

        st.markdown("---")
        col_c, col_d = st.columns(2)
        with col_c:
            st.subheader("Domination par discipline")
            if all(col in filtered_main.columns for col in ['noc','discipline','medal']):
                pivot = medals.pivot_table(index='noc', columns='discipline', values='medal', aggfunc='count', fill_value=0)
                # Prendre top 10 pays et top 10 disciplines
                top_countries = medal_counts.nlargest(10).index
                # Intersection avec l'index du pivot
                top_countries = [c for c in top_countries if c in pivot.index]
                if len(top_countries) == 0:
                    st.info("Pas de données suffisantes.")
                else:
                    top_disciplines = pivot.sum().nlargest(10).index
                    # Intersection avec les colonnes du pivot
                    top_disciplines = [d for d in top_disciplines if d in pivot.columns]
                    if not top_disciplines:
                        st.info("Pas de disciplines suffisantes.")
                    else:
                        fig3 = px.imshow(pivot.loc[top_countries, top_disciplines], title="Médailles par pays/discipline", aspect="auto")
                        st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info("Données incomplètes")

        with col_d:
            st.subheader("Heatmap pays × années")
            if all(col in filtered_main.columns for col in ['noc','year','medal']):
                heat = medals.pivot_table(index='noc', columns='year', values='medal', aggfunc='count', fill_value=0)
                # Limiter aux top 15 pays
                top15 = medal_counts.nlargest(15).index
                fig4 = px.imshow(heat.loc[top15], title="Médailles par pays et année", aspect="auto", color_continuous_scale='Viridis')
                st.plotly_chart(fig4, use_container_width=True)
            else:
                st.info("Données incomplètes")

        st.markdown("---")
        st.subheader("Taux de croissance des médailles par pays")
        if all(col in filtered_main.columns for col in ['noc','year','medal']):
            # Calculer le taux de croissance d'une élection à l'autre pour chaque pays
            counts = medals.groupby(['noc','year']).size().unstack(fill_value=0)
            counts['Growth'] = counts.pct_change(axis=1).mean(axis=1) * 100
            growth_df = counts[['Growth']].reset_index().sort_values('Growth', ascending=False).dropna()
            fig_g = px.bar(growth_df.head(20), x='Growth', y='noc', orientation='h', title="Pays avec la plus forte croissance moyenne")
            st.plotly_chart(fig_g, use_container_width=True)

    # --- TAB 2: TEMPOREL ---
    with tabs[1]:
        st.subheader("Évolution des médailles par année")
        if all(col in filtered_main.columns for col in ['year','medal']):
            by_year = filtered_main[filtered_main['medal'].isin(['Gold','Silver','Bronze'])].groupby(['year','medal']).size().reset_index(name='Count')
            fig = px.line(by_year, x='year', y='Count', color='medal', markers=True, title="Évolution des médailles par type")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Part des médailles par continent (top)")
            # Hypothèse : on aurait une colonne 'continent' sinon on skip
            if 'continent' in filtered_main.columns:
                cont_share = filtered_main.groupby(['year','continent']).size().groupby(level=0).apply(lambda x: x/x.sum()*100).reset_index(name='Share')
                fig2 = px.area(cont_share, x='year', y='Share', color='continent', title="Part par continent")
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("Ajoutez une colonne 'continent' pour cette vue.")

        with col_b:
            st.subheader("Nombre de pays participants par année")
            if 'noc' in filtered_main.columns and 'year' in filtered_main.columns:
                n_countries_by_year = filtered_main.groupby('year')['noc'].nunique().reset_index(name='Countries')
                fig3 = px.bar(n_countries_by_year, x='year', y='Countries', title="Pays participants par année")
                st.plotly_chart(fig3, use_container_width=True)

        st.markdown("---")
        st.subheader("Heatmap : Médailles (années × pays)")
        if all(col in filtered_main.columns for col in ['year','noc','medal']):
            heat = medals.pivot_table(index='year', columns='noc', values='medal', aggfunc='count', fill_value=0)
            # Limiter aux top 15 pays présents dans la heatmap
            top_countries = medal_counts.nlargest(15).index
            # Intersection avec les colonnes disponibles
            top_countries = [c for c in top_countries if c in heat.columns]
            if top_countries:
                fig4 = px.imshow(heat[top_countries], title="Médailles par année/pays", aspect="auto")
                st.plotly_chart(fig4, use_container_width=True)
            else:
                st.info("Pas de données suffisantes pour la heatmap.")

    # --- TAB 3: DISCIPLINES ---
    with tabs[2]:
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Top disciplines (participations)")
            if 'discipline' in filtered_main.columns:
                disc_counts = filtered_main['discipline'].value_counts().reset_index()
                disc_counts.columns = ['discipline','Count']
                top15 = disc_counts.head(15)
                fig = px.bar(top15, x='Count', y='discipline', orientation='h', title="Top 15 disciplines (participations)")
                st.plotly_chart(fig, use_container_width=True)

        with col_b:
            st.subheader("Répartition des disciplines")
            if 'discipline' in filtered_main.columns:
                fig2 = px.pie(disc_counts.head(10), values='Count', names='discipline', title="Top 10 disciplines")
                st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")
        col_c, col_d = st.columns(2)
        with col_c:
            st.subheader("Équité par discipline")
            if all(col in filtered_main.columns for col in ['discipline','gender']):
                eq = filtered_main.groupby(['discipline','gender']).size().reset_index(name='Count')
                fig3 = px.bar(eq, x='discipline', y='Count', color='gender', barmode='group', title="Participants par genre/discipline")
                st.plotly_chart(fig3, use_container_width=True)

        with col_d:
            st.subheader("Disciplines en croissance")
            if all(col in filtered_main.columns for col in ['discipline','year']):
                # Nombre d'événements par discipline par année (approximation)
                growth = filtered_main.groupby(['discipline','year']).size().reset_index(name='Events')
                # Pourcentage de croissance moyen
                growth_pct = growth.pivot(index='discipline', columns='year', values='Events').fillna(0)
                growth_pct['Growth'] = growth_pct.pct_change(axis=1).mean(axis=1) * 100
                growth_df = growth_pct[['Growth']].reset_index().sort_values('Growth', ascending=False).head(20)
                fig4 = px.bar(growth_df, x='Growth', y='discipline', orientation='h', title="Disciplines en croissance")
                st.plotly_chart(fig4, use_container_width=True)

    # --- TAB 4: GENRE ---
    with tabs[3]:
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Répartition globale par genre")
            if 'gender' in filtered_main.columns:
                counts = filtered_main['gender'].value_counts().reset_index()
                counts.columns = ['gender','Count']
                fig = px.pie(counts, values='Count', names='gender', title="Participants par genre")
                st.plotly_chart(fig, use_container_width=True)

        with col_b:
            st.subheader("Médailles par genre")
            if all(col in filtered_main.columns for col in ['gender','medal']):
                gm = filtered_main[filtered_main['medal'].isin(['Gold','Silver','Bronze'])].groupby(['gender','medal']).size().reset_index(name='Count')
                fig2 = px.bar(gm, x='gender', y='Count', color='medal', barmode='group', title="Médailles par genre")
                st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")
        st.subheader("Évolution de la participation féminine")
        if all(col in filtered_main.columns for col in ['year','gender']):
            female = filtered_main[filtered_main['gender']=='F'].groupby('year').size().reset_index(name='Female')
            total = filtered_main.groupby('year').size().reset_index(name='Total')
            evol = pd.merge(female, total, on='year')
            evol['Pct'] = evol['Female'] / evol['Total'] * 100
            fig3 = px.line(evol, x='year', y='Pct', markers=True, title="Pourcentage de femmes participants par année")
            st.plotly_chart(fig3, use_container_width=True)

    # --- TAB 5: ATHLÈTES ---
    with tabs[4]:
        st.subheader("Top 20 athlètes (médailles)")
        # Chercher colonne d'athlète
        athlete_col = next((c for c in ['as','Name','Athlete','athlete_name'] if c in filtered_main.columns), None)
        if athlete_col and 'medal' in filtered_main.columns:
            top_ath = filtered_main[filtered_main['medal'].isin(['Gold','Silver','Bronze'])].groupby(athlete_col).size().reset_index(name='Medals')
            top_ath = top_ath.sort_values('Medals', ascending=False).head(20)
            fig = px.bar(top_ath, x='Medals', y=athlete_col, orientation='h', color='Medals', title="Top athlètes")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Longévité des médaillés")
            if all(col in filtered_main.columns for col in [athlete_col,'year','medal']):
                # Nombre d'années de participation par athlète
                longevity = filtered_main[filtered_main['medal'].isin(['Gold','Silver','Bronze'])].groupby(athlete_col)['year'].nunique().reset_index(name='Years')
                fig2 = px.histogram(longevity, x='Years', nbins=20, title="Distribution de la longévité des médaillés")
                st.plotly_chart(fig2, use_container_width=True)

        with col_b:
            st.subheader("Âge des médaillés")
            # Chercher colonne d'âge ('as'? pas sûr)
            age_col = next((c for c in ['age','Age','as'] if c in filtered_main.columns), None)
            if age_col and 'medal' in filtered_main.columns:
                ages = filtered_main[filtered_main['medal'].isin(['Gold','Silver','Bronze'])][[age_col]].dropna()
                fig3 = px.histogram(ages, x=age_col, nbins=30, title="Distribution de l'âge des médaillés")
                st.plotly_chart(fig3, use_container_width=True)

        st.markdown("---")
        st.subheader("Athlètes en progression (médailles par année)")
        if all(col in filtered_main.columns for col in [athlete_col,'year','medal']):
            # Médailles par athlète par année
            prog = filtered_main[filtered_main['medal'].isin(['Gold','Silver','Bronze'])].groupby([athlete_col,'year']).size().reset_index(name='Count')
            # Calculer la moyenne cumulative par athlète (simple proxy de progression)
            prog['CumAvg'] = prog.groupby(athlete_col)['Count'].cumsum() / (prog.groupby(athlete_col).cumcount()+1)
            # Prendre les 100 athlètes les plus médaillés
            top100 = top_ath.head(100)[athlete_col].tolist()
            prog_top = prog[prog[athlete_col].isin(top100)]
            fig4 = px.line(prog_top, x='year', y='CumAvg', color=athlete_col, title="Moyenne cumulative de médailles (top 100)")
            st.plotly_chart(fig4, use_container_width=True)

    # --- TAB 6: NATATION ---
    with tabs[5]:
        st.subheader("Analyse de la natation")
        if not df_swim.empty:
            st.write(f"Données de natation : {len(df_swim)} lignes")
            col_a, col_b = st.columns(2)
            with col_a:
                if 'Stroke' in df_swim.columns:
                    stroke_counts = df_swim['Stroke'].value_counts().reset_index()
                    stroke_counts.columns = ['Stroke','Count']
                    fig = px.pie(stroke_counts, values='Count', names='Stroke', title="Répartition des nages")
                    st.plotly_chart(fig, use_container_width=True)
            with col_b:
                if 'Distance' in df_swim.columns:
                    dist_counts = df_swim['Distance'].value_counts().reset_index()
                    dist_counts.columns = ['Distance','Count']
                    fig2 = px.bar(dist_counts, x='Distance', y='Count', title="Distances")
                    st.plotly_chart(fig2, use_container_width=True)

            st.markdown("---")
            st.subheader("Évolution des temps (Records)")
            if all(col in df_swim.columns for col in ['Year','Stroke','Distance','Results']):
                # Meilleurs temps par année, stroke, distance
                best = df_swim.groupby(['Year','Stroke','Distance'])['Results'].min().reset_index()
                # Filtre par stroke et distance si sélectionné
                sel_stroke = st.selectbox("Sélectionner une nage", options=best['Stroke'].unique())
                sel_dist = st.selectbox("Sélectionner une distance", options=best[best['Stroke']==sel_stroke]['Distance'].unique())
                chart_data = best[(best['Stroke']==sel_stroke) & (best['Distance']==sel_dist)]
                fig3 = px.line(chart_data, x='Year', y='Results', markers=True, title=f"Évolution du meilleur temps : {sel_stroke} {sel_dist}m")
                st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("Données de natation non disponibles.")

    # --- TAB 7: ATHLÉTISME ---
    with tabs[6]:
        st.subheader("Analyse athlétisme")
        if not df_ath.empty:
            st.write(f"Données athlétisme : {len(df_ath)} lignes")
            # À compléter selon colonnes disponibles
            st.dataframe(df_ath.head(100), use_container_width=True)
        else:
            st.info("Données athlétisme non disponibles.")

    # --- TAB 8: PRÉDICTIONS ---
    with tabs[7]:
        st.subheader("Prédictions pour 2028")
        if 'medal' in filtered_main.columns and 'noc' in filtered_main.columns and 'year' in filtered_main.columns:
            from components.predictor import predict_2028
            preds = predict_2028(filtered_main)
            if not preds.empty:
                fig = px.bar(preds.head(15), x='Score', y='Country', orientation='h', title="Top 15 pays prédits pour 2028")
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(preds, use_container_width=True)
            else:
                st.info("Pas assez de données pour générer des prédictions.")
        else:
            st.info("Données insuffisantes.")

    # ========== TÉLÉCHARGEMENT ==========
    st.markdown("---")
    csv = filtered_main.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Télécharger les données filtrées", csv, "filtered_olympic.csv", "text/csv")
