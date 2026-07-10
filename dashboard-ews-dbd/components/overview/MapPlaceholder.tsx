"use client";
import { useState } from "react";
import {
  ComposableMap,
  Geographies,
  Geography,
  Marker,
  ZoomableGroup,
} from "react-simple-maps";
import { kabKotaData } from "@/lib/data";

const GEO_URL = "/jawa-barat.json";

// Mapping nama di TopoJSON (field: kabkot) → nama di dataset kita
// Kabupaten: nilai sama persis. Kota: perlu prefix "Kota "
const NAMA_MAP: Record<string, string> = {
  // Kota (perlu tambah prefix)
  "Bogor":       "Kota Bogor",      // baris ke-19 di topojson = Kota Bogor
  "Sukabumi":    "Kota Sukabumi",   // baris ke-20
  "Bandung":     "Kota Bandung",    // baris ke-21
  "Cirebon":     "Kota Cirebon",    // baris ke-22
  "Bekasi":      "Kota Bekasi",     // baris ke-23
  "Depok":       "Kota Depok",      // baris ke-24
  "Cimahi":      "Kota Cimahi",     // baris ke-25
  "Tasikmalaya": "Kota Tasikmalaya",// baris ke-26
  "Banjar":      "Kota Banjar",     // baris ke-27
};
// Kabupaten: nama di TopoJSON sudah sama dengan dataset kita
// Bogor(kab), Sukabumi(kab), dst — di-resolve lewat index geometry
// GeometryIndex 0-17 = Kabupaten, 18-26 = Kota (urutan file)
const KAB_NAMES = [
  "Bogor","Sukabumi","Cianjur","Bandung","Garut","Tasikmalaya",
  "Ciamis","Kuningan","Cirebon","Majalengka","Sumedang","Indramayu",
  "Subang","Purwakarta","Karawang","Bekasi","Bandung Barat","Pangandaran",
];

const ZONA_STYLE: Record<string, { fill: string; stroke: string; label: string }> = {
  merah:  { fill: "#E74C3C", stroke: "#c0392b", label: "Zona Merah (Rawan)" },
  kuning: { fill: "#F39C12", stroke: "#d68910", label: "Zona Kuning (Waspada)" },
  hijau:  { fill: "#27AE60", stroke: "#1e8449", label: "Zona Hijau (Aman)" },
};

// Lookup zona & IR per nama wilayah
const zonaLookup: Record<string, string> = {};
const irLookup:   Record<string, number>  = {};
kabKotaData.forEach((d) => {
  zonaLookup[d.nama] = d.zona;
  irLookup[d.nama]   = d.ir_dbd;
});

interface TooltipState { nama: string; ir: number; zona: string }

