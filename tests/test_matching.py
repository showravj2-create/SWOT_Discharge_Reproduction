import pandas as pd
from src.swot_repro.matching import filter_study_period, apply_time_tolerance


def test_period_and_tolerance_filters():
    df = pd.DataFrame({
        "reach_id": ["a", "a"],
        "swot_time": pd.to_datetime(["2023-04-01T00:00:00Z", "2024-09-01T00:00:00Z"]),
        "gauge_time": pd.to_datetime(["2023-04-01T01:00:00Z", "2024-09-01T00:00:00Z"]),
        "swot_q": [10., 20.],
        "gauge_q": [11., 21.],
        "quality_ok": [True, True],
    })
    period = filter_study_period(df)
    matched = apply_time_tolerance(period, 24)
    assert len(matched) == 1
    assert matched.iloc[0]["reach_id"] == "a"
