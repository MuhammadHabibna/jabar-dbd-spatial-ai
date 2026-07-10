"use client";
import { useState, useMemo } from "react";
import { ChevronUp, ChevronDown, Filter, Search } from "lucide-react";
import { kabKotaData, KabKotaData } from "@/lib/data";

type SortKey = keyof KabKotaData;
type SortDir = "asc" | "desc";

const ZONA_BADGE: Record<string, string> = {
  merah:  "badge-merah",
  kuning: "badge-kuning",
  hijau:  "badge-hijau",
};
const ZONA_LABELS: Record<string, string> = {
  merah: "Zona Merah", kuning: "Zona Kuning", hijau: "Zona Hijau",
};

export default function DataTable() {
  const [filterZona, setFilterZona] = useState<string>("all");
  const [search, setSearch] = useState("");
  const [sortKey, setSortKey] = useState<SortKey>("ir_dbd");
  const [sortDir, setSortDir] = useState<SortDir>("desc");

  const filtered = useMemo(() => {
    let data = [...kabKotaData];
    if (filterZona !== "all") data = data.filter(d => d.zona === filterZona);
    if (search) data = data.filter(d => d.nama.toLowerCase().includes(search.toLowerCase()));
    data.sort((a, b) => {
      const av = a[sortKey], bv = b[sortKey];
      if (typeof av === "number" && typeof bv === "number") return sortDir === "asc" ? av - bv : bv - av;
      return sortDir === "asc" ? String(av).localeCompare(String(bv)) : String(bv).localeCompare(String(av));
    });
    return data;
  }, [filterZona, search, sortKey, sortDir]);

  const handleSort = (key: SortKey) => {
    if (sortKey === key) setSortDir(d => d === "asc" ? "desc" : "asc");
    else { setSortKey(key); setSortDir("desc"); }
  };

  const SortIcon = ({ k }: { k: SortKey }) => (
    <span className="ml-1 inline-flex flex-col opacity-50">
      <ChevronUp  className={`w-2.5 h-2.5 -mb-0.5 ${sortKey === k && sortDir==="asc"  ? "opacity-100 text-blue-400" : ""}`} />
      <ChevronDown className={`w-2.5 h-2.5 ${sortKey === k && sortDir==="desc" ? "opacity-100 text-blue-400" : ""}`} />
    </span>
  );

  const cols: { key: SortKey; label: string; fmt: (d: KabKotaData) => React.ReactNode }[] = [
    { key: "nama",       label: "Kab/Kota",          fmt: d => <span className="font-medium text-slate-800 dark:text-white">{d.nama}</span> },
    { key: "zona",       label: "Zona",               fmt: d => <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold ${ZONA_BADGE[d.zona]}`}>{ZONA_LABELS[d.zona]}</span> },
    { key: "ir_dbd",     label: "IR DBD Aktual",      fmt: d => <span className={`font-bold ${d.ir_dbd > 250 ? "text-red-500" : d.ir_dbd > 210 ? "text-amber-500" : "text-emerald-500"}`}>{d.ir_dbd.toFixed(1)}</span> },
    { key: "ir_prediksi",label: "Prediksi Jan 2026",  fmt: d => <span className="text-blue-500 font-semibold">{d.ir_prediksi.toFixed(1)}</span> },
    { key: "kepadatan",  label: "Kepadatan (jiwa/km²)",fmt: d => d.kepadatan.toLocaleString() },
    { key: "sanitasi",   label: "Sanitasi (%)",       fmt: d => (
      <div className="flex items-center gap-2">
        <div className="w-16 h-1.5 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
          <div className="h-full rounded-full" style={{ width: `${d.sanitasi}%`, background: d.sanitasi > 80 ? "#27AE60" : d.sanitasi > 60 ? "#F39C12" : "#E74C3C" }} />
        </div>
        <span className="text-slate-600 dark:text-slate-300">{d.sanitasi.toFixed(1)}%</span>
      </div>
    )},
    { key: "prioritas",  label: "Prioritas",          fmt: d => (
      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
        d.prioritas==="TINGGI" ? "bg-red-500/15 text-red-500" :
        d.prioritas==="SEDANG" ? "bg-amber-500/15 text-amber-500" :
        "bg-emerald-500/15 text-emerald-500"}`}>{d.prioritas}</span>
    )},
  ];

  return (
    <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 overflow-hidden">
      {/* Toolbar */}
      <div className="px-5 py-4 border-b border-slate-100 dark:border-slate-800 flex flex-wrap items-center gap-3">
        <h3 className="font-semibold text-slate-900 dark:text-white text-sm mr-auto">Data 27 Kab/Kota Jawa Barat</h3>
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400" />
          <input value={search} onChange={e => setSearch(e.target.value)}
            placeholder="Cari wilayah..." className="pl-8 pr-3 py-1.5 text-xs rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-300 w-36 focus:outline-none focus:ring-1 focus:ring-blue-500" />
        </div>
        {/* Filter */}
        <div className="relative flex items-center gap-1.5">
          <Filter className="w-3.5 h-3.5 text-slate-400" />
          <select value={filterZona} onChange={e => setFilterZona(e.target.value)}
            className="text-xs rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-300 px-3 py-1.5 focus:outline-none focus:ring-1 focus:ring-blue-500 cursor-pointer">
            <option value="all">Semua Zona ({kabKotaData.length})</option>
            <option value="merah">Zona Merah (2)</option>
            <option value="kuning">Zona Kuning (18)</option>
            <option value="hijau">Zona Hijau (7)</option>
          </select>
        </div>
        <span className="text-xs text-slate-400">{filtered.length} wilayah</span>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-xs">
          <thead>
            <tr className="border-b border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50">
              {cols.map(col => (
                <th key={String(col.key)} onClick={() => handleSort(col.key)}
                  className="px-4 py-3 text-left text-slate-500 dark:text-slate-400 font-semibold uppercase tracking-wider cursor-pointer hover:text-slate-700 dark:hover:text-slate-200 select-none whitespace-nowrap">
                  <span className="flex items-center">{col.label}<SortIcon k={col.key} /></span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-50 dark:divide-slate-800">
            {filtered.map((row) => (
              <tr key={row.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
                {cols.map(col => (
                  <td key={String(col.key)} className="px-4 py-3 text-slate-600 dark:text-slate-300 whitespace-nowrap">
                    {col.fmt(row)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {filtered.length === 0 && (
        <div className="text-center py-8 text-slate-400 text-sm">Tidak ada data ditemukan</div>
      )}
    </div>
  );
}
