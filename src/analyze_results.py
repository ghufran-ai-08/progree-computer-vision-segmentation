
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "results" / "frame_metrics.csv"
FIGURES_DIR = ROOT / "results" / "figures"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Metrics CSV not found: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)

    required = {
        "frame_index",
        "regions_detected",
        "processing_time_ms",
        "processing_fps",
    }

    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing CSV columns: {sorted(missing)}")

    df = df.sort_values("frame_index")
    df = df.dropna(subset=list(required))

    if df.empty:
        raise ValueError("No valid frame metrics were found.")

    # 1. Processing time per frame
    plt.figure(figsize=(10, 5))
    plt.plot(df["frame_index"], df["processing_time_ms"])
    plt.xlabel("Frame index")
    plt.ylabel("Processing time (ms)")
    plt.title("Frame-by-Frame Processing Time")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "processing_time.png", dpi=160)
    plt.close()

    # 2. Detected regions per frame
    plt.figure(figsize=(10, 5))
    plt.plot(df["frame_index"], df["regions_detected"])
    plt.xlabel("Frame index")
    plt.ylabel("Detected contour regions")
    plt.title("Contour Regions Detected per Frame")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "regions_per_frame.png", dpi=160)
    plt.close()

    # 3. Processing FPS per frame
    plt.figure(figsize=(10, 5))
    plt.plot(df["frame_index"], df["processing_fps"])
    plt.xlabel("Frame index")
    plt.ylabel("Processing FPS")
    plt.title("Frame-by-Frame Processing Throughput")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "processing_fps.png", dpi=160)
    plt.close()

    # Summary statistics
    summary = pd.DataFrame([{
        "frames_processed": len(df),
        "mean_processing_time_ms": df["processing_time_ms"].mean(),
        "median_processing_time_ms": df["processing_time_ms"].median(),
        "mean_processing_fps": df["processing_fps"].mean(),
        "median_processing_fps": df["processing_fps"].median(),
        "mean_regions_detected": df["regions_detected"].mean(),
        "max_regions_detected": df["regions_detected"].max(),
        "min_regions_detected": df["regions_detected"].min(),
    }])

    summary.to_csv(ROOT / "results" / "performance_summary.csv", index=False)

    print("\nPerformance analysis completed.")
    print(summary.to_string(index=False))
    print(f"\nGraphs saved to: {FIGURES_DIR}")
    print("Summary saved to: results/performance_summary.csv")


if __name__ == "__main__":
    main()