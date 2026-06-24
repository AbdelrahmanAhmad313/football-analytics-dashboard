import pandas as pd


def checkNulls(df):
    invalid_df = df[
        df.isna().any(axis=1)
    ].copy()

    return {
        "check": "null_values",
        "passed": len(invalid_df) == 0,
        "invalid_rows": len(invalid_df),
        "reason": "one or more required fields contain null values",
        "sample": invalid_df.head()
    }
 

def checkGoalDiff(df):

    invalid_df = df[
       df["goal_diff"] !=
        (df["goals_scored"] - df["goals_conceded"])
    ].copy()

    invalid_df["expected_goal_diff"] = (
        invalid_df["goals_scored"] -
        invalid_df["goals_conceded"]
    )

    return {
        "check": "goal_diff",
        "passed": len(invalid_df) == 0,
        "invalid_rows": len(invalid_df),
        "reason": "goal_diff does not match goals_scored - goals_conceded",
        "sample": invalid_df.head()
    }


def checkPoints(df):

    expected_points = pd.Series(0, index=df.index)


    expected_points.loc[
        df["goals_scored"] > df["goals_conceded"]
    ] = 3

    expected_points.loc[
        df["goals_scored"] == df["goals_conceded"]
    ] = 1

    invalid_mask = (
    df["points"] != expected_points
)
    invalid_df = df[invalid_mask].copy()

    invalid_df["expected_points"] = expected_points[invalid_mask]

    return {
        "check": "points",
        "passed": len(invalid_df) == 0,
        "invalid_rows": len(invalid_df),
       "reason": "points do not match the match result",
        "sample": invalid_df.head()
    }
    

def checkCleanSheet(df):

    invalid_df = df[
    df["clean_sheet"] != (df["goals_conceded"] == 0)
].copy()

    invalid_df["expected_clean_sheet"] = (invalid_df["goals_conceded"]==0)

    return {
        "check": "clean_sheet",
        "passed": len(invalid_df) == 0,
        "invalid_rows": len(invalid_df),
       "reason": "clean_sheet does not match goals_conceded",
        "sample": invalid_df.head()
    }

def checkMatchOutcomeConsistency(df):
    invalid_mask = (
    (df["won"] != (df["goals_scored"] > df["goals_conceded"])) |
    (df["drawn"] != (df["goals_scored"] == df["goals_conceded"])) |
    (df["lost"] != (df["goals_scored"] < df["goals_conceded"])) |
    (
        df["won"].astype(int) +
        df["drawn"].astype(int) +
        df["lost"].astype(int)
    ) != 1
)

    invalid_df=df[invalid_mask].copy()

    invalid_df["expected_won"]= (invalid_df["goals_scored"] > invalid_df["goals_conceded"])

    invalid_df["expected_drawn"]= (invalid_df["goals_scored"] == invalid_df["goals_conceded"])

    invalid_df["expected_loss"]= (invalid_df["goals_scored"] < invalid_df["goals_conceded"])
    return {
        "check": "match_outcome_consistency",
        "passed": len(invalid_df) == 0,
        "invalid_rows": len(invalid_df),
       "reason": "won, draw, and loss flags do not match goals scored and goals conceded",
        "sample": invalid_df.head()
    }

def runQualityChecks(df):
    checks = [
        checkNulls,
        checkGoalDiff,
        checkPoints,
        checkCleanSheet,
        checkMatchOutcomeConsistency
    ]

    all_results = []

    for check in checks:
        all_results.append(check(df))

    summary_df = pd.DataFrame([
        {
            "check": result["check"],
            "passed": result["passed"],
            "invalid_rows": result["invalid_rows"]
        }
        for result in all_results
    ])

    # print(summary_df)

    # print("\nFailed Checks:")
    # print("-" * 50)

    for result in all_results:

        if not result["passed"]:

            print(f"\nCheck: {result['check']}")
            print(f"Reason: {result['reason']}")
            print(f"Invalid Rows: {result['invalid_rows']}")
            print(result["sample"])

    return summary_df,all_results