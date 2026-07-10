// lib/data.ts - Mock data untuk Dashboard AIDES Jawa Barat

export type ZonaType = "merah" | "kuning" | "hijau";

export interface KabKotaData {
  id: number;
  nama: string;
  lat: number;
  lon: number;
  zona: ZonaType;
  zona_label: string;
  zona_color: string;
  ir_dbd: number;
  ir_prediksi: number;
  kepadatan: number;
  sanitasi: number;
  curah_hujan: number;
  ch_lag1: number;
  suhu: number;
  prioritas: "TINGGI" | "SEDANG" | "RENDAH";
}

export const kabKotaData: KabKotaData[] = [
  { id: 1, nama: "Kota Bandung", lat: -6.914, lon: 107.609, zona: "merah", zona_label: "Zona Merah", zona_color: "#E74C3C", ir_dbd: 298.34, ir_prediksi: 306.20, kepadatan: 15396, sanitasi: 55.00, curah_hujan: 4445, ch_lag1: 4727, suhu: 21.3, prioritas: "TINGGI" },
  { id: 2, nama: "Kota Cimahi", lat: -6.884, lon: 107.543, zona: "merah", zona_label: "Zona Merah", zona_color: "#E74C3C", ir_dbd: 281.83, ir_prediksi: 276.23, kepadatan: 14860, sanitasi: 83.87, curah_hujan: 4321, ch_lag1: 4519, suhu: 21.1, prioritas: "TINGGI" },
  { id: 3, nama: "Kota Bekasi", lat: -6.238, lon: 106.975, zona: "kuning", zona_label: "Zona Kuning", zona_color: "#F39C12", ir_dbd: 260.39, ir_prediksi: 253.06, kepadatan: 12881, sanitasi: 99.50, curah_hujan: 3527, ch_lag1: 3921, suhu: 27.5, prioritas: "SEDANG" },
  { id: 4, nama: "Kota Sukabumi", lat: -6.918, lon: 106.927, zona: "kuning", zona_label: "Zona Kuning", zona_color: "#F39C12", ir_dbd: 258.06, ir_prediksi: 261.33, kepadatan: 7599, sanitasi: 42.76, curah_hujan: 4024, ch_lag1: 4384, suhu: 23.3, prioritas: "SEDANG" },
  { id: 5, nama: "Kota Tasikmalaya", lat: -7.327, lon: 108.219, zona: "kuning", zona_label: "Zona Kuning", zona_color: "#F39C12", ir_dbd: 249.02, ir_prediksi: 271.81, kepadatan: 4372, sanitasi: 56.80, curah_hujan: 4389, ch_lag1: 4930, suhu: 24.1, prioritas: "SEDANG" },
  { id: 6, nama: "Tasikmalaya", lat: -7.353, lon: 108.224, zona: "kuning", zona_label: "Zona Kuning", zona_color: "#F39C12", ir_dbd: 244.34, ir_prediksi: 241.49, kepadatan: 756, sanitasi: 54.59, curah_hujan: 4435, ch_lag1: 5055, suhu: 24.6, prioritas: "SEDANG" },
  { id: 7, nama: "Kota Bogor", lat: -6.597, lon: 106.806, zona: "kuning", zona_label: "Zona Kuning", zona_color: "#F39C12", ir_dbd: 242.49, ir_prediksi: 247.67, kepadatan: 9263, sanitasi: 79.77, curah_hujan: 3422, ch_lag1: 4034, suhu: 24.8, prioritas: "SEDANG" },
  { id: 8, nama: "Bandung", lat: -7.021, lon: 107.57, zona: "kuning", zona_label: "Zona Kuning", zona_color: "#F39C12", ir_dbd: 238.72, ir_prediksi: 229.26, kepadatan: 2188, sanitasi: 69.76, curah_hujan: 4224, ch_lag1: 4489, suhu: 21.6, prioritas: "SEDANG" },
  { id: 9, nama: "Kota Banjar", lat: -7.365, lon: 108.538, zona: "kuning", zona_label: "Zona Kuning", zona_color: "#F39C12", ir_dbd: 237.49, ir_prediksi: 201.35, kepadatan: 1875, sanitasi: 86.50, curah_hujan: 3523, ch_lag1: 3784, suhu: 25.1, prioritas: "SEDANG" },
  { id: 10, nama: "Ciamis", lat: -7.329, lon: 108.351, zona: "kuning", zona_label: "Zona Kuning", zona_color: "#F39C12", ir_dbd: 235.26, ir_prediksi: 241.99, kepadatan: 859, sanitasi: 72.20, curah_hujan: 4611, ch_lag1: 4905, suhu: 24.6, prioritas: "SEDANG" },
  { id: 11, nama: "Kota Depok", lat: -6.401, lon: 106.819, zona: "kuning", zona_label: "Zona Kuning", zona_color: "#F39C12", ir_dbd: 234.18, ir_prediksi: 245.60, kepadatan: 10824, sanitasi: 99.50, curah_hujan: 3611, ch_lag1: 4096, suhu: 24.6, prioritas: "SEDANG" },
  { id: 12, nama: "Cianjur", lat: -6.822, lon: 107.139, zona: "kuning", zona_label: "Zona Kuning", zona_color: "#F39C12", ir_dbd: 234.14, ir_prediksi: 215.01, kepadatan: 686, sanitasi: 63.01, curah_hujan: 3979, ch_lag1: 4333, suhu: 23.9, prioritas: "SEDANG" },
  { id: 13, nama: "Bogor", lat: -6.595, lon: 106.816, zona: "kuning", zona_label: "Zona Kuning", zona_color: "#F39C12", ir_dbd: 225.19, ir_prediksi: 198.08, kepadatan: 2036, sanitasi: 68.17, curah_hujan: 3282, ch_lag1: 3915, suhu: 24.8, prioritas: "SEDANG" },
  { id: 14, nama: "Bandung Barat", lat: -6.917, lon: 107.425, zona: "kuning", zona_label: "Zona Kuning", zona_color: "#F39C12", ir_dbd: 219.37, ir_prediksi: 218.41, kepadatan: 1463, sanitasi: 68.29, curah_hujan: 4139, ch_lag1: 4455, suhu: 20.9, prioritas: "SEDANG" },
  { id: 15, nama: "Sukabumi", lat: -6.918, lon: 106.929, zona: "kuning", zona_label: "Zona Kuning", zona_color: "#F39C12", ir_dbd: 214.24, ir_prediksi: 215.67, kepadatan: 708, sanitasi: 71.66, curah_hujan: 4035, ch_lag1: 4216, suhu: 24.0, prioritas: "SEDANG" },
  { id: 16, nama: "Purwakarta", lat: -6.556, lon: 107.443, zona: "kuning", zona_label: "Zona Kuning", zona_color: "#F39C12", ir_dbd: 210.49, ir_prediksi: 203.60, kepadatan: 1134, sanitasi: 77.77, curah_hujan: 3597, ch_lag1: 4030, suhu: 24.8, prioritas: "SEDANG" },
  { id: 17, nama: "Bekasi", lat: -6.374, lon: 107.13, zona: "kuning", zona_label: "Zona Kuning", zona_color: "#F39C12", ir_dbd: 205.12, ir_prediksi: 217.73, kepadatan: 2690, sanitasi: 85.03, curah_hujan: 3691, ch_lag1: 4053, suhu: 24.8, prioritas: "SEDANG" },
  { id: 18, nama: "Garut", lat: -7.212, lon: 107.906, zona: "kuning", zona_label: "Zona Kuning", zona_color: "#F39C12", ir_dbd: 198.67, ir_prediksi: 202.11, kepadatan: 903, sanitasi: 48.68, curah_hujan: 3478, ch_lag1: 3788, suhu: 23.1, prioritas: "SEDANG" },
  { id: 19, nama: "Karawang", lat: -6.321, lon: 107.339, zona: "kuning", zona_label: "Zona Kuning", zona_color: "#F39C12", ir_dbd: 195.32, ir_prediksi: 203.30, kepadatan: 1506, sanitasi: 82.27, curah_hujan: 3470, ch_lag1: 4255, suhu: 25.7, prioritas: "SEDANG" },
  { id: 20, nama: "Pangandaran", lat: -7.689, lon: 108.65, zona: "kuning", zona_label: "Zona Kuning", zona_color: "#F39C12", ir_dbd: 181.06, ir_prediksi: 182.45, kepadatan: 418, sanitasi: 86.42, curah_hujan: 3263, ch_lag1: 3828, suhu: 25.7, prioritas: "SEDANG" },
  { id: 21, nama: "Majalengka", lat: -6.836, lon: 108.228, zona: "hijau", zona_label: "Zona Hijau", zona_color: "#27AE60", ir_dbd: 223.49, ir_prediksi: 181.73, kepadatan: 1103, sanitasi: 85.57, curah_hujan: 3370, ch_lag1: 3680, suhu: 22.6, prioritas: "RENDAH" },
  { id: 22, nama: "Kota Cirebon", lat: -6.706, lon: 108.557, zona: "hijau", zona_label: "Zona Hijau", zona_color: "#27AE60", ir_dbd: 218.25, ir_prediksi: 240.13, kepadatan: 9361, sanitasi: 96.88, curah_hujan: 3124, ch_lag1: 3516, suhu: 27.5, prioritas: "RENDAH" },
  { id: 23, nama: "Subang", lat: -6.571, lon: 107.762, zona: "hijau", zona_label: "Zona Hijau", zona_color: "#27AE60", ir_dbd: 191.75, ir_prediksi: 198.98, kepadatan: 859, sanitasi: 91.44, curah_hujan: 3564, ch_lag1: 3942, suhu: 25.2, prioritas: "RENDAH" },
  { id: 24, nama: "Cirebon", lat: -6.761, lon: 108.476, zona: "hijau", zona_label: "Zona Hijau", zona_color: "#27AE60", ir_dbd: 187.54, ir_prediksi: 186.24, kepadatan: 2294, sanitasi: 89.23, curah_hujan: 3157, ch_lag1: 3554, suhu: 24.9, prioritas: "RENDAH" },
  { id: 25, nama: "Kuningan", lat: -6.975, lon: 108.48, zona: "hijau", zona_label: "Zona Hijau", zona_color: "#27AE60", ir_dbd: 187.13, ir_prediksi: 182.26, kepadatan: 1046, sanitasi: 85.67, curah_hujan: 3107, ch_lag1: 3628, suhu: 24.8, prioritas: "RENDAH" },
  { id: 26, nama: "Sumedang", lat: -6.855, lon: 107.92, zona: "hijau", zona_label: "Zona Hijau", zona_color: "#27AE60", ir_dbd: 182.34, ir_prediksi: 188.17, kepadatan: 784, sanitasi: 91.87, curah_hujan: 3503, ch_lag1: 3884, suhu: 23.2, prioritas: "RENDAH" },
  { id: 27, nama: "Indramayu", lat: -6.327, lon: 108.324, zona: "hijau", zona_label: "Zona Hijau", zona_color: "#27AE60", ir_dbd: 182.14, ir_prediksi: 188.43, kepadatan: 944, sanitasi: 94.83, curah_hujan: 3317, ch_lag1: 3553, suhu: 26.4, prioritas: "RENDAH" }
];