export default function MapPlaceholder() {
  const [tooltip, setTooltip] = useState<TooltipState | null>(null);
  const [hovered, setHovered] = useState<string>("");

  const resolveNama = (geoProps: Record<string, string>, geoIndex: number) => {
    // Field di TopoJSON: 'kabkot'
    const kabkot = geoProps?.kabkot ?? "";
    // Kota (index 18-26) → pakai NAMA_MAP untuk tambah prefix "Kota"
    if (geoIndex >= 18) {
      return { raw: kabkot, mapped: NAMA_MAP[kabkot] ?? `Kota ${kabkot}` };
    }
    // Kabupaten (index 0-17) → nama langsung
    return { raw: kabkot, mapped: kabkot };
  };

  return (
    <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 overflow-hidden">
      {/* ── Header ── */}
      <div className="px-5 py-4 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between flex-wrap gap-3">
        <div>
          <h3 className="font-semibold text-slate-900 dark:text-white text-sm">
            Peta Kerawanan DBD — Jawa Barat
          </h3>
          <p className="text-slate-400 text-xs mt-0.5">
            Desember 2025 · 27 Kab/Kota · Spatially Constrained Clustering
          </p>
        </div>
        <div className="flex items-center gap-3 text-[11px] flex-wrap">
          {Object.entries(ZONA_STYLE).map(([z, cfg]) => (
            <span key={z} className="flex items-center gap-1.5 text-slate-500">
              <span className="w-3 h-3 rounded-sm border border-white/20 inline-block" style={{ background: cfg.fill }} />
              {cfg.label}
            </span>
          ))}
          <span className="flex items-center gap-1.5 text-slate-500">
            <span className="w-3 h-3 rounded-sm bg-slate-600 inline-block" />
            Data N/A
          </span>
        </div>
      </div>

      {/* ── Map area ── */}
      <div
        className="relative bg-gradient-to-b from-slate-50 to-slate-100 dark:from-[#0a0f1e] dark:to-[#0f172a]"
        style={{ height: 360 }}
      >
        <ComposableMap
          projection="geoMercator"
          projectionConfig={{ center: [107.6, -7.05], scale: 7200 }}
          style={{ width: "100%", height: "100%" }}
        >
          <ZoomableGroup zoom={1} minZoom={0.8} maxZoom={6}>
            {/* ── District polygons ── */}
            <Geographies geography={GEO_URL}>
              {({ geographies }: { geographies: any[] }) =>
                geographies.map((geo: any, geoIndex: number) => {
                  const { raw, mapped } = resolveNama(geo.properties ?? {}, geoIndex);
                  const zona  = zonaLookup[mapped] ?? "";
                  const ir    = irLookup[mapped]   ?? 0;
                  const style = zona ? ZONA_STYLE[zona] : { fill: "#334155", stroke: "#475569" };
                  const isHov = hovered === (mapped || raw);

                  return (
                    <Geography
                      key={geo.rsmKey}
                      geography={geo}
                      onMouseEnter={() => {
                        setHovered(mapped || raw);
                        setTooltip({ nama: mapped || raw, ir, zona });
                      }}
                      onMouseLeave={() => {
                        setHovered("");
                        setTooltip(null);
                      }}
                      style={{
                        default: {
                          fill:        style.fill,
                          stroke:      style.stroke,
                          strokeWidth: 0.7,
                          fillOpacity: 0.82,
                          outline:     "none",
                        },
                        hover: {
                          fill:        style.fill,
                          stroke:      "#ffffff",
                          strokeWidth: 1.8,
                          fillOpacity: 1,
                          outline:     "none",
                          cursor:      "pointer",
                          filter:      "brightness(1.2) drop-shadow(0 0 4px rgba(255,255,255,0.4))",
                        },
                        pressed: { fill: style.fill, outline: "none" },
                      }}
                    />
                  );
                })
              }
            </Geographies>

            {/* ── Zona Merah markers ── */}
            {kabKotaData
              .filter((d) => d.zona === "merah")
              .map((d) => (
                <Marker key={d.id} coordinates={[d.lon, d.lat]}>
                  {/* Pulsing ring */}
                  <circle r={9} fill="#E74C3C" fillOpacity={0.25} />
                  <circle r={5} fill="white" stroke="#E74C3C" strokeWidth={2} />
                  <circle r={3} fill="#E74C3C" />
                  <text
                    textAnchor="middle"
                    y={-13}
                    style={{
                      fontSize: 7.5,
                      fill: "#fff",
                      fontWeight: 800,
                      pointerEvents: "none",
                      textShadow: "0 1px 3px rgba(0,0,0,0.8)",
                    }}
                  >
                    ⚡ {d.nama}
                  </text>
                </Marker>
              ))}
          </ZoomableGroup>
        </ComposableMap>

        {/* ── Live tooltip (top-left) ── */}
        {tooltip && (
          <div className="absolute top-3 left-3 z-20 bg-slate-950/95 border border-slate-700 rounded-xl px-3.5 py-3 shadow-2xl pointer-events-none backdrop-blur-sm">
            <p className="text-white font-bold text-xs mb-1.5">{tooltip.nama}</p>
            {tooltip.zona ? (
              <>
                <p className="text-[10px] text-slate-400 leading-relaxed">
                  Zona:{" "}
                  <span className="font-semibold" style={{ color: ZONA_STYLE[tooltip.zona]?.fill }}>
                    {ZONA_STYLE[tooltip.zona]?.label}
                  </span>
                </p>
                <p className="text-[10px] text-slate-400">
                  IR DBD:{" "}
                  <span className="text-white font-bold text-xs">{tooltip.ir.toFixed(1)}</span>
                  <span className="text-slate-500"> /100.000 pddk</span>
                </p>
              </>
            ) : (
              <p className="text-slate-500 text-[10px]">Data tidak tersedia</p>
            )}
          </div>
        )}

        {/* ── Zoom hint ── */}
        <div className="absolute bottom-3 right-3 text-[10px] text-slate-400 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-lg px-2.5 py-1.5 border border-slate-200 dark:border-slate-700 select-none">
          🖱️ Scroll untuk zoom · Drag untuk geser
        </div>

        {/* ── Critical zone badge ── */}
        <div className="absolute top-3 right-3 bg-red-500/15 border border-red-500/30 rounded-lg px-2.5 py-1.5 text-[10px] text-red-400 font-semibold">
          ⚡ Episentrum: Bandung Raya
        </div>
      </div>

      {/* ── Footer ── */}
      <div className="px-5 py-3 border-t border-slate-100 dark:border-slate-800 flex items-center gap-4 text-[10px] text-slate-500 flex-wrap">
        <span className="font-semibold text-slate-600 dark:text-slate-400">Skala IR DBD:</span>
        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-sm bg-[#E74C3C] inline-block" /> &gt;250 (Kritis)</span>
        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-sm bg-[#F39C12] inline-block" /> 190–250 (Waspada)</span>
        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-sm bg-[#27AE60] inline-block" /> &lt;190 (Aman)</span>
        <span className="ml-auto text-slate-400">Peta: GADM v4.1 · Data: BPS + NASA POWER 2021–2025</span>
      </div>
    </div>
  );
}
