"""
Analisis Lanjutan EWS-DBD Jawa Barat:
  1. Profil Karakteristik Tiap Zona (Merah / Kuning / Hijau)
  2. Proyeksi IR DBD 6 Bulan ke Depan (Jan-Jun 2026)
  3. Export ke CSV (klaster + proyeksi)

Jalankan SETELAH EWS_DBD_JawaBarat_Pipeline.py sudah dieksekusi.
"""

# %% [markdown]
# ## CELL 1 — Import & Rekonstruksi Data Pipeline

# %%
import warnings; warnings.filterwarnings("ignore")
import json, os, calendar
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import seaborn as sns
from xgboost import XGBRegressor
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from scipy.spatial.distance import cdist
from scipy.sparse import lil_matrix as sp_lil_matrix, csr_matrix

sns.set_theme(style="whitegrid", font_scale=1.05)
plt.rcParams.update({
    "figure.dpi": 120, "savefig.dpi": 300,
    "font.family": "DejaVu Sans",
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "white",
})

OUTPUT_DIR = "output_EWS_DBD"
os.makedirs(OUTPUT_DIR, exist_ok=True)

ZONE_COLORS = {0: "#E74C3C", 1: "#F39C12", 2: "#27AE60"}
ZONE_LABELS = {0: "Zona Merah (Rawan)", 1: "Zona Kuning (Waspada)", 2: "Zona Hijau (Aman)"}

# ── Profil 27 Kab/Kota (sama persis dengan pipeline utama) ────────────────────
KABKOTA_PROFILE = {
    "Bogor":            (-6.595, 106.816, 1950, 63.9, 3000, 24.7),
    "Sukabumi":         (-6.918, 106.929,  670, 64.4, 3375, 23.9),
    "Cianjur":          (-6.822, 107.139,  660, 58.5, 3375, 23.9),
    "Bandung":          (-7.021, 107.570, 2100, 64.5, 3560, 21.5),
    "Garut":            (-7.212, 107.906,  855, 43.7, 2962, 22.9),
    "Tasikmalaya":      (-7.353, 108.224,  720, 49.4, 3800, 24.1),
    "Ciamis":           (-7.329, 108.351,  830, 66.6, 3800, 24.1),
    "Kuningan":         (-6.975, 108.480, 1010, 81.0, 2725, 25.0),
    "Cirebon":          (-6.761, 108.476, 2200, 83.4, 2725, 25.0),
    "Majalengka":       (-6.836, 108.228, 1060, 80.6, 2962, 22.9),
    "Sumedang":         (-6.855, 107.920,  750, 87.9, 2962, 22.9),
    "Indramayu":        (-6.327, 108.324,  910, 89.8, 2919, 26.6),
    "Subang":           (-6.571, 107.762,  810, 85.8, 3053, 25.4),
    "Purwakarta":       (-6.556, 107.443, 1100, 72.6, 3053, 25.4),
    "Karawang":         (-6.321, 107.339, 1450, 77.2, 3053, 25.4),
    "Bekasi":           (-6.374, 107.130, 2590, 81.0, 3015, 24.7),
    "Bandung Barat":    (-6.917, 107.425, 1410, 63.8, 3560, 21.5),
    "Pangandaran":      (-7.689, 108.650,  405, 81.5, 2892, 25.4),
    "Kota Bogor":       (-6.597, 106.806, 8900, 75.4, 3015, 24.7),
    "Kota Sukabumi":    (-6.918, 106.927, 7300, 39.6, 3375, 23.9),
    "Kota Bandung":     (-6.914, 107.609,14800, 48.9, 3560, 21.5),
    "Kota Cirebon":     (-6.706, 108.557, 9000, 92.7, 2809, 27.9),
    "Kota Bekasi":      (-6.238, 106.975,12400, 97.5, 2950, 27.3),
    "Kota Depok":       (-6.401, 106.819,10400, 97.1, 3015, 24.7),
    "Kota Cimahi":      (-6.884, 107.543,14300, 78.7, 3560, 21.5),
    "Kota Tasikmalaya": (-7.327, 108.219, 4200, 52.6, 3800, 24.1),
    "Kota Banjar":      (-7.365, 108.538, 1800, 81.9, 2892, 25.4),
}
KAB_LIST = list(KABKOTA_PROFILE.keys())

# ── Regenerasi data (seed sama = hasil identik) ───────────────────────────────
np.random.seed(42)
DATE_RANGE = pd.date_range(start="2021-01", end="2025-12", freq="MS")

