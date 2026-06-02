import pandas as pd
import os
from functools import lru_cache

# Obtenir le chemin absolu du répertoire racine du projet
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@lru_cache
def load_all_participations():
    """Charge les données de toutes les participations."""
    return pd.read_csv(os.path.join(PROJECT_ROOT, 'cleaned_data', 'all_participations.csv'))

@lru_cache
def load_athletism():
    """Charge les données d'athlétisme."""
    return pd.read_csv(os.path.join(PROJECT_ROOT, 'cleaned_data', 'athletism_completed.csv'))

@lru_cache
def load_swimming():
    """Charge les données de natation."""
    return pd.read_csv(os.path.join(PROJECT_ROOT, 'cleaned_data', 'swimming.csv'))

def get_available_columns():
    """Retourne les colonnes disponibles dans le DataFrame principal."""
    df = load_all_participations()
    return df.columns.tolist()

def get_combined_data():
    """Retourne un DataFrame combiné de toutes les disciplines."""
    all_df = load_all_participations()
    ath_df = load_athletism()
    swim_df = load_swimming()
    # Concatène tous les DataFrames (assumer columns similaires)
    combined = pd.concat([all_df, ath_df, swim_df], ignore_index=True)
    return combined

def get_disciplines():
    """Retourne la liste des disciplines disponibles."""
    all_df = load_all_participations()
    disciplines = all_df['discipline'].dropna().unique() if 'discipline' in all_df.columns else []
    # Convertir en str et trier
    disciplines = [str(d) for d in disciplines if pd.notna(d)]
    return sorted(disciplines)

def get_countries():
    """Retourne la liste des pays (noc)."""
    all_df = load_all_participations()
    countries = all_df['noc'].dropna().unique() if 'noc' in all_df.columns else []
    countries = [str(c) for c in countries if pd.notna(c)]
    return sorted(countries)

def get_years():
    """Retourne la liste des années de JO."""
    all_df = load_all_participations()
    years = all_df['year'].dropna().unique() if 'year' in all_df.columns else []
    # Les années sont numériques, trier directement
    return sorted(years)

def get_medals():
    """Retourne les types de médailles."""
    return ['Gold', 'Silver', 'Bronze']
