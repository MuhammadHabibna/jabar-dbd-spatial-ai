"use client";
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, Legend, ZAxis } from "recharts";
import { kabKotaData } from "@/lib/data";

const ZONA_COLORS = { merah: "#E74C3C", kuning: "#F39C12", hijau: "#27AE60" };
const ZONA_LABELS = { merah: "Zona Merah (Rawan)", kuning: "Zona Kuning (Waspada)", hijau: "Zona Hijau (Aman)" };

const CustomTooltip = ({ active, payload }: any) => {
  if (!active || !payload?.length) return null;
  const d = payload[0].payload;
  return (
    <div className="bg-slate-900 border border-slate-700 rounded-xl p-3 shadow-2xl text-xs max-w-[200px]">
      <p className="font-bold text-white mb-2">{d.nama}</p>
      <div className="space-y-1 text-slate-300">
        <p>IR DBD: <span className="text-white font-semibold">{d.ir_dbd.toFixed(1)}</span>/100rb</p>
        <p>Kepadatan: <span className="text-white font-semibold">{d.kepadatan.toLocaleString()}</span> jiwa/km²</p>
        <p>Sanitasi: <span className="text-white font-semibold">{d.sanitasi.toFixed(1)}%</span></p>
        <p>CH Lag-1: <span className="text-white font-semibold">{d.ch_lag1.toFixed(0)}</span> mm</p>
      </div>
      <div className="mt-2 pt-2 border-t border-slate-700">
        <span className="px-2 py-0.5 rounded-full text-[10px] font-bold"
          style={{ background: ZONA_COLORS[d.zona as keyof typeof ZONA_COLORS] + "30",
                   color: ZONA_COLORS[d.zona as keyof typeof ZONA_COLORS] }}>
          {ZONA_LABELS[d.zona as keyof typeof ZONA_LABELS]}
        </span>
      </div>
    </div>
  );
};

export default function ClusterScatter() {
  // Group by zona for separate Scatter components (to get legend)
  const byZona = {
    merah:  kabKotaData.filter(d => d.zona === "merah"),
    kuning: kabKotaData.filter(d => d.zona === "kuning"),
    hijau:  kabKotaData.filter(d => d.zona === "hijau"),
  };

  return (
    <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5">
      <div className="mb-4">
        <h3 className="font-semibold text-slate-900 dark:text-white text-sm">Scatter Plot Klaster Spasial</h3>
        <p className="text-slate-400 text-xs mt-0.5">Kepadatan Penduduk vs IR DBD · Ukuran titik = Curah Hujan Lag-1 · Warna = Zona</p>
      </div>
      <ResponsiveContainer width="100%" height={340}>
        <ScatterChart margin={{ top: 10, right: 20, bottom: 20, left: 10 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" opacity={0.5} />
          <XAxis dataKey="kepadatan" name="Kepadatan" type="number"
            label={{ value: "Kepadatan Penduduk (jiwa/km²)", position: "insideBottom", offset: -12, fontSize: 11, fill: "#64748b" }}
            tick={{ fontSize: 10, fill: "#64748b" }} tickFormatter={(v) => v >= 1000 ? `${(v/1000).toFixed(0)}k` : v} />
          <YAxis dataKey="ir_dbd" name="IR DBD" type="number"
            label={{ value: "IR DBD per 100.000", angle: -90, position: "insideLeft", offset: 15, fontSize: 11, fill: "#64748b" }}
            tick={{ fontSize: 10, fill: "#64748b" }} domain={[150, 320]} />
          <ZAxis dataKey="ch_lag1" range={[60, 400]} name="CH Lag-1" />
          <Tooltip content={<CustomTooltip />} />
          <Legend wrapperStyle={{ fontSize: 11, paddingTop: 16 }}
            formatter={(value) => <span style={{ color: "#94a3b8" }}>{value}</span>} />

          {(Object.entries(byZona) as [keyof typeof byZona, typeof kabKotaData][]).map(([zona, data]) => (
            <Scatter key={zona} name={ZONA_LABELS[zona]} data={data} fill={ZONA_COLORS[zona]}>
              {data.map((entry) => (
                <Cell key={entry.id} fill={ZONA_COLORS[zona]} fillOpacity={0.8} stroke={ZONA_COLORS[zona]} strokeWidth={1.5} />
              ))}
            </Scatter>
          ))}
        </ScatterChart>
      </ResponsiveContainer>

      {/* Annotation */}
      <div className="mt-3 flex flex-wrap gap-2">
        <div className="text-[10px] text-slate-500 bg-slate-50 dark:bg-slate-800 rounded-lg px-3 py-1.5 border border-slate-200 dark:border-slate-700">
          💡 Titik lebih besar = CH Lag-1 lebih tinggi (potensi breeding site nyamuk lebih banyak)
        </div>
        <div className="text-[10px] text-red-500 bg-red-500/5 rounded-lg px-3 py-1.5 border border-red-500/20">
          ⚡ Zona Merah: ultra-padat &amp; IR ekstrem — intervensi darurat
        </div>
      </div>
    </div>
  );
}
