import matplotlib.pyplot as plt
from cleaner import buildTeamsMatches
from data_loader import *
from visualization import * 
from transforms import addTeamNames
from analytics.analytics import *
from analysis.correlation import *
from insight import interpretCorrelation
from cleaner import getTeamIDByName

secondry_df = buildTeamsMatches(load_matches())
# secondry_df=secondry_df[
#     (secondry_df["team_api_id"]==getTeamIDByName(load_teams(),"Real Madrid CF"))&
#     (secondry_df["season"]=="2011/2012")
#                         ].sort_values("stage",ascending=True)
metric1="win_pct"
metric2="goal_std"
top_n=20
df = getTeamMetrics(
    secondry_df,
    [
        metric1,
    ],
    metric1
)
# teams_df = load_teams()
# df= addTeamNames(df,teams_df)
#TODO make text more visible 
# corr = calculateCorrelation(
#     df[metric1],#TODO make it depend on the column not the metric
#     df[metric2]
# )
# insight , comment =interpretCorrelation(corr,metric1,metric2)
# final_df=addTeamNames(df,load_teams()).head(50)

# final_insight=f"{insight} \n {comment}"

all_corr=calculateMetricCorrelations(secondry_df,"teams_points")
matrix_corr= calculateMatrixCorrelations(secondry_df)

df=addTeamNames(df,load_teams()).head(top_n)

# createTeamGoalDifferenceChart #TODO fix those two  
# createGoalsChart

fig = createHeatMapChart(matrix_corr)
plt.show()
# print(all_corr)

