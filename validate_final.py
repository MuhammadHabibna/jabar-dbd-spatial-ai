import re
import csv
import json
import os

BASE_DIR = r"d:\Draft Perlombaan UNESA\ESSAI - UMEDS"
DASHBOARD_DATA_PATH = os.path.join(BASE_DIR, "dashboard-ews-dbd", "lib", "data.ts")
CSV_KLASTER_PATH = os.path.join(BASE_DIR, "output_EWS_DBD", "klaster_DBD_Des2025.csv")
CSV_PROJ_PATH = os.path.join(BASE_DIR, "output_EWS_DBD", "proyeksi_IR_DBD_Jan_Jun_2026.csv")

def parse_ts_data():
    with open(DASHBOARD_DATA_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ekstrak blok kabKotaData
    match = re.search(r'export const kabKotaData: KabKotaData\[\] = \[(.*?)\];', content, re.DOTALL)
    if not match:
        print("Gagal menemukan kabKotaData di data.ts")
        return []
    
    data_str = match.group(1)
    
    # Parsing manual dengan regex
    pattern = r'\{.*?nama:\s*"([^"]+)",.*?zona:\s*"([^"]+)",.*?ir_dbd:\s*([\d.]+).*?\}'
    items = re.findall(pattern, data_str)
    
    parsed = []
    for nama, zona, ir_dbd in items:
        parsed.append({
            'nama': nama,
            'zona': zona,
            'ir_dbd': float(ir_dbd)
        })
    return parsed

def load_csv_klaster():
    parsed = []
    with open(CSV_KLASTER_PATH, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            zona_label = row['Zona_Label'].lower()
            if 'merah' in zona_label:
                zona = 'merah'
            elif 'kuning' in zona_label:
                zona = 'kuning'
            else:
                zona = 'hijau'
                
            parsed.append({
                'nama': row['Kab_Kota'],
                'zona': zona,
                'ir_dbd': float(row['IR_DBD_Aktual'])
            })
    return parsed

def run_validation():
    print("="*60)
    print("VALIDASI AKHIR: DASHBOARD vs DATA SUMBER (EWS_DBD)")
    print("="*60)
    
    ts_data = parse_ts_data()
    csv_data = load_csv_klaster()
    
    ts_dict = {d['nama']: d for d in ts_data}
    csv_dict = {d['nama']: d for d in csv_data}
    
    issues = []
    
    # 1. Cek jumlah data
    print(f"Jumlah Kab/Kota di Dashboard : {len(ts_data)}")
    print(f"Jumlah Kab/Kota di CSV       : {len(csv_data)}")
    if len(ts_data) != len(csv_data):
        issues.append("Mismatch jumlah data!")
        
    # 2. Cek kecocokan per wilayah
    for nama, csv_row in csv_dict.items():
        if nama not in ts_dict:
            issues.append(f"Wilayah {nama} ada di CSV tapi tidak ada di Dashboard!")
            continue
            
        ts_row = ts_dict[nama]
        
        # Cek Zona
        if csv_row['zona'] != ts_row['zona']:
            issues.append(f"[{nama}] Mismatch Zona! CSV={csv_row['zona']}, Dashboard={ts_row['zona']}")
            
        # Cek IR DBD (Toleransi pembulatan 1 desimal)
        if abs(csv_row['ir_dbd'] - ts_row['ir_dbd']) > 0.2:
            issues.append(f"[{nama}] Mismatch IR_DBD! CSV={csv_row['ir_dbd']:.1f}, Dashboard={ts_row['ir_dbd']:.1f}")

    if len(issues) == 0:
        print("\n[OK] HASIL: SEMUA DATA DASHBOARD COCOK DENGAN CSV OUTPUT!")
        print("Tidak ada mismatch pada zona maupun nilai IR DBD.")
    else:
        print("\n[FAIL] HASIL: DITEMUKAN MASALAH!")
        for issue in issues:
            print("  -", issue)
            
    print("="*60)

if __name__ == "__main__":
    run_validation()
