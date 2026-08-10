import polars as pl
import matplotlib.pyplot as plt

from benchmarks.config import DATASET_PATH, SIZES, TARGET_COLUMNS
from benchmarks.generator import DatasetGenerator
from benchmarks.dataframe_ops import run_pandas_ops, run_polars_ops


OUTPUT_FIGURE = "benchmark_polars_vs_pandas.png"

OPERATIONS = ["groupby_mean", "filter", "sort", "nunique", "describe"]


# ==========================================================
# Benchmark Runner
# ==========================================================

def run_benchmark(generator: DatasetGenerator):

    pandas_totals = []
    polars_totals = []
    breakdown = []

    print("=" * 70)
    print("Polars vs Pandas Benchmark")
    print("=" * 70)

    for size in SIZES:

        print(
            f"\nGenerating dataset:"
            f" {size:,} rows x {TARGET_COLUMNS} columns"
        )

        df_pd = generator.generate(
            target_rows=size,
            target_columns=TARGET_COLUMNS,
        )

        df_pl = pl.from_pandas(df_pd)

        pandas_times = run_pandas_ops(df_pd)
        polars_times = run_polars_ops(df_pl)

        pandas_total = sum(pandas_times.values())
        polars_total = sum(polars_times.values())

        pandas_totals.append(pandas_total)
        polars_totals.append(polars_total)

        breakdown.append((size, pandas_times, polars_times))

        print(f"Pandas total : {pandas_total:.3f} sec")
        print(f"Polars total : {polars_total:.3f} sec")

    return pandas_totals, polars_totals, breakdown


# ==========================================================
# Results
# ==========================================================

def print_results(pandas_totals, polars_totals, breakdown):

    print("\n")
    print("=" * 70)
    print("RESULTS (total time: groupby + filter + sort + nunique + describe)")
    print("=" * 70)

    print(
        f"{'Rows':>12}"
        f"{'Pandas':>15}"
        f"{'Polars':>15}"
        f"{'Pandas/Polars':>18}"
    )

    for size, pd_t, pl_t in zip(SIZES, pandas_totals, polars_totals):

        print(
            f"{size:>12,}"
            f"{pd_t:>15.3f}"
            f"{pl_t:>15.3f}"
            f"{pd_t / pl_t:>17.2f}x"
        )

    # Per-operation breakdown for the largest dataset size only,
    # to keep the console output readable.
    size, pandas_times, polars_times = breakdown[-1]

    print("\n")
    print("=" * 70)
    print(f"PER-OPERATION BREAKDOWN ({size:,} rows)")
    print("=" * 70)

    print(f"{'Operation':>15}{'Pandas':>15}{'Polars':>15}")

    for op in OPERATIONS:
        print(
            f"{op:>15}"
            f"{pandas_times[op]:>15.4f}"
            f"{polars_times[op]:>15.4f}"
        )


# ==========================================================
# Plot
# ==========================================================

def plot_results(pandas_totals, polars_totals):

    plt.figure(figsize=(8, 5))

    plt.plot(SIZES, pandas_totals, marker="o", label="Pandas")
    plt.plot(SIZES, polars_totals, marker="o", label="Polars")

    plt.xscale("log")

    plt.xlabel("Number of Rows")
    plt.ylabel("Total Execution Time (seconds)")
    plt.title("Polars vs Pandas Benchmark")

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

    pandas_totals, polars_totals, breakdown = run_benchmark(generator)

    print_results(pandas_totals, polars_totals, breakdown)

    plot_results(pandas_totals, polars_totals)


if __name__ == "__main__":
    main()