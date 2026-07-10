"""
Script pengambilan data curah hujan & suhu udara dari NASA POWER API
untuk 27 Kabupaten/Kota di Provinsi Jawa Barat, tahun 2021-2025

NASA POWER API (Monthly endpoint):
  https://power.larc.nasa.gov/api/temporal/monthly/point
  Key YYYYMM13 = nilai rata-rata/total tahunan (bulan ke-13 = annual summary)
  
Parameter:
  - PRECTOTCORR : mm/day → kita hitung mm/tahun dari 12 bulan
  - T2M         : Temperature at 2 Meters rata-rata tahunan (°C)

Sumber data: NASA MERRA-2 reanalysis (resolusi 0.5° × 0.625°)
"""

import urllib.request
import json
import csv
import time
import os
import calendar

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# KOORDINAT PUSAT TIAP KAB/KOTA DI JAWA BARAT (Lat, Lon)
# ============================================================
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

TAHUN_LIST = [2021, 2022, 2023, 2024, 2025]

# ============================================================
# FUNGSI FETCH NASA POWER API (Monthly endpoint)
# Key "YYYYMM13" = nilai annual summary dari NASA POWER
# ============================================================
def fetch_nasa_power(lat, lon, year):
    """
    Mengambil data T2M (suhu) dan PRECTOTCORR (curah hujan)
    dari NASA POWER Monthly API, lalu hitung rata-rata/total tahunan.
    
    Returns: dict {suhu_C, curah_hujan_mm} atau None jika gagal
    """
    url = (
        f"https://power.larc.nasa.gov/api/temporal/monthly/point"
        f"?parameters=T2M,PRECTOTCORR"
        f"&community=AG"
        f"&longitude={lon}"
        f"&latitude={lat}"
        f"&start={year}"
        f"&end={year}"
        f"&format=JSON"
    )
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        
        props = data["properties"]["parameter"]
        prec_data = props["PRECTOTCORR"]
        t2m_data  = props["T2M"]
        
        # Annual key = YYYYMM13 (bulan ke-13 = annual summary NASA)
        ann_key = f"{year}13"
        
        # Suhu tahunan: gunakan key annual langsung
        t_ann = t2m_data.get(ann_key)
        if t_ann is not None and t_ann != -999:
            suhu = round(t_ann, 1)
        else:
            # Fallback: rata-rata 12 bulan
            vals = [t2m_data.get(f"{year}{str(m).zfill(2)}", -999) for m in range(1,13)]
            vals = [v for v in vals if v != -999]
            suhu = round(sum(vals)/len(vals), 1) if vals else None
        
        # Curah hujan tahunan: jumlah dari 12 bulan × hari per bulan (mm/day → mm/bulan)
        total_ch = 0.0
        for m in range(1, 13):
            key = f"{year}{str(m).zfill(2)}"
            ch_day = prec_data.get(key, -999)
            if ch_day != -999 and ch_day is not None:
                days_in_month = calendar.monthrange(year, m)[1]
                total_ch += ch_day * days_in_month
        curah_hujan = round(total_ch, 0) if total_ch > 0 else None
        
        return {"suhu_C": suhu, "curah_hujan_mm": curah_hujan}
    
    except Exception as e:
        print(f"    [ERROR] {e}")
        return None


# ============================================================
# MAIN: Fetch semua data
# ============================================================
print("=" * 65)
print("  NASA POWER Data Fetcher - Jawa Barat 2021-2025")
print("  Endpoint: Monthly (MERRA-2 Reanalysis)")
print("=" * 65)
print(f"  Jumlah kab/kota : {len(KOORDINAT)}")
print(f"  Tahun           : {TAHUN_LIST}")
print(f"  Total permintaan: {len(KOORDINAT) * len(TAHUN_LIST)} API calls")
print("=" * 65)

hasil = {}  # {kab_kota: {tahun: {suhu, curah_hujan}}}

for kk, (lat, lon) in KOORDINAT.items():
    hasil[kk] = {}
    for tahun in TAHUN_LIST:
        print(f"  {kk} {tahun}...", end=" ", flush=True)
        data = fetch_nasa_power(lat, lon, tahun)
        if data and data["suhu_C"] is not None:
            hasil[kk][tahun] = data
            print(f"T={data['suhu_C']}C  CH={data['curah_hujan_mm']}mm")
        else:
            hasil[kk][tahun] = {"suhu_C": None, "curah_hujan_mm": None}
            print("GAGAL")
        time.sleep(0.4)  # hindari rate limiting

