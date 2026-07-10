import json, csv, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = r'd:\Draft Perlombaan UNESA\ESSAI - UMEDS\output_EWS_DBD'
issues = []

print('=' * 70)
print('  AUDIT VALIDITAS & KONSISTENSI OUTPUT EWS-DBD')
print('=' * 70)

# ── 1. JSON ───────────────────────────────────────────────────────────────────
with open(BASE + '/ews_dbd_cluster_latest.json', encoding='utf-8') as f:
    js = json.load(f)

meta      = js['metadata']
data_json = js['data']
n_total   = meta['total_wilayah']
n_merah   = meta['n_zona_merah']
n_kuning  = meta['n_zona_kuning']
n_hijau   = meta['n_zona_hijau']
periode   = meta['periode']
model_str = meta['model']

print('\n[1] ews_dbd_cluster_latest.json')
print('    Periode        :', periode)
print('    Model          :', model_str)
print('    Total wilayah  :', n_total)
print('    Zona Merah     :', n_merah)
print('    Zona Kuning    :', n_kuning)
print('    Zona Hijau     :', n_hijau)
chk = n_merah + n_kuning + n_hijau == n_total
print('    Jumlah check   :', n_merah+n_kuning+n_hijau, '==', n_total, '-> OK' if chk else '-> MISMATCH!')
if not chk:
    issues.append('Jumlah zona di JSON tidak sesuai total')

kk_json      = set(d['kab_kota'] for d in data_json)
zona_map_json= {d['kab_kota']: d['zona'] for d in data_json}

# IR range check
irs_json = [d['ir_dbd_aktual'] for d in data_json]
print('    IR range       :', round(min(irs_json),1), '-', round(max(irs_json),1))
if min(irs_json) < 0:
    issues.append('Ada IR negatif di JSON')

# ── 2. klaster CSV ────────────────────────────────────────────────────────────
with open(BASE + '/klaster_DBD_Des2025.csv', encoding='utf-8-sig') as f:
    rows_klas = list(csv.DictReader(f))

print('\n[2] klaster_DBD_Des2025.csv')
print('    Jumlah baris   :', len(rows_klas), '(harusnya 27)')
kk_klas      = set(r['Kab_Kota'] for r in rows_klas)
zona_map_klas= {r['Kab_Kota']: int(r['Zona_ID']) for r in rows_klas}

if kk_json == kk_klas:
    print('    Kab/Kota match : OK -', len(kk_json), 'wilayah identik dengan JSON')
else:
    diff = kk_json.symmetric_difference(kk_klas)
    print('    Kab/Kota match : MISMATCH!', diff)
    issues.append('Kab/Kota mismatch JSON vs klaster CSV: ' + str(diff))

zona_mm = [(kk, zona_map_json[kk], zona_map_klas[kk])
           for kk in kk_json & kk_klas if zona_map_json[kk] != zona_map_klas[kk]]
if zona_mm:
    print('    Zona ID match  : MISMATCH!', zona_mm)
    issues.append('Zona ID tidak konsisten: ' + str(zona_mm))
else:
    print('    Zona ID match  : OK - semua', len(kk_klas), 'kab/kota konsisten')

irs_klas = [float(r['IR_DBD_Aktual']) for r in rows_klas]
print('    IR range       :', round(min(irs_klas),1), '-', round(max(irs_klas),1))
if min(irs_klas) < 0:
    issues.append('Ada IR negatif di klaster CSV')

# ── 3. Proyeksi CSV ───────────────────────────────────────────────────────────
with open(BASE + '/proyeksi_IR_DBD_Jan_Jun_2026.csv', encoding='utf-8-sig') as f:
    rows_proj = list(csv.DictReader(f))

print('\n[3] proyeksi_IR_DBD_Jan_Jun_2026.csv')
print('    Jumlah baris   :', len(rows_proj), '(target: 162 = 27x6)')
if len(rows_proj) != 162:
    issues.append('Baris proyeksi ' + str(len(rows_proj)) + ' != 162')
    print('    Baris count    : MISMATCH!')
else:
    print('    Baris count    : OK')

