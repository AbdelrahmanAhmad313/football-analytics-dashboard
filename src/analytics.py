import pandas as pd



def getTopAttackingTeams(team_matches):


    top_attacking_team_df= (
    team_matches
    .groupby("team_api_id")
    .agg(
        goals_scored=("goals_scored", "sum"),
        matches_played=("team_api_id", "size"),
        avg_goals=("goals_scored","mean")
    )
    .query("matches_played >= 100 ")
    .sort_values("goals_scored",ascending=False)
    .reset_index()
)
    top_attacking_team_df["avg_goals"] =(top_attacking_team_df["avg_goals"].round(2))

    return top_attacking_team_df

def getTopAttackingTeamsByAvgGoals(top_attacking):

    return top_attacking.sort_values("avg_goals",ascending= False)

def getTopDefensiveTeams(team_matches):


    top_defensive_team_df = (
        team_matches
                          .groupby("team_api_id")
                          .agg(
                              goals_conceded=("goals_conceded","sum"),
                              matches_played=("team_api_id","size"),
                              avg_goals_conceded=("goals_conceded","mean")
                          )
                          .query("matches_played >= 100")
                          .sort_values("goals_conceded",ascending=True)
                        #   .head(10)
                          .reset_index()
                        
                          )
    
    top_defensive_team_df["avg_goals_conceded"] =(top_defensive_team_df["avg_goals_conceded"].round(2))
    return top_defensive_team_df

def getTopDefensiveTeamsByAvgGoals(top_defensive):

    return top_defensive.sort_values("avg_goals_conceded",ascending=True)


def getTopTeamsByGoalDiff(attacking_teams,defensive_teams):
   
    top_teams = pd.merge(
        attacking_teams,
        defensive_teams.drop(columns=["matches_played"]),
        on="team_api_id"
    )
    top_teams["goals_diff"]=(top_teams["goals_scored"]- top_teams["goals_conceded"])
    top_teams["avg_goals_diff"] = (
        top_teams["avg_goals"]
        - top_teams["avg_goals_conceded"]
    ).round(2)

    top_teams=(top_teams
    .sort_values("avg_goals_diff",ascending=False)
    .reset_index(drop=True)
)
    
    top_teams = top_teams[
    [
        "team_api_id",
        "matches_played",
        "goals_scored",
        "goals_conceded",
        "goals_diff",
        "avg_goals",
        "avg_goals_conceded",
        "avg_goals_diff"
    ]
    ]
    

    return top_teams


def getVenuePPG(team_matches,venue,team_id=None,season=None):
   

    matches_df = team_matches[
    team_matches["venue"] == venue
].copy()
    points = f"{venue}_points"
    matches = f"{venue}_matches"
    ppg = f"{venue}_ppg"

    ppg_df = (
        matches_df
        .groupby("team_api_id")
        .agg(
           **{
            points: ("points", "sum"),
            matches: ("team_api_id", "size")
        }
        )
        .reset_index()
    )
    ppg_df[ppg]=(ppg_df[points]/ppg_df[matches]).round(2)
    ppg_df=(ppg_df.sort_values(ppg,ascending=False))

    if team_id is not None and season is not None:
        return(
            team_matches[team_matches["team_api_id"]==team_id]&
               team_matches[team_matches["season"]==season]
               )
    elif team_id is not None:
        return team_matches[team_matches["team_api_id"]==team_id]
    elif season is not None:
        return team_matches[team_matches["season"]==season]
    
    
    return ppg_df



def getMostConsistentTeams(home_ppg_df,away_ppg_df):

    teams_ppg=pd.merge(
        home_ppg_df,
        away_ppg_df,
        left_on="team_api_id",
        right_on="team_api_id"
    )


    teams_ppg["matches_played"] = teams_ppg["home_matches"]+ teams_ppg["away_matches"]
    teams_ppg["consistency_gap"]=abs(teams_ppg["home_ppg"]-teams_ppg["away_ppg"])
    teams_ppg=(teams_ppg
               .query("matches_played > 100")
                .sort_values("consistency_gap", ascending=True)
               )
            
    teams_ppg= teams_ppg[["team_api_id","home_ppg","away_ppg","consistency_gap","matches_played"]]
    return teams_ppg

def getCleanSheets(team_matches):
    team_clean_sheets = (
    team_matches
    .groupby("team_api_id")
    .agg(
        clean_sheets=("clean_sheet", "sum"),
        matches_played=("team_api_id", "size"),
    )
    .query("matches_played > 100")
)

    pct = (
    team_clean_sheets["clean_sheets"]
    / team_clean_sheets["matches_played"]
    * 100
).round(1)

    team_clean_sheets = team_clean_sheets.assign(
    clean_sheets_pct=pct
).sort_values(
    "clean_sheets_pct",
    ascending=False
).reset_index()

    team_clean_sheets["clean_sheets_%"] = (
    team_clean_sheets["clean_sheets_pct"].astype(str) + "%"
)

    return team_clean_sheets.drop(columns="clean_sheets_pct")

