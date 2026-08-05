import os
import time
import psutil
import pandas as pd

from dataxid_profiling import ProfileReport, ProfileConfig

process = psutil.Process(os.getpid())

df = pd.read_csv("sales_20k.csv")

os.makedirs("reports", exist_ok=True)

print("=" * 60)
print("DataXID Profiling Benchmark")
print("=" * 60)
print(f"Veri Boyutu : {df.shape}")

ram_before = process.memory_info().rss / 1024 / 1024

config = ProfileConfig(
    mode="complete"
)

# Profil oluşturma
profile_start = time.perf_counter()

report = ProfileReport(df, config=config)

profile_time = time.perf_counter() - profile_start

# HTML oluşturma
html_start = time.perf_counter()

report.to_html("reports/dataxid_profile.html")

html_time = time.perf_counter() - html_start

ram_after = process.memory_info().rss / 1024 / 1024

report_dict = report.to_dict()

overview = report_dict["overview"]
columns = report_dict["columns"]
alerts = report_dict["alerts"]
correlations = report_dict["correlations"]
interactions = report_dict["interactions"]

print("\n" + "=" * 60)
print("SONUÇLAR")
print("=" * 60)

print(f"Profil Oluşturma Süresi : {profile_time:.2f} sn")
print(f"HTML Oluşturma Süresi   : {html_time:.2f} sn")
print(f"Toplam Süre             : {profile_time + html_time:.2f} sn")

print()

print(f"RAM Başlangıç           : {ram_before:.2f} MB")
print(f"RAM Son                 : {ram_after:.2f} MB")
print(f"RAM Artışı              : {ram_after - ram_before:.2f} MB")

print()

print("Profil Özeti")
print("-" * 60)
print(overview)

print()

print(f"Kolon Sayısı            : {len(columns)}")
print(f"Alert Sayısı            : {len(alerts)}")
print(f"Korelasyon Sayısı       : {len(correlations)}")
print(f"Interaction Sayısı      : {len(interactions)}")

print()

print("HTML Raporu")
print("-" * 60)
print("reports/dataxid_profile.html")