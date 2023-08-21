import streamlit as st
import pandas as pd
import ast

# Create a new markdown section and add a title for the stats page.
st.set_page_config(layout="wide")

st.markdown(
        "<h1 style='text-align: center; color: blue;'>Statistics</h1>",
        unsafe_allow_html=True,
    )

players = ["Marc", "Monnier", "Stephen"]
ranking = {i: {
    "MJ": 0,
    "G": 0,
    "N": 0,
    "P": 0,
    "BP": 0,
    "BC": 0, 
    "DB": 0,
    "Pts": 0,
}  for i in players}

players_pts = {i: 0 for i in players}
players_goals = {i: 0 for i in players}
teams = {i: 0 for i in list(set(list(st.session_state.df["Domestic team"].drop_duplicates()) + list(st.session_state.df["Exterior team"].drop_duplicates())))}

for _, row in st.session_state.df.iterrows():
    domestic_players = row["Domestic players"].split(', ')
    exterior_players = row["Exterior players"].split(', ')
    victory = row["Victory"]

    if victory == "domestic":
        for d_player in domestic_players:
            players_pts[d_player] += 3
            ranking[d_player]["Pts"] += 3
            ranking[d_player]["G"] += 1
            
        for e_player in exterior_players:
            ranking[e_player]["P"] += 1
            
    elif victory == "exterior":
        for e_player in exterior_players:
            players_pts[e_player] += 3
            ranking[e_player]["Pts"] += 3
            ranking[e_player]["G"] += 1

        for d_player in domestic_players:
            ranking[d_player]["P"] += 1
    else:
        for player in domestic_players + exterior_players:
            players_pts[player] += 1
            ranking[player]["Pts"] += 1
            ranking[player]["N"] += 1
    
    for d_player in domestic_players:
        ranking[d_player]["BP"] += row["Domestic goals"]
        ranking[d_player]["BC"] += row["Exterior goals"]
        ranking[d_player]["DB"] += row["Domestic goals"] - row["Exterior goals"]

    for e_player in exterior_players:
        ranking[e_player]["BP"] += row["Exterior goals"]
        ranking[e_player]["BC"] += row["Domestic goals"]
        ranking[e_player]["DB"] += row["Exterior goals"] - row["Domestic goals"]

    for player in domestic_players + exterior_players:
        ranking[player]["MJ"] += 1
    
    scorers_dct = ast.literal_eval(row["Scorers"])
    for k, v in scorers_dct.items():
        players_goals[k] += v
    
    d_team, e_team = row["Domestic team"], row["Exterior team"]
    if victory == "domestic":
        teams[d_team]  += 3
    elif victory == "exterior":
        teams[e_team] += 3
    else:
        teams[d_team] += 1
        teams[e_team] += 1

st.markdown(
    "<h3 style='text-align: center; color: red;'>Ranking</h3>",
    unsafe_allow_html=True,
)

def highlight_cols(s):
    color = '#90EE90'
    return 'background-color: %s' % color

table = pd.DataFrame.from_dict(ranking, orient='index').sort_values(by=['Pts'], ascending=False).astype(int).style.applymap(highlight_cols, subset=pd.IndexSlice[:, ['Pts']])
st.table(table)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
            "<h3 style='text-align: center; color: red;'>Top Players</h3>",
            unsafe_allow_html=True,
        )

    st.table(dict(sorted(players_pts.items(), key=lambda item: item[1], reverse=True)))

with col2:
    st.markdown(
            "<h3 style='text-align: center; color: red;'>Top Scorers</h3>",
            unsafe_allow_html=True,
        )

    st.table(dict(sorted(players_goals.items(), key=lambda item: item[1], reverse=True)))

with col3:
    st.markdown(
            "<h3 style='text-align: center; color: red;'>Top Teams</h3>",
            unsafe_allow_html=True,
        )

    st.table(dict(sorted(teams.items(), key=lambda item: item[1], reverse=True)))