// Proyeksi 6 bulan Jan-Jun 2026
export const forecastData = [
  { periode: "Jan 2026", merah: 265.1, kuning: 202.5, hijau: 178.9 },
  { periode: "Feb 2026", merah: 252.8, kuning: 180.5, hijau: 157.1 },
  { periode: "Mar 2026", merah: 223.0, kuning: 164.6, hijau: 144.7 },
  { periode: "Apr 2026", merah: 207.8, kuning: 158.7, hijau: 140.0 },
  { periode: "Mei 2026", merah: 218.0, kuning: 164.6, hijau: 144.7 },
  { periode: "Jun 2026", merah: 231.3, kuning: 179.0, hijau: 158.8 },
];

// Feature importance XGBoost
export const featureImportance = [
  { feature: "IR DBD Lag-1 (Autoregresif)", nilai: 0.287, color: "#E74C3C" },
  { feature: "Curah Hujan Lag-1", nilai: 0.198, color: "#E74C3C" },
  { feature: "Kepadatan Penduduk", nilai: 0.167, color: "#E74C3C" },
  { feature: "Curah Hujan Roll-3 bln", nilai: 0.124, color: "#3498DB" },
  { feature: "Sanitasi Layak (%)", nilai: 0.098, color: "#3498DB" },
  { feature: "Curah Hujan Lag-2", nilai: 0.062, color: "#95A5A6" },
  { feature: "Suhu Udara", nilai: 0.034, color: "#95A5A6" },
  { feature: "Suhu Lag-1", nilai: 0.019, color: "#95A5A6" },
  { feature: "Musim (Bulan)", nilai: 0.011, color: "#95A5A6" },
];

