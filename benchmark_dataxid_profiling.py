import os

import pandas as pd

from benchmarks.config import DATASET_PATH, REPORTS_DIR, get_dataxid_overview_config
from benchmarks.dataxid import profile
from benchmarks.utils import get_ram_usage_mb


df = pd.read_csv(DATASET_PATH)

os.makedirs(REPORTS_DIR, exist_ok=True)

print("=" * 60)
print("DataXID Profiling Benchmark")
print("=" * 60)
print(f"Veri Boyutu : {df.shape}")

ram_before = get_ram_usage_mb()

config = get_dataxid_overview_config()

report, elapsed = profile(
    df,
    config,
    f"{REPORTS_DIR}/dataxid_profile.html",
)

ram_after = get_ram_usage_mb()

report_dict = report.to_dict()

overview = report_dict["overview"]
columns = report_dict["columns"]
alerts = report_dict["alerts"]
correlations = report_dict["correlations"]
interactions = report_dict["interactions"]

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
print(overview)

print()

print(f"Kolon Sayisi             : {len(columns)}")
print(f"Alert Sayisi             : {len(alerts)}")
print(f"Korelasyon Sayisi        : {len(correlations) if correlations is not None else 0}")
print(f"Interaction Sayisi       : {len(interactions) if interactions is not None else 0}")

print()

print("HTML Raporu")
print("-" * 60)
print(f"{REPORTS_DIR}/dataxid_profile.html")