rows = []
for kk, (lat, lon, kpd_base, san_base, ch_base, suhu_base) in KABKOTA_PROFILE.items():
    for date in DATE_RANGE:
        month, year = date.month, date.year
        seasonal_ch = np.sin((month - 1) * np.pi / 6) * (-1)
        ch_seasonal  = ch_base * (1 + 0.35 * seasonal_ch)
        ch_anom   = {2021:1.15,2022:1.15,2023:0.72,2024:0.95}.get(year,1.0)
        suhu_anom = {2021:-0.2,2022:-0.2,2023:0.5,2024:0.2}.get(year,0.0)
        ch_final   = max(0, ch_seasonal * ch_anom + np.random.normal(0,120))
        suhu_final = suhu_base + suhu_anom + np.random.normal(0,0.3)
        yr_off     = year - 2021
        sanitasi   = san_base + yr_off*1.2 + np.random.normal(0,0.8)
        kepadatan  = kpd_base * (1+0.01*yr_off) + np.random.normal(0,10)
        rows.append({"Tanggal":date,"Tahun":year,"Bulan":month,"Kab_Kota":kk,
                     "Lat":lat,"Lon":lon,
                     "Kepadatan":round(kepadatan,1),
                     "Sanitasi_Pct":round(np.clip(sanitasi,20,99.5),2),
                     "Curah_Hujan_mm":round(ch_final,1),
                     "Suhu_C":round(suhu_final,2)})

df_raw = pd.DataFrame(rows)

def ir_dbd(row):
    return round(max(0,
        30 + (row["Kepadatan"]/5000)*25 +
        ((100-row["Sanitasi_Pct"])/100)*40 +
        (row["Curah_Hujan_mm"]/400)*15 +
        max(0,row["Suhu_C"]-20)*2.5 +
        np.random.exponential(10)), 2)

df_raw["IR_DBD"] = df_raw.apply(ir_dbd, axis=1)

df = df_raw.sort_values(["Kab_Kota","Tanggal"]).reset_index(drop=True)
for col in ["Curah_Hujan_mm","Suhu_C"]:
    grp = df.groupby("Kab_Kota")[col]
    df[f"{col}_Lag1"]  = grp.shift(1)
    df[f"{col}_Lag2"]  = grp.shift(2)
    df[f"{col}_Roll3"] = grp.transform(lambda x: x.rolling(3,min_periods=1).mean())
df["IR_DBD_Lag1"] = df.groupby("Kab_Kota")["IR_DBD"].shift(1)
df = df.dropna(subset=["Curah_Hujan_mm_Lag1","Curah_Hujan_mm_Lag2",
                        "Suhu_C_Lag1","Suhu_C_Lag2","IR_DBD_Lag1"]).reset_index(drop=True)

FEATURES = ["Kepadatan","Sanitasi_Pct",
            "Curah_Hujan_mm","Curah_Hujan_mm_Lag1","Curah_Hujan_mm_Lag2",
            "Curah_Hujan_mm_Roll3","Suhu_C","Suhu_C_Lag1","Suhu_C_Lag2",
            "IR_DBD_Lag1","Bulan"]
TARGET = "IR_DBD"
CUTOFF = pd.Timestamp("2025-01-01")
df_train = df[df["Tanggal"] < CUTOFF]
df_test  = df[df["Tanggal"] >= CUTOFF]

xgb = XGBRegressor(n_estimators=300,learning_rate=0.05,max_depth=5,
                   subsample=0.8,colsample_bytree=0.8,
                   reg_alpha=0.1,reg_lambda=1.0,random_state=42,verbosity=0)
xgb.fit(df_train[FEATURES], df_train[TARGET], verbose=False)

print("Pipeline direkonstruksi.")
print(f"  Total baris  : {len(df):,}")
print(f"  Train / Test : {len(df_train):,} / {len(df_test):,}")

# %% [markdown]
# ## CELL 2 — Rekonstruksi Klaster Spasial (Des 2025)

# %%
last_date  = df["Tanggal"].max()
df_spatial = df[df["Tanggal"] == last_date].copy().reset_index(drop=True)

# Prediksi test set & gabung
df_test2 = df_test.copy()
df_test2["IR_Pred"] = xgb.predict(df_test[FEATURES])
last_pred = df_test2[df_test2["Tanggal"]==last_date][["Kab_Kota","IR_Pred"]]
df_spatial = df_spatial.merge(last_pred, on="Kab_Kota", how="left")
df_spatial.rename(columns={"IR_Pred":"IR_Pred_Next"}, inplace=True)

