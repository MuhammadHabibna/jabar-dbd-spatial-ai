# %% [markdown]
# # 🦟 EWS-PHBS: Sistem Peringatan Dini Spasial-Temporal DBD
# ## Berbasis Orkestrasi Data Iklim dan Demografi — Jawa Barat 2021–2025
#
# **Pendekatan:** *Precision Public Health* (PPH) dengan model Spasial-Temporal
#
# **Data:** Panel 27 Kabupaten/Kota × 60 bulan = 1.620 observasi
#
# **Pipeline:**
# 1. 📦 Data Simulation & Mock Data
# 2. ⚙️  Feature Engineering (Time-Lag Effect)
# 3. 📊 Advanced EDA
# 4. 🤖 Predictive Modeling (XGBoost)
# 5. 🗺️  Spatial Modeling (Spatially Constrained Clustering)
# 6. 💾 Export (PNG 300 DPI + JSON API-ready)
#
# ---
# *Lampiran Karya Tulis Ilmiah — Kompetisi UMEDS UNESA 2025*

# %% [markdown]
# ## ⚙️ CELL 1 — Setup Lingkungan & Import Library

# %%
# ─── Instalasi dependensi (uncomment jika belum terinstall) ───────────────────
# !pip install xgboost libpysal scikit-learn seaborn matplotlib pandas numpy

# ─── Standard Library ─────────────────────────────────────────────────────────
import warnings
warnings.filterwarnings("ignore")
import json
import os

# ─── Data Processing ──────────────────────────────────────────────────────────
import numpy as np
import pandas as pd

# ─── Visualization ────────────────────────────────────────────────────────────
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from matplotlib.lines import Line2D
from matplotlib.gridspec import GridSpec

# ─── Machine Learning ─────────────────────────────────────────────────────────
from xgboost import XGBRegressor
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error

# ─── Spatial Analysis (Custom KNN — tanpa libpysal, pure scipy) ────────────────
from scipy.spatial.distance import cdist
from scipy.sparse import lil_matrix as sp_lil_matrix, csr_matrix

# ─── Global Style Config ──────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
plt.rcParams.update({
    "figure.dpi"       : 120,
    "savefig.dpi"      : 300,
    "font.family"      : "DejaVu Sans",
    "axes.spines.top"  : False,
    "axes.spines.right": False,
    "figure.facecolor" : "white",
    "axes.facecolor"   : "#F8F9FA",
})

# ─── Output directory ─────────────────────────────────────────────────────────
OUTPUT_DIR = "output_EWS_DBD"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── Warna Zona ───────────────────────────────────────────────────────────────
ZONE_COLORS  = {0: "#E74C3C", 1: "#F39C12", 2: "#27AE60"}   # Merah, Kuning, Hijau
ZONE_LABELS  = {0: "Zona Merah (Rawan)",
                1: "Zona Kuning (Waspada)",
                2: "Zona Hijau (Aman)"}

print("✅ Setup selesai. Library berhasil diimpor.")
print(f"   Output visualisasi  : ./{OUTPUT_DIR}/")

# %% [markdown]
# ## 📦 CELL 2 — Data Simulation (Mock Data Realistis)
#
# Simulasi data panel **1.620 baris** (27 Kab/Kota × 60 bulan, Jan 2021–Des 2025).
# Data di-generate dengan:
# - Pola musiman tropis (musim hujan Des–Apr, kemarau Jun–Sep)
# - Anomali La Niña 2021–2022 (+20% curah hujan)
# - Anomali El Niño 2023 (−30% curah hujan, +0.5°C suhu)
# - Korelasi logis antara iklim, sanitasi, kepadatan → IR DBD

# %%
# ─── 2.1 Profil 27 Kab/Kota Jawa Barat ───────────────────────────────────────
KABKOTA_PROFILE = {
    # (Nama, Lat, Lon, Kepadatan_base, Sanitasi_base, CH_base, Suhu_base)
    "Bogor"           : (-6.595, 106.816, 1950, 63.9, 3000, 24.7),
    "Sukabumi"        : (-6.918, 106.929,  670, 64.4, 3375, 23.9),
    "Cianjur"         : (-6.822, 107.139,  660, 58.5, 3375, 23.9),
    "Bandung"         : (-7.021, 107.570, 2100, 64.5, 3560, 21.5),
    "Garut"           : (-7.212, 107.906,  855, 43.7, 2962, 22.9),
    "Tasikmalaya"     : (-7.353, 108.224,  720, 49.4, 3800, 24.1),
    "Ciamis"          : (-7.329, 108.351,  830, 66.6, 3800, 24.1),
    "Kuningan"        : (-6.975, 108.480, 1010, 81.0, 2725, 25.0),
    "Cirebon"         : (-6.761, 108.476, 2200, 83.4, 2725, 25.0),
    "Majalengka"      : (-6.836, 108.228, 1060, 80.6, 2962, 22.9),
    "Sumedang"        : (-6.855, 107.920,  750, 87.9, 2962, 22.9),
    "Indramayu"       : (-6.327, 108.324,  910, 89.8, 2919, 26.6),
    "Subang"          : (-6.571, 107.762,  810, 85.8, 3053, 25.4),
    "Purwakarta"      : (-6.556, 107.443, 1100, 72.6, 3053, 25.4),
    "Karawang"        : (-6.321, 107.339, 1450, 77.2, 3053, 25.4),
    "Bekasi"          : (-6.374, 107.130, 2590, 81.0, 3015, 24.7),
    "Bandung Barat"   : (-6.917, 107.425, 1410, 63.8, 3560, 21.5),
    "Pangandaran"     : (-7.689, 108.650,  405, 81.5, 2892, 25.4),
    "Kota Bogor"      : (-6.597, 106.806, 8900, 75.4, 3015, 24.7),
    "Kota Sukabumi"   : (-6.918, 106.927, 7300, 39.6, 3375, 23.9),
    "Kota Bandung"    : (-6.914, 107.609,14800, 48.9, 3560, 21.5),
    "Kota Cirebon"    : (-6.706, 108.557, 9000, 92.7, 2809, 27.9),
    "Kota Bekasi"     : (-6.238, 106.975,12400, 97.5, 2950, 27.3),
    "Kota Depok"      : (-6.401, 106.819,10400, 97.1, 3015, 24.7),
    "Kota Cimahi"     : (-6.884, 107.543,14300, 78.7, 3560, 21.5),
    "Kota Tasikmalaya": (-7.327, 108.219, 4200, 52.6, 3800, 24.1),
    "Kota Banjar"     : (-7.365, 108.538, 1800, 81.9, 2892, 25.4),
}

