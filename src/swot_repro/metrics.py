import numpy as np
import pandas as pd
from scipy.stats import pearsonr


def per_reach_metrics(df, min_pairs=5):
    rows = []
    for reach_id, group in df.groupby("reach_id", sort=True):
        g = group.sort_values("swot_time")
        x = g["swot_q"].to_numpy(dtype=float)
        y = g["gauge_q"].to_numpy(dtype=float)
        valid = np.isfinite(x) & np.isfinite(y)
        x, y = x[valid], y[valid]
        if len(x) < min_pairs:
            continue
        corr = float(pearsonr(x, y).statistic) if np.std(x) > 0 and np.std(y) > 0 else np.nan
        mean_gauge = float(np.mean(y))
        mean_bias_pct = (100 * (float(np.mean(x)) - mean_gauge) / mean_gauge
                         if mean_gauge != 0 else np.nan)
        rows.append({
            "reach_id": str(reach_id),
            "n_pairs": int(len(x)),
            "pearson_r": corr,
            "mean_relative_bias_pct": mean_bias_pct,
            "mae": float(np.mean(np.abs(x-y))),
            "rmse": float(np.sqrt(np.mean((x-y)**2))),
            "median_absolute_error": float(np.median(np.abs(x-y))),
        })
    return pd.DataFrame(rows)


def aggregate_metrics(per_reach):
    corr = per_reach["pearson_r"].dropna()
    bias = per_reach["mean_relative_bias_pct"].dropna()
    def q(s, p):
        return float(s.quantile(p)) if len(s) else None
    return {
        "n_reaches_with_metrics": int(len(per_reach)),
        "n_reaches_with_correlation": int(len(corr)),
        "median_correlation": q(corr, .5),
        "correlation_q25": q(corr, .25),
        "correlation_q75": q(corr, .75),
        "median_mean_relative_bias_pct": q(bias, .5),
        "median_pairs_per_reach": q(per_reach["n_pairs"], .5),
        "bias_definition": "100 * (mean(SWOT Q) - mean(gauge Q)) / mean(gauge Q), computed per reach",
    }