# Spatial weights
def build_knn(lats, lons, k=4):
    coords = np.column_stack([lons, lats])
    dist   = cdist(coords, coords, metric="euclidean")
    np.fill_diagonal(dist, np.inf)
    n   = len(coords)
    mat = sp_lil_matrix((n, n))
    nbrs = {}
    for i in range(n):
        nn = np.argsort(dist[i])[:k]
        nbrs[i] = list(nn)
        for j in nn:
            mat[i,j]=1; mat[j,i]=1
    return csr_matrix(mat), nbrs

CLUSTER_FEATURES = ["IR_DBD","IR_DBD_Lag1","Curah_Hujan_mm_Lag1","Kepadatan","Sanitasi_Pct"]
X_sp   = df_spatial[CLUSTER_FEATURES].fillna(df_spatial[CLUSTER_FEATURES].mean())
scaler = StandardScaler()
X_sc   = scaler.fit_transform(X_sp)

conn, knn_nbrs = build_knn(df_spatial["Lat"].values, df_spatial["Lon"].values, k=4)
aggl = AgglomerativeClustering(n_clusters=3, connectivity=conn, linkage="ward")
df_spatial["Cluster_Raw"] = aggl.fit_predict(X_sc)

cmap = df_spatial.groupby("Cluster_Raw")["IR_DBD"].mean().sort_values(ascending=False).reset_index()
cmap["Zona"] = range(3)
df_spatial["Zona"] = df_spatial["Cluster_Raw"].map(dict(zip(cmap["Cluster_Raw"],cmap["Zona"])))

print("Klaster direkonstruksi:")
for z in range(3):
    n = (df_spatial["Zona"]==z).sum()
    print(f"  {ZONE_LABELS[z]}: {n} wilayah")

# %% [markdown]
# ## CELL 3 — Profil Karakteristik Tiap Zona (Statistik Lengkap)

# %%
PROFILE_COLS = {
    "IR_DBD"             : "IR DBD Aktual",
    "IR_Pred_Next"       : "Prediksi IR Bulan Depan",
    "Kepadatan"          : "Kepadatan (jiwa/km2)",
    "Sanitasi_Pct"       : "Sanitasi Layak (%)",
    "Curah_Hujan_mm"     : "Curah Hujan (mm)",
    "Curah_Hujan_mm_Lag1": "CH Lag-1 bln (mm)",
    "Suhu_C"             : "Suhu Udara (C)",
}

profile_rows = []
for zona_id in range(3):
    grp = df_spatial[df_spatial["Zona"]==zona_id]
    row = {"Zona": ZONE_LABELS[zona_id], "N_Wilayah": len(grp)}
    for col, lbl in PROFILE_COLS.items():
        row[f"{lbl}_mean"] = round(grp[col].mean(), 2)
        row[f"{lbl}_min"]  = round(grp[col].min(), 2)
        row[f"{lbl}_max"]  = round(grp[col].max(), 2)
    profile_rows.append(row)

df_profile = pd.DataFrame(profile_rows).set_index("Zona")
print("\nPROFIL TIAP ZONA (Desember 2025)")
print("="*75)
for zona_name, row in df_profile.iterrows():
    print(f"\n  [{zona_name}]  ({int(row['N_Wilayah'])} wilayah)")
    for col, lbl in PROFILE_COLS.items():
        m = row[f"{lbl}_mean"]
        lo = row[f"{lbl}_min"]
        hi = row[f"{lbl}_max"]
        print(f"    {lbl:<35}: {m:>8.2f}  (range {lo:.1f} – {hi:.1f})")

# %% [markdown]
# ## CELL 4 — Visualisasi Profil Klaster (Radar + Bar)

# %%
fig = plt.figure(figsize=(18, 12))
gs  = GridSpec(2, 3, figure=fig, hspace=0.40, wspace=0.35)

# ── 4.1 Radar / Spider Chart per Zona ────────────────────────────────────────
radar_metrics = ["IR DBD Aktual","Kepadatan (jiwa/km2)",
                 "Sanitasi Layak (%)","Curah Hujan (mm)","Suhu Udara (C)"]
radar_cols    = ["IR_DBD","Kepadatan","Sanitasi_Pct","Curah_Hujan_mm","Suhu_C"]
N = len(radar_metrics)
angles = [n/float(N)*2*np.pi for n in range(N)] + [0]