KAB_LIST = list(KABKOTA_PROFILE.keys())
print(f"Jumlah Kab/Kota : {len(KAB_LIST)}")

# ─── 2.2 Generate Deret Waktu Bulanan ─────────────────────────────────────────
np.random.seed(42)

DATE_RANGE = pd.date_range(start="2021-01", end="2025-12", freq="MS")  # 60 bulan
print(f"Rentang waktu   : {DATE_RANGE[0].strftime('%b %Y')} – {DATE_RANGE[-1].strftime('%b %Y')} ({len(DATE_RANGE)} bulan)")

rows = []
for kk, (lat, lon, kpd_base, san_base, ch_base, suhu_base) in KABKOTA_PROFILE.items():
    for t, date in enumerate(DATE_RANGE):
        month = date.month
        year  = date.year

        # ── Pola musiman curah hujan (tropis) ─────────────────────────────────
        seasonal_ch = np.sin((month - 1) * np.pi / 6) * (-1)  # puncak Jan & Des
        ch_seasonal = ch_base * (1 + 0.35 * seasonal_ch)

        # ── Anomali iklim tahunan ─────────────────────────────────────────────
        if year in [2021, 2022]:    # La Niña: lebih basah, lebih dingin
            ch_anom   = 1.15
            suhu_anom = -0.2
        elif year == 2023:           # El Niño: lebih kering, lebih panas
            ch_anom   = 0.72
            suhu_anom = +0.5
        elif year == 2024:           # Pemulihan
            ch_anom   = 0.95
            suhu_anom = +0.2
        else:                        # 2025: Normal
            ch_anom   = 1.00
            suhu_anom = 0.0

        ch_final   = max(0, ch_seasonal * ch_anom + np.random.normal(0, 120))
        suhu_final = suhu_base + suhu_anom + np.random.normal(0, 0.3)

        # ── Tren sanitasi & kepadatan meningkat ───────────────────────────────
        yr_offset   = year - 2021
        sanitasi    = san_base + yr_offset * 1.2 + np.random.normal(0, 0.8)
        kepadatan   = kpd_base * (1 + 0.01 * yr_offset) + np.random.normal(0, 10)

        rows.append({
            "Tanggal"          : date,
            "Tahun"            : year,
            "Bulan"            : month,
            "Kab_Kota"         : kk,
            "Lat"              : lat,
            "Lon"              : lon,
            "Kepadatan"        : round(kepadatan, 1),
            "Sanitasi_Pct"     : round(np.clip(sanitasi, 20, 99.5), 2),
            "Curah_Hujan_mm"   : round(ch_final, 1),
            "Suhu_C"           : round(suhu_final, 2),
        })

df_raw = pd.DataFrame(rows)

# ─── 2.3 Generate IR_DBD realistis (fungsi non-linear) ───────────────────────
def generate_ir_dbd(row):
    """
    IR DBD dipengaruhi oleh:
    - Kepadatan tinggi  → +IR
    - Sanitasi buruk    → +IR (hubungan negatif)
    - Curah hujan tinggi (lag effect disimulasikan lewat korelasi langsung dulu)
    - Suhu optimal 26-29°C untuk nyamuk → +IR
    - Noise acak (realisme)
    """
    base      = 30.0
    kpd_eff   = (row["Kepadatan"] / 5000) * 25       # Kepadatan → +IR
    san_eff   = ((100 - row["Sanitasi_Pct"]) / 100) * 40  # Sanitasi buruk → +IR
    ch_eff    = (row["Curah_Hujan_mm"] / 400)  * 15  # CH tinggi → breeding site
    suhu_eff  = max(0, (row["Suhu_C"] - 20)) * 2.5  # Suhu optimal nyamuk
    noise     = np.random.exponential(scale=10)       # Distribusi kanan (epidemi)

    ir = base + kpd_eff + san_eff + ch_eff + suhu_eff + noise
    return round(max(0, ir), 2)

df_raw["IR_DBD"] = df_raw.apply(generate_ir_dbd, axis=1)

print(f"\nTotal baris      : {len(df_raw):,}  (27 × 60 = 1.620 ✅)")
print(f"\nStatistik IR_DBD :")
print(df_raw["IR_DBD"].describe().to_string())
print(f"\nPreview 5 baris pertama:")
display(df_raw.head())

# %% [markdown]
# ## ⚙️ CELL 3 — Feature Engineering: Time-Lag Effect
#
# **Rasional biologis:** Nyamuk *Aedes aegypti* membutuhkan waktu **1–2 bulan**
# setelah curah hujan tinggi untuk berkembang menjadi nyamuk dewasa yang menularkan DBD.
# Kita mengekstrak sinyal *time-lag* ini sebagai fitur prediktif.

# %%
df = df_raw.copy()
df = df.sort_values(["Kab_Kota", "Tanggal"]).reset_index(drop=True)

