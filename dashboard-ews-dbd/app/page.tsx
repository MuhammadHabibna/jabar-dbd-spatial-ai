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
      <main className="flex-1 overflow-y-auto">
        {activeTab === "overview"    && <OverviewPage />}
        {activeTab === "clustering"  && <ClusteringPage />}
        {activeTab === "forecasting" && <ForecastingPage />}
      </main>
    </div>
  );
}
