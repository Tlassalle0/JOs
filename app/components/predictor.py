import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from functools import lru_cache

@lru_cache
def get_country_medal_trends(df):
    """
    Calcule la tendance (pente) de l'évolution des médailles par pays.
    Retourne un DataFrame avec Country, Trend (médailes/an), RecentAvg.
    """
    # Vérifier les colonnes nécessaires
    if 'medal' not in df.columns or 'noc' not in df.columns or 'year' not in df.columns:
        return pd.DataFrame()

    medal_counts = df.groupby(['noc', 'year']).size().reset_index(name='MedalCount')
    trends = []
    for country, group in medal_counts.groupby('noc'):
        if len(group) < 2:
            continue
        X = group['year'].values.reshape(-1, 1)
        y = group['MedalCount'].values
        model = LinearRegression()
        model.fit(X, y)
        trend = model.coef_[0]  # augmentation par an
        recent_avg = group['MedalCount'].iloc[-2:].mean() if len(group) >= 2 else group['MedalCount'].mean()
        trends.append({
            'Country': country,  # on garde 'Country' pour la compatibilité
            'Trend': trend,
            'RecentAvg': recent_avg,
            'TotalMedals': group['MedalCount'].sum()
        })
    trends_df = pd.DataFrame(trends)
    return trends_df

def predict_2028(df, trends_df=None):
    """
    Prédit les performances pour 2028 basées sur la tendance linéaire.
    Retourne un DataFrame trié par prédiction décroissante.
    """
    if trends_df is None:
        trends_df = get_country_medal_trends(df)
    if trends_df.empty:
        return pd.DataFrame()
    # Prédiction pour 2028
    last_year = df['year'].max() if 'year' in df.columns else 2024
    years_ahead = 2028 - last_year
    trends_df['Predicted2028'] = trends_df['RecentAvg'] + trends_df['Trend'] * years_ahead
    # On ne garde que les prédictions positives
    trends_df['Predicted2028'] = trends_df['Predicted2028'].clip(lower=0)
    # Score composite : tendance + récent
    trends_df['Score'] = trends_df['Predicted2028'] * (1 + trends_df['Trend'].abs())
    result = trends_df.sort_values('Score', ascending=False)
    return result

def get_top_athletes_prediction(df, top_n=10):
    """
    Identifie les athlètes avec le plus de médailles récentes (derniers Jeux)
    comme favoris pour 2028.
    """
    # Chercher une colonne de nom d'athlète: 'Name', 'Athlete', 'as', 'athlete' etc.
    athlete_col = None
    for col in ['Name', 'Athlete', 'athlete_name', 'as', 'athlete']:
        if col in df.columns:
            athlete_col = col
            break
    if athlete_col is None or 'medal' not in df.columns or 'year' not in df.columns:
        return pd.DataFrame()
    # Considérer seulement les dernières éditions (2 plus récentes)
    recent_years = sorted(df['year'].unique())[-2:]
    recent_df = df[df['year'].isin(recent_years)]
    athlete_medals = recent_df.groupby([athlete_col, 'noc']).size().reset_index(name='MedalCount')
    top_athletes = athlete_medals.sort_values('MedalCount', ascending=False).head(top_n)
    # Renommer la colonne de l'athlète en 'Name' et 'noc' en 'Country' pour la compatibilité
    top_athletes = top_athletes.rename(columns={athlete_col: 'Name', 'noc': 'Country'})
    return top_athletes
