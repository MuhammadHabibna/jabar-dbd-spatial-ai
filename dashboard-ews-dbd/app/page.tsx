"use client";
import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import OverviewPage from "@/components/overview/OverviewPage";
import ClusteringPage from "@/components/clustering/ClusteringPage";
import ForecastingPage from "@/components/forecasting/ForecastingPage";

export type TabType = "overview" | "clustering" | "forecasting";

export default function Home() {
  const [activeTab, setActiveTab] = useState<TabType>("overview");

  return (
    <div className="flex h-screen overflow-hidden bg-[#f8fafc] dark:bg-[#0a0f1e]">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <main className="flex-1 overflow-y-auto flex flex-col relative">
        <div className="flex-1">
          {activeTab === "overview"    && <OverviewPage />}
          {activeTab === "clustering"  && <ClusteringPage />}
          {activeTab === "forecasting" && <ForecastingPage />}
        </div>

        {/* Global Footer Competition */}
        <footer className="mt-8 border-t border-slate-200 dark:border-slate-800 py-6 px-6 text-center text-slate-500 dark:text-slate-400 text-xs bg-white/50 dark:bg-[#0a0f1e]/50 backdrop-blur-sm">
          <p className="font-bold text-slate-700 dark:text-slate-300 mb-1.5 text-[13px]">
            Prototipe Sistem AIDES (AI Dengue Early-warning System)
          </p>
          <p className="mb-1">
            Dikembangkan khusus untuk kompetisi <span className="font-bold text-emerald-600 dark:text-emerald-400">ECOHEALTH COMPETITION</span>
          </p>
          <p>
            Oleh: <span className="font-medium text-slate-600 dark:text-slate-300">Muhammad Habib Nur Aiman (Kategori Individu)</span> — Universitas Negeri Surabaya
          </p>
        </footer>
      </main>
    </div>
  );
}
