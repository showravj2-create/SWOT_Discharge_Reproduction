"""Create fake rows to smoke-test the pipeline; never use as scientific evidence."""
from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
rows = []
dates = pd.date_range("2023-03-01", periods=120, freq="5D", tz="UTC")
for reach in ["toy_A", "toy_B", "toy_C"]:
    gauge = np.maximum(1, 50 + 15*np.sin(np.arange(len(dates))/8) + rng.normal(0, 5, len(dates)))
    swot = np.maximum(1, gauge * rng.normal(1.05, .12, len(dates)))
    for d, g, s in zip(dates, gauge, swot):
        rows.append({"reach_id": reach, "swot_time": d, "swot_q": s,
                     "gauge_time": d + pd.Timedelta(hours=2), "gauge_q": g,
                     "quality_ok": True, "product_version": "SYNTHETIC-DO-NOT-CITE"})
out = Path("data/processed/smoke_test.csv")
out.parent.mkdir(parents=True, exist_ok=True)
pd.DataFrame(rows).to_csv(out, index=False)
print(f"Wrote {out}; these are synthetic smoke-test values, not real SWOT data.")