// EWS Alerts
export const ewsAlerts = [
  {
    id: 1, level: "KRITIS", color: "red",
    waktu: "10 Jul 2026, 14:22",
    pesan: "Lonjakan CH di Kota Bandung: 4.727mm (Lag-1). Potensi episentrum dalam 30 hari.",
    wilayah: "Kota Bandung",
  },
  {
    id: 2, level: "KRITIS", color: "red",
    waktu: "10 Jul 2026, 14:22",
    pesan: "IR DBD Kota Cimahi: 281.83/100rb — melampaui ambang wabah nasional (100/100rb).",
    wilayah: "Kota Cimahi",
  },
  {
    id: 3, level: "WASPADA", color: "yellow",
    waktu: "09 Jul 2026, 08:15",
    pesan: "Sanitasi Kota Sukabumi (42.76%) di bawah rata-rata Jawa Barat. Risiko breeding site tinggi.",
    wilayah: "Kota Sukabumi",
  },
  {
    id: 4, level: "WASPADA", color: "yellow",
    waktu: "08 Jul 2026, 16:40",
    pesan: "18 wilayah Zona Kuning terdeteksi. Monitoring mingguan diaktifkan otomatis.",
    wilayah: "18 Kab/Kota",
  },
  {
    id: 5, level: "INFO", color: "blue",
    waktu: "07 Jul 2026, 09:00",
    pesan: "Model XGBoost diperbarui. Akurasi test set 2025: R²=0.9317, RMSE=11.20.",
    wilayah: "Sistem",
  },
];

// Radar data per zona
export const radarData = [
  { metric: "IR DBD", merah: 95, kuning: 72, hijau: 58 },
  { metric: "Kepadatan", merah: 98, kuning: 45, hijau: 30 },
  { metric: "Sanitasi\n(invers)", merah: 78, kuning: 52, hijau: 20 },
  { metric: "CH Lag-1", merah: 92, kuning: 78, hijau: 60 },
  { metric: "Risiko\nKomposit", merah: 90, kuning: 62, hijau: 38 },
];

// Statistik ringkasan
export const zonaSummary = {
  merah:  { n: 2,  ir_mean: 290.08, kepadatan_mean: 15128, sanitasi_mean: 69.44 },
  kuning: { n: 18, ir_mean: 226.86, kepadatan_mean: 3453,  sanitasi_mean: 72.93 },
  hijau:  { n: 7,  ir_mean: 196.09, kepadatan_mean: 2342,  sanitasi_mean: 90.78 },
};
