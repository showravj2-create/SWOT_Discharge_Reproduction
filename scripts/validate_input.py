import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import argparse
from src.swot_repro.io import read_matched_csv, validate_table

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
args = parser.parse_args()
df = read_matched_csv(args.input)
problems = validate_table(df)
print(f"Rows: {len(df)} | reaches: {df['reach_id'].nunique()}")
if problems:
    print("Validation warnings:")
    for problem in problems:
        print(f"- {problem}")
    raise SystemExit(1)
print("Input structure passed basic validation. Scientific metadata still require manual verification.")
