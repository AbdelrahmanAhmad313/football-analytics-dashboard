import pandas as pd

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
