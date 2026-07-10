import csv
import re
import os

BASE_DIR = r"d:\Draft Perlombaan UNESA\ESSAI - UMEDS"
DASHBOARD_DATA_PATH = os.path.join(BASE_DIR, "dashboard-ews-dbd", "lib", "data.ts")
CSV_KLASTER_PATH = os.path.join(BASE_DIR, "output_EWS_DBD", "klaster_DBD_Des2025.csv")

def update_data_ts():
    # 1. Read CSV
    kab_kota_list = []
    with open(CSV_KLASTER_PATH, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            zona_label = row['Zona_Label'].lower()
            if 'merah' in zona_label:
                zona = 'merah'
                zona_color = "#E74C3C"
                prioritas = "TINGGI"
                zl = "Zona Merah"
            elif 'kuning' in zona_label:
                zona = 'kuning'
                zona_color = "#F39C12"
                prioritas = "SEDANG"
                zl = "Zona Kuning"
            else:
                zona = 'hijau'
                zona_color = "#27AE60"
                prioritas = "RENDAH"
                zl = "Zona Hijau"
            
            kab_kota_list.append(f"""  {{ id: {i+1}, nama: "{row['Kab_Kota']}", lat: {row['Latitude']}, lon: {row['Longitude']}, zona: "{zona}", zona_label: "{zl}", zona_color: "{zona_color}", ir_dbd: {float(row['IR_DBD_Aktual']):.2f}, ir_prediksi: {float(row['IR_DBD_Prediksi_Jan2026']):.2f}, kepadatan: {float(row['Kepadatan_jiwa_per_km2']):.0f}, sanitasi: {float(row['Sanitasi_Layak_Pct']):.2f}, curah_hujan: {float(row['Curah_Hujan_mm']):.0f}, ch_lag1: {float(row['CH_Lag1_mm']):.0f}, suhu: {float(row['Suhu_C']):.1f}, prioritas: "{prioritas}" }}""")

    new_kab_kota_str = "export const kabKotaData: KabKotaData[] = [\n" + ",\n".join(kab_kota_list) + "\n];"
    
    # 2. Update data.ts
    with open(DASHBOARD_DATA_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
        
    content = re.sub(r'export const kabKotaData: KabKotaData\[\] = \[.*?\];', new_kab_kota_str, content, flags=re.DOTALL)
    
    with open(DASHBOARD_DATA_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Updated lib/data.ts with values from klaster_DBD_Des2025.csv!")

if __name__ == "__main__":
    update_data_ts()
