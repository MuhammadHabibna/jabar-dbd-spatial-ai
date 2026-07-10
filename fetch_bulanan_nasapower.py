"""
Ambil data BULANAN NYATA dari NASA POWER API
untuk 27 Kab/Kota Jawa Barat, Januari 2021 - Desember 2025

Output: data_iklim_bulanan_nasapower_2021_2025.csv
  - 27 kab/kota x 60 bulan = 1.620 baris
  - Curah_Hujan_mm (real, MERRA-2)
  - Suhu_C (real, MERRA-2)
"""

import urllib.request, json, csv, time, os, calendar
import pandas as pd, numpy as np

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

KOORDINAT = {
    "Bogor":             (-6.595,  106.816),
    "Sukabumi":          (-6.918,  106.929),
    "Cianjur":           (-6.822,  107.139),
    "Bandung":           (-7.021,  107.570),
    "Garut":             (-7.212,  107.906),
    "Tasikmalaya":       (-7.353,  108.224),
    "Ciamis":            (-7.329,  108.351),
    "Kuningan":          (-6.975,  108.480),
    "Cirebon":           (-6.761,  108.476),
    "Majalengka":        (-6.836,  108.228),
    "Sumedang":          (-6.855,  107.920),
    "Indramayu":         (-6.327,  108.324),
    "Subang":            (-6.571,  107.762),
    "Purwakarta":        (-6.556,  107.443),
    "Karawang":          (-6.321,  107.339),
    "Bekasi":            (-6.374,  107.130),
    "Bandung Barat":     (-6.917,  107.425),
    "Pangandaran":       (-7.689,  108.650),
    "Kota Bogor":        (-6.597,  106.806),
    "Kota Sukabumi":     (-6.918,  106.927),
    "Kota Bandung":      (-6.914,  107.609),
    "Kota Cirebon":      (-6.706,  108.557),
    "Kota Bekasi":       (-6.238,  106.975),
    "Kota Depok":        (-6.401,  106.819),
    "Kota Cimahi":       (-6.884,  107.543),
    "Kota Tasikmalaya":  (-7.327,  108.219),
    "Kota Banjar":       (-7.365,  108.538),
}

def fetch_monthly_nasa(lat, lon, year):
    """Ambil data bulanan (12 baris) T2M dan PRECTOTCORR dari NASA POWER."""
    url = (
        f"https://power.larc.nasa.gov/api/temporal/monthly/point"
        f"?parameters=T2M,PRECTOTCORR&community=AG"
        f"&longitude={lon}&latitude={lat}&start={year}&end={year}&format=JSON"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode())
        prec = data["properties"]["parameter"]["PRECTOTCORR"]
        t2m  = data["properties"]["parameter"]["T2M"]
        monthly = []
        for m in range(1, 13):
            key = f"{year}{str(m).zfill(2)}"
            ch_day = prec.get(key, -999)
            t_val  = t2m.get(key, -999)
            days   = calendar.monthrange(year, m)[1]
            monthly.append({
                "Tahun"          : year,
                "Bulan"          : m,
                "CH_harian_mm"   : ch_day if ch_day != -999 else None,
                "CH_bulanan_mm"  : round(ch_day * days, 1) if ch_day != -999 else None,
                "Suhu_C"         : round(t_val, 2) if t_val != -999 else None,
            })
        return monthly
    except Exception as e:
        print(f"    ERROR: {e}")
        return None

# ── FETCH ────────────────────────────────────────────────────────────────────
print("=" * 65)
print("  NASA POWER — Data BULANAN Nyata 2021-2025")
print(f"  27 kab/kota x 5 tahun = 135 API calls (masing-masing 12 bln)")
print("=" * 65)

rows = []
for kk, (lat, lon) in KOORDINAT.items():
    for year in [2021, 2022, 2023, 2024, 2025]:
        print(f"  {kk} {year}...", end=" ", flush=True)
        monthly = fetch_monthly_nasa(lat, lon, year)
        if monthly:
            ok = sum(1 for m in monthly if m["CH_bulanan_mm"] is not None)
            print(f"OK ({ok}/12 bulan)")
            for m in monthly:
                rows.append({
                    "Kab_Kota"       : kk,
                    "Lat"            : lat,
                    "Lon"            : lon,
                    "Tahun"          : m["Tahun"],
                    "Bulan"          : m["Bulan"],
                    "Periode"        : f"{m['Tahun']}-{str(m['Bulan']).zfill(2)}",
                    "Curah_Hujan_mm" : m["CH_bulanan_mm"],
                    "Suhu_C"         : m["Suhu_C"],
                })
        else:
            print("GAGAL")
            for m_num in range(1, 13):
                rows.append({"Kab_Kota":kk,"Lat":lat,"Lon":lon,
                             "Tahun":year,"Bulan":m_num,
                             "Periode":f"{year}-{str(m_num).zfill(2)}",
                             "Curah_Hujan_mm":None,"Suhu_C":None})
        time.sleep(0.35)

df = pd.DataFrame(rows)

# ── SIMPAN CSV ───────────────────────────────────────────────────────────────
out = os.path.join(OUTPUT_DIR, "data_iklim_bulanan_nasapower_2021_2025.csv")
df.to_csv(out, index=False, encoding="utf-8-sig")

total   = len(df)
valid   = df["Curah_Hujan_mm"].notna().sum()
print(f"\n[OK] Tersimpan: {out}")
print(f"     Total baris : {total:,}  (target: 1.620)")
print(f"     Data valid  : {valid:,}  ({valid/total*100:.1f}%)")

# ── VERIFIKASI: Tampilkan contoh Kota Bandung ──────────────────────────────
print("\nContoh data Kota Bandung 2021-2022:")
sample = df[(df["Kab_Kota"]=="Kota Bandung") & (df["Tahun"].isin([2021,2022]))]
print(sample[["Periode","Curah_Hujan_mm","Suhu_C"]].to_string(index=False))

# ── STATISTIK FENOMENA IKLIM ─────────────────────────────────────────────────
print("\nRata-rata CH Tahunan (seluruh Jawa Barat):")
yr_agg = df.groupby("Tahun")["Curah_Hujan_mm"].mean().round(1)
for yr, val in yr_agg.items():
    fenomena = {2021:"(La Nina)",2022:"(La Nina)",2023:"(El Nino)",
                2024:"(Pemulihan)",2025:"(Normal)"}.get(yr,"")
    bar = "#"*int(val/100)
    print(f"  {yr} {fenomena:<13}: {val:>7.1f} mm/bln  {bar}")
