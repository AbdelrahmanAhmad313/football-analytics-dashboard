import sqlite3
import pandas as pd


conn = sqlite3.connect("data/database.sqlite")


def load_teams():

    query="""
SELECT 
team_api_id,
team_long_name
FROM Team
"""
    teams_df=pd.read_sql_query(query,conn)

    return teams_df


def load_matches():
    match_query="""
SELECT 
    home_team_api_id,
    away_team_api_id,
    home_team_goal,
    away_team_goal
FROM Match
"""
    match_df =pd.read_sql_query(match_query,conn)

    return match_df

