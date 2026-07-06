import streamlit as st
from components.style import inject_style, section_header, styled_divider, leaderboard_row, info_box
from components.swimming_predictor import (
    load_swimming_model, predict_swimming_time,
    get_swimming_data, predict_top_ten,
)

st.set_page_config(layout="wide")
inject_style()
st.title("\U0001f52e Prédictions JO 2028")

info_box(
    "Modèle CatBoost entraîné sur les données historiques de natation olympique (1912-2020). "
    "Prédit les temps de finale pour Los Angeles 2028."
)

model = load_swimming_model()

if model is None:
    st.error("Modèle CatBoost non disponible.")
    st.markdown(
        """
        **Pour activer les prédictions :**
        1. `pip install catboost`
        2. Exécutez `notebooks/swimming_prediction.ipynb`
        3. Le modèle est sauvegardé dans `model/swimming_model.cbm`
        4. Redémarrez l'application.
        """
    )
    st.stop()

st.success("Modèle CatBoost chargé")
swim_df = get_swimming_data()

# Build valid Distance/Stroke combinations
valid_combos = swim_df[["Distance", "Stroke"]].drop_duplicates()

tab1, tab2 = st.tabs(["\U0001f3c6 Top 10 par épreuve", "\u2709\ufe0f Prédiction manuelle"])

# === TAB 1: TOP 10 ===
with tab1:
    section_header("Classement prédit pour 2028")

    if swim_df.empty or "Stroke" not in swim_df.columns:
        st.info("Données de natation insuffisantes.")
    else:
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1:
            distance_options = sorted(swim_df["Distance"].dropna().unique().tolist())
            distance = st.selectbox(
                "Distance (m)", options=distance_options,
                index=distance_options.index(100) if 100 in distance_options else 0,
                key="t10_dist",
            )
        with c2:
            # Filter strokes to only those valid for the selected distance
            valid_strokes = sorted(
                valid_combos[valid_combos["Distance"] == distance]["Stroke"].tolist()
            )
            stroke = st.selectbox(
                "Style", options=valid_strokes if valid_strokes else ["Aucun"],
                key="t10_stroke",
            )
        with c3:
            st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
            combo_exists = not valid_combos[
                (valid_combos["Distance"] == distance) & (valid_combos["Stroke"] == stroke)
            ].empty
            predict_btn = st.button("Prédire le Top 10", key="top10_btn", width="stretch",
                                    disabled=not combo_exists)

        if not combo_exists:
            st.warning(f"La combinaison {distance}m {stroke} n'existe pas dans les données.")
        elif predict_btn:
            result = predict_top_ten(model, swim_df, distance, stroke)
            if result.empty:
                st.warning(f"Aucune donnée pour {distance}m {stroke}.")
            else:
                section_header(f"Résultat — {distance}m {stroke}")
                for i, (_, row) in enumerate(result.iterrows(), 1):
                    leaderboard_row(i, row["Athlete"], row["Team"], row["Predicted_Time"])

# === TAB 2: MANUEL ===
with tab2:
    section_header("Prédiction individuelle")

    if swim_df.empty or "Stroke" not in swim_df.columns or "Gender" not in swim_df.columns:
        st.info("Données insuffisantes pour le formulaire.")
    else:
        with st.form("prediction_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                distance = st.selectbox("Distance", [50, 100, 200, 400, 800, 1500], index=1, key="m_dist")
                valid_strokes = sorted(
                    valid_combos[valid_combos["Distance"] == distance]["Stroke"].tolist()
                )
                stroke = st.selectbox("Stroke", valid_strokes if valid_strokes else ["Aucun"], key="m_stroke")
                gender_opts = sorted(swim_df["Gender"].dropna().unique().tolist())
                gender = st.selectbox("Gender", gender_opts, key="m_gender")
            with c2:
                relay = st.selectbox("Relay?", [False, True], format_func=lambda x: "Oui" if x else "Non", key="m_relay")
                team = st.text_input("Team (code pays)", value="FRA", key="m_team")
                year = st.number_input("Year", min_value=1900, max_value=2030, value=2024, key="m_year")
            with c3:
                experience = st.slider("Experience", 0, 20, 5, key="m_exp")
                previous_best = st.number_input("Previous Best (s)", min_value=0.0, value=50.0, step=0.1, key="m_pb")
                previous_average = st.number_input("Previous Average (s)", min_value=0.0, value=50.5, step=0.1, key="m_pa")

            submitted = st.form_submit_button("Prédire", width="stretch")

            if submitted:
                features = {
                    "Distance": distance, "Stroke": stroke, "Gender": gender,
                    "Relay?": relay, "Year": year, "Team": team,
                    "Experience": experience, "Previous_Best": previous_best,
                    "Previous_Average": previous_average,
                }
                pred = predict_swimming_time(model, features)
                if pred is not None:
                    st.markdown(
                        f"""<div class="prediction-card" style="text-align:center; margin-top:1rem;">
                            <div style="font-size:0.9rem; color:#94a3b8;">Temps prédit</div>
                            <div style="font-size:2.5rem; font-weight:700; color:#FFD700;">{pred:.3f}s</div>
                            <div style="font-size:0.85rem; color:#94a3b8;">{distance}m {stroke} — {team}</div>
                        </div>""",
                        unsafe_allow_html=True,
                    )
                else:
                    st.error("Erreur lors de la prédiction.")
