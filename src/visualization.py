from chart_utils import *
from analytics.analytics import METRIC_REGISTRY
from style import *
from transforms import formatValue
import numpy as np



def createHorizontalBarChart(df,metric,top_n=None):

    fig , ax = createFigure()
    if metric=="correlation":
        bary=df["metric_name"]
        xlabel="Pearson Correlation"
        title="Correlation of Engineered Metrics with Team Points"
    else:
        bary=df["team_name"]
        xlabel=METRIC_REGISTRY[metric]["label"]
        title=f"top "
        if top_n is not None:
            title+=f"{top_n} "
        title+=f"Teams by {METRIC_REGISTRY[metric]["label"]}"

    
    BAR_OFFSET = 0.01
    bars = ax.barh(
    bary,
    df[metric],
)

   
    
    ax.set_xlabel(xlabel,fontsize=LABEL_FONT_SIZE)
    ax.set_title(title,
                    fontsize=TITLE_FONT_SIZE,
                    fontweight=TITLE_FONT_WEIGHT
                    )

    for bar in bars:
        if bar.get_width() >= 0:
            bar.set_color("blue")
            ha = "left"
        else:
            bar.set_color("red")
            ha = "right"

        width = bar.get_width()
        
        ax.text(
            width +BAR_OFFSET,                 
           bar.get_y() + bar.get_height()/2,
            formatValue("avg_goals", width),
            va="center",
            ha=ha
        )
   
    ax.axvline(
            0,
            color="black",
            linestyle="--",
            alpha=0.7
        )

    ax.invert_yaxis()

    applyChartGrid(ax=ax,axis="x")

    fig.tight_layout()
    return fig


def createTeamGoalDifferenceChart(df,team_name):
    fig , ax = createFigure()
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
    
    ax.set_xlabel("Match Week",fontsize=LABEL_FONT_SIZE)
    ax.set_ylabel("Goal Difference",fontsize=LABEL_FONT_SIZE)
    ax.set_title(f"{team_name} Goal Difference by Match Week (2014/15) ",#TODO make season dynamic
                    fontsize=TITLE_FONT_SIZE,
                    fontweight=TITLE_FONT_WEIGHT
    )
    ax.axhline(y=0,linewidth=1,color="black")
    ax.set_xticks(df["stage"])

    applyChartGrid(ax)

    fig.tight_layout()

    return fig

def createGoalsChart(df):
    fig , ax = createFigure()

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
   

    ax.set_xlabel("Stages",fontsize=LABEL_FONT_SIZE)
    ax.set_ylabel("Goals",fontsize=LABEL_FONT_SIZE)
    ax.set_title(f"Goals Scored vs Goals Conceded by {df["team_name"].iloc[0]} in {df["season"].iloc[0]}",
                fontsize=TITLE_FONT_SIZE,
                fontweight=TITLE_FONT_WEIGHT
    )

    ax.set_xticks(df["stage"].iloc[::2])
    ax.legend()
    applyChartGrid(ax)

    fig.tight_layout()
    return fig

def createScatterChart(df,metric1,metric2,corr,insight):
    fig , ax = createFigure(figsize=(12,6))

    ax.scatter(
        df[metric1],
        df[metric2],
        s=70,
        alpha=0.8,
        edgecolors="black"
    )
    mean_x = df[metric1].mean()
    mean_y = df[metric2].mean()
    xlabel = METRIC_REGISTRY[metric1]["label"]
    ylabel = METRIC_REGISTRY[metric2]["label"]

    ax.axvline(
    mean_x,
    color="red",
    linestyle="--",
    linewidth=2,
    label=f" Avg {xlabel}"
)

    ax.axhline(
    mean_y,
    color="blue",
    linestyle="--",
    linewidth=2,
    label=f" Avg {ylabel}"
)
    ax.set_xlabel(xlabel,fontsize=LABEL_FONT_SIZE)
    ax.set_ylabel(ylabel,fontsize=LABEL_FONT_SIZE)
    title =(f"{METRIC_REGISTRY[metric1]["label"]} vs "
            f"{METRIC_REGISTRY[metric2]["label"]}"
            f"\n Pearson Correlation: {corr}"
            f"\n {insight}"
            )
    ax.set_title(
        title,
        fontsize=TITLE_FONT_SIZE,
        fontweight=TITLE_FONT_WEIGHT
    )

    applyChartGrid(ax)
    for _, row in df.iterrows():

        ax.annotate(

        row["team_name"],

        (row[metric1], row[metric2]),

        fontsize=8
    )

    ax.legend()
    fig.tight_layout()

    return fig

def createHistogramChart(df,metric,bins=10):

    fig , ax = createFigure()

    mean_value = df[metric].mean()

    ax.hist(
       df[metric],
        bins=bins,
        edgecolor="black",
    linewidth=1,
    alpha=0.8
        )
    ax.axvline(
    mean_value,
    color="red",
    linestyle="--",
    linewidth=2,
    label=f"Mean = {mean_value:.2f}"
)
    
    ax.set_title(f"Distribution of {METRIC_REGISTRY[metric]['label']}",
                fontsize=TITLE_FONT_SIZE,
                fontweight=TITLE_FONT_WEIGHT)
    ax.set_xlabel(METRIC_REGISTRY[metric]["label"],fontsize=LABEL_FONT_SIZE)
    ax.set_ylabel("Number of Teams",fontsize=LABEL_FONT_SIZE)
    ax.legend()
    applyChartGrid(ax,"y")

    fig.tight_layout()
    return fig

def createHeatMapChart(corr_matrix):

    fig , ax= createFigure()
    mask = np.triu(np.ones(corr_matrix.shape, dtype=bool), k=1)

    corr_matrix = corr_matrix.mask(mask)

    im=ax.imshow(
        corr_matrix,
    cmap="coolwarm",
    vmin=-1,
    vmax=1
    )
    ax.set_xticks(range(len(corr_matrix.columns)))
    ax.set_yticks(range(len(corr_matrix.index)))

    ax.set_xticklabels(
    corr_matrix.columns,
    rotation=45,
    ha="right"
)

    ax.set_yticklabels(corr_matrix.index)
    fig.colorbar(
        im,
        ax=ax,
        label="Pearson Correlation"
    )
    

    ax.set_title(
    "Correlation Matrix of Engineered Metrics",
    fontsize=TITLE_FONT_SIZE,
    fontweight=TITLE_FONT_WEIGHT
)
    fig.tight_layout()


    return fig
