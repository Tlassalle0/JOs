import pandas as pd
import os
import streamlit as st

# Chemin du modèle sauvegardé
MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'model',
    'swimming_model.cbm'
)

def load_swimming_model():
    """Charge le modèle CatBoost entraîné. Retourne le modèle ou None si non trouvé."""
    try:
        from catboost import CatBoostRegressor
        if os.path.exists(MODEL_PATH):
            model = CatBoostRegressor()
            model.load_model(MODEL_PATH)
            return model
        else:
            return None
    except ImportError:
        return None

def get_swimming_features():
    """Retourne la liste des features attendues par le modèle."""
    return [
        "Distance",
        "Stroke",
        "Gender",
        "Relay?",
        "Year",
        "Team",
        "Experience",
        "Previous_Best",
        "Previous_Average"
    ]

def predict_swimming_time(model, features_dict):
    """
    Prédit le temps de natation à partir d'un dictionnaire de features.
    Retourne le temps prédit (en secondes? le modèle prédit probablement la même unité que la cible 'Results').
    """
    try:
        import catboost
    except ImportError:
        return None
    if model is None:
        return None
    # Créer un DataFrame à partir du dict
    X = pd.DataFrame([features_dict])
    # S'assurer que l'ordre des colonnes correspond
    features = get_swimming_features()
    X = X[features]
    prediction = model.predict(X)
    return prediction[0]

def get_swimming_data():
    """Charge les données de natation nettoyées."""
    from .data_loader import load_swimming
    return load_swimming()