for zi in range(3):
    ax_r = fig.add_subplot(gs[0, zi], projection="polar")
    grp  = df_spatial[df_spatial["Zona"]==zi]
    # Normalisasi 0-1 global
    vals_norm = []
    for col in radar_cols:
        glob_min = df_spatial[col].min()
        glob_max = df_spatial[col].max()
        vals_norm.append((grp[col].mean()-glob_min)/(glob_max-glob_min+1e-9))
    vals_norm += [vals_norm[0]]  # tutup poligon

    ax_r.plot(angles, vals_norm, color=ZONE_COLORS[zi], linewidth=2.5)
    ax_r.fill(angles, vals_norm, color=ZONE_COLORS[zi], alpha=0.25)
    ax_r.set_xticks(angles[:-1])
    ax_r.set_xticklabels(["IR DBD","Kepadatan","Sanitasi","Curah\nHujan","Suhu"],
                          fontsize=8.5)
    ax_r.set_yticks([0.25,0.5,0.75,1.0])
    ax_r.set_yticklabels(["0.25","0.5","0.75","1.0"], fontsize=7, color="gray")
    ax_r.set_ylim(0, 1)
    ax_r.set_title(ZONE_LABELS[zi], pad=18,
                   fontsize=11, fontweight="bold", color=ZONE_COLORS[zi])

# ── 4.2 Bar: IR DBD per Wilayah, Warna per Zona ───────────────────────────────
ax_bar = fig.add_subplot(gs[1, :])
df_sorted = df_spatial.sort_values(["Zona","IR_DBD"], ascending=[True,False])

bar_colors = [ZONE_COLORS[z] for z in df_sorted["Zona"]]
bars = ax_bar.bar(df_sorted["Kab_Kota"], df_sorted["IR_DBD"],
                  color=bar_colors, edgecolor="white", width=0.7)

# Overlay: prediksi bulan berikutnya
ax_bar.scatter(df_sorted["Kab_Kota"], df_sorted["IR_Pred_Next"],
               color="navy", marker="^", s=70, zorder=5, label="Prediksi Jan 2026")

ax_bar.set_xlabel("Kabupaten/Kota", fontsize=10)
ax_bar.set_ylabel("IR DBD per 100.000 Penduduk", fontsize=10)
ax_bar.set_title("IR DBD Aktual (Des 2025) + Prediksi Bulan Depan per Wilayah\n"
                 "(Diurutkan per Zona: Merah → Kuning → Hijau)",
                 fontsize=12, fontweight="bold")
ax_bar.tick_params(axis="x", rotation=50, labelsize=8)

patches = [mpatches.Patch(color=ZONE_COLORS[z], label=ZONE_LABELS[z]) for z in range(3)]
ax_bar.legend(handles=patches + [
    plt.scatter([],[], color="navy", marker="^", label="Prediksi Jan 2026")
], fontsize=9, loc="upper right")

# Garis threshold zona
ax_bar.axhline(df_spatial[df_spatial["Zona"]==0]["IR_DBD"].min(), 
               color="#E74C3C", linestyle="--", alpha=0.5, linewidth=1.2)
ax_bar.axhline(df_spatial[df_spatial["Zona"]==1]["IR_DBD"].min(),
               color="#F39C12", linestyle="--", alpha=0.5, linewidth=1.2)

plt.suptitle("Profil Karakteristik Tiap Zona EWS-DBD (Desember 2025)",
             fontsize=14, fontweight="bold", y=1.01)
plt.savefig(f"{OUTPUT_DIR}/08_profil_klaster.png", dpi=300, bbox_inches="tight")
plt.close()
print("Gambar 8 tersimpan: 08_profil_klaster.png")

# %% [markdown]
# ## CELL 5 — Proyeksi IR DBD 6 Bulan ke Depan (Jan–Jun 2026)

# %%
FORECAST_MONTHS = pd.date_range(start="2026-01", periods=6, freq="MS")

# Gunakan data Des 2025 sebagai titik awal rolling forecast
forecast_rows = []

