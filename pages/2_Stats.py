import streamlit as st
import pandas as pd
import json
import ast

# Create a new markdown section and add a title for the stats page.
st.set_page_config(layout="wide")

st.markdown(
        "<h1 style='text-align: center; color: blue;'>Statistics</h1>",
        unsafe_allow_html=True,
    )

col1, col2, col3 = st.columns(3)
players = ["Marc", "Monnier", "Stephen"]

with col1:
    st.markdown(
            "<h3 style='text-align: center; color: red;'>Top Players</h3>",
            unsafe_allow_html=True,
        )

    players_pts = {i: 0 for i in players}
    for _, row in st.session_state.df.iterrows():
        domestic_players = row["Domestic players"].split(', ')
        exterior_players = row["Exterior players"].split(', ')
        victory = row["Victory"]
        if victory == "domestic":
            for d_player in domestic_players:
                players_pts[d_player] += 3
        elif victory == "exterior":
            for e_player in exterior_players:
                players_pts[e_player] += 3
        else:
            for player in domestic_players + exterior_players:
                players_pts[player] += 1

    st.table(dict(sorted(players_pts.items(), key=lambda item: item[1], reverse=True)))

with col2:
    st.markdown(
            "<h3 style='text-align: center; color: red;'>Top Scorers</h3>",
            unsafe_allow_html=True,
        )

    players_goals = {i: 0 for i in players}
    for _, row in st.session_state.df.iterrows():
        scorers_dct = ast.literal_eval(row["Scorers"])
        for k, v in scorers_dct.items():
            players_goals[k] += v

    st.table(dict(sorted(players_goals.items(), key=lambda item: item[1], reverse=True)))

with col3:
    st.markdown(
            "<h3 style='text-align: center; color: red;'>Top Teams</h3>",
            unsafe_allow_html=True,
        )

    teams = {i: 0 for i in list(set(list(st.session_state.df["Domestic team"].drop_duplicates()) + list(st.session_state.df["Exterior team"].drop_duplicates())))}
    for _, row in st.session_state.df.iterrows():
        victory = row["Victory"]
        d_team, e_team = row["Domestic team"], row["Exterior team"]
        if victory == "domestic":
            teams[d_team]  += 3
        elif victory == "exterior":
            teams[e_team] += 3
        else:
            teams[d_team] += 1
            teams[e_team] += 1

    st.table(dict(sorted(teams.items(), key=lambda item: item[1], reverse=True)))
