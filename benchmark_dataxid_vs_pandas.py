import os
import time
import pandas as pd
import matplotlib.pyplot as plt

from dataxid_profiling import ProfileReport, ProfileConfig

from data_profiling import ProfileReport as FGProfileReport


from dataset_generator import DatasetGenerator


# ==========================================================
# Constants
# ==========================================================

DATASET_PATH = "sales_20k.csv"

OUTPUT_FIGURE = "benchmark_dataxid_vs_fgdata.png"

REPORTS_DIR = "reports"


# Change benchmark sizes here
SIZES = [
    100_000,
    250_000,
    500_000,
    1_000_000,
    2_500_000,
    5_000_000,
    10_000_000,
    20_000_000,
]


# Change column count here
TARGET_COLUMNS = 10


FG_CONFIG_PATH = "fgdata_config.yaml"


# ==========================================================
# Dataset Loading
# ==========================================================

def load_dataset(path: str) -> pd.DataFrame:
    """Load original dataset."""

    return pd.read_csv(path)



def _export_html(report, path: str) -> None:
    """
    Save a profiling report as HTML.
    """

    if hasattr(report, "to_file"):

        report.to_file(path)

    elif hasattr(report, "to_html"):

        html = report.to_html()

        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

    else:

        raise AttributeError(
            "Report object has no to_file/to_html method, "
            "check the library's export API."
        )



# ==========================================================
# Benchmark Functions
# ==========================================================

def benchmark_dataxid(df: pd.DataFrame, output_path: str) -> float:
    """Measure DataXID profiling execution time."""

    config = ProfileConfig(
        mode="overview",

        # Type inference
        text_unique_ratio=0.5,

        # Alert thresholds
        missing_threshold=0.05,
        cardinality_threshold=0.95,
        correlation_threshold=0.8,
        constant_threshold=1,
        zero_threshold=0.05,
        skewness_threshold=2.0,
        imbalance_threshold=0.9,
        duplicate_threshold=0.0,
        uniform_pvalue_threshold=0.05,

        # Interaction settings
        interaction_sample_size=100_000,
        interaction_sample_seed=42,
        interaction_cardinality_limit=50,

        # Display settings
        n_top_values=5,
        histogram_bins=50,
    )


    start = time.perf_counter()

    report = ProfileReport(
        df,
        config=config
    )

    # Export triggers the actual profiling computation
    # (report generation is lazy otherwise)
    _export_html(report, output_path)

    return time.perf_counter() - start



def benchmark_fgdata(df: pd.DataFrame, output_path: str) -> float:
    """Measure FG Data Profiling execution time."""

    start = time.perf_counter()


    report = FGProfileReport(
        df,
        config_file=FG_CONFIG_PATH
    )

    # Export triggers the actual profiling computation
    # (report generation is lazy otherwise)
    _export_html(report, output_path)


    return time.perf_counter() - start



# ==========================================================
# Benchmark Runner
# ==========================================================

def run_benchmark(
    generator: DatasetGenerator
):

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


        print(
            f"Actual shape: {df.shape}"
        )


        dataxid_html = os.path.join(
            REPORTS_DIR, f"dataxid_{size}.html"
        )

        fgdata_html = os.path.join(
            REPORTS_DIR, f"fgdata_{size}.html"
        )


        print("Running DataXID...")

        dataxid_time = benchmark_dataxid(df, dataxid_html)


        print("Running FG Data...")

        fgdata_time = benchmark_fgdata(df, fgdata_html)



        dataxid_times.append(dataxid_time)

        fgdata_times.append(fgdata_time)



        print(
            f"DataXID : {dataxid_time:.3f} sec"
        )

        print(
            f"FG Data : {fgdata_time:.3f} sec"
        )


    return dataxid_times, fgdata_times



# ==========================================================
# Results
# ==========================================================

def print_results(
    dataxid_times,
    fgdata_times
):

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


    for size, dx, fg in zip(
        SIZES,
        dataxid_times,
        fgdata_times
    ):

        print(
            f"{size:>12,}"
            f"{dx:>15.3f}"
            f"{fg:>15.3f}"
            f"{fg/dx:>15.2f}x"
        )



# ==========================================================
# Plot
# ==========================================================

def plot_results(
    dataxid_times,
    fgdata_times
):

    plt.figure(figsize=(8,5))


    plt.plot(
        SIZES,
        dataxid_times,
        marker="o",
        label="DataXID"
    )


    plt.plot(
        SIZES,
        fgdata_times,
        marker="o",
        label="FG Data"
    )


    plt.xscale("log")


    plt.xlabel(
        "Number of Rows"
    )

    plt.ylabel(
        "Execution Time (seconds)"
    )


    plt.title(
        "DataXID vs FG Data Profiling Benchmark"
    )


    plt.grid(True)

    plt.legend()


    plt.tight_layout()


    plt.savefig(
        OUTPUT_FIGURE,
        dpi=300
    )


    print(
        f"\nFigure saved -> {OUTPUT_FIGURE}"
    )



# ==========================================================
# Main
# ==========================================================

def main():

    generator = DatasetGenerator(
        DATASET_PATH,
        seed=42
    )


    dataxid_times, fgdata_times = run_benchmark(
        generator
    )


    print_results(
        dataxid_times,
        fgdata_times
    )


    plot_results(
        dataxid_times,
        fgdata_times
    )



if __name__ == "__main__":
    main()