"""
Script untuk update dataset_DBD_Jawa_Barat_2021_2025.csv
dengan data curah hujan & suhu dari NASA POWER (MERRA-2 Reanalysis)

Mengganti kolom Curah_Hujan_mm dan Suhu_Udara_Celcius dengan data valid
dari file data_iklim_nasapower_jabar.csv
"""

import csv
import os

DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# 1. Baca data NASA POWER
# ============================================================
nasa_data = {}  # key: (kab_kota, tahun)
nasapower_file = os.path.join(DIR, "data_iklim_nasapower_jabar.csv")

with open(nasapower_file, encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = (row["Kab/Kota"], int(row["Tahun"]))
        nasa_data[key] = {
            "suhu": row["Suhu_Udara_C"],
            "ch":   row["Curah_Hujan_mm"],
        }

print(f"[OK] Data NASA POWER dibaca: {len(nasa_data)} entri")

# ============================================================
# 2. Baca dataset utama & update kolom iklim
# ============================================================
input_file  = os.path.join(DIR, "dataset_DBD_Jawa_Barat_2021_2025.csv")
output_file = os.path.join(DIR, "dataset_DBD_Jawa_Barat_2021_2025_NASAPOWER.csv")

rows_in = []
with open(input_file, encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        rows_in.append(dict(row))

updated = 0
not_found = []
for row in rows_in:
    kk    = row["Kab/Kota"]
    tahun = int(row["Tahun"])
    key   = (kk, tahun)
    if key in nasa_data:
        row["Curah_Hujan_mm"]    = nasa_data[key]["ch"]
        row["Suhu_Udara_Celcius"] = nasa_data[key]["suhu"]
        updated += 1
    else:
        not_found.append(key)

# ============================================================
# 3. Simpan kembali
# ============================================================
with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows_in)

print(f"[OK] Dataset diperbarui: {updated} baris")
if not_found:
    print(f"[WARN] Tidak ditemukan di NASA POWER: {not_found}")

# ============================================================
# 4. Preview hasil akhir
# ============================================================
print()
print("=" * 100)
print("  PREVIEW DATASET FINAL (10 baris pertama)")
print("=" * 100)
print(f"  {'Tahun':>5}  {'Kab/Kota':<22} {'Kepadatan':>10} {'Sanitasi':>9} {'CH_mm':>7} {'Suhu_C':>7} {'DBD/100rb':>10}")
print("-" * 100)

count = 0
with open(output_file, encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  {row['Tahun']:>5}  {row['Kab/Kota']:<22} "
              f"{row['Kepadatan_Penduduk_jiwa_per_km2']:>10} "
              f"{row['Persen_Sanitasi_Layak']:>9} "
              f"{row['Curah_Hujan_mm']:>7} "
              f"{row['Suhu_Udara_Celcius']:>7} "
              f"{row['Angka_Kesakitan_DBD_per_100rb']:>10}")
        count += 1
        if count >= 10:
            break

print("  ...")
print()
print(f"  Total baris: 135 (5 tahun x 27 kab/kota)")
print(f"  File: {output_file}")