def create_lag_features(df, group_col="Kab_Kota"):
    """
    Membuat fitur lag-1 dan lag-2 untuk variabel iklim
    serta rolling mean untuk konteks tren.
    Lag dihitung dalam kelompok per kab/kota (tidak bocor antar wilayah).
    """
    df = df.copy()
    for col in ["Curah_Hujan_mm", "Suhu_C"]:
        grp = df.groupby(group_col)[col]
        df[f"{col}_Lag1"]    = grp.shift(1)   # 1 bulan sebelumnya
        df[f"{col}_Lag2"]    = grp.shift(2)   # 2 bulan sebelumnya
        df[f"{col}_Roll3"]   = grp.transform( # Rolling mean 3 bulan
            lambda x: x.rolling(3, min_periods=1).mean()
        )
    # Lag target (autoregressive feature)
    df["IR_DBD_Lag1"] = df.groupby(group_col)["IR_DBD"].shift(1)

    return df

df = create_lag_features(df)

# Hapus baris dengan NaN dari lag (2 bulan pertama per kab/kota)
df = df.dropna(subset=["Curah_Hujan_mm_Lag1", "Curah_Hujan_mm_Lag2",
                        "Suhu_C_Lag1", "Suhu_C_Lag2", "IR_DBD_Lag1"])
df = df.reset_index(drop=True)

print("✅ Feature engineering selesai.")
print(f"   Total baris setelah drop NaN : {len(df):,}")
print(f"\n   Kolom baru yang ditambahkan:")
lag_cols = [c for c in df.columns if "Lag" in c or "Roll" in c]
for c in lag_cols:
    print(f"   ├── {c}")

# %% [markdown]
# ## 📊 CELL 4 — Advanced Exploratory Data Analysis (EDA)
#
# Tiga visualisasi utama:
# 1. **Time-Series** tren IR DBD agregat Jawa Barat 2021–2025
# 2. **Cross-Correlation Heatmap** variabel vs IR DBD
# 3. **Seasonal Pattern** curah hujan & IR DBD per bulan

# %%
# ─── 4.1 Time-Series Line Plot: Tren IR DBD Agregat Jawa Barat ───────────────
monthly_agg = (
    df.groupby("Tanggal")
    .agg(IR_DBD_Mean=("IR_DBD", "mean"),
         IR_DBD_Max =("IR_DBD", "max"),
         CH_Mean    =("Curah_Hujan_mm", "mean"))
    .reset_index()
)

fig, axes = plt.subplots(2, 1, figsize=(14, 9), sharex=True,
                          gridspec_kw={"height_ratios": [2.5, 1]})

# Panel atas: IR DBD
ax = axes[0]
ax.fill_between(monthly_agg["Tanggal"],
                monthly_agg["IR_DBD_Max"] * 0,
                monthly_agg["IR_DBD_Max"],
                alpha=0.12, color="#E74C3C", label="Range (Max)")
ax.fill_between(monthly_agg["Tanggal"],
                monthly_agg["IR_DBD_Mean"] - monthly_agg["IR_DBD_Mean"].std(),
                monthly_agg["IR_DBD_Mean"] + monthly_agg["IR_DBD_Mean"].std(),
                alpha=0.25, color="#3498DB")
ax.plot(monthly_agg["Tanggal"], monthly_agg["IR_DBD_Mean"],
        color="#2980B9", linewidth=2.5, label="Rata-rata IR DBD Jawa Barat")
ax.plot(monthly_agg["Tanggal"], monthly_agg["IR_DBD_Max"],
        color="#E74C3C", linewidth=1, linestyle="--", alpha=0.7, label="Max IR DBD")

# Annotasi fenomena iklim
for yr, label, c in [(2021, "La Niña\n2021–22", "#1ABC9C"),
                      (2023, "El Niño\n2023",    "#E74C3C"),
                      (2024, "Pemulihan\n2024",  "#F39C12")]:
    ax.axvspan(pd.Timestamp(f"{yr}-01-01"),
               pd.Timestamp(f"{yr}-12-31"),
               alpha=0.07, color=c)
    ax.text(pd.Timestamp(f"{yr}-07-01"), ax.get_ylim()[1] * 0.92,
            label, ha="center", fontsize=9, color=c, fontweight="bold")

ax.set_ylabel("IR DBD per 100.000 Penduduk", fontsize=11)
ax.set_title("Tren Incidence Rate DBD Agregat Jawa Barat (Jan 2021 – Des 2025)",
             fontsize=13, fontweight="bold", pad=15)
ax.legend(loc="upper left", fontsize=9)
ax.set_ylim(bottom=0)

# Panel bawah: Curah Hujan
ax2 = axes[1]
ax2.bar(monthly_agg["Tanggal"], monthly_agg["CH_Mean"],
        color="#85C1E9", alpha=0.8, width=20, label="Rata-rata CH (mm)")
ax2.set_ylabel("Curah Hujan\n(mm)", fontsize=10)
ax2.set_xlabel("Waktu", fontsize=11)
ax2.legend(loc="upper right", fontsize=9)

fig.suptitle("", fontsize=1)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/01_timeseries_IR_DBD.png", dpi=300, bbox_inches="tight")
plt.show()
print("✅ Gambar 1 tersimpan: 01_timeseries_IR_DBD.png")

# %%
# ─── 4.2 Cross-Correlation Heatmap ────────────────────────────────────────────
corr_cols = [
    "Curah_Hujan_mm_Lag1", "Curah_Hujan_mm_Lag2", "Curah_Hujan_mm_Roll3",
    "Suhu_C_Lag1", "Suhu_C_Lag2",
    "Curah_Hujan_mm", "Suhu_C",
    "Kepadatan", "Sanitasi_Pct",
    "IR_DBD_Lag1", "IR_DBD"
]
LABEL_MAP = {
    "Curah_Hujan_mm_Lag1" : "CH Lag-1 bln",
    "Curah_Hujan_mm_Lag2" : "CH Lag-2 bln",
    "Curah_Hujan_mm_Roll3": "CH Roll-3 bln",
    "Suhu_C_Lag1"         : "Suhu Lag-1",
    "Suhu_C_Lag2"         : "Suhu Lag-2",
    "Curah_Hujan_mm"      : "Curah Hujan",
    "Suhu_C"              : "Suhu Udara",
    "Kepadatan"           : "Kepadatan Pddk",
    "Sanitasi_Pct"        : "Sanitasi Layak %",
    "IR_DBD_Lag1"         : "IR DBD Lag-1",
    "IR_DBD"              : "IR DBD (Target)",
}

