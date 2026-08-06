from dataxid_profiling import ProfileConfig


# ==========================================================
# Dataset settings
# ==========================================================

DATASET_PATH = "sales_20k.csv"

REPORTS_DIR = "reports"


# ==========================================================
# Scaling benchmark settings
# ==========================================================

OUTPUT_FIGURE = "benchmark_dataxid_vs_fgdata.png"

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

TARGET_COLUMNS = 10

FG_CONFIG_PATH = "benchmarks/fgdata_config.yaml"


# ==========================================================
# DataXID configs
# ==========================================================

def get_dataxid_overview_config() -> ProfileConfig:
    """Config used for the scaling benchmark (fast, no correlations)."""

    return ProfileConfig(
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


def get_dataxid_complete_config() -> ProfileConfig:
    """Config used for the single-run full profiling script."""

    return ProfileConfig(mode="complete")