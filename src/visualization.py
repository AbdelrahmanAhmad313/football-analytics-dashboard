import pandas as pd
import matplotlib.pyplot as plt
from analytics import *
from cleaner import *
from data_loader import *

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

secondry_df = getTopAttackingTeamsByAvgGoals(getTopAttackingTeams(buildTeamsMatches(load_matches()))).head(10)
df= addTeamNames(secondry_df,load_teams())



def createTopAttackingTeamsChart(df):

    fig, ax = plt.subplots(figsize=(10, 6))


    BAR_OFFSET = 0.02
    bars = ax.barh(
    df["team_name"],
    df["avg_goals"]
)

    ax.set_xlabel("Average Goals per Match")
    # plt.ylabel("Team")
    ax.set_title("Top 10 Teams by Average Goals per Match")

    for bar in bars:
        width = bar.get_width()

        ax.text(
            width +BAR_OFFSET,                 
           bar.get_y() + bar.get_height()/2,
            f"{width:.2f}",
            va="center"
        )

    ax.invert_yaxis()
    ax.grid(axis="x", linestyle="--", alpha=0.4)

    fig.tight_layout()
    return fig

def createTeamGoalDifferenceChart(df,team_name):
    fig, ax = plt.subplots(figsize=(10,6))
    POINT_OFFSET= 0.1
    ax.plot(
        df["stage"],
        df["goal_diff"],
        marker="o"
    )
    highest = df.loc[df["goal_diff"].idxmax()]
    lowest = df.loc[df["goal_diff"].idxmin()]

    ax.annotate(
    f"  Highest (+{highest["goal_diff"]})",
    xy=(highest["stage"], highest["goal_diff"]),
    xytext=(
        highest["stage"] + 2,
        highest["goal_diff"] 
    ),
    arrowprops={
        "arrowstyle": "-|>",
        "color": "green",
        "linewidth": 2

    },
    color="green",
    fontsize=10,
    fontweight="normal"
    )


    ax.annotate(
    f"  Lowest ({lowest["goal_diff"]})",
    xy=(lowest["stage"], lowest["goal_diff"]),
    xytext=(
        lowest["stage"] + 2,
        lowest["goal_diff"]
    ),
    arrowprops={
        "arrowstyle": "-|>",
        "color": "red",
        "linewidth": 2
    },
    color="red",
    fontsize=10,
    fontweight="normal"
    )
    ax.set_xlabel("Match Week")
    ax.set_ylabel("Goal Difference")
    ax.set_title(f"{team_name} Goal Difference by Match Week (2014/15)")
    ax.axhline(y=0,linewidth=1,color="black")
    ax.set_xticks(df["stage"])

    ax.grid(True)

    fig.tight_layout()

    return fig

def createTeamVenuePointsChart(home_df,away_df,team_name):

    return

fig = createTopAttackingTeamsChart(df)
plt.show()

