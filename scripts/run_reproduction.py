import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import argparse
import json
from pathlib import Path

from src.swot_repro.io import read_matched_csv
from src.swot_repro.matching import filter_study_period, apply_time_tolerance
from src.swot_repro.metrics import per_reach_metrics, aggregate_metrics
from src.swot_repro.plots import make_plots

parser = argparse.ArgumentParser(description="Evaluate matched SWOT/gauge discharge observations.")
parser.add_argument("--input", required=True)
parser.add_argument("--outdir", default="reports")
parser.add_argument("--start", default="2023-03-01")
parser.add_argument("--end-exclusive", default="2024-08-01")
parser.add_argument("--tolerance-hours", type=float, default=24)
parser.add_argument("--min-pairs", type=int, default=5)
parser.add_argument("--include-quality-failures", action="store_true")
args = parser.parse_args()

outdir = Path(args.outdir)
outdir.mkdir(parents=True, exist_ok=True)
raw = read_matched_csv(args.input)
period = filter_study_period(
    raw, args.start, args.end_exclusive,
    require_quality=not args.include_quality_failures
)
matched = apply_time_tolerance(period, args.tolerance_hours)
per_reach = per_reach_metrics(matched, min_pairs=args.min_pairs)
summary = aggregate_metrics(per_reach)
summary.update({
    "input_rows": int(len(raw)),
    "rows_in_study_period_after_quality_filter": int(len(period)),
    "rows_after_time_tolerance": int(len(matched)),
    "time_tolerance_hours": args.tolerance_hours,
    "study_start_utc": args.start,
    "study_end_exclusive_utc": args.end_exclusive,
    "quality_failures_included": bool(args.include_quality_failures),
    "scientific_status": "evaluation output; exact reproduction requires verification of the paper's precise filters and metric definitions",
})
per_reach.to_csv(outdir / "per_reach_metrics.csv", index=False)
with open(outdir / "summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)
make_plots(matched, per_reach, outdir)
print(json.dumps(summary, indent=2))
