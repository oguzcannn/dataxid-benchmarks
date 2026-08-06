import os

import pandas as pd

from benchmarks.config import DATASET_PATH, REPORTS_DIR, FG_CONFIG_PATH
from benchmarks.fgdata import profile
from benchmarks.utils import get_ram_usage_mb


df = pd.read_csv(DATASET_PATH)

os.makedirs(REPORTS_DIR, exist_ok=True)

print("=" * 60)
print("FG Data Profiling Benchmark")
print("=" * 60)
print(f"Veri Boyutu : {df.shape}")

ram_before = get_ram_usage_mb()

report, elapsed = profile(
    df,
    f"{REPORTS_DIR}/fgdata_profile.html",
    config_file=FG_CONFIG_PATH,
    title="FG Data Profiling Report",
    progress_bar=False,
)

ram_after = get_ram_usage_mb()

desc = report.get_description()

print("\n" + "=" * 60)
print("SONUCLAR")
print("=" * 60)

print(f"Toplam Sure              : {elapsed:.2f} sn")

print()

print(f"RAM Baslangic            : {ram_before:.2f} MB")
print(f"RAM Son                  : {ram_after:.2f} MB")
print(f"RAM Artisi               : {ram_after - ram_before:.2f} MB")

print()

print("Profil Ozeti")
print("-" * 60)
print(desc.table)

print()

print(f"Kolon Sayisi             : {len(desc.variables)}")
print(f"Alert Sayisi             : {len(desc.alerts)}")
print(f"Korelasyon Sayisi        : {len(desc.correlations)}")

print()

print("HTML Raporu")
print("-" * 60)
print(f"{REPORTS_DIR}/fgdata_profile.html")