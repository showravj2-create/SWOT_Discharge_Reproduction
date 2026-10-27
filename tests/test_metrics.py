import pandas as pd
from src.swot_repro.metrics import per_reach_metrics, aggregate_metrics


def test_perfect_correlation_and_zero_bias():
    df = pd.DataFrame({
        "reach_id": ["a"]*5,
        "swot_time": pd.date_range("2023-01-01", periods=5, tz="UTC"),
        "swot_q": [1, 2, 3, 4, 5],
        "gauge_q": [1, 2, 3, 4, 5],
    })
    result = per_reach_metrics(df, min_pairs=5)
    assert len(result) == 1
    assert abs(result.iloc[0]["pearson_r"] - 1) < 1e-8
    assert abs(result.iloc[0]["mean_relative_bias_pct"]) < 1e-8


def test_aggregate_empty():
    out = aggregate_metrics(pd.DataFrame(columns=[
        "pearson_r", "mean_relative_bias_pct", "n_pairs"
    ]))
    assert out["n_reaches_with_metrics"] == 0
