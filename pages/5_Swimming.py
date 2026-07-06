import streamlit as st
from components.swimming_predictor import load_swimming_model, predict_swimming_time, get_swimming_features, get_swimming_data

st.set_page_config(layout="wide")
st.title("🏊 Prédictions Natation JO 2028")

st.markdown(
    """
    Cette page utilise un modèle CatBoost pour prédire les temps de natation
    en fonction des caractéristiques de la course et du nageur.
    """
)

# Charger le modèle
model = load_swimming_model()

if model is None:
    st.error("Modèle CatBoost non disponible.")
    st.markdown(
        """
        ### Pour activer les prédictions :

        1. Assurez-vous que `catboost` est installé :
           ```bash
           pip install catboost
           ```
        2. Entraînez le modèle en exécutant le notebook :
           ```
           model/swimming_prediction.ipynb
           ```
        3. Sauvegardez le modèle en ajoutant dans le notebook :
           ```python
           model.save_model('model/swimming_model.cbm')
           ```
        4. Redémarrez l'application.
        """
    )
else:
    st.success("Modèle CatBoost chargé ✅")

    # Charger les données pour obtenir les valeurs uniques des features catégorielles
    swim_df = get_swimming_data()

    # Onglets
    tab1, tab2 = st.tabs(["Prédiction manuelle", "Prédiction sur données existantes"])

    with tab1:
        st.subheader("Prédiction d'un temps")
        st.markdown("Remplissez les caractéristiques de la course :")

        # Vérifier que les données sont disponibles
        if swim_df.empty or 'Stroke' not in swim_df.columns or 'Gender' not in swim_df.columns:
            st.info("Données de natation insuffisantes pour le formulaire.")
        else:
            with st.form("prediction_form"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    distance = st.selectbox("Distance", options=[50, 100, 200, 400, 800, 1500], index=1)
                    stroke_options = sorted(swim_df['Stroke'].dropna().unique().tolist())
                    stroke = st.selectbox("Stroke", options=stroke_options if stroke_options else ['Freestyle'])
                    gender_options = sorted(swim_df['Gender'].dropna().unique().tolist())
                    gender = st.selectbox("Gender", options=gender_options if gender_options else ['M'])
                with col2:
                    relay = st.selectbox("Relay?", options=[False, True], format_func=lambda x: "Oui" if x else "Non")
                    team = st.text_input("Team (code pays)", value="FRA")
                    year = st.number_input("Year", min_value=1900, max_value=2030, value=2024)
                with col3:
                    experience = st.slider("Experience (années)", min_value=0, max_value=20, value=5)
                    previous_best = st.number_input("Previous Best (seconds)", min_value=0.0, value=50.0, step=0.1)
                    previous_average = st.number_input("Previous Average (seconds)", min_value=0.0, value=50.5, step=0.1)

                submitted = st.form_submit_button("Prédire le temps")

                if submitted:
                    features_dict = {
                        "Distance": distance,
                        "Stroke": stroke,
                        "Gender": gender,
                        "Relay?": relay,
                        "Year": year,
                        "Team": team,
                        "Experience": experience,
                        "Previous_Best": previous_best,
                        "Previous_Average": previous_average
                    }
                    pred = predict_swimming_time(model, features_dict)
                    if pred is not None:
                        st.success(f"Temps prédit : **{pred:.3f} secondes**")
                    else:
                        st.error("Erreur lors de la prédiction.")

    with tab2:
        st.subheader("Prédiction sur un nageur existant")
        st.markdown("Sélectionnez un nageur dans la base de données pour voir sa performance réelle et la prédiction.")

        # Sélection par index ou par nom? On n'a pas forcément de nom. On peut afficher un tableau avec les données et permettre de choisir une ligne.
        # Pour simplifier, on montre un échantillon des données
        sample = swim_df.head(100)
        st.write("Échantillon de 100 premières lignes :")
        st.dataframe(sample, use_container_width=True, height=400)

        st.info("Fonctionnalité à venir : sélection d'un athlète et comparaison.")
