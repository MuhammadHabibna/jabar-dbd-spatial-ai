"use client";
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend, Tooltip } from "recharts";
import { radarData } from "@/lib/data";

const ZONA_COLORS = { merah: "#E74C3C", kuning: "#F39C12", hijau: "#27AE60" };

export default function RadarComparison() {
  return (
    <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5">
      <div className="mb-4">
        <h3 className="font-semibold text-slate-900 dark:text-white text-sm">Radar Profil Klaster</h3>
        <p className="text-slate-400 text-xs mt-0.5">Perbandingan 3 Zona · Nilai ternormalisasi 0–100</p>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <RadarChart data={radarData} outerRadius={110}>
          <PolarGrid stroke="#1e293b" />
          <PolarAngleAxis dataKey="metric" tick={{ fontSize: 11, fill: "#94a3b8", fontWeight: 500 }} />
          <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fontSize: 9, fill: "#475569" }} tickCount={4} />
          <Radar name="Zona Merah" dataKey="merah" stroke={ZONA_COLORS.merah} fill={ZONA_COLORS.merah} fillOpacity={0.2} strokeWidth={2} />
          <Radar name="Zona Kuning" dataKey="kuning" stroke={ZONA_COLORS.kuning} fill={ZONA_COLORS.kuning} fillOpacity={0.15} strokeWidth={2} />
          <Radar name="Zona Hijau" dataKey="hijau" stroke={ZONA_COLORS.hijau} fill={ZONA_COLORS.hijau} fillOpacity={0.15} strokeWidth={2} />
          <Legend wrapperStyle={{ fontSize: 11 }} formatter={(v) => <span style={{ color: "#94a3b8" }}>{v}</span>} />
          <Tooltip contentStyle={{ background: "#0f172a", border: "1px solid #334155", borderRadius: 8, fontSize: 11 }}
            labelStyle={{ color: "#e2e8f0", fontWeight: 600 }} itemStyle={{ color: "#94a3b8" }} />
        </RadarChart>
      </ResponsiveContainer>
      <div className="mt-3 grid grid-cols-3 gap-2 text-center text-[10px] text-slate-500">
        <div className="bg-red-500/5 border border-red-500/20 rounded-lg p-2">
          <p className="text-red-400 font-bold text-sm">90</p>
          <p>Risiko Zona Merah</p>
        </div>
        <div className="bg-amber-500/5 border border-amber-500/20 rounded-lg p-2">
          <p className="text-amber-400 font-bold text-sm">62</p>
          <p>Risiko Zona Kuning</p>
        </div>
        <div className="bg-green-500/5 border border-green-500/20 rounded-lg p-2">
          <p className="text-emerald-400 font-bold text-sm">38</p>
          <p>Risiko Zona Hijau</p>
        </div>
      </div>
    </div>
  );
}
