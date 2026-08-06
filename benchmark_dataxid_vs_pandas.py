import time
import pandas as pd
import matplotlib.pyplot as plt

from dataxid_profiling import ProfileReport, ProfileConfig


# ==========================================================
# Constants
# ==========================================================

DATASET_PATH = "sales_20k.csv"
OUTPUT_FIGURE = "benchmark_dataxid_vs_pandas.png"

SIZES = [
    100_000,
    500_000,
    1_000_000,
    2_500_000,
    5_000_000,
    10_000_000,
    20_000_000,
]


# ==========================================================
# Dataset Utilities
# ==========================================================

def load_dataset(path: str) -> pd.DataFrame:
    """Load the benchmark dataset."""

    return pd.read_csv(path)


def create_dataset(df: pd.DataFrame, size: int) -> pd.DataFrame:
    """
    Expand the original dataset to the requested number of rows.
    """

    repeat = (size // len(df)) + 1

    return (
        pd.concat([df] * repeat, ignore_index=True)
        .iloc[:size]
        .reset_index(drop=True)
    )


# ==========================================================
# Benchmark Functions
# ==========================================================

def benchmark_dataxid(df: pd.DataFrame) -> float:
    """Measure DataXID Profiling execution time."""

    config = ProfileConfig(mode="overview")

    start = time.perf_counter()

    ProfileReport(df, config=config)

    return time.perf_counter() - start


def benchmark_pandas(df: pd.DataFrame) -> float:
    """Measure equivalent Pandas analysis time."""

    start = time.perf_counter()

    # Dataset overview
    _ = df.shape
    _ = df.dtypes

    # Basic statistics
    _ = df.describe(include="all")

    # Missing values
    _ = df.isnull().sum()

    # Duplicate rows
    _ = df.duplicated().sum()

    # Unique values
    _ = df.nunique()

    # Memory usage
    _ = df.memory_usage(deep=True).sum()

    return time.perf_counter() - start


# ==========================================================
# Benchmark Runner
# ==========================================================

def run_benchmark(df_original: pd.DataFrame):

    dataxid_times = []
    pandas_times = []

    print("=" * 70)
    print("DataXID Profiling vs Pandas Benchmark")
    print("=" * 70)

    for size in SIZES:

        df = create_dataset(df_original, size)

        print(f"\nDataset Size : {len(df):,} rows")

        dataxid_time = benchmark_dataxid(df)
        pandas_time = benchmark_pandas(df)

        dataxid_times.append(dataxid_time)
        pandas_times.append(pandas_time)

        print(f"DataXID : {dataxid_time:.3f} s")
        print(f"Pandas  : {pandas_time:.3f} s")

    return dataxid_times, pandas_times


# ==========================================================
# Output Functions
# ==========================================================

def print_results(dataxid_times, pandas_times):
    """Print benchmark summary."""

    print("\n")
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)

    print(f"{'Rows':>12} {'DataXID':>12} {'Pandas':>12} {'Speedup':>12}")

    for size, dx, pd_time in zip(SIZES, dataxid_times, pandas_times):

        print(
            f"{size:>12,}"
            f"{dx:>12.3f}"
            f"{pd_time:>12.3f}"
            f"{pd_time / dx:>12.2f}x"
        )


def plot_results(dataxid_times, pandas_times):
    """Generate and save the benchmark figure."""

    plt.figure(figsize=(8, 5))

    plt.plot(
        SIZES,
        dataxid_times,
        marker="o",
        linewidth=2,
        label="DataXID Profiling",
    )

    plt.plot(
        SIZES,
        pandas_times,
        marker="o",
        linewidth=2,
        label="Pandas",
    )

    plt.xscale("log")

    plt.xlabel("Number of Rows")
    plt.ylabel("Execution Time (seconds)")
    plt.title("DataXID Profiling vs Pandas Benchmark")

    plt.grid(True)
    plt.legend()

    plt.tight_layout()

    plt.savefig(OUTPUT_FIGURE, dpi=300)

    print(f"\nFigure saved -> {OUTPUT_FIGURE}")

    plt.show()


# ==========================================================
# Main
# ==========================================================

def main():

    df = load_dataset(DATASET_PATH)

    dataxid_times, pandas_times = run_benchmark(df)

    print_results(dataxid_times, pandas_times)

    plot_results(dataxid_times, pandas_times)


if __name__ == "__main__":
    main()