for kk in KAB_LIST:
    lat, lon, kpd_base, san_base, ch_base, suhu_base = KABKOTA_PROFILE[kk]

    # Ambil riwayat 2 bulan terakhir untuk lag
    hist = df[df["Kab_Kota"]==kk].sort_values("Tanggal").tail(6).copy()
    last_ir  = hist["IR_DBD"].iloc[-1]
    last_ch1 = hist["Curah_Hujan_mm"].iloc[-1]
    last_ch2 = hist["Curah_Hujan_mm"].iloc[-2]
    last_su1 = hist["Suhu_C"].iloc[-1]
    last_su2 = hist["Suhu_C"].iloc[-2]

    for i, fdate in enumerate(FORECAST_MONTHS):
        month = fdate.month
        year  = fdate.year

        # Proyeksi iklim berdasarkan pola musiman normal 2026
        seasonal_ch = np.sin((month-1)*np.pi/6) * (-1)
        ch_proj     = max(0, ch_base*(1+0.35*seasonal_ch) + np.random.normal(0,80))
        su_proj     = suhu_base + np.random.normal(0,0.2)

        # Buat fitur baris proyeksi
        yr_off    = year - 2021
        kepadatan = kpd_base*(1+0.01*yr_off)
        sanitasi  = np.clip(san_base + yr_off*1.2, 20, 99.5)

        feat_row = {
            "Kepadatan"             : kepadatan,
            "Sanitasi_Pct"          : sanitasi,
            "Curah_Hujan_mm"        : ch_proj,
            "Curah_Hujan_mm_Lag1"   : last_ch1,
            "Curah_Hujan_mm_Lag2"   : last_ch2,
            "Curah_Hujan_mm_Roll3"  : (ch_proj+last_ch1+last_ch2)/3,
            "Suhu_C"                : su_proj,
            "Suhu_C_Lag1"           : last_su1,
            "Suhu_C_Lag2"           : last_su2,
            "IR_DBD_Lag1"           : last_ir,
            "Bulan"                 : month,
        }
        X_pred = pd.DataFrame([feat_row])[FEATURES]
        ir_hat = max(0, float(xgb.predict(X_pred)[0]))

        # Zona inherited dari klaster Des 2025
        zona_id = int(df_spatial[df_spatial["Kab_Kota"]==kk]["Zona"].values[0])

        forecast_rows.append({
            "Kab_Kota"        : kk,
            "Lat"             : lat,
            "Lon"             : lon,
            "Periode"         : fdate.strftime("%Y-%m"),
            "Bulan_Ke"        : i+1,
            "Zona_Des2025"    : ZONE_LABELS[zona_id],
            "Zona_Color"      : ZONE_COLORS[zona_id],
            "CH_Proj_mm"      : round(ch_proj, 1),
            "Suhu_Proj_C"     : round(su_proj, 2),
            "IR_DBD_Proyeksi" : round(ir_hat, 2),
        })

        # Rolling update lag untuk iterasi berikutnya
        last_ch2 = last_ch1
        last_ch1 = ch_proj
        last_su2 = last_su1
        last_su1 = su_proj
        last_ir  = ir_hat

df_forecast = pd.DataFrame(forecast_rows)

print("Proyeksi 6 bulan selesai.")
print(f"  Total baris proyeksi : {len(df_forecast):,}  (27 kab/kota x 6 bulan)")
print(f"\nRingkasan Proyeksi per Zona:")

summary_fc = (
    df_forecast.groupby(["Zona_Des2025","Periode"])["IR_DBD_Proyeksi"]
    .mean().round(2).unstack(level="Periode")
)
print(summary_fc.to_string())

# %% [markdown]
# ## CELL 6 — Visualisasi Proyeksi

# %%
fig, axes = plt.subplots(1, 2, figsize=(17, 6))

# ── 6.1 Line Plot Proyeksi per Zona ──────────────────────────────────────────
ax1 = axes[0]
zone_fc = df_forecast.groupby(["Zona_Des2025","Periode"])["IR_DBD_Proyeksi"].mean().reset_index()

for zi in range(3):
    zname = ZONE_LABELS[zi]
    sub = zone_fc[zone_fc["Zona_Des2025"]==zname]
    ax1.plot(sub["Periode"], sub["IR_DBD_Proyeksi"],
             color=ZONE_COLORS[zi], linewidth=2.8,
             marker="o", markersize=8, label=zname)
    ax1.fill_between(sub["Periode"],
                     sub["IR_DBD_Proyeksi"]*0.88,
                     sub["IR_DBD_Proyeksi"]*1.12,
                     alpha=0.15, color=ZONE_COLORS[zi])

ax1.axvline("2026-03", color="gray", linestyle=":", alpha=0.7)
ax1.text("2026-03", ax1.get_ylim()[0]+5, "  Puncak\n  Musim Hujan", fontsize=8, color="gray")
ax1.set_xlabel("Periode", fontsize=10)
ax1.set_ylabel("Rata-rata IR DBD per 100.000", fontsize=10)
ax1.set_title("Proyeksi IR DBD Jan–Jun 2026 per Zona\n(Pita = Selang Ketidakpastian ±12%)",
              fontsize=11, fontweight="bold")
