import pandas as pd
import numpy as np


def filter_study_period(df, start="2023-03-01", end_exclusive="2024-08-01",
                        require_quality=True):
    out = df.copy()
    start = pd.Timestamp(start, tz="UTC")
    end = pd.Timestamp(end_exclusive, tz="UTC")
    out = out[(out["swot_time"] >= start) & (out["swot_time"] < end)]
    if require_quality:
        out = out[out["quality_ok"]]
    out = out.replace([np.inf, -np.inf], np.nan)
    out = out.dropna(subset=["reach_id", "swot_time", "gauge_time", "swot_q", "gauge_q"])
    return out.sort_values(["reach_id", "swot_time"])


def add_time_difference(df):
    out = df.copy()
    out["time_difference_hours"] = (
        (out["swot_time"] - out["gauge_time"]).abs().dt.total_seconds() / 3600
    )
    return out


def apply_time_tolerance(df, tolerance_hours=24):
    out = add_time_difference(df)
    return out[out["time_difference_hours"] <= tolerance_hours].copy()
