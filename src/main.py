from data_loader import *
from cleaner import getTeamMatches
from analytics import *
from visualization import addTeamNames


def main():
    matches_df = load_matches()
    teams_df = load_teams()

    team_matches = getTeamMatches(matches_df)

    menu = {
    1: ("Top Attacking Teams", lambda:getTopAttackingTeams(team_matches)),
    2: ("Top Defensive Teams", lambda:getTopDefensiveTeams(team_matches)),
    3:("Top Teams By Goal Difference",lambda:getTopTeamsByGoalDiff(getTopAttackingTeams(team_matches),getTopDefensiveTeams(team_matches))),
    4:("Home Win Percentage",lambda:getVenuePPG(team_matches,"home")),
    5:("Away Win Percentage",lambda:getVenuePPG(team_matches,"away")),
    6:("Most Consistent Team",lambda:getMostConsistentTeams(getVenuePPG(team_matches,"home"),getVenuePPG(team_matches,"away"))),
    7: ("Win Percentage", lambda: getOutcomePercentage(team_matches, "win")),
    8: ("Draw Percentage", lambda: getOutcomePercentage(team_matches, "draw")),
    9: ("Loss Percentage", lambda: getOutcomePercentage(team_matches, "loss")),
    10:("Clean Sheet Percentage", lambda:getCleanSheets(team_matches)),
    11:("Home Clean Sheets Percentage",lambda:getVenueCleanSheetPct(team_matches,"home")),
    12:("Away Clean Sheets Percentage", lambda: getVenueCleanSheetPct(team_matches,"away")),
}

    print("=== Football Analytics Dashboard ===")
    for num, (name, _) in menu.items():
        print(f"{num}. {name}")

    choice = int(input("Choose a metric: "))
    top_n = int(input("Show top N teams: "))

    name, func = menu[choice]
    result=addTeamNames(func(),teams_df).head(top_n)
    print(f"\n------{name}------\n")
    print(result)


if __name__ == "__main__":
    main()