"use client";
import { AlertTriangle, Info, CheckCircle, Bell } from "lucide-react";
import { ewsAlerts } from "@/lib/data";

const LEVEL_CONFIG = {
  KRITIS:  { icon: AlertTriangle, bg: "bg-red-500/10",    border: "border-red-500/20",    text: "text-red-400",    badge: "bg-red-500/20 text-red-400",    dot: "bg-red-500" },
  WASPADA: { icon: AlertTriangle, bg: "bg-amber-500/10",  border: "border-amber-500/20",  text: "text-amber-400",  badge: "bg-amber-500/20 text-amber-400",  dot: "bg-amber-500" },
  INFO:    { icon: Info,          bg: "bg-blue-500/10",   border: "border-blue-500/20",   text: "text-blue-400",   badge: "bg-blue-500/20 text-blue-400",    dot: "bg-blue-500" },
} as const;

export default function AlertLog() {
  return (
    <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 overflow-hidden">
      <div className="px-5 py-4 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Bell className="w-4 h-4 text-slate-500" />
          <h3 className="font-semibold text-slate-900 dark:text-white text-sm">Log Peringatan AIDES</h3>
        </div>
        <span className="text-xs bg-red-500/15 text-red-500 px-2.5 py-1 rounded-full font-medium">
          2 Kritis Aktif
        </span>
      </div>
      <div className="divide-y divide-slate-100 dark:divide-slate-800">
        {ewsAlerts.map((alert) => {
          const cfg = LEVEL_CONFIG[alert.level as keyof typeof LEVEL_CONFIG];
          const Icon = cfg.icon;
          return (
            <div key={alert.id} className={`flex gap-3 px-5 py-4 ${cfg.bg} border-l-2 ${cfg.border} hover:brightness-105 transition-all`}>
              <div className={`mt-0.5 flex-shrink-0 w-7 h-7 rounded-lg ${cfg.bg} ${cfg.border} border flex items-center justify-center`}>
                <Icon className={`w-3.5 h-3.5 ${cfg.text}`} />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1 flex-wrap">
                  <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-md ${cfg.badge}`}>
                    {alert.level}
                  </span>
                  <span className="text-slate-400 dark:text-slate-500 text-[10px]">📍 {alert.wilayah}</span>
                  <span className="text-slate-300 dark:text-slate-600 text-[10px] ml-auto">{alert.waktu}</span>
                </div>
                <p className="text-slate-600 dark:text-slate-300 text-xs leading-relaxed">{alert.pesan}</p>
              </div>
            </div>
          );
        })}
      </div>
      <div className="px-5 py-3 bg-slate-50 dark:bg-slate-900/50 border-t border-slate-100 dark:border-slate-800">
        <p className="text-slate-400 text-[10px] flex items-center gap-1.5">
          <CheckCircle className="w-3 h-3 text-emerald-500" />
          Sistem memperbarui alert otomatis setiap 24 jam berdasarkan data NASA POWER & prediksi XGBoost
        </p>
      </div>
    </div>
  );
}