# ============================================================
# SIMPAN HASIL KE CSV
# ============================================================
output_iklim = os.path.join(OUTPUT_DIR, "data_iklim_nasapower_jabar.csv")
with open(output_iklim, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["Kab/Kota", "Lat", "Lon", "Tahun", "Suhu_Udara_C", "Curah_Hujan_mm"])
    for kk, (lat, lon) in KOORDINAT.items():
        for tahun in TAHUN_LIST:
            d = hasil[kk][tahun]
            writer.writerow([kk, lat, lon, tahun, d.get("suhu_C",""), d.get("curah_hujan_mm","")])

print()
print(f"[OK] Data iklim NASA POWER disimpan: {output_iklim}")

# ============================================================
# BANDINGKAN DENGAN ESTIMASI SEBELUMNYA (tahun 2021)
# ============================================================
estimasi_suhu_2021 = {
    "Bogor": 25.6, "Sukabumi": 25.3, "Cianjur": 24.8,
    "Bandung": 23.2, "Garut": 23.5, "Tasikmalaya": 24.1,
    "Ciamis": 24.6, "Kuningan": 24.3, "Sumedang": 24.8,
    "Cirebon": 27.8, "Majalengka": 26.7, "Indramayu": 28.3,
    "Subang": 27.1, "Karawang": 27.6, "Bekasi": 27.9,
    "Purwakarta": 26.4, "Bandung Barat": 23.7, "Pangandaran": 26.8,
    "Kota Bogor": 25.9, "Kota Sukabumi": 24.7, "Kota Bandung": 23.5,
    "Kota Cirebon": 27.6, "Kota Bekasi": 27.8, "Kota Depok": 27.2,
    "Kota Cimahi": 23.8, "Kota Tasikmalaya": 24.3, "Kota Banjar": 24.9,
}
estimasi_ch_2021 = {
    "Bogor": 3765, "Sukabumi": 2890, "Cianjur": 2650,
    "Bandung": 2076, "Garut": 2347, "Tasikmalaya": 2456,
    "Ciamis": 2187, "Kuningan": 2034, "Sumedang": 1876,
    "Cirebon": 1523, "Majalengka": 1654, "Indramayu": 1287,
    "Subang": 1812, "Karawang": 1689, "Bekasi": 1934,
    "Purwakarta": 2103, "Bandung Barat": 2245, "Pangandaran": 2534,
    "Kota Bogor": 4003, "Kota Sukabumi": 2761, "Kota Bandung": 2125,
    "Kota Cirebon": 1456, "Kota Bekasi": 1876, "Kota Depok": 2345,
    "Kota Cimahi": 2234, "Kota Tasikmalaya": 2398, "Kota Banjar": 2098,
}

print()
print("=" * 95)
print("  PERBANDINGAN DATA 2021: ESTIMASI vs NASA POWER (MERRA-2)")
print("=" * 95)
print(f"  {'Kab/Kota':<22} {'T_Est':>6} {'T_NASA':>7} {'dT':>6} | {'CH_Est':>7} {'CH_NASA':>8} {'dCH':>8}")
print("-" * 95)

total_dt = 0; total_dch = 0; n = 0
for kk in KOORDINAT:
    d = hasil[kk].get(2021, {})
    t_n = d.get("suhu_C"); ch_n = d.get("curah_hujan_mm")
    t_e = estimasi_suhu_2021.get(kk); ch_e = estimasi_ch_2021.get(kk)
    if t_n and ch_n:
        dt = round(t_n - t_e, 1); dch = round(ch_n - ch_e, 0)
        total_dt += abs(dt); total_dch += abs(dch); n += 1
        flag_t  = " !" if abs(dt)  > 1.5  else ""
        flag_ch = " !" if abs(dch) > 500  else ""
        print(f"  {kk:<22} {t_e:>6} {t_n:>7} {dt:>+6.1f}{flag_t} | {ch_e:>7} {ch_n:>8.0f} {dch:>+8.0f}{flag_ch}")
    else:
        print(f"  {kk:<22} {t_e:>6} {'N/A':>7} {'N/A':>7} | {ch_e:>7} {'N/A':>8} {'N/A':>9}")

if n:
    print("-" * 95)
    print(f"  {'Mean |Delta|':<22} {'':<14} {total_dt/n:>+6.1f}   | {'':<16} {total_dch/n:>+8.0f}")
    print(f"\n  ! = selisih besar (|dT|>1.5 C atau |dCH|>500 mm)")
