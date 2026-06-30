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

secondry_df = buildTeamsMatches(load_matches())
# secondry_df=secondry_df[
#     (secondry_df["team_api_id"]==getTeamIDByName(load_teams(),"Real Madrid CF"))&
#     (secondry_df["season"]=="2011/2012")
#                         ].sort_values("stage",ascending=True)

df = getTeamMetrics(
    secondry_df,
    [
        "avg_goals",
        "win_pct"
    ]
)
final_df=addTeamNames(df,load_teams()).head(20)


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

def createGoalsChart(df):

    fig, ax = plt.subplots(figsize=(12, 6))
    highest_goals_scored = df.loc[df["goals_scored"].idxmax()]
    highest_goals_conceded= df.loc[df["goals_conceded"].idxmax()]
    ax.plot(
    df["stage"],
    df["goals_scored"],
    marker="o",
    linewidth=2,
    label="Goals Scored"
)

    ax.plot(
    df["stage"],
    df["goals_conceded"],
    marker="s",
    linewidth=2,
    label="Goals Conceded"
)
    
    ax.annotate(
    f"  most goals scored ( {highest_goals_scored["goal_diff"]})",
    xy=(highest_goals_scored["stage"], highest_goals_scored["goals_scored"]),
    xytext=(
        highest_goals_scored["stage"] + 2,
        highest_goals_scored["goals_scored"] 
    ),
    arrowprops={
        "arrowstyle": "-|>",
        "color": "green",
        "linewidth": 2

    },
    color="green",
    fontsize=10,
    fontweight="bold"
    )


    ax.annotate(
    f"  most goals conceded ({highest_goals_conceded["goals_conceded"]})",
    xy=(highest_goals_conceded["stage"], highest_goals_conceded["goals_conceded"]),
    xytext=(
        highest_goals_conceded["stage"] + 2,
        highest_goals_conceded["goals_conceded"]
    ),
    arrowprops={
        "arrowstyle": "-|>",
        "color": "red",
        "linewidth": 2
    },
    color="red",
    fontsize=10,
    fontweight="bold"
    )
   

    ax.set_xlabel("Stages")
    ax.set_ylabel("Goals")
    ax.set_title(f"Goals Scored vs Goals Conceded by {df["team_name"].iloc[0]} in {df["season"].iloc[0]}")

    ax.set_xticks(df["stage"].iloc[::2])
    ax.legend()
    ax.grid(axis="both", linestyle="--", alpha=0.5)

    fig.tight_layout()
    return fig

def createScatterChart(df,metric1,metric2):
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(
        df[metric1],
        df[metric2],
        s=70,
        alpha=0.8,
        edgecolors="black"
    )

    xlabel = METRIC_REGISTRY[metric1]["label"]
    ylabel = METRIC_REGISTRY[metric2]["label"]

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    title =(f"{METRIC_REGISTRY[metric1]["label"]} vs "
            f"{METRIC_REGISTRY[metric2]["label"]}")
    ax.set_title(
        title
    )

    ax.grid(True, linestyle="--", alpha=0.8)
    for _, row in df.iterrows():

        ax.annotate(

        row["team_name"],

        (row[metric1], row[metric2]),

        fontsize=8
    )
    fig.tight_layout()

    return fig


fig = createScatterChart(final_df,"avg_goals","win_pct")
plt.show()

