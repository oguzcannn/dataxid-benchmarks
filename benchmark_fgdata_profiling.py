import time
import os
import psutil
import pandas as pd

from data_profiling import ProfileReport

process = psutil.Process(os.getpid())

# Veri
df = pd.read_csv("sales_20k.csv")

print("=" * 60)
print("FG Data Profiling Benchmark")
print("=" * 60)
print(f"Veri Boyutu : {df.shape}")

ram_before = process.memory_info().rss / 1024 / 1024

# Profil oluşturma
profile_start = time.perf_counter()

report = ProfileReport(
    df,
    title="FG Data Profiling Report",
    progress_bar=False
)

desc = report.get_description()

profile_time = time.perf_counter() - profile_start

# HTML oluşturma
os.makedirs("reports", exist_ok=True)

html_start = time.perf_counter()

report.to_file("reports/fgdata_profile.html")

html_time = time.perf_counter() - html_start

ram_after = process.memory_info().rss / 1024 / 1024

print("\n" + "=" * 60)
print("SONUÇLAR")
print("=" * 60)

print(f"Profil Oluşturma Süresi : {profile_time:.2f} sn")
print(f"HTML Oluşturma Süresi   : {html_time:.2f} sn")
print(f"Toplam Süre             : {profile_time + html_time:.2f} sn")

print(f"\nRAM Başlangıç           : {ram_before:.2f} MB")
print(f"RAM Son                 : {ram_after:.2f} MB")
print(f"RAM Artışı              : {ram_after - ram_before:.2f} MB")

print("\nProfil Özeti")
print("-" * 60)
print(desc.table)

print(f"\nKolon Sayısı            : {len(desc.variables)}")
print(f"Alert Sayısı            : {len(desc.alerts)}")
print(f"Korelasyon Sayısı       : {len(desc.correlations)}")

print("\nHTML Raporu")
print("-" * 60)
print("reports/fgdata_profile.html")