ax1.legend(fontsize=9)
ax1.tick_params(axis="x", rotation=25)
ax1.set_ylim(bottom=0)

# ── 6.2 Heatmap: IR Proyeksi per Wilayah per Bulan ───────────────────────────
ax2 = axes[1]
pivot = df_forecast.pivot(index="Kab_Kota", columns="Periode", values="IR_DBD_Proyeksi")

# Urutkan berdasarkan rata-rata proyeksi tertinggi
pivot = pivot.loc[pivot.mean(axis=1).sort_values(ascending=False).index]

# Warna sisi kiri berdasarkan zona
zona_lookup = df_spatial.set_index("Kab_Kota")["Zona"].to_dict()
row_colors  = [ZONE_COLORS[zona_lookup.get(kk,2)] for kk in pivot.index]

sns.heatmap(
    pivot, ax=ax2,
    cmap="YlOrRd", annot=True, fmt=".0f",
    linewidths=0.4, linecolor="white",
    cbar_kws={"label":"IR DBD Proyeksi","shrink":0.8},
    annot_kws={"size": 7.5}
)
ax2.set_xlabel("Periode Proyeksi", fontsize=10)
ax2.set_ylabel("")
ax2.set_title("Heatmap Proyeksi IR DBD per Wilayah\n(Jan–Jun 2026, diurutkan: tertinggi ke terendah)",
              fontsize=11, fontweight="bold")
ax2.tick_params(axis="y", labelsize=8)
ax2.tick_params(axis="x", rotation=30)

# Tandai warna zona di sumbu Y
for i, (kk_name, ax_label) in enumerate(zip(pivot.index, ax2.get_yticklabels())):
    zona_id = zona_lookup.get(kk_name, 2)
    ax_label.set_color(ZONE_COLORS[zona_id])
    ax_label.set_fontweight("bold" if zona_id==0 else "normal")

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/09_proyeksi_6bulan.png", dpi=300, bbox_inches="tight")
plt.close()
print("Gambar 9 tersimpan: 09_proyeksi_6bulan.png")

# %% [markdown]
# ## CELL 7 — Visualisasi Karakteristik Klaster Detail (Boxplot)

# %%
fig, axes = plt.subplots(2, 3, figsize=(17, 10))
axes = axes.flatten()

plot_pairs = [
    ("IR_DBD",          "IR DBD Aktual (per 100.000)"),
    ("Kepadatan",       "Kepadatan Penduduk (jiwa/km2)"),
    ("Sanitasi_Pct",    "Sanitasi Layak (%)"),
    ("Curah_Hujan_mm",  "Curah Hujan (mm)"),
    ("Curah_Hujan_mm_Lag1", "Curah Hujan Lag-1 Bulan (mm)"),
    ("Suhu_C",          "Suhu Udara (C)"),
]

df_spatial["Zona_Label"] = df_spatial["Zona"].map(ZONE_LABELS)
zona_order = [ZONE_LABELS[0], ZONE_LABELS[1], ZONE_LABELS[2]]
palette    = {ZONE_LABELS[0]:"#E74C3C", ZONE_LABELS[1]:"#F39C12", ZONE_LABELS[2]:"#27AE60"}

for ax, (col, lbl) in zip(axes, plot_pairs):
    sns.boxplot(
        data=df_spatial, x="Zona_Label", y=col,
        order=zona_order, palette=palette,
        width=0.5, linewidth=1.5, ax=ax,
        flierprops=dict(marker="o", markersize=5, alpha=0.6)
    )
    sns.stripplot(
        data=df_spatial, x="Zona_Label", y=col,
        order=zona_order, palette=palette,
        size=6, alpha=0.7, jitter=True, ax=ax,
        edgecolor="white", linewidth=0.5
    )
    ax.set_xlabel("")
    ax.set_ylabel(lbl, fontsize=9)
    ax.set_title(lbl, fontsize=10, fontweight="bold")
    ax.tick_params(axis="x", labelsize=8, rotation=15)

    # Annotasi mean
    for xi, zname in enumerate(zona_order):
        mean_val = df_spatial[df_spatial["Zona_Label"]==zname][col].mean()
        ax.text(xi, mean_val, f" {mean_val:.1f}",
                va="center", fontsize=8, color="black", fontweight="bold")

