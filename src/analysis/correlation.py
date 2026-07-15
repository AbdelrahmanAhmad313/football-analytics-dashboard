import pandas as pd
from analytics.analytics import METRIC_REGISTRY, getTeamMetrics
from insight import interpretCorrelation

def calculateCorrelation(metric1, metric2, method="pearson"):
    return metric1.corr(metric2, method=method).round(2)


def calculateMetricCorrelations(team_matches, base_metric, method="pearson"):

    metrics = list(METRIC_REGISTRY.keys())
    
    df = getTeamMetrics(
    team_matches,
    metrics
        )

    results = []

    for metric in metrics:

        if metric == base_metric:
            continue

        corr = calculateCorrelation(
        df[METRIC_REGISTRY[base_metric]["column"]],
        df[METRIC_REGISTRY[metric]["column"]],
        method
        )

        insight, comment = interpretCorrelation(
        corr,
        base_metric,
        metric
        )

        results.append({
        "metric": METRIC_REGISTRY[metric]["label"],
        "correlation": corr,
        "interpretation": insight,
        "comment": comment
        })

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
            "correlation",
            key=lambda s: s.abs(),
            ascending=False
        )
    results_df=results_df.rename(
        columns={
            "metric":"metric_name"
        }
    )

    return results_df.reset_index(drop=True)


def calculateMatrixCorrelations(team_matches,method="pearson"):
    metrics = list(METRIC_REGISTRY.keys())

    df = getTeamMetrics(
            team_matches,
            metrics
        )
    columns = [
    METRIC_REGISTRY[m]["column"]
    for m in METRIC_REGISTRY
        ]
    
    metrics_df = df[columns]

    corr_matrix = metrics_df.corr(method=method).round(2)

    labels = {
    info["column"]: info["label"]
    for info in METRIC_REGISTRY.values()
    }

    corr_matrix = corr_matrix.rename(
        index=labels,
        columns=labels
        )

    return corr_matrix