from data_loader import *
from cleaner import buildTeamsMatches
from analytics.analytics import *
from transforms import addTeamNames , formatDataFrame, filterTeamMatches
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
    1: ("Top Attacking Teams","avg_goals"),
    2: ("Top Defensive Teams", "goals_conceded"),
    3:("Top Teams By Goal Difference","goal_diff"),
    4:("Home Point Per Game","home_ppg"),
    5:("Away Point Per","away_ppg"),
    6:("Most Consistent Team","consistency_gap"),
    7: ("Win Percentage", "win_pct"),
    8: ("Draw Percentage","draw_pct"),
    9: ("Loss Percentage", "loss_pct"),
    10:("Clean Sheet Percentage", "clean_sheet_pct"),
    11:("Home Clean Sheets Percentage","home_clean_sheet_pct"),
    12:("Away Clean Sheets Percentage", "away_clean_sheet_pct"),
    13:("Teams Goal Consistency", "goal_std"),
    14:("Teams Points","teams_points"),
    0:("Exit", exit)
}
    
    while True:
        chosen_season=None#TODO make choices for seasons
        chosen_team=None #TODO make team names format the right one e.g.(real madrid -> Real Madrid CF)
        print("=== Football Analytics Dashboard ===")
        for num, (name, _) in menu.items():
            print(f"{num}. {name}")
        
        choice = int(input("Choose a metric: "))
        if choice == 0:
            print("Goodbye!")
            break

        top_n = int(input("Show top N teams: "))
        name, metric = menu[choice]
        filtered_df=filterTeamMatches(team_matches,chosen_team,chosen_season)
        result = getTeamMetrics(
        filtered_df,
        [metric],       
        sort_by=metric
        )
        result = result.head(top_n)
        result = addTeamNames(result, teams_df)
        result = formatDataFrame(result, metric)
        
        print(f"\n------{name}------\n")
        print(result)
        print("\n")


if __name__ == "__main__":
    main()