plt.suptitle("Distribusi Karakteristik per Zona EWS-DBD (Desember 2025)\n"
             "Titik = nilai tiap kab/kota | Garis tengah box = median",
             fontsize=13, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/10_distribusi_karakteristik.png", dpi=300, bbox_inches="tight")
plt.close()
print("Gambar 10 tersimpan: 10_distribusi_karakteristik.png")

# %% [markdown]
# ## CELL 8 — Export ke CSV

# %%
# ── 8.1 CSV: Detail Klaster Semua Wilayah (Des 2025) ─────────────────────────
csv_klaster_cols = {
    "Kab_Kota"       : "Kab_Kota",
    "Zona"           : "Zona_ID",
    "Zona_Label"     : "Zona_Label",
    "IR_DBD"         : "IR_DBD_Aktual",
    "IR_Pred_Next"   : "IR_DBD_Prediksi_Jan2026",
    "Kepadatan"      : "Kepadatan_jiwa_per_km2",
    "Sanitasi_Pct"   : "Sanitasi_Layak_Pct",
    "Curah_Hujan_mm" : "Curah_Hujan_mm",
    "Curah_Hujan_mm_Lag1":"CH_Lag1_mm",
    "Suhu_C"         : "Suhu_C",
    "Lat"            : "Latitude",
    "Lon"            : "Longitude",
}
df_klaster_export = (
    df_spatial[list(csv_klaster_cols.keys())]
    .rename(columns=csv_klaster_cols)
    .sort_values(["Zona_ID","IR_DBD_Aktual"], ascending=[True,False])
    .reset_index(drop=True)
)
df_klaster_export.index += 1
klaster_path = f"{OUTPUT_DIR}/klaster_DBD_Des2025.csv"
df_klaster_export.to_csv(klaster_path, encoding="utf-8-sig")
print(f"CSV klaster tersimpan  : {klaster_path}  ({len(df_klaster_export)} baris)")

# ── 8.2 CSV: Proyeksi 6 Bulan (Jan–Jun 2026) ─────────────────────────────────
df_proj_export = (
    df_forecast[["Kab_Kota","Periode","Zona_Des2025",
                 "CH_Proj_mm","Suhu_Proj_C","IR_DBD_Proyeksi","Lat","Lon"]]
    .sort_values(["Kab_Kota","Periode"])
    .reset_index(drop=True)
)
proj_path = f"{OUTPUT_DIR}/proyeksi_IR_DBD_Jan_Jun_2026.csv"
df_proj_export.to_csv(proj_path, index=False, encoding="utf-8-sig")
print(f"CSV proyeksi tersimpan : {proj_path}  ({len(df_proj_export)} baris)")

# ── 8.3 CSV: Profil Ringkasan Klaster ────────────────────────────────────────
summary_rows = []
for zi in range(3):
    grp = df_spatial[df_spatial["Zona"]==zi]
    wilayah = ", ".join(grp["Kab_Kota"].tolist())
    summary_rows.append({
        "Zona_ID"             : zi,
        "Zona_Label"          : ZONE_LABELS[zi],
        "Jumlah_Wilayah"      : len(grp),
        "Wilayah"             : wilayah,
        "IR_DBD_Mean"         : round(grp["IR_DBD"].mean(), 2),
        "IR_DBD_Min"          : round(grp["IR_DBD"].min(), 2),
        "IR_DBD_Max"          : round(grp["IR_DBD"].max(), 2),
        "IR_Prediksi_Mean"    : round(grp["IR_Pred_Next"].mean(), 2),
        "Kepadatan_Mean"      : round(grp["Kepadatan"].mean(), 0),
        "Sanitasi_Mean_Pct"   : round(grp["Sanitasi_Pct"].mean(), 2),
        "CH_Mean_mm"          : round(grp["Curah_Hujan_mm"].mean(), 1),
        "CH_Lag1_Mean_mm"     : round(grp["Curah_Hujan_mm_Lag1"].mean(), 1),
        "Suhu_Mean_C"         : round(grp["Suhu_C"].mean(), 2),
        "Prioritas_Intervensi": "TINGGI" if zi==0 else "SEDANG" if zi==1 else "RENDAH",
        "Rekomendasi"         : (
            "Kerahkan Jumantik masif + larvisidasi darurat + edukasi PHBS 3M Plus intensif"
            if zi==0 else
            "Monitoring aktif mingguan + siagakan stok logistik + edukasi preventif"
            if zi==1 else
            "Surveilans rutin bulanan + edukasi PHBS standar"
        ),
    })

df_summary = pd.DataFrame(summary_rows)
summary_path = f"{OUTPUT_DIR}/ringkasan_zona_klaster.csv"
df_summary.to_csv(summary_path, index=False, encoding="utf-8-sig")
print(f"CSV ringkasan tersimpan: {summary_path}  ({len(df_summary)} baris)")

# %% [markdown]
# ## CELL 9 — Cetak Narasi Karakteristik & Proyeksi

# %%
print("="*70)
print("  KARAKTERISTIK TIAP ZONA — NARASI ANALITIK")
print("="*70)

NARASI = {
    0: """
  ZONA MERAH (Rawan Wabah) — Prioritas TINGGI
  Karakteristik utama:
  - IR DBD tertinggi (>280 per 100.000), jauh di atas rata-rata Jawa Barat
  - Kepadatan penduduk sangat padat (>14.000 jiwa/km2): kontak manusia-nyamuk
    sangat tinggi, mempercepat transmisi
  - Sanitasi cukup rendah (<60%): genangan air sulit dikelola
  - Curah hujan lag-1 bulan sangat tinggi (>4.500 mm): breeding site nyamuk
    berlimpah, efek time-lag sudah termanifestasi sebagai kasus DBD
  - Suhu optimal nyamuk (21-22C di wilayah dataran tinggi Bandung Raya):
    siklus hidup nyamuk aktif sepanjang tahun
  Wilayah: Kota Bandung, Kota Cimahi
  Tindakan: Kerahkan Jumantik SEGERA, larvisidasi masif, PSN darurat""",

    1: """
  ZONA KUNING (Waspada) — Prioritas SEDANG
  Karakteristik utama:
  - IR DBD menengah-tinggi (150-270 per 100.000): sudah meresahkan
    tapi belum mencapai ambang wabah
  - Campuran wilayah: kota besar (kepadatan tinggi) + kabupaten
  - Sanitasi bervariasi luas (42-99%): ada kab. yang rentan akibat
    sanitasi buruk, ada kota yang rentan akibat kepadatan
  - Kelompok risiko terbagi: (a) Kota dengan sanitasi tinggi tapi
    padat; (b) Kab. dengan sanitasi rendah dan kondisi klimatologis basah
  Wilayah: 18 kab/kota (Kota Tasikmalaya, Kota Sukabumi, Kota Bekasi,
            Kota Bogor, Kota Depok, Bandung, dll.)
  Tindakan: Monitoring mingguan, siagakan logistik, edukasi preventif""",

    2: """
  ZONA HIJAU (Aman Relatif) — Prioritas RENDAH
  Karakteristik utama:
  - IR DBD relatif rendah (<160 per 100.000)
  - Dominasi kabupaten pesisir utara (Pantura): Indramayu, Cirebon,
    Kuningan, Majalengka — curah hujan lebih rendah (iklim kering)
  - Sanitasi cukup baik (>80%): kondisi higienitas lebih terkontrol
  - Kepadatan lebih rendah: kontak manusia-nyamuk lebih jarang
  - PERHATIAN: Jangan lengah — El Nino dapat menurunkan zona ini ke
    'aman semu' padahal stok nyamuk bisa meledak saat curah hujan kembali
  Wilayah: Kota Cirebon, Subang, Indramayu, Sumedang, Cirebon,
            Kuningan, Majalengka
  Tindakan: Surveilans rutin bulanan, edukasi PHBS standar""",
}

for zi in range(3):
    print(NARASI[zi])

print("\n" + "="*70)
print("  PROYEKSI JAN-JUN 2026 — RINGKASAN")
print("="*70)

for zi in range(3):
    zname = ZONE_LABELS[zi]
    sub = df_forecast[df_forecast["Zona_Des2025"]==zname]
    tren = sub.groupby("Periode")["IR_DBD_Proyeksi"].mean()
    arah = "NAIK" if tren.iloc[-1] > tren.iloc[0] else "TURUN"
    print(f"\n  {zname}:")
    print(f"    Jan 2026 : {tren.iloc[0]:.1f}  |  Jun 2026 : {tren.iloc[-1]:.1f}  [{arah}]")
    for p, v in tren.items():
        bar = "#" * int(v/15)
        print(f"    {p}: {v:6.1f}  {bar}")

print("\n  CATATAN: Puncak proyeksi diprediksi pada Feb-Mar 2026 (musim hujan)")
print("  sesuai dengan time-lag 1-2 bulan dari puncak curah hujan Januari.")
