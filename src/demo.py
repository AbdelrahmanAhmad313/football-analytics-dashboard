import matplotlib.pyplot as plt
from cleaner import buildTeamsMatches
from data_loader import *
from visualization import * 
from transforms import addTeamNames
from analytics import *


secondry_df = buildTeamsMatches(load_matches())
# secondry_df=secondry_df[
#     (secondry_df["team_api_id"]==getTeamIDByName(load_teams(),"Real Madrid CF"))&
#     (secondry_df["season"]=="2011/2012")
#                         ].sort_values("stage",ascending=True)

df = getTeamMetrics(
    secondry_df,
    [
        "avg_goals",
        "goal_std"
    ],
    "avg_goals"
)
final_df=addTeamNames(df,load_teams()).head(10)



fig = createScatterChart(final_df,"avg_goals","goal_std")
plt.show()

