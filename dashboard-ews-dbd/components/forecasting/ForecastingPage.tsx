import ForecastChart from "./ForecastChart";
import FeatureImportance from "./FeatureImportance";
import RecommendationPanel from "./RecommendationPanel";
import { TrendingUp } from "lucide-react";

export default function ForecastingPage() {
  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      <div>
        <div className="flex items-center gap-2 mb-1">
          <TrendingUp className="w-5 h-5 text-blue-500" />
          <h1 className="text-xl font-bold text-slate-900 dark:text-white">Proyeksi Temporal XGBoost</h1>
        </div>
        <p className="text-slate-500 dark:text-slate-400 text-sm">
          Time-Series Forecasting · Fitur Time-Lag Iklim · Jan–Jun 2026 · Resolusi Bulanan
        </p>
      </div>

      {/* Model stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { label: "R² Score", value: "0.9317", desc: "Sangat baik (>0.9)", color: "emerald" },
          { label: "RMSE", value: "11.20", desc: "Error rata-rata", color: "blue" },
          { label: "MAE", value: "8.45", desc: "Mean Absolute Error", color: "blue" },
          { label: "Fitur Terbaik", value: "IR Lag-1", desc: "Kontribusi 28.7%", color: "amber" },
        ].map(s => (
          <div key={s.label} className={`bg-${s.color}-500/5 border border-${s.color}-500/20 rounded-xl p-3 text-center`}>
            <p className={`text-lg font-bold text-${s.color}-500`}>{s.value}</p>
            <p className="text-slate-500 text-[10px] font-semibold uppercase tracking-wider">{s.label}</p>
            <p className="text-slate-400 text-[10px] mt-0.5">{s.desc}</p>
          </div>
        ))}
      </div>

      {/* Forecast Chart */}
      <ForecastChart />

      {/* Feature Importance + Recommendation */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <FeatureImportance />
        <RecommendationPanel />
      </div>

      {/* Time-lag explanation */}
      <div className="bg-blue-500/5 border border-blue-500/20 rounded-xl px-5 py-4">
        <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
          <span className="font-semibold text-blue-400">💧 Mengapa Time-Lag?</span> Nyamuk{" "}
          <span className="italic">Aedes aegypti</span> membutuhkan <span className="font-medium text-slate-700 dark:text-slate-300">1–2 bulan</span> dari fase telur hingga menjadi nyamuk dewasa infeksius.
          Lonjakan curah hujan bulan Oktober → November (mengisi breeding site) → baru menghasilkan wabah DBD bulan Desember–Januari.
          Dengan memasukkan fitur <span className="font-medium text-slate-700 dark:text-slate-300">Curah_Hujan_Lag1 dan Lag2</span>, model XGBoost menangkap pola ini secara presisi,
          memungkinkan Dinas Kesehatan mendapat alarm <span className="font-medium text-blue-400">6 minggu lebih awal</span> sebelum wabah meledak.
        </p>
      </div>
    </div>
  );
}
