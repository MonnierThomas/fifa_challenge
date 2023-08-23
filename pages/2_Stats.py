import streamlit as st
import pandas as pd
import ast

# Create a new markdown section and add a title for the stats page.
st.set_page_config(layout="wide")

if 'df' not in st.session_state:
    with open("database.csv", "r") as file:
        st.session_state.df = pd.read_csv(file)

st.markdown(
        "<h1 style='text-align: center; color: blue;'>Statistics</h1>",
        unsafe_allow_html=True,
    )

def highlight_cols(s):
    color = '#90EE90'
    return 'background-color: %s' % color

players = ["Marc", "Monnier", "Stephen"]
ranking = {i: {
    "MJ": 0,
    "MJS": 0,
    "G": 0,
    "GS": 0,
    "N": 0,
    "NS": 0,
    "P": 0,
    "BP": 0,
    "BC": 0, 
    "DB": 0,
    "Pts": 0,
}  for i in players}

players_goals = {i: {"Goals": 0} for i in players}
teams = {i: {"MJ": 0, "MJS": 0, "BP": 0, "Pts": 0} for i in list(set(list(st.session_state.df["Domestic team"].drop_duplicates()) + list(st.session_state.df["Exterior team"].drop_duplicates())))}

for _, row in st.session_state.df.iterrows():
    domestic_players = row["Domestic players"].split(', ')
    exterior_players = row["Exterior players"].split(', ')
    victory = row["Victory"]

    if victory == "domestic":
        for d_player in domestic_players:
            ranking[d_player]["Pts"] += 3
            ranking[d_player]["G"] += 1
            
        for e_player in exterior_players:
            ranking[e_player]["P"] += 1
            
    elif victory == "exterior":
        for e_player in exterior_players:
            ranking[e_player]["Pts"] += 3
            ranking[e_player]["G"] += 1

        for d_player in domestic_players:
            ranking[d_player]["P"] += 1
    else:
        for player in domestic_players + exterior_players:
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
        players_goals[k]["Goals"] += v
    
    d_team, e_team = row["Domestic team"], row["Exterior team"]
    if victory == "domestic":
        teams[d_team]["Pts"] += 3
    elif victory == "exterior":
        teams[e_team]["Pts"] += 3
    else:
        teams[d_team]["Pts"] += 1
        teams[e_team]["Pts"] += 1

    teams[d_team]["MJ"] += 1
    teams[e_team]["MJ"] += 1
    teams[d_team]["BP"]  += row["Domestic goals"]
    teams[e_team]["BP"]  += row["Exterior goals"]
    
    if len(domestic_players) == 1:
        ranking[domestic_players[0]]["MJS"] += 1
        teams[d_team]["MJS"]  += 1
        if victory == "domestic":
            ranking[domestic_players[0]]["GS"] += 1
        elif victory == "draw":
            ranking[domestic_players[0]]["NS"] += 1
    
    if len(exterior_players) == 1:
        ranking[exterior_players[0]]["MJS"] += 1
        teams[e_team]["MJS"]  += 1
        if victory == "exterior":
            ranking[exterior_players[0]]["GS"] += 1
        elif victory == "draw":
            ranking[exterior_players[0]]["NS"] += 1

st.markdown(
    "<h3 style='text-align: center; color: red;'>Ranking</h3>",
    unsafe_allow_html=True,
)

df_ranking = pd.DataFrame.from_dict(ranking, orient='index').sort_values(by=['Pts'], ascending=False).drop(["GS", "NS"], axis=1, inplace=False).astype(int)
st.table(df_ranking.style.applymap(highlight_cols, subset=pd.IndexSlice[:, ['Pts']]))

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
            "<h3 style='text-align: center; color: red;'>Top Players</h3>",
            unsafe_allow_html=True,
        )

    st.table(df_ranking["Pts"])
    
    st.markdown(
            "<h3 style='text-align: center; color: red;'>Top Scorers</h3>",
            unsafe_allow_html=True,
        )

    df_scorers = pd.DataFrame.from_dict(players_goals, orient="index").sort_values(by="Goals", ascending=False).astype(int)
    st.table(df_scorers)

with col2:
    st.markdown(
            "<h3 style='text-align: center; color: red;'>Pts per Solo Match</h3>",
            unsafe_allow_html=True,
        )

    ratio_victory_solo = {i: {"RVS": 0} for i in players}
    for player, dct in ranking.items():
        ratio_victory_solo[player]["RVS"] = round((3 * dct["GS"] + 1 * dct["NS"]) / dct["MJS"] , 2)
    df_ratio_victory_solo = pd.DataFrame.from_dict(ratio_victory_solo, orient="index").sort_values(by="RVS", ascending=False).astype(float).round(4)
    st.table(df_ratio_victory_solo)

    st.markdown(
            "<h3 style='text-align: center; color: red;'>Pts per Multi Match</h3>",
            unsafe_allow_html=True,
        )

    ratio_victory_multi = {i: {"RVM": 0} for i in players}
    for player, dct in ranking.items():
        ratio_victory_multi[player]["RVM"] = round((3 * (dct["G"] - dct["GS"]) + 1 * (dct["N"] - dct["NS"])) / (dct["MJ"] - dct["MJS"]) , 2)
    df_ratio_victory_multi = pd.DataFrame.from_dict(ratio_victory_multi, orient="index").sort_values(by="RVM", ascending=False).astype(float).round(4)
    st.table(df_ratio_victory_multi)

with col3:
    st.markdown(
            "<h3 style='text-align: center; color: red;'>Top Teams</h3>",
            unsafe_allow_html=True,
        )

    df_teams = pd.DataFrame.from_dict(teams, orient="index").sort_values(by="Pts", ascending=False).astype(int).style.applymap(highlight_cols, subset=pd.IndexSlice[:, ['Pts']])
    st.table(df_teams)
