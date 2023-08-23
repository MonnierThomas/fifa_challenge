import streamlit as st
import pandas as pd

from datetime import datetime

st.set_page_config(layout="wide")

if 'df' not in st.session_state:
    with open("database.csv", "r") as file:
        st.session_state.df = pd.read_csv(file)

st.markdown(
        "<h1 style='text-align: center; color: blue;'>Fifa Match</h1>",
        unsafe_allow_html=True,
    )

players = ["Marc", "Monnier", "Stephen"]

with st.form(key="add_match"):
    col1, col2, col3 = st.columns(3)

    scorers = {i: -1 for i in players}

    with col1:
        # Domestic players
        domestic_players = st.multiselect("Domestic players:", players, key="domestic_players")

        # Soccer teams chosen (Optional)
        domestic_team = st.text_input("Team chosen (Optional):", key="domestic_team")

        # Total Goals
        domestic_goals = st.number_input("Goals:", key="domestic_goals", step=1)

    with col2:
        # Exterior players
        exterior_players = st.multiselect("Exterior players:", players, key="exterior_players")

        # Soccer teams chosen (Optional)
        exterior_team = st.text_input("Team chosen (Optional):", key="exterior_team")

        # Goals
        exterior_goals = st.number_input("Goals:", key="exterior_goals", step=1)
    
    with col3:
        # Scorers (Optional)
        for player in players:
            scorers[player] = st.number_input(f"Goals {player} (Optional):", step=1)

    # Every form must have a submit button
    submitted = st.form_submit_button("Submit")


if submitted:
    victory = "domestic" if st.session_state.domestic_goals > st.session_state.exterior_goals else "exterior" if st.session_state.exterior_goals > st.session_state.domestic_goals else "draw"
    
    df = pd.DataFrame({
        "Domestic players": ", ".join(domestic_players),
        "Exterior players": ", ".join(exterior_players),
        "Victory": victory,
        "Goals diff": abs(exterior_goals - domestic_goals),
        "Domestic goals": st.session_state.domestic_goals,
        "Exterior goals": st.session_state.exterior_goals,
        "Scorers": str(scorers),
        "Domestic team": st.session_state.domestic_team,
        "Exterior team": st.session_state.exterior_team,
        "Time": datetime.utcnow()
    }, index=["Time"])

    st.balloons()

    final_df = pd.concat([st.session_state.df, df], ignore_index=True)
    final_df.drop_duplicates().to_csv("database.csv", index=False)

    del st.session_state["df"]
