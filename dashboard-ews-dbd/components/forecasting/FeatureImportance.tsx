"use client";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { featureImportance } from "@/lib/data";

const data = [...featureImportance].sort((a, b) => a.nilai - b.nilai);

const CustomTooltip = ({ active, payload }: any) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="bg-slate-900 border border-slate-700 rounded-xl p-3 text-xs shadow-2xl">
      <p className="text-white font-semibold mb-1">{payload[0].payload.feature}</p>
      <p className="text-slate-400">Importance Score: <span className="text-blue-400 font-bold">{(payload[0].value * 100).toFixed(1)}%</span></p>
    </div>
  );
};

export default function FeatureImportance() {
  const maxVal = Math.max(...data.map(d => d.nilai));
  return (
    <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5">
      <div className="mb-4">
        <h3 className="font-semibold text-slate-900 dark:text-white text-sm">Kontribusi Fitur (XGBoost)</h3>
        <p className="text-slate-400 text-xs mt-0.5">Feature importance score — semakin tinggi, semakin berpengaruh pada prediksi IR DBD</p>
      </div>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data} layout="vertical" margin={{ top: 0, right: 30, bottom: 0, left: 8 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" horizontal={false} opacity={0.5} />
          <XAxis type="number" tick={{ fontSize: 9, fill: "#64748b" }}
            tickFormatter={v => `${(v*100).toFixed(0)}%`} domain={[0, maxVal * 1.1]} />
          <YAxis type="category" dataKey="feature" width={155} tick={{ fontSize: 10, fill: "#94a3b8" }} />
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="nilai" radius={[0, 4, 4, 0]} maxBarSize={18}>
            {data.map((entry, i) => (
              <Cell key={i} fill={entry.nilai > 0.15 ? "#E74C3C" : entry.nilai > 0.08 ? "#3B82F6" : "#64748b"} fillOpacity={0.85} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <div className="mt-3 flex gap-3 text-[10px]">
        <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-sm bg-red-500"/><span className="text-slate-500">Utama (&gt;15%)</span></span>
        <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-sm bg-blue-500"/><span className="text-slate-500">Pendukung (8–15%)</span></span>
        <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-sm bg-slate-500"/><span className="text-slate-500">Sekunder (&lt;8%)</span></span>
      </div>
    </div>
  );
}
