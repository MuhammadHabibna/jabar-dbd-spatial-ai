import MetricCards from "./MetricCards";
import MapPlaceholder from "./MapPlaceholder";
import AlertLog from "./AlertLog";
import { Shield } from "lucide-react";

export default function OverviewPage() {
  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Shield className="w-5 h-5 text-blue-500" />
            <h1 className="text-xl font-bold text-slate-900 dark:text-white">Dashboard Eksekutif</h1>
          </div>
          <p className="text-slate-500 dark:text-slate-400 text-sm">
            Sistem Peringatan Dini DBD · Jawa Barat · Data per Desember 2025
          </p>
        </div>
        <div className="text-right">
          <span className="inline-flex items-center gap-1.5 text-xs bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 px-3 py-1.5 rounded-full font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
            Model: XGBoost R²=0.9317
          </span>
        </div>
      </div>

      {/* KPI Cards */}
      <MetricCards />

      {/* Map + Alerts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <MapPlaceholder />
        </div>
        <div className="lg:col-span-1 flex flex-col">
          {/* Zona summary mini */}
          <div className="grid grid-cols-3 gap-2 mb-4">
            {[
              { label: "Zona Merah", n: 2,  color: "red",   border: "border-red-500/30",   bg: "bg-red-500/10",   text: "text-red-500" },
              { label: "Zona Kuning", n: 18, color: "amber", border: "border-amber-500/30", bg: "bg-amber-500/10", text: "text-amber-500" },
              { label: "Zona Hijau", n: 7,  color: "green", border: "border-green-500/30", bg: "bg-green-500/10", text: "text-emerald-500" },
            ].map((z) => (
              <div key={z.label} className={`rounded-xl border ${z.border} ${z.bg} p-3 text-center`}>
                <p className={`text-2xl font-bold ${z.text}`}>{z.n}</p>
                <p className="text-slate-500 text-[10px] leading-tight mt-0.5">{z.label}</p>
              </div>
            ))}
          </div>
          <AlertLog />
        </div>
      </div>

      {/* Footer note */}
      <p className="text-slate-400 dark:text-slate-600 text-[11px] text-center">
        AIDES Jawa Barat · Model: Spatially Constrained Agglomerative Clustering (Ward, KNN-4) + XGBoost Regressor ·
        Sumber data: BPS Jawa Barat & NASA POWER MERRA-2 (2021–2025)
      </p>
    </div>
  );
}
