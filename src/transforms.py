import pandas as pd
from analytics.analytics import METRIC_REGISTRY

def addTeamNames(df,teams_df):
   
    final_df=pd.merge(
        df,
        teams_df,
        on="team_api_id"
    )
    final_df=final_df.rename(
        columns={
            "team_long_name":"team_name"
        }
    )
    final_df = final_df.drop(columns=["team_api_id"])

    cols = ["team_name"] + [
        col for col in final_df.columns
        if col != "team_name"
    ]

    return final_df[cols]


def formatValue(metric, value):
    fmt = METRIC_REGISTRY[metric].get("format", "float")

    if fmt == "percent":
        return f"{value:.1f}%"

    if fmt == "integer":
        return f"{int(value)}"

    return f"{value:.2f}"

def formatDataFrame(df, metric):
    df = df.copy()

    metric_info = METRIC_REGISTRY[metric]
    column = metric_info["column"]
    fmt = metric_info.get("format", "float")

    if fmt == "percent":
        df[column] = df[column].map(lambda x: f"{x:.1f}%")

    elif fmt == "integer":
        df[column] = df[column].map(lambda x: f"{int(x)}")

    else:  # float
        df[column] = df[column].map(lambda x: f"{x:.2f}")

    return df

def filterTeamMatches(team_matches, team_id=None, season=None):
    filtered_df = team_matches.copy()

    if team_id is not None:
        filtered_df = filtered_df[filtered_df["team_api_id"] == team_id]

    if season is not None:
        filtered_df = filtered_df[filtered_df["season"] == season]

    return filtered_df