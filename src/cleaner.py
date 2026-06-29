import pandas as pd

def buildTeamsMatches(match_df):

  
    home_df = match_df[
    ["home_team_api_id", "home_team_goal", "away_team_goal","season","stage"]
].rename(
    columns={
        "home_team_api_id": "team_api_id",
        "home_team_goal": "goals_scored",
        "away_team_goal": "goals_conceded"
    }
)
    home_df["venue"] ="home"
  
    away_df = match_df[ 
    ["away_team_api_id", "away_team_goal", "home_team_goal","season","stage"]
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
    team_matches_df["goal_diff"]=team_matches_df["goals_scored"]-team_matches_df["goals_conceded"]

    
    team_matches_df["points"] = 0

    team_matches_df.loc[
        team_matches_df["goals_scored"] > team_matches_df["goals_conceded"],
        "points"
    ] = 3
    team_matches_df.loc[
        team_matches_df["goals_scored"] == team_matches_df["goals_conceded"],
        "points"
    ] = 1
    
    team_matches_df["score"] = (
    team_matches_df["goals_scored"].astype(str)
    + "-"
    + team_matches_df["goals_conceded"].astype(str)
)
    team_matches_df["clean_sheet"] = (team_matches_df["goals_conceded"] == 0)

    team_matches_df["won"]= (team_matches_df["points"] == 3)

    team_matches_df["drawn"]= (team_matches_df["points"] == 1)

    team_matches_df["lost"]= (team_matches_df["points"] == 0)
  
    team_matches_df=team_matches_df[[
        "team_api_id",
        "goals_scored",
        "goals_conceded",
        "goal_diff",
        "venue",
        "points",
        "score",
        "clean_sheet",
        "won",
        "drawn",
        "lost",
        "season",
        "stage"
    ]]
    


    return team_matches_df
 
def getTeamMatches(team_matches_df,team_api_id= None,season=None):
    filtered_df = team_matches_df.copy()

    if team_api_id is not None:
        filtered_df = filtered_df[
            filtered_df["team_api_id"] == team_api_id
        ]

    if season is not None:
        filtered_df = filtered_df[
            filtered_df["season"] == season
        ]

    return filtered_df

def getTeamIDByName(teams_df,team_name):
    team_id =teams_df[teams_df["team_long_name"]==team_name]
    if team_id.empty:
        raise ValueError(f"Team '{team_name}' not found.")

    return team_id.iloc[0]["team_api_id"]
