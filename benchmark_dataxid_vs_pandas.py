import os

import matplotlib.pyplot as plt

from benchmarks.config import (
    DATASET_PATH,
    REPORTS_DIR,
    OUTPUT_FIGURE,
    SIZES,
    TARGET_COLUMNS,
    FG_CONFIG_PATH,
    get_dataxid_overview_config,
)
from benchmarks.generator import DatasetGenerator
from benchmarks.dataxid import profile as profile_dataxid
from benchmarks.fgdata import profile as profile_fgdata


# ==========================================================
# Benchmark Runner
# ==========================================================

def run_benchmark(generator: DatasetGenerator):

    dataxid_times = []
    fgdata_times = []

    os.makedirs(REPORTS_DIR, exist_ok=True)

    print("=" * 70)
    print("DataXID vs FG Data Profiling Benchmark")
    print("=" * 70)

    for size in SIZES:

        print(
            f"\nGenerating dataset:"
            f" {size:,} rows x {TARGET_COLUMNS} columns"
        )

        df = generator.generate(
            target_rows=size,
            target_columns=TARGET_COLUMNS,
        )

        print(f"Actual shape: {df.shape}")

        dataxid_html = os.path.join(REPORTS_DIR, f"dataxid_{size}.html")
        fgdata_html = os.path.join(REPORTS_DIR, f"fgdata_{size}.html")

        print("Running DataXID...")

        dataxid_config = get_dataxid_overview_config()

        _, dataxid_time = profile_dataxid(
            df,
            dataxid_config,
            dataxid_html,
        )

        print("Running FG Data...")

        _, fgdata_time = profile_fgdata(
            df,
            fgdata_html,
            config_file=FG_CONFIG_PATH,
        )

        dataxid_times.append(dataxid_time)
        fgdata_times.append(fgdata_time)

        print(f"DataXID : {dataxid_time:.3f} sec")
        print(f"FG Data : {fgdata_time:.3f} sec")

    return dataxid_times, fgdata_times


# ==========================================================
# Results
# ==========================================================

def print_results(dataxid_times, fgdata_times):

    print("\n")
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)

    print(
        f"{'Rows':>12}"
        f"{'DataXID':>15}"
        f"{'FG Data':>15}"
        f"{'FG/DataXID':>15}"
    )

    for size, dx, fg in zip(SIZES, dataxid_times, fgdata_times):

        print(
            f"{size:>12,}"
            f"{dx:>15.3f}"
            f"{fg:>15.3f}"
            f"{fg/dx:>15.2f}x"
        )


# ==========================================================
# Plot
# ==========================================================

def plot_results(dataxid_times, fgdata_times):

    plt.figure(figsize=(8, 5))

    plt.plot(SIZES, dataxid_times, marker="o", label="DataXID")
    plt.plot(SIZES, fgdata_times, marker="o", label="FG Data")

    plt.xscale("log")

    plt.xlabel("Number of Rows")
    plt.ylabel("Execution Time (seconds)")
    plt.title("DataXID vs FG Data Profiling Benchmark")

    plt.grid(True)
    plt.legend()

    plt.tight_layout()

    plt.savefig(OUTPUT_FIGURE, dpi=300)

    print(f"\nFigure saved -> {OUTPUT_FIGURE}")


# ==========================================================
# Main
# ==========================================================

def main():

    generator = DatasetGenerator(DATASET_PATH, seed=42)

    dataxid_times, fgdata_times = run_benchmark(generator)

    print_results(dataxid_times, fgdata_times)

    plot_results(dataxid_times, fgdata_times)


if __name__ == "__main__":
    main()