def getOutcomePercentage(team_matches,key):
    matches_wanted=f"matches_{key}"
    wanted_pct=f"{key}_pct"
    ascending = key != "win"
    past_wanted={
        "win":"won",
        "draw":"drawn",
        "loss":"lost"
    }
    team_pct=(
        team_matches
        .groupby("team_api_id")
        .agg(
            **{
            matches_wanted: (past_wanted[key], "sum")
        },
            matches_played = ("team_api_id","size")
        )
        .query("matches_played > 100")
    )
    pct = (
    team_pct[matches_wanted]
    / team_pct["matches_played"]
    * 100
).round(1)

    team_pct = team_pct.assign(
    outcome_pct=pct
).sort_values(
    "outcome_pct",
    ascending=ascending
).reset_index()

    team_pct[wanted_pct] = (
    team_pct["outcome_pct"].astype(str) + "%"
)

    return team_pct.drop(columns="outcome_pct")

def getVenueCleanSheetPct(team_matches,venue):
    team_clean_sheets=team_matches[
    team_matches["venue"] == venue
    ].copy()
    clean_sheets= getCleanSheets(team_clean_sheets)
    return clean_sheets

def getGoalDifferenceByTeamInSeason(team_matches):
    
    return team_matches.sort_values("stage")[["team_api_id","goal_diff","stage"]]


METRIC_REGISTRY = {
        "avg_goals": {
        "function": getTopAttackingTeams,
        "column": "avg_goals",
        "label":"Average Goals Scored",
        "higher_is_better": True,
    },

    "goals_scored": {
        "function": getTopAttackingTeams,
        "column": "goals_scored",
        "label":"Goals Scored",
        "higher_is_better": True,
    },

    "home_ppg": {
        "function": getVenuePPG,
        "column": "home_ppg",
        "kwargs": {"venue": "home"},
        "label":"Home Points Per Game",
        "higher_is_better": True,
    },

    "away_ppg": {
        "function": getVenuePPG,
        "column": "away_ppg",
        "kwargs": {"venue": "away"},
        "label":"Away Points Per Game",
        "higher_is_better": True,
    },
    "avg_goals_conceded":{
        "function": getTopDefensiveTeams,
        "column": "avg_goals_conceded",
        "label":"Average Goals Conceded",
        "higher_is_better": False,
        },
    "goals_conceded":{
        "function": getTopDefensiveTeams,
        "column": "goals_conceded",
        "label":"Goals Conceded",
        "higher_is_better": False,
        },

    "clean_sheet_pct":{
        "function": getCleanSheets,
        "column":"clean_sheet_pct",
        "label":"Clean Sheets Percentage",
        "higher_is_better": True,},


    "win_pct": {
        "function": getOutcomePercentage,
                "kwargs": {
                    "key": "win"
                    },
                "column":"win_pct",
        "label":"Win Percentage",
        "higher_is_better": True,},

    "draw_pct": {
        "function": getOutcomePercentage,
                 "kwargs": {
                    "key": "draw"
                        },
                "column":"draw_pct",
        "label":"Draw Percentage",
        "higher_is_better": True,},

    "loss_pct": {
        "function": getOutcomePercentage,
                 "kwargs": {
                    "key": "loss"
                    },
                "column":"loss_pct",
        "label":"Loss Percentage",
        "higher_is_better": False,},

    
}

def getTeamMetrics(team_matches,metrics):
    
    
    execution_plan={}
    for metric in metrics:
        if metric not in METRIC_REGISTRY:
            raise ValueError(f"Unknown metric: {metric}")
    
        metric_info = METRIC_REGISTRY[metric]
        func = metric_info["function"]
        kwargs = metric_info.get("kwargs", {})
        column = metric_info["column"]
        computation_key = (
        func,
        tuple(kwargs.items())
    )
        if computation_key not in execution_plan:
            execution_plan[computation_key] = {
            "columns": [column]
            }
        elif column not in execution_plan[computation_key]["columns"]:
            execution_plan[computation_key]["columns"].append(column)

    metric_dfs=[]

    for computation_key, info in execution_plan.items():

        func, kwargs_tuple = computation_key
        kwargs = dict(kwargs_tuple)

        df = func(team_matches, **kwargs)
        columns = ["team_api_id"] + info["columns"]

        metric_dfs.append(
            df[columns]
        )
        
    if not metric_dfs:
        return pd.DataFrame()
    
    final_df = metric_dfs[0]

    for df in metric_dfs[1:]:
        final_df = final_df.merge(
            df,
            on="team_api_id"
        )
        
    
    return final_df