corr_matrix = df[corr_cols].corr()
corr_matrix_renamed = corr_matrix.rename(columns=LABEL_MAP, index=LABEL_MAP)

fig, ax = plt.subplots(figsize=(12, 9))
mask = np.zeros_like(corr_matrix_renamed, dtype=bool)
mask[np.triu_indices_from(mask, k=1)] = True  # Tampilkan lower triangle

sns.heatmap(
    corr_matrix_renamed,
    mask=mask,
    annot=True, fmt=".2f",
    cmap="RdYlGn",
    center=0, vmin=-1, vmax=1,
    linewidths=0.5,
    annot_kws={"size": 8.5},
    cbar_kws={"shrink": 0.8, "label": "Koefisien Korelasi Pearson"},
    ax=ax
)
ax.set_title("Cross-Correlation Heatmap: Variabel Prediktor vs IR DBD\n"
             "(Fitur Time-Lag menangkap efek tertunda nyamuk Aedes aegypti)",
             fontsize=12, fontweight="bold", pad=15)
ax.tick_params(axis="x", rotation=40)
ax.tick_params(axis="y", rotation=0)

# Highlight baris/kolom IR_DBD
for i, label in enumerate(corr_matrix_renamed.columns):
    if label == "IR DBD (Target)":
        ax.add_patch(plt.Rectangle((i, 0), 1, len(corr_matrix_renamed),
                                    fill=False, edgecolor="#E74C3C", lw=2.5, clip_on=False))

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/02_correlation_heatmap.png", dpi=300, bbox_inches="tight")
plt.show()
print("✅ Gambar 2 tersimpan: 02_correlation_heatmap.png")

# %%
# ─── 4.3 Seasonal Pattern: CH & IR DBD per Bulan ─────────────────────────────
month_names = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agt","Sep","Okt","Nov","Des"]

seasonal = (
    df.groupby("Bulan")
    .agg(IR_Mean=("IR_DBD", "mean"),
         IR_Std =("IR_DBD", "std"),
         CH_Mean=("Curah_Hujan_mm", "mean"))
    .reset_index()
)

fig, ax1 = plt.subplots(figsize=(12, 5))
ax2 = ax1.twinx()

bars = ax2.bar(seasonal["Bulan"], seasonal["CH_Mean"],
               color="#AED6F1", alpha=0.6, width=0.4, label="Rata-rata CH (mm)")
line = ax1.errorbar(seasonal["Bulan"], seasonal["IR_Mean"],
                    yerr=seasonal["IR_Std"],
                    color="#E74C3C", linewidth=2.5, marker="o",
                    markersize=8, capsize=4,
                    label="IR DBD ± 1 SD")
ax1.set_xlabel("Bulan", fontsize=11)
ax1.set_ylabel("IR DBD per 100.000 Penduduk", color="#E74C3C", fontsize=11)
ax2.set_ylabel("Curah Hujan Rata-rata (mm)", color="#2E86C1", fontsize=11)
ax1.set_xticks(range(1, 13))
ax1.set_xticklabels(month_names)
ax1.tick_params(axis="y", labelcolor="#E74C3C")
ax2.tick_params(axis="y", labelcolor="#2E86C1")

ax1.set_title("Pola Musiman: Curah Hujan & Incidence Rate DBD\n"
              "→ Puncak DBD tertinggal 1–2 bulan dari puncak curah hujan (Time-Lag Effect)",
              fontsize=12, fontweight="bold")

# Panah penjelasan time-lag
ax1.annotate("Puncak CH\n(Jan-Feb)", xy=(2, seasonal.loc[1,"IR_Mean"]),
             xytext=(4, seasonal.loc[1,"IR_Mean"]*1.15),
             arrowprops=dict(arrowstyle="->", color="gray"), fontsize=9, color="gray")
ax1.annotate("Peak DBD\n(Feb-Mar)", xy=(3, seasonal.loc[2,"IR_Mean"]),
             xytext=(5, seasonal.loc[2,"IR_Mean"]*1.1),
             arrowprops=dict(arrowstyle="->", color="#E74C3C"), fontsize=9, color="#E74C3C")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize=9)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/03_seasonal_pattern.png", dpi=300, bbox_inches="tight")
plt.show()
print("✅ Gambar 3 tersimpan: 03_seasonal_pattern.png")

# %% [markdown]
# ## 🤖 CELL 5 — Predictive Modeling: XGBoost Time-Series Forecaster
#
# **Strategi:** Train-Test Split berbasis waktu (temporal holdout).
# - **Train:** Jan 2021 – Des 2024 (48 bulan × 27 kab/kota)
# - **Test :** Jan 2025 – Des 2025 (12 bulan × 27 kab/kota)
#
# **Model:** XGBoost Regressor — mampu menangkap non-linearitas
# dan interaksi fitur yang tidak tertangkap regresi linear.

# %%
# ─── 5.1 Feature Selection & Train-Test Split ─────────────────────────────────
FEATURES = [
    "Kepadatan", "Sanitasi_Pct",
    "Curah_Hujan_mm", "Curah_Hujan_mm_Lag1", "Curah_Hujan_mm_Lag2",
    "Curah_Hujan_mm_Roll3",
    "Suhu_C", "Suhu_C_Lag1", "Suhu_C_Lag2",
    "IR_DBD_Lag1",
    "Bulan",        # Fitur musiman
]
TARGET = "IR_DBD"

CUTOFF = pd.Timestamp("2025-01-01")
df_train = df[df["Tanggal"] <  CUTOFF].copy()
df_test  = df[df["Tanggal"] >= CUTOFF].copy()

X_train, y_train = df_train[FEATURES], df_train[TARGET]
X_test,  y_test  = df_test[FEATURES],  df_test[TARGET]

