"use client";
import { Activity, Map, TrendingUp, AlertTriangle, ShieldAlert, ChevronRight, Zap } from "lucide-react";
import { TabType } from "@/app/page";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { id: "overview"    as TabType, label: "Dashboard Eksekutif", sublabel: "Overview & KPI", icon: Activity },
  { id: "clustering"  as TabType, label: "Analisis Kerawanan",  sublabel: "Spatial Clustering", icon: Map },
  { id: "forecasting" as TabType, label: "Proyeksi XGBoost",    sublabel: "Temporal Forecasting", icon: TrendingUp },
];

interface SidebarProps {
  activeTab: TabType;
  setActiveTab: (tab: TabType) => void;
}

export default function Sidebar({ activeTab, setActiveTab }: SidebarProps) {
  return (
    <aside className="w-64 flex-shrink-0 flex flex-col bg-[#0f172a] border-r border-[#1e293b] overflow-hidden">
      {/* Logo */}
      <div className="px-5 py-5 border-b border-[#1e293b]">
          <div className="flex items-center gap-3 mb-8 px-2">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center flex-shrink-0 shadow-lg shadow-blue-500/20">
              <ShieldAlert className="w-5 h-5 text-white" />
            </div>
            <div>
              <p className="text-white font-bold text-sm leading-tight">AIDES</p>
              <p className="text-blue-300 text-[10px] uppercase tracking-wider font-semibold">Jawa Barat</p>
            </div>
          </div>
      </div>

      {/* Status badge */}
      <div className="mx-4 mt-4 px-3 py-2 rounded-lg bg-red-500/10 border border-red-500/20 flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-red-500 pulse-red flex-shrink-0" />
        <div>
          <p className="text-red-400 text-xs font-semibold">SISTEM AKTIF</p>
          <p className="text-red-300/70 text-[10px]">2 Zona Kritis Terdeteksi</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        <p className="text-slate-500 text-[10px] font-semibold uppercase tracking-wider px-3 mb-2">Menu Utama</p>
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={cn(
                "w-full flex items-center gap-3 px-3 py-3 rounded-xl text-left transition-all duration-200 group",
                isActive
                  ? "bg-blue-600/20 border border-blue-500/30 text-white"
                  : "text-slate-400 hover:text-white hover:bg-white/5"
              )}
            >
              <div className={cn("w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 transition-all",
                isActive ? "bg-blue-500/30" : "bg-white/5 group-hover:bg-white/10"
              )}>
                <Icon className={cn("w-4 h-4", isActive ? "text-blue-400" : "text-slate-400 group-hover:text-slate-300")} />
              </div>
              <div className="flex-1 min-w-0">
                <p className={cn("text-sm font-medium truncate", isActive ? "text-white" : "text-slate-300")}>{item.label}</p>
                <p className="text-[10px] text-slate-500 truncate">{item.sublabel}</p>
              </div>
              {isActive && <ChevronRight className="w-4 h-4 text-blue-400 flex-shrink-0" />}
            </button>
          );
        })}
      </nav>

      {/* Alert indicator */}
      <div className="mx-4 mb-4 px-3 py-3 rounded-xl bg-[#1e293b] border border-[#334155]">
        <div className="flex items-center gap-2 mb-2">
          <AlertTriangle className="w-4 h-4 text-yellow-400" />
          <span className="text-xs font-semibold text-slate-300">Alert Terbaru</span>
        </div>
        <p className="text-[10px] text-slate-400 leading-relaxed">CH Kota Bandung: 4.727mm — episentrum dalam 30 hari.</p>
      </div>

      {/* Footer */}
      <div className="px-5 py-4 border-t border-[#1e293b]">
        <div className="flex items-center gap-2">
          <Zap className="w-3 h-3 text-blue-400" />
          <p className="text-[10px] text-slate-500">Model: XGBoost + Spatial Clustering</p>
        </div>
        <p className="text-[10px] text-slate-600 mt-0.5">Data: NASA POWER + BPS Jabar 2021-25</p>
      </div>
    </aside>
  );
}
