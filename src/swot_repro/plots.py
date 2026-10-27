from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def make_plots(df, metrics, outdir):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    if not metrics.empty:
        values = metrics["pearson_r"].dropna()
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.hist(values, bins=15)
        ax.set_xlabel("Per-reach Pearson correlation")
        ax.set_ylabel("Number of reaches")
        ax.set_title("SWOT vs gauge discharge correlation")
        fig.tight_layout()
        fig.savefig(outdir / "correlation_by_reach.png", dpi=160)
        plt.close(fig)

    reaches = df["reach_id"].drop_duplicates().head(4).tolist()
    if reaches:
        fig, axes = plt.subplots(len(reaches), 1, figsize=(11, 3*len(reaches)), squeeze=False)
        for ax, reach in zip(axes[:, 0], reaches):
            g = df[df["reach_id"] == reach].sort_values("swot_time")
            ax.plot(g["swot_time"], g["gauge_q"], marker=".", label="Gauge")
            ax.plot(g["swot_time"], g["swot_q"], marker="x", label="SWOT")
            ax.set_title(f"Reach {reach}")
            ax.set_ylabel("Discharge (input units)")
            ax.legend()
        fig.tight_layout()
        fig.savefig(outdir / "timeseries_examples.png", dpi=160)
        plt.close(fig)