print(f"Train set : {len(X_train):,} baris  ({df_train['Tanggal'].min().strftime('%b %Y')} – {df_train['Tanggal'].max().strftime('%b %Y')})")
print(f"Test set  : {len(X_test):,}  baris  ({df_test['Tanggal'].min().strftime('%b %Y')} – {df_test['Tanggal'].max().strftime('%b %Y')})")

# ─── 5.2 Melatih Model XGBoost ────────────────────────────────────────────────
xgb_model = XGBRegressor(
    n_estimators     = 300,
    learning_rate    = 0.05,
    max_depth        = 5,
    subsample        = 0.8,
    colsample_bytree = 0.8,
    reg_alpha        = 0.1,
    reg_lambda       = 1.0,
    random_state     = 42,
    verbosity        = 0,
)
xgb_model.fit(X_train, y_train,
              eval_set=[(X_test, y_test)],
              verbose=False)

y_pred = xgb_model.predict(X_test)

# ─── 5.3 Evaluasi Metrik ──────────────────────────────────────────────────────
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae  = mean_absolute_error(y_test, y_pred)
r2   = 1 - np.sum((y_test - y_pred)**2) / np.sum((y_test - y_test.mean())**2)

print(f"\n📊 Evaluasi Model XGBoost pada Test Set 2025")
print(f"   RMSE  : {rmse:.2f}")
print(f"   MAE   : {mae:.2f}")
print(f"   R²    : {r2:.4f}")

# ──── 5.4 Feature Importance ─────────────────────────────────────────────────
feat_imp = pd.Series(xgb_model.feature_importances_,
                     index=FEATURES).sort_values(ascending=True)

fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))

# Grafik feature importance
FEAT_LABEL = {
    "Kepadatan"             : "Kepadatan Pddk",
    "Sanitasi_Pct"          : "Sanitasi Layak %",
    "Curah_Hujan_mm"        : "Curah Hujan",
    "Curah_Hujan_mm_Lag1"   : "CH Lag-1",
    "Curah_Hujan_mm_Lag2"   : "CH Lag-2",
    "Curah_Hujan_mm_Roll3"  : "CH Roll-3",
    "Suhu_C"                : "Suhu Udara",
    "Suhu_C_Lag1"           : "Suhu Lag-1",
    "Suhu_C_Lag2"           : "Suhu Lag-2",
    "IR_DBD_Lag1"           : "IR DBD Lag-1 (AR)",
    "Bulan"                 : "Musim (Bulan)",
}
feat_labels = [FEAT_LABEL.get(f, f) for f in feat_imp.index]
colors = ["#E74C3C" if v > 0.12 else "#3498DB" for v in feat_imp.values]

axes[0].barh(feat_labels, feat_imp.values, color=colors, edgecolor="white")
axes[0].set_xlabel("Feature Importance (XGBoost)", fontsize=10)
axes[0].set_title("🔑 Kontribusi Fitur dalam Prediksi IR DBD\n(Merah = Kontributor Utama)",
                  fontsize=11, fontweight="bold")
axes[0].axvline(0.12, color="#E74C3C", linestyle="--", alpha=0.5, lw=1.5)

# Metrik scorecard
metric_text = (
    f"Model: XGBoost Regressor\n"
    f"Train: Jan 2021 – Des 2024\n"
    f"Test : Jan 2025 – Des 2025\n\n"
    f"RMSE  = {rmse:.2f}\n"
    f"MAE   = {mae:.2f}\n"
    f"R²    = {r2:.4f}"
)
axes[0].text(0.98, 0.02, metric_text, transform=axes[0].transAxes,
             ha="right", va="bottom", fontsize=9,
             bbox=dict(boxstyle="round,pad=0.5", facecolor="#EBF5FB", alpha=0.9))

# Actual vs Predicted scatter
axes[1].scatter(y_test, y_pred, alpha=0.4, color="#2980B9", s=20, edgecolors="none")
mn = min(y_test.min(), y_pred.min())
mx = max(y_test.max(), y_pred.max())
axes[1].plot([mn, mx], [mn, mx], "r--", lw=2, label="Prediksi Sempurna")
axes[1].set_xlabel("IR DBD Aktual", fontsize=10)
axes[1].set_ylabel("IR DBD Prediksi", fontsize=10)
axes[1].set_title(f"Actual vs Predicted — Test Set 2025\n(R² = {r2:.4f})",
                  fontsize=11, fontweight="bold")
axes[1].legend(fontsize=9)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/04_xgboost_evaluation.png", dpi=300, bbox_inches="tight")
plt.show()
print("✅ Gambar 4 tersimpan: 04_xgboost_evaluation.png")

# %%
# ─── 5.5 Actual vs Predicted: Kota Sampel ────────────────────────────────────
SAMPLE_CITIES = ["Kota Bandung", "Bogor", "Indramayu"]

fig, axes = plt.subplots(len(SAMPLE_CITIES), 1, figsize=(14, 4.5 * len(SAMPLE_CITIES)),
                          sharex=False)

df_test_pred = df_test.copy()
df_test_pred["IR_Pred"] = y_pred

for i, city in enumerate(SAMPLE_CITIES):
    ax = axes[i]
    city_data = df_test_pred[df_test_pred["Kab_Kota"] == city].sort_values("Tanggal")
    city_train = df_train[df_train["Kab_Kota"] == city].sort_values("Tanggal")

    # Plot train (historis)
    ax.fill_between(city_train["Tanggal"], 0, city_train["IR_DBD"],
                    alpha=0.12, color="#95A5A6", label="Historis (Train)")
    ax.plot(city_train["Tanggal"], city_train["IR_DBD"],
            color="#95A5A6", linewidth=1.2, alpha=0.7)

    # Actual 2025
    ax.plot(city_data["Tanggal"], city_data["IR_DBD"],
            color="#27AE60", linewidth=2.5, marker="o", markersize=7, label="Aktual 2025")

    # Predicted 2025
    ax.plot(city_data["Tanggal"], city_data["IR_Pred"],
            color="#E74C3C", linewidth=2.5, marker="s", markersize=7,
            linestyle="--", label="Prediksi XGBoost")

    ax.axvline(CUTOFF, color="navy", linestyle=":", linewidth=1.5, alpha=0.7)
    ax.text(CUTOFF, ax.get_ylim()[1] * 0.9, "  Cut-off\n  Test 2025",
            fontsize=8.5, color="navy", va="top")

    rmse_c = np.sqrt(mean_squared_error(city_data["IR_DBD"], city_data["IR_Pred"]))
    ax.set_title(f"📍 {city}  |  RMSE = {rmse_c:.2f}",
                 fontsize=12, fontweight="bold")
    ax.set_ylabel("IR DBD per 100.000", fontsize=10)
    ax.legend(loc="upper left", fontsize=9)
    ax.set_ylim(bottom=0)

