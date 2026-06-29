from data_loader import *
from cleaner import buildTeamsMatches
from analytics import *
from visualization import addTeamNames
from quality import runQualityChecks


def main():
    matches_df = load_matches()
    teams_df = load_teams()

    team_matches = buildTeamsMatches(matches_df)
    summary_df, all_results = runQualityChecks(team_matches)

    failed_checks = [
        result
        for result in all_results
        if not result["passed"]
    ]

    if failed_checks:

        print("\nData Quality Checks Failed\n")
        print(summary_df)

        for result in failed_checks:
            print(f"\nCheck: {result['check']}")
            print(f"Reason: {result['reason']}")
            print(result["sample"])

        return

    print("\nData Quality Checks Passed\n")

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
    13:("Exit", exit)
}
    
    while True:
        print("=== Football Analytics Dashboard ===")
        for num, (name, _) in menu.items():
            print(f"{num}. {name}")
        # print(team_matches.head())
        choice = int(input("Choose a metric: "))
        if choice == 13:
            print("Goodbye!")
            break
        top_n = int(input("Show top N teams: "))

        name, func = menu[choice]
        result=addTeamNames(func(),teams_df).head(top_n)
        print(f"\n------{name}------\n")
        print(result)
        print("\n")


if __name__ == "__main__":
    main()