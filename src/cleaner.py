import pandas as pd

def getTeamMatches(match_df):

  
    home_df = match_df[
    ["home_team_api_id", "home_team_goal", "away_team_goal"]
].rename(
    columns={
        "home_team_api_id": "team_api_id",
        "home_team_goal": "goals_scored",
        "away_team_goal": "goals_conceded"
    }
)
    home_df["venue"] ="home"
  
    away_df = match_df[ 
    ["away_team_api_id", "away_team_goal", "home_team_goal"]
].rename(
    columns={
        "away_team_api_id": "team_api_id",
        "away_team_goal": "goals_scored",
        "home_team_goal": "goals_conceded"
    }
)
    away_df["venue"]="away"

    team_matches_df = pd.concat(
    [home_df, away_df],
    ignore_index=True
)

    team_matches_df["points"] = 0

    team_matches_df.loc[
        team_matches_df["goals_scored"] > team_matches_df["goals_conceded"],
        "points"
    ] = 3
    team_matches_df.loc[
        team_matches_df["goals_scored"] == team_matches_df["goals_conceded"],
        "points"
    ] = 1
    team_matches_df["goal_diff"]=team_matches_df["goals_scored"]-team_matches_df["goals_conceded"]

    team_matches_df["score"] = (
    team_matches_df["goals_scored"].astype(str)
    + "-"
    + team_matches_df["goals_conceded"].astype(str)
)
    team_matches_df["clean_sheet"] = (team_matches_df["goals_conceded"] == 0)

    team_matches_df["won"]= (team_matches_df["points"] == 3)

    team_matches_df["drawn"]= (team_matches_df["points"] == 1)

    team_matches_df["lost"]= (team_matches_df["points"] == 0)

    


    return team_matches_df
 