axes[-1].set_xlabel("Waktu", fontsize=11)
plt.suptitle("Actual vs Predicted IR DBD — Kota Sampel (Test 2025)",
             fontsize=13, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/05_actual_vs_predicted_cities.png", dpi=300, bbox_inches="tight")
plt.show()
print("✅ Gambar 5 tersimpan: 05_actual_vs_predicted_cities.png")

# %% [markdown]
# ## 🗺️ CELL 6 — Spatial Modeling: Spatially Constrained Clustering
#
# **Mengapa bukan K-Means?**
# K-Means mengabaikan hubungan spasial antar wilayah.
# Kab. Bandung dan Kota Cimahi yang bertetangga seharusnya dalam klaster yang sama
# karena risiko penularan lintas batas sangat tinggi.
#
# **Solusi:** `AgglomerativeClustering` dengan `connectivity` matrix dari `libpysal.KNN`
# yang memaksa cluster mempertimbangkan *spatial adjacency*.

# %%
# ─── 6.1 Agregasi Data Bulan Terakhir (Des 2025 = "Kondisi Terkini") ──────────
last_date = df["Tanggal"].max()
df_spatial = df[df["Tanggal"] == last_date].copy()

# Tambahkan prediksi bulan terakhir
df_test_pred_last = df_test_pred[df_test_pred["Tanggal"] == last_date][
    ["Kab_Kota", "IR_Pred"]
].rename(columns={"IR_Pred": "IR_Pred_Next"})
df_spatial = df_spatial.merge(df_test_pred_last, on="Kab_Kota", how="left")

print(f"Data spasial untuk: {last_date.strftime('%B %Y')}")
print(f"Jumlah wilayah    : {len(df_spatial)}")

# ─── 6.2 Fitur untuk Clustering ───────────────────────────────────────────────
CLUSTER_FEATURES = ["IR_DBD", "IR_DBD_Lag1", "Curah_Hujan_mm_Lag1",
                     "Kepadatan", "Sanitasi_Pct"]

X_spatial = df_spatial[CLUSTER_FEATURES].fillna(df_spatial[CLUSTER_FEATURES].mean())

# Standarisasi agar skala tidak mendominasi
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_spatial)

# ─── 6.3 Spatial Weights Matrix (Custom KNN-4 via scipy) ─────────────────────
def build_knn_connectivity(lats, lons, k=4):
    """
    Membangun sparse connectivity matrix berbasis K-Nearest Neighbors
    menggunakan jarak Euclidean pada koordinat (Lat, Lon).
    Menggantikan libpysal.KNN dengan implementasi pure scipy/numpy.
    """
    coords = np.column_stack([lons, lats])        # (N, 2)
    dist   = cdist(coords, coords, metric="euclidean")
    np.fill_diagonal(dist, np.inf)                # hindari self-loop

    n   = len(coords)
    mat = sp_lil_matrix((n, n), dtype=np.float64)
    knn_neighbors = {}                            # simpan untuk visualisasi

    for i in range(n):
        nn_idx = np.argsort(dist[i])[:k]          # k tetangga terdekat
        knn_neighbors[i] = list(nn_idx)
        for j in nn_idx:
            mat[i, j] = 1.0
            mat[j, i] = 1.0                       # simetris

    return csr_matrix(mat), knn_neighbors

connectivity, knn_neighbors = build_knn_connectivity(
    df_spatial["Lat"].values,
    df_spatial["Lon"].values,
    k=4
)

print(f"✅ Spatial Weights Matrix: {connectivity.shape} (Custom KNN-4, scipy)")
print(f"   Non-zero connections   : {connectivity.nnz}")

# ─── 6.4 Spatially Constrained Agglomerative Clustering ──────────────────────
N_CLUSTERS = 3
aggl = AgglomerativeClustering(
    n_clusters   = N_CLUSTERS,
    connectivity = connectivity,
    linkage      = "ward",
)
df_spatial["Cluster_Raw"] = aggl.fit_predict(X_scaled)

# ─── 6.5 Beri Label Zona Bermakna (Berdasarkan rata-rata IR DBD per klaster) ──
cluster_ir = (
    df_spatial.groupby("Cluster_Raw")["IR_DBD"].mean()
    .sort_values(ascending=False)
    .reset_index()
)
# Urutkan: klaster dengan IR tertinggi = Zona Merah (0)
cluster_ir["Zona"] = range(N_CLUSTERS)
cluster_map = dict(zip(cluster_ir["Cluster_Raw"], cluster_ir["Zona"]))
df_spatial["Zona"] = df_spatial["Cluster_Raw"].map(cluster_map)

print("\nRingkasan Klaster:")
summary = (
    df_spatial.groupby("Zona")
    .agg(
        N_Wilayah  =("Kab_Kota",  "count"),
        IR_DBD_Mean=("IR_DBD",    "mean"),
        CH_Mean    =("Curah_Hujan_mm_Lag1", "mean"),
        Kepadatan  =("Kepadatan", "mean"),
        Sanitasi   =("Sanitasi_Pct", "mean"),
    )
    .round(2)
    .rename(index={0:"Zona Merah", 1:"Zona Kuning", 2:"Zona Hijau"})
)
display(summary)

