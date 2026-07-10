"use client";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Legend, ReferenceLine, Area, ComposedChart,
} from "recharts";
import { forecastData } from "@/lib/data";

// Extend with CI bounds (±12%)
const dataWithCI = forecastData.map(d => ({
  ...d,
  merah_hi:  parseFloat((d.merah * 1.12).toFixed(1)),
  merah_lo:  parseFloat((d.merah * 0.88).toFixed(1)),
  kuning_hi: parseFloat((d.kuning * 1.12).toFixed(1)),
  kuning_lo: parseFloat((d.kuning * 0.88).toFixed(1)),
  hijau_hi:  parseFloat((d.hijau * 1.12).toFixed(1)),
  hijau_lo:  parseFloat((d.hijau * 0.88).toFixed(1)),
}));

const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null;
  const vals: Record<string, number> = {};
  payload.forEach((p: any) => { vals[p.dataKey] = p.value; });
  return (
    <div className="bg-slate-900 border border-slate-700 rounded-xl p-3 shadow-2xl text-xs min-w-[180px]">
      <p className="font-bold text-white mb-2">{label}</p>
      {[["merah","#E74C3C","Zona Merah"],["kuning","#F39C12","Zona Kuning"],["hijau","#27AE60","Zona Hijau"]].map(([z,c,lbl]) => (
        vals[z] !== undefined && (
          <div key={z} className="flex items-center justify-between gap-4 mb-1">
            <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full" style={{background:c}}/><span className="text-slate-400">{lbl}</span></span>
            <span className="font-bold" style={{color:c}}>{vals[z]?.toFixed(1)}</span>
          </div>
        )
      ))}
      <p className="text-slate-600 text-[9px] mt-1.5 border-t border-slate-700 pt-1.5">±12% confidence interval</p>
    </div>
  );
};

export default function ForecastChart() {
  return (
    <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5">
      <div className="mb-4 flex items-start justify-between">
        <div>
          <h3 className="font-semibold text-slate-900 dark:text-white text-sm">Proyeksi IR DBD — Jan s/d Jun 2026</h3>
          <p className="text-slate-400 text-xs mt-0.5">XGBoost Regressor · Time-Lag Features · Resolusi Bulanan · CI ±12%</p>
        </div>
        <span className="text-[10px] bg-blue-500/10 text-blue-400 border border-blue-500/20 px-2.5 py-1 rounded-full font-medium">
          Tren: TURUN di semua zona
        </span>
      </div>
      <ResponsiveContainer width="100%" height={320}>
        <ComposedChart data={dataWithCI} margin={{ top: 10, right: 20, bottom: 20, left: 10 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" opacity={0.5} />
          <XAxis dataKey="periode" tick={{ fontSize: 10, fill: "#64748b" }}
            label={{ value: "Periode Proyeksi", position: "insideBottom", offset: -14, fontSize: 11, fill: "#64748b" }} />
          <YAxis domain={[100, 340]} tick={{ fontSize: 10, fill: "#64748b" }}
            label={{ value: "IR DBD per 100.000", angle: -90, position: "insideLeft", offset: 15, fontSize: 11, fill: "#64748b" }} />
          <Tooltip content={<CustomTooltip />} />
          <Legend wrapperStyle={{ fontSize: 11, paddingTop: 16 }}
            formatter={(v) => ({ merah:"Zona Merah", kuning:"Zona Kuning", hijau:"Zona Hijau", merah_hi:"", merah_lo:"", kuning_hi:"", kuning_lo:"", hijau_hi:"", hijau_lo:"" }[v] ?? "")}/>

          {/* CI areas */}
          <Area dataKey="merah_hi"  fill="#E74C3C" fillOpacity={0.06} stroke="none" legendType="none" />
          <Area dataKey="merah_lo"  fill="#ffffff" fillOpacity={1}    stroke="none" legendType="none" />
          <Area dataKey="kuning_hi" fill="#F39C12" fillOpacity={0.06} stroke="none" legendType="none" />
          <Area dataKey="kuning_lo" fill="#ffffff" fillOpacity={1}    stroke="none" legendType="none" />
          <Area dataKey="hijau_hi"  fill="#27AE60" fillOpacity={0.06} stroke="none" legendType="none" />
          <Area dataKey="hijau_lo"  fill="#ffffff" fillOpacity={1}    stroke="none" legendType="none" />

          {/* Main lines */}
          <Line dataKey="merah"  name="merah"  stroke="#E74C3C" strokeWidth={2.5} dot={{ r:5, fill:"#E74C3C", stroke:"#fff", strokeWidth:2 }} activeDot={{ r:7 }} />
          <Line dataKey="kuning" name="kuning" stroke="#F39C12" strokeWidth={2.5} dot={{ r:5, fill:"#F39C12", stroke:"#fff", strokeWidth:2 }} activeDot={{ r:7 }} />
          <Line dataKey="hijau"  name="hijau"  stroke="#27AE60" strokeWidth={2.5} dot={{ r:5, fill:"#27AE60", stroke:"#fff", strokeWidth:2 }} activeDot={{ r:7 }} />

          {/* Threshold line */}
          <ReferenceLine y={100} stroke="#e74c3c" strokeDasharray="6 3" strokeWidth={1.5}
            label={{ value: "Ambang Wabah (100)", position: "insideTopRight", fontSize: 10, fill: "#e74c3c" }} />
        </ComposedChart>
      </ResponsiveContainer>
      <div className="mt-3 grid grid-cols-3 gap-2 text-center text-[10px]">
        {[
          { zona: "Zona Merah", jan: 265.1, jun: 231.3, color: "red" },
          { zona: "Zona Kuning", jan: 202.5, jun: 179.0, color: "amber" },
          { zona: "Zona Hijau", jan: 178.9, jun: 158.8, color: "green" },
        ].map(z => (
          <div key={z.zona} className={`bg-${z.color}-500/5 border border-${z.color}-500/20 rounded-lg p-2`}>
            <p className="text-slate-500">{z.zona}</p>
            <p className="font-bold text-slate-700 dark:text-slate-300">{z.jan} → {z.jun}</p>
            <p className="text-slate-400">Jan → Jun</p>
          </div>
        ))}
      </div>
    </div>
  );
}
