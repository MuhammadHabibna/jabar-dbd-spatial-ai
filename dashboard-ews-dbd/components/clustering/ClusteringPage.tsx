import ClusterScatter from "./ClusterScatter";
import RadarComparison from "./RadarComparison";
import DataTable from "./DataTable";
import { Network } from "lucide-react";

export default function ClusteringPage() {
  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      <div>
        <div className="flex items-center gap-2 mb-1">
          <Network className="w-5 h-5 text-purple-500" />
          <h1 className="text-xl font-bold text-slate-900 dark:text-white">Analisis Kerawanan Spasial</h1>
        </div>
        <p className="text-slate-500 dark:text-slate-400 text-sm">
          Spatially Constrained Agglomerative Clustering · Ward Linkage · KNN-4 · Desember 2025
        </p>
      </div>

      {/* Methodology note */}
      <div className="bg-purple-500/5 border border-purple-500/20 rounded-xl px-5 py-3 flex items-start gap-3">
        <span className="text-purple-400 text-lg mt-0.5">🧠</span>
        <div className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
          <span className="font-semibold text-purple-400">Metodologi:</span> Berbeda dengan K-Means biasa, model ini menggunakan{" "}
          <span className="font-medium text-slate-700 dark:text-slate-300">Agglomerative Clustering dengan Spatial Connectivity Matrix (KNN-4)</span>{" "}
          yang memaksa klaster mempertimbangkan kedekatan geografis. Artinya, Kota Bandung dan Cimahi yang bertetangga
          diperlakukan sebagai episentrum tunggal — mencerminkan realita risiko penularan lintas batas wilayah.
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        <div className="lg:col-span-3">
          <ClusterScatter />
        </div>
        <div className="lg:col-span-2">
          <RadarComparison />
        </div>
      </div>

      {/* Data Table */}
      <DataTable />
    </div>
  );
}
