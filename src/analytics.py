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


def getVenuePPG(team_matches,venue):
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
    wanted_pct=f"{key}_%"
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
