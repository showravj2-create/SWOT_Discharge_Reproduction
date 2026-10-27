from pathlib import Path
import numpy as np
import pandas as pd

REQUIRED = ["reach_id", "swot_time", "swot_q", "gauge_time", "gauge_q",
            "quality_ok", "product_version"]


def read_matched_csv(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Input CSV not found: {path}")
    df = pd.read_csv(path)
    missing = sorted(set(REQUIRED) - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    df["reach_id"] = df["reach_id"].astype(str)
    for col in ("swot_time", "gauge_time"):
        df[col] = pd.to_datetime(df[col], utc=True, errors="coerce")
    for col in ("swot_q", "gauge_q"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    if df["quality_ok"].dtype != bool:
        mapping = {"true": True, "1": True, "yes": True,
                   "false": False, "0": False, "no": False}
        df["quality_ok"] = df["quality_ok"].astype(str).str.lower().map(mapping)
    df["quality_ok"] = df["quality_ok"].fillna(False).astype(bool)
    return df


def validate_table(df):
    problems = []
    if df["reach_id"].isna().any():
        problems.append("reach_id contains missing values")
    if df["swot_time"].isna().any():
        problems.append("swot_time contains invalid timestamps")
    if df["gauge_time"].isna().any():
        problems.append("gauge_time contains invalid timestamps")
    if (df["swot_q"].dropna() < 0).any() or (df["gauge_q"].dropna() < 0).any():
        problems.append("negative discharge values found; inspect units/quality flags")
    if df.duplicated(["reach_id", "swot_time"]).any():
        problems.append("duplicate reach_id + swot_time pairs found")
    return problems
