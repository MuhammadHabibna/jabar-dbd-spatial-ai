"use client";
import { Users, MapPin, Brain, Droplets, TrendingUp, TrendingDown } from "lucide-react";
import { kabKotaData, zonaSummary } from "@/lib/data";

const avgSanitasi = kabKotaData.reduce((s, d) => s + d.sanitasi, 0) / kabKotaData.length;
const totalPrediksiJan = kabKotaData.reduce((s, d) => s + d.ir_prediksi, 0).toFixed(0);

const CARDS = [
  {
    title: "Total Prediksi IR (Jan 2026)",
    value: totalPrediksiJan,
    unit: "per 100rb",
    sub: "Agregat 27 kab/kota Jawa Barat",
    icon: TrendingUp,
    color: "blue",
    glow: "card-glow-blue",
    delta: "+2.3%",
    deltaUp: true,
  },
  {
    title: "Wilayah Zona Merah (Kritis)",
    value: "2",
    unit: "Kab/Kota",
    sub: "Kota Bandung & Kota Cimahi",
    icon: MapPin,
    color: "red",
    glow: "card-glow-red",
    delta: "Stabil",
    deltaUp: null,
  },
  {
    title: "Akurasi Model AI",
    value: "93.17",
    unit: "%  R²",
    sub: "XGBoost, RMSE=11.20, MAE=8.45",
    icon: Brain,
    color: "green",
    glow: "card-glow-green",
    delta: "Excellent",
    deltaUp: true,
  },
  {
    title: "Rata-rata Sanitasi Jawa Barat",
    value: avgSanitasi.toFixed(1),
    unit: "%",
    sub: "Nasional target: ≥85% (RPJMN 2025)",
    icon: Droplets,
    color: "yellow",
    glow: "card-glow-yellow",
    delta: "-14.1% dari target",
    deltaUp: false,
  },
];

const COLOR_MAP: Record<string, string> = {
  blue:   "from-blue-500/20 to-blue-600/10 border-blue-500/20 text-blue-400",
  red:    "from-red-500/20 to-red-600/10 border-red-500/20 text-red-400",
  green:  "from-emerald-500/20 to-emerald-600/10 border-emerald-500/20 text-emerald-400",
  yellow: "from-amber-500/20 to-amber-600/10 border-amber-500/20 text-amber-400",
};

export default function MetricCards() {
  return (
    <div className="grid grid-cols-2 xl:grid-cols-4 gap-4">
      {CARDS.map((card) => {
        const Icon = card.icon;
        return (
          <div key={card.title}
            className={`${card.glow} relative overflow-hidden rounded-2xl border bg-white dark:bg-slate-900 dark:border-slate-800 p-5 hover:scale-[1.01] transition-transform duration-200`}
          >
            <div className={`absolute inset-0 bg-gradient-to-br ${COLOR_MAP[card.color]} opacity-50`} />
            <div className="relative z-10">
              <div className="flex items-start justify-between mb-3">
                <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${COLOR_MAP[card.color]} border flex items-center justify-center`}>
                  <Icon className={`w-5 h-5 ${COLOR_MAP[card.color].split(" ").pop()}`} />
                </div>
                {card.delta && (
                  <span className={`text-xs font-medium px-2 py-0.5 rounded-full flex items-center gap-1 ${
                    card.deltaUp === true  ? "bg-emerald-500/15 text-emerald-500" :
                    card.deltaUp === false ? "bg-red-500/15 text-red-400" :
                    "bg-slate-500/15 text-slate-400"
                  }`}>
                    {card.deltaUp === true && <TrendingUp className="w-3 h-3" />}
                    {card.deltaUp === false && <TrendingDown className="w-3 h-3" />}
                    {card.delta}
                  </span>
                )}
              </div>
              <p className="text-slate-500 dark:text-slate-400 text-xs font-medium mb-1">{card.title}</p>
              <div className="flex items-baseline gap-1.5">
                <span className="text-3xl font-bold text-slate-900 dark:text-white">{card.value}</span>
                <span className="text-slate-400 text-xs">{card.unit}</span>
              </div>
              <p className="text-slate-400 text-[11px] mt-1.5 leading-relaxed">{card.sub}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
}
