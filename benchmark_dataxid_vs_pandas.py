import time
import pandas as pd
import matplotlib.pyplot as plt

from dataxid_profiling import ProfileReport, ProfileConfig


# ==========================================================
# DataXID Profiling Benchmark
# ==========================================================
def benchmark_dataxid(df):
    config = ProfileConfig(mode="overview")

    start = time.perf_counter()

    ProfileReport(df, config=config)

    return time.perf_counter() - start


# ==========================================================
# Pandas Benchmark
# ==========================================================
def benchmark_pandas(df):

    start = time.perf_counter()

    # Dataset bilgileri
    _ = df.shape
    _ = df.dtypes

    # Temel istatistikler
    _ = df.describe(include="all")

    # Eksik değerler
    _ = df.isnull().sum()

    # Duplicate kayıtlar
    _ = df.duplicated().sum()

    # Unique değerler
    _ = df.nunique()

    # Bellek kullanımı
    _ = df.memory_usage(deep=True).sum()

    return time.perf_counter() - start


# ==========================================================
# MAIN
# ==========================================================

DATASET = "sales_20k.csv"

df_original = pd.read_csv(DATASET)

sizes = [
    100_000,
    500_000,
    1_000_000,
    2_500_000,
    5_000_000,
    10_000_000,
    20_000_000,
]

dataxid_times = []
pandas_times = []

print("=" * 70)
print("DataXID Profiling vs Pandas Benchmark")
print("=" * 70)

for size in sizes:

    # Veri setini büyüt
    repeat = (size // len(df_original)) + 1

    df = (
        pd.concat([df_original] * repeat, ignore_index=True)
        .iloc[:size]
        .reset_index(drop=True)
    )

    print(f"\nVeri Boyutu : {len(df):,} satır")

    t_dataxid = benchmark_dataxid(df)
    t_pandas = benchmark_pandas(df)

    dataxid_times.append(t_dataxid)
    pandas_times.append(t_pandas)

    print(f"DataXID : {t_dataxid:.3f} sn")
    print(f"Pandas  : {t_pandas:.3f} sn")


print("\n")
print("=" * 70)
print("SONUÇLAR")
print("=" * 70)

print(f"{'Rows':>12} {'DataXID':>12} {'Pandas':>12} {'Speedup':>12}")

for size, dx, pd_time in zip(sizes, dataxid_times, pandas_times):

    print(
        f"{size:>12,}"
        f"{dx:>12.3f}"
        f"{pd_time:>12.3f}"
        f"{pd_time/dx:>12.2f}x"
    )


# ==========================================================
# GRAFİK
# ==========================================================

plt.figure(figsize=(8, 5))

plt.plot(
    sizes,
    dataxid_times,
    marker="o",
    linewidth=2,
    label="DataXID Profiling",
)

plt.plot(
    sizes,
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

plt.savefig("benchmark_dataxid_vs_pandas.png", dpi=300)

print("\nGrafik kaydedildi -> benchmark_dataxid_vs_pandas.png")

plt.show()