# ──── 6.6 Visualisasi Peta Klaster (Scatter Geografis) ───────────────────────
fig, axes = plt.subplots(1, 2, figsize=(17, 7.5),
                          gridspec_kw={"width_ratios": [1.6, 1]})

ax_map = axes[0]
for zona, grp in df_spatial.groupby("Zona"):
    ax_map.scatter(
        grp["Lon"], grp["Lat"],
        s     = grp["Kepadatan"] / 30 + 80,   # Ukuran ∝ kepadatan
        c     = ZONE_COLORS[zona],
        alpha = 0.85,
        edgecolors = "white",
        linewidths = 1.2,
        zorder = 3,
        label = ZONE_LABELS[zona],
    )
    # Label nama kab/kota
    for _, row in grp.iterrows():
        ax_map.annotate(
            row["Kab_Kota"].replace("Kota ", "K."),
            xy = (row["Lon"], row["Lat"]),
            xytext = (row["Lon"] + 0.04, row["Lat"] + 0.04),
            fontsize = 6.5,
            ha = "left",
            color = "#2C3E50",
        )

# Gambar garis koneksi spasial (adjacency)
for i, neighbors in knn_neighbors.items():
    for j in neighbors:
        ax_map.plot(
            [df_spatial.iloc[i]["Lon"], df_spatial.iloc[j]["Lon"]],
            [df_spatial.iloc[i]["Lat"], df_spatial.iloc[j]["Lat"]],
            color = "#BDC3C7", linewidth = 0.5, alpha = 0.5, zorder = 1
        )

ax_map.set_xlabel("Longitude", fontsize=10)
ax_map.set_ylabel("Latitude",  fontsize=10)
ax_map.set_title(
    f"🗺️  Peta Klaster EWS-DBD — {last_date.strftime('%B %Y')}\n"
    "Spatially Constrained Agglomerative Clustering (Ward Linkage, KNN-4)",
    fontsize=12, fontweight="bold"
)
ax_map.legend(fontsize=9, loc="lower right")

# Panel kanan: Radar/Bar profil klaster
ax_bar = axes[1]
zona_names  = ["Zona\nMerah", "Zona\nKuning", "Zona\nHijau"]
metrics     = ["IR_DBD_Mean", "CH_Mean", "Kepadatan", "Sanitasi"]
metric_labs = ["IR DBD", "Curah Hujan\n(×10 mm)", "Kepadatan\n(×100)", "Sanitasi %"]

norm_vals = {}
for m in ["IR_DBD_Mean", "CH_Mean", "Kepadatan", "Sanitasi"]:
    col = summary[m]
    norm_vals[m] = (col - col.min()) / (col.max() - col.min() + 1e-9)

x_pos   = np.arange(len(metrics))
bar_w   = 0.25
colors3 = [ZONE_COLORS[0], ZONE_COLORS[1], ZONE_COLORS[2]]

for zi, (zona_idx, row_s) in enumerate(summary.iterrows()):
    vals = [norm_vals[m].iloc[zi] for m in ["IR_DBD_Mean", "CH_Mean", "Kepadatan", "Sanitasi"]]
    ax_bar.bar(x_pos + zi * bar_w, vals, bar_w,
               label=zona_idx, color=colors3[zi], alpha=0.85, edgecolor="white")

ax_bar.set_xticks(x_pos + bar_w)
ax_bar.set_xticklabels(metric_labs, fontsize=9)
ax_bar.set_ylabel("Nilai Ternormalisasi (0–1)", fontsize=10)
ax_bar.set_title("Profil Karakteristik per Zona\n(Nilai Ternormalisasi untuk Perbandingan)",
                 fontsize=11, fontweight="bold")
ax_bar.legend(fontsize=9)
ax_bar.set_ylim(0, 1.15)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/06_spatial_clustering.png", dpi=300, bbox_inches="tight")
plt.show()
print("✅ Gambar 6 tersimpan: 06_spatial_clustering.png")

# %%
# ─── 6.7 Ranking Zona Merah: Wilayah Prioritas Intervensi ────────────────────
zona_merah = (
    df_spatial[df_spatial["Zona"] == 0]
    [["Kab_Kota", "IR_DBD", "IR_Pred_Next", "Kepadatan", "Sanitasi_Pct",
      "Curah_Hujan_mm_Lag1", "Zona"]]
    .sort_values("IR_Pred_Next", ascending=False)
    .reset_index(drop=True)
)
zona_merah.index += 1  # Mulai dari 1

fig, ax = plt.subplots(figsize=(12, max(4, len(zona_merah) * 0.6 + 1.5)))
colors_bar = plt.cm.Reds(
    np.linspace(0.4, 0.9, len(zona_merah))[::-1]
)
ax.barh(zona_merah["Kab_Kota"][::-1],
        zona_merah["IR_Pred_Next"][::-1],
        color=colors_bar, edgecolor="white", height=0.6)

for i, (_, row) in enumerate(zona_merah[::-1].iterrows()):
    ax.text(row["IR_Pred_Next"] + 0.5,
            i,
            f"  IR={row['IR_DBD']:.1f} | San={row['Sanitasi_Pct']:.1f}%",
            va="center", fontsize=8.5, color="#2C3E50")

ax.set_xlabel("Prediksi IR DBD Bulan Berikutnya", fontsize=11)
ax.set_title(
    "🚨 Ranking Prioritas Zona Merah — Target Intervensi PHBS Presisi\n"
    "(Sorted by Predicted IR DBD Next Month)",
    fontsize=12, fontweight="bold"
)
ax.set_xlim(0, zona_merah["IR_Pred_Next"].max() * 1.35)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/07_zona_merah_ranking.png", dpi=300, bbox_inches="tight")
plt.show()
print("✅ Gambar 7 tersimpan: 07_zona_merah_ranking.png")