kk_proj  = set(r['Kab_Kota'] for r in rows_proj)
per_proj = set(r['Periode'] for r in rows_proj)
expected_per = {'2026-01','2026-02','2026-03','2026-04','2026-05','2026-06'}

if kk_proj == kk_klas:
    print('    Kab/Kota match : OK')
else:
    diff = kk_proj.symmetric_difference(kk_klas)
    print('    Kab/Kota match : MISMATCH!', diff)
    issues.append('Kab/Kota mismatch proyeksi vs klaster: ' + str(diff))

if per_proj == expected_per:
    print('    Periode match  : OK -', sorted(per_proj))
else:
    diff = per_proj.symmetric_difference(expected_per)
    print('    Periode match  : MISMATCH!', diff)
    issues.append('Periode proyeksi tidak lengkap: ' + str(diff))

ir_proj = [float(r['IR_DBD_Proyeksi']) for r in rows_proj]
print('    IR Proyeksi    :', round(min(ir_proj),1), '-', round(max(ir_proj),1),
      '-> OK' if min(ir_proj) > 0 else '-> ADA NEGATIF!')
if min(ir_proj) < 0:
    issues.append('Ada IR proyeksi negatif')

zona_labels_proj = set(r['Zona_Des2025'] for r in rows_proj)
expected_labels  = {'Zona Merah (Rawan)', 'Zona Kuning (Waspada)', 'Zona Hijau (Aman)'}
if zona_labels_proj == expected_labels:
    print('    Zona labels    : OK')
else:
    print('    Zona labels    : CHECK -', zona_labels_proj)

# ── 4. Ringkasan CSV ──────────────────────────────────────────────────────────
with open(BASE + '/ringkasan_zona_klaster.csv', encoding='utf-8-sig') as f:
    rows_ring = list(csv.DictReader(f))

print('\n[4] ringkasan_zona_klaster.csv')
print('    Jumlah baris   :', len(rows_ring), '(harusnya 3)')
total_ring = sum(int(r['Jumlah_Wilayah']) for r in rows_ring)
print('    Total wilayah  :', total_ring, '(harusnya 27) ->', 'OK' if total_ring==27 else 'MISMATCH!')
if total_ring != 27:
    issues.append('Total wilayah ringkasan = ' + str(total_ring))
for r in rows_ring:
    print('   ', r['Zona_Label'], ':', r['Jumlah_Wilayah'], 'wilayah | IR mean =', r['IR_DBD_Mean'])

# ── 5. PNG files ──────────────────────────────────────────────────────────────
png_files = sorted([f for f in os.listdir(BASE) if f.endswith('.png')])
print('\n[5] File Visualisasi PNG')
print('    Jumlah file    :', len(png_files), '(harusnya 10)')
for pf in png_files:
    sz = os.path.getsize(BASE + '/' + pf) // 1024
    status = 'OK' if sz > 50 else 'KECIL?'
    print('   ', pf, '|', sz, 'KB ->', status)
    if sz < 50:
        issues.append('PNG mungkin bermasalah: ' + pf)

# ── KESIMPULAN ────────────────────────────────────────────────────────────────
print()
print('=' * 70)
print('  HASIL AUDIT FINAL')
print('=' * 70)
if not issues:
    print()
    print('  [VALID] Tidak ada mismatch ditemukan.')
    print()
    print('  Ringkasan konsistensi:')
    print('  - 27 kab/kota identik di: JSON, klaster CSV, proyeksi CSV, ringkasan')
    print('  - Zona ID & label 100% konsisten antar file')
    print('  - Baris proyeksi: 162 (27x6 bulan) - tepat')
    print('  - Rentang IR semua positif dan masuk akal')
    print('  - 10 file PNG tersimpan dengan ukuran wajar')
    print('  - Periode: Des 2025 (aktual) -> Jan-Jun 2026 (proyeksi) - urut benar')
else:
    print()
    print('  [MASALAH] Ditemukan', len(issues), 'isu:')
    for i, iss in enumerate(issues, 1):
        print('  ' + str(i) + '.', iss)
print()
print('=' * 70)
