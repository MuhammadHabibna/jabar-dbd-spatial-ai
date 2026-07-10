"use client";
import { AlertTriangle, CheckCircle, ArrowRight, Target, Clock, DollarSign } from "lucide-react";

const RECOMMENDATIONS = [
  {
    id: 1, level: "DARURAT", icon: AlertTriangle,
    wilayah: "Kota Bandung & Kota Cimahi",
    aksi: "Intervensi Asimetris Terfokus",
    deskripsi: "Relokasi 100% dana edukasi PHBS ke Kota Bandung dan Kota Cimahi sebelum Januari 2026. Kerahkan seluruh armada Jumantik (Juru Pemantau Jentik) untuk operasi PSN masif dan larvisidasi di seluruh kelurahan.",
    deadline: "Sebelum 1 Januari 2026",
    estimasi: "Potensi penurunan IR: -35% dalam 60 hari",
    color: "red",
    border: "border-red-500/30", bg: "bg-red-500/5", text: "text-red-500", badge: "bg-red-500/20 text-red-400",
  },
  {
    id: 2, level: "WASPADA", icon: Target,
    wilayah: "18 Wilayah Zona Kuning",
    aksi: "Monitoring Aktif & Pra-Posisi Logistik",
    deskripsi: "Aktifkan monitoring mingguan untuk 18 kab/kota Zona Kuning. Pra-posisikan stok insektisida, bubuk abate, dan kit edukasi PHBS di puskesmas terdekat. Prioritaskan Kota Tasikmalaya dan Kota Sukabumi (sanitasi terendah di zona ini).",
    deadline: "Berlaku Desember 2025 — Mar 2026",
    estimasi: "Cegah eskalasi ke Zona Merah",
    color: "amber",
    border: "border-amber-500/30", bg: "bg-amber-500/5", text: "text-amber-500", badge: "bg-amber-500/20 text-amber-400",
  },
  {
    id: 3, level: "PENCEGAHAN", icon: CheckCircle,
    wilayah: "7 Wilayah Zona Hijau (Pantura)",
    aksi: "Surveilans Rutin & Edukasi Standar",
    deskripsi: "Pertahankan kapasitas surveilans rutin bulanan. Fokus edukasi PHBS 3M Plus pada komunitas rentan. PERHATIAN: Jangan lengah — anomali curah hujan dapat mengubah status Zona Hijau menjadi Zona Kuning dalam 1–2 bulan.",
    deadline: "Monitoring berkelanjutan",
    estimasi: "Pertahankan IR < 200 per 100.000",
    color: "green",
    border: "border-emerald-500/30", bg: "bg-emerald-500/5", text: "text-emerald-500", badge: "bg-emerald-500/20 text-emerald-400",
  },
];

export default function RecommendationPanel() {
  return (
    <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 overflow-hidden">
      <div className="px-5 py-4 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
        <div>
          <h3 className="font-semibold text-slate-900 dark:text-white text-sm">Rekomendasi Kebijakan AI</h3>
          <p className="text-slate-400 text-xs mt-0.5">Output otomatis berdasarkan prediksi XGBoost + Spatial Clustering · Precision Public Health</p>
        </div>
        <span className="text-[10px] bg-blue-500/10 text-blue-400 border border-blue-500/20 px-2.5 py-1 rounded-full font-medium flex items-center gap-1">
          <span className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse" />
          AI Generated
        </span>
      </div>

      <div className="p-5 space-y-4">
        {RECOMMENDATIONS.map((rec) => {
          const Icon = rec.icon;
          return (
            <div key={rec.id} className={`rounded-xl border ${rec.border} ${rec.bg} p-4`}>
              <div className="flex items-start gap-3">
                <div className={`w-9 h-9 rounded-xl ${rec.bg} border ${rec.border} flex items-center justify-center flex-shrink-0`}>
                  <Icon className={`w-4.5 h-4.5 ${rec.text}`} />
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2 flex-wrap">
                    <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-md ${rec.badge}`}>{rec.level}</span>
                    <span className="text-slate-400 text-[11px] font-medium">📍 {rec.wilayah}</span>
                  </div>
                  <p className={`text-sm font-bold ${rec.text} mb-2`}>{rec.aksi}</p>
                  <p className="text-slate-600 dark:text-slate-300 text-xs leading-relaxed mb-3">{rec.deskripsi}</p>
                  <div className="flex flex-wrap gap-3 text-[10px] text-slate-500">
                    <span className="flex items-center gap-1"><Clock className="w-3 h-3" />{rec.deadline}</span>
                    <span className="flex items-center gap-1"><Target className="w-3 h-3 text-blue-400" /><span className="text-blue-400">{rec.estimasi}</span></span>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Footer: Ethical note */}
      <div className="px-5 py-4 bg-slate-50 dark:bg-slate-900/50 border-t border-slate-100 dark:border-slate-800">
        <div className="flex items-start gap-2">
          <DollarSign className="w-4 h-4 text-slate-400 flex-shrink-0 mt-0.5" />
          <p className="text-[10px] text-slate-400 leading-relaxed">
            <span className="font-semibold text-slate-500">Efisiensi Anggaran:</span> Intervensi terfokus ke Zona Merah (7.4% wilayah) vs kampanye merata se-Jawa Barat berpotensi menghemat hingga{" "}
            <span className="text-blue-400 font-semibold">~60–70% biaya logistik</span> tanpa mengorbankan efektivitas.{" "}
            <span className="font-semibold text-amber-400">⚠️ Catatan Etis:</span> Sistem ini harus diaudit berkala untuk memastikan tidak ada wilayah{" "}
            <span className="italic">blank spot</span> (underreporting) yang terklasifikasi Zona Hijau secara salah.
          </p>
        </div>
      </div>
    </div>
  );
}
