"use client";

import { useState, useEffect } from "react";
import dynamic from "next/dynamic";
import { Header } from "@/components/layout/Header";
import { Sidebar } from "@/components/layout/Sidebar";
import type { BahasaMarker } from "@/lib/types";

const LanguageMap = dynamic(
  () => import("@/components/map/LanguageMap").then((m) => ({ default: m.LanguageMap })),
  { ssr: false, loading: () => <div className="flex-1 bg-earth-200 flex items-center justify-center">Memuat peta...</div> }
);

export default function MapPage() {
  const [markers, setMarkers] = useState<BahasaMarker[]>([]);
  const [bahasaList, setBahasaList] = useState<BahasaMarker[]>([]);
  const [rumpunList, setRumpunList] = useState<{ id: string; namaRumpun: string; bahasaCount: number }[]>([]);
  const [search, setSearch] = useState("");
  const [rumpunFilter, setRumpunFilter] = useState("");
  const [vitalitasFilter, setVitalitasFilter] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/locations/markers").then((r) => r.json()).then((data) => { setMarkers(data); setBahasaList(data); }).finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    fetch("/api/rumpun").then((r) => r.json()).then((data) => setRumpunList(data));
  }, []);

  useEffect(() => {
    let filtered = markers;
    if (search) { const q = search.toLowerCase(); filtered = filtered.filter((b) => b.namaBahasa.toLowerCase().includes(q) || b.namaLokal?.toLowerCase().includes(q)); }
    if (rumpunFilter) filtered = filtered.filter((b) => b.rumpunNama === rumpunFilter);
    if (vitalitasFilter) filtered = filtered.filter((b) => b.statusVitalitas === vitalitasFilter);
    setBahasaList(filtered);
  }, [search, rumpunFilter, vitalitasFilter, markers]);

  return (
    <div className="h-screen flex flex-col">
      <Header />
      <div className="flex-1 flex overflow-hidden">
        <Sidebar search={search} onSearchChange={setSearch} rumpunFilter={rumpunFilter} onRumpunChange={setRumpunFilter} vitalitasFilter={vitalitasFilter} onVitalitasChange={setVitalitasFilter} rumpunList={rumpunList} bahasaList={bahasaList.map((b) => ({ id: b.id, namaBahasa: b.namaBahasa, namaLokal: b.namaLokal, jumlahPenutur: b.jumlahPenutur, statusVitalitas: b.statusVitalitas, rumpunNama: b.rumpunNama }))} loading={loading} />
        <div className="flex-1"><LanguageMap markers={bahasaList} /></div>
      </div>
    </div>
  );
}