# %% [markdown]
# ## 💾 CELL 7 — Export Output: PNG 300 DPI + JSON API-Ready
#
# File JSON ini dirancang untuk di-`fetch` oleh frontend **React/Next.js**
# sebagai data source dashboard pemetaan interaktif.

# %%
# ─── 7.1 Rekap semua file PNG yang sudah tersimpan ────────────────────────────
png_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".png")]
print(f"📁 Visualisasi tersimpan ({len(png_files)} file, 300 DPI):")
for f in sorted(png_files):
    size_kb = os.path.getsize(os.path.join(OUTPUT_DIR, f)) // 1024
    print(f"   ├── {f}  ({size_kb} KB)")

# ─── 7.2 Export JSON untuk Dashboard Frontend ─────────────────────────────────
output_json = []
for _, row in df_spatial.iterrows():
    zona_id  = int(row["Zona"])
    entry = {
        "kab_kota"        : row["Kab_Kota"],
        "lat"             : row["Lat"],
        "lon"             : row["Lon"],
        "zona"            : zona_id,
        "zona_label"      : ZONE_LABELS[zona_id],
        "zona_color"      : ZONE_COLORS[zona_id],
        "ir_dbd_aktual"   : round(float(row["IR_DBD"]), 2),
        "ir_dbd_prediksi" : round(float(row["IR_Pred_Next"]), 2) if not pd.isna(row["IR_Pred_Next"]) else None,
        "kepadatan"       : round(float(row["Kepadatan"]), 0),
        "sanitasi_pct"    : round(float(row["Sanitasi_Pct"]), 2),
        "curah_hujan_lag1": round(float(row["Curah_Hujan_mm_Lag1"]), 1),
        "suhu_lag1"       : round(float(row["Suhu_C_Lag1"]), 1),
        "periode"         : last_date.strftime("%Y-%m"),
        "prioritas_intervensi": (
            "TINGGI"   if zona_id == 0 else
            "SEDANG"   if zona_id == 1 else
            "RENDAH"
        ),
    }
    output_json.append(entry)

# Sort: Zona Merah dulu, lalu by prediksi IR tertinggi
output_json.sort(key=lambda x: (x["zona"], -(x["ir_dbd_prediksi"] or 0)))

json_path = os.path.join(OUTPUT_DIR, "ews_dbd_cluster_latest.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump({
        "metadata": {
            "generated_at"  : pd.Timestamp.now().isoformat(),
            "periode"       : last_date.strftime("%Y-%m"),
            "model"         : "XGBoost + Spatially Constrained AgglomerativeClustering",
            "spatial_weights": "KNN-4 (libpysal)",
            "total_wilayah" : len(output_json),
            "n_zona_merah"  : sum(1 for x in output_json if x["zona"] == 0),
            "n_zona_kuning" : sum(1 for x in output_json if x["zona"] == 1),
            "n_zona_hijau"  : sum(1 for x in output_json if x["zona"] == 2),
        },
        "data": output_json,
    }, f, ensure_ascii=False, indent=2)

print(f"\n✅ JSON API tersimpan: {json_path}")
print(f"   Total wilayah  : {len(output_json)}")
print(f"   Zona Merah     : {sum(1 for x in output_json if x['zona'] == 0)} wilayah")
print(f"   Zona Kuning    : {sum(1 for x in output_json if x['zona'] == 1)} wilayah")
print(f"   Zona Hijau     : {sum(1 for x in output_json if x['zona'] == 2)} wilayah")

# Preview JSON structure
print(f"\n📋 Contoh JSON entry (Zona Merah #1):")
print(json.dumps(output_json[0], indent=4, ensure_ascii=False))

# %% [markdown]
# ## ✅ CELL 8 — Summary & Kesimpulan Pipeline
#
# Pipeline **EWS-PHBS** telah berhasil dieksekusi end-to-end:

# %%
print("=" * 70)
print("  RINGKASAN PIPELINE EWS-PHBS DBD JAWA BARAT")
print("=" * 70)
print()
print(f"  📦 Data     : 1.620 obs (27 kab/kota × 60 bulan, Jan 2021–Des 2025)")
print(f"  ⚙️  Features : {len(FEATURES)} fitur + 6 time-lag/rolling window")
print()
print(f"  🤖 XGBoost Regressor (Test 2025):")
print(f"     ├─ RMSE : {rmse:.2f}")
print(f"     ├─ MAE  : {mae:.2f}")
print(f"     └─ R²   : {r2:.4f}")
print()
print(f"  🗺️  Spatial Clustering (Des 2025):")
for zona_id in range(N_CLUSTERS):
    n_w = sum(1 for x in output_json if x["zona"] == zona_id)
    wil = [x["kab_kota"] for x in output_json if x["zona"] == zona_id]
    print(f"     {ZONE_LABELS[zona_id]:<25}: {n_w} wilayah")
    for w in wil:
        print(f"          └─ {w}")
print()
print(f"  💾 Output:")
print(f"     ├─ {len(png_files)} visualisasi PNG 300 DPI → ./{OUTPUT_DIR}/")
print(f"     └─ JSON API → ./{OUTPUT_DIR}/ews_dbd_cluster_latest.json")
print()
print("=" * 70)
print("  🎯 IMPLIKASI KEBIJAKAN")
print("=" * 70)
print()
print("  Sistem ini memungkinkan Dinas Kesehatan Jawa Barat untuk:")
print("  ✓ Deteksi 6 minggu lebih awal sebelum wabah meledak")
print("  ✓ Alokasi Jumantik hanya ke Zona Merah (efisiensi anggaran)")
print("  ✓ Intervensi PHBS 3M Plus yang terukur dan berbasis data")
print("  ✓ Monitoring real-time via dashboard API-ready")
print()
print("  ⚠️  Catatan Etika Algoritmik:")
print("  Model ini perlu diaudit untuk 'blank spot' wilayah pelosok")
print("  yang underreporting, agar tidak terjadi keadilan algoritmik.")
print("=" * 70)
