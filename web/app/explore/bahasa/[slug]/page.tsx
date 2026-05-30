import { notFound } from "next/navigation";
import Link from "next/link";
import { Header } from "@/components/layout/Header";
import { VitalityBadge } from "@/components/ui/VitalityBadge";

interface BahasaDetailData {
  id: string;
  namaBahasa: string;
  namaLokal: string | null;
  kodeIso639: string | null;
  autoSummary: string | null;
  jumlahPenutur: number | null;
  statusVitalitas: string | null;
  rumpun: { namaRumpun: string | null; subRumpun: string | null } | null;
  lokasi: { provinsi: string | null; kabupaten: string | null; tipeWilayah: string | null }[];
  fiturLinguistik: { sistemTulisan: string | null; tipeMorfologi: string | null; urutanKata: string | null; jumlahVokal: number | null; jumlahKonsonan: number | null } | null;
  kosakata: { kata: string; artiIndonesia: string; fonetikIpa: string | null }[];
}

async function getBahasa(id: string): Promise<BahasaDetailData | null> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL ?? "http://localhost:3000"}/api/bahasa/${id}`, { cache: "no-store" });
  if (!res.ok) return null;
  return res.json();
}

export default async function BahasaDetailPage({ params }: { params: { slug: string } }) {
  const bahasa = await getBahasa(params.slug);
  if (!bahasa) notFound();

  const penuturFormatted = bahasa.jumlahPenutur ? bahasa.jumlahPenutur.toLocaleString("id-ID") : "Tidak diketahui";

  return (
    <div className="min-h-screen">
      <Header />
      <main className="max-w-4xl mx-auto px-4 py-8">
        <Link href="/explore/map" className="inline-flex items-center gap-1 text-sm text-earth-600 hover:text-earth-700 mb-6">← Kembali ke peta</Link>
        <div className="mb-8">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold text-earth-700">{bahasa.namaBahasa}</h1>
              {bahasa.namaLokal && <p className="text-lg text-earth-600 italic mt-1">{bahasa.namaLokal}</p>}
            </div>
            <VitalityBadge status={bahasa.statusVitalitas} size="md" />
          </div>
        </div>
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <div className="glass-panel p-5">
            <h2 className="font-semibold text-earth-700 mb-3">Informasi Dasar</h2>
            <dl className="space-y-2 text-sm">
              <div className="flex justify-between"><dt className="text-earth-600">ISO 639-3</dt><dd className="font-mono text-earth-700">{bahasa.kodeIso639 ?? "—"}</dd></div>
              <div className="flex justify-between"><dt className="text-earth-600">Rumpun</dt><dd className="text-earth-700">{bahasa.rumpun?.namaRumpun ?? "—"}</dd></div>
              {bahasa.rumpun?.subRumpun && <div className="flex justify-between"><dt className="text-earth-600">Sub-rumpun</dt><dd className="text-earth-700">{bahasa.rumpun.subRumpun}</dd></div>}
              <div className="flex justify-between"><dt className="text-earth-600">Jumlah Penutur</dt><dd className="font-semibold text-earth-700">{penuturFormatted}</dd></div>
            </dl>
          </div>
          <div className="glass-panel p-5">
            <h2 className="font-semibold text-earth-700 mb-3">Fitur Linguistik</h2>
            {bahasa.fiturLinguistik ? (
              <dl className="space-y-2 text-sm">
                <div className="flex justify-between"><dt className="text-earth-600">Sistem Tulisan</dt><dd className="text-earth-700">{bahasa.fiturLinguistik.sistemTulisan ?? "—"}</dd></div>
                <div className="flex justify-between"><dt className="text-earth-600">Tipe Morfologi</dt><dd className="text-earth-700">{bahasa.fiturLinguistik.tipeMorfologi ?? "—"}</dd></div>
                <div className="flex justify-between"><dt className="text-earth-600">Urutan Kata</dt><dd className="font-mono text-earth-700">{bahasa.fiturLinguistik.urutanKata ?? "—"}</dd></div>
              </dl>
            ) : (<p className="text-sm text-earth-600">Data fitur linguistik belum tersedia.</p>)}
          </div>
        </div>
        {bahasa.lokasi.length > 0 && (
          <div className="glass-panel p-5 mb-8">
            <h2 className="font-semibold text-earth-700 mb-3">Lokasi Sebaran</h2>
            <div className="flex flex-wrap gap-2">
              {bahasa.lokasi.map((loc, i) => (<span key={i} className="px-3 py-1 bg-earth-200 text-earth-700 rounded-full text-sm">{loc.provinsi}{loc.kabupaten && `, ${loc.kabupaten}`}</span>))}
            </div>
          </div>
        )}
        {bahasa.autoSummary && (
          <div className="glass-panel p-5 mb-8">
            <h2 className="font-semibold text-earth-700 mb-3">Ringkasan</h2>
            <div className="text-sm text-earth-600">{bahasa.autoSummary.split("\n").map((p, i) => (<p key={i}>{p}</p>))}</div>
          </div>
        )}
        {bahasa.kosakata.length > 0 && (
          <div className="glass-panel p-5">
            <h2 className="font-semibold text-earth-700 mb-3">Kosakata Sampel</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead><tr className="border-b border-earth-300"><th className="text-left py-2 text-earth-600 font-medium">Kata</th><th className="text-left py-2 text-earth-600 font-medium">Arti</th><th className="text-left py-2 text-earth-600 font-medium">Fonetik (IPA)</th></tr></thead>
                <tbody>{bahasa.kosakata.map((k, i) => (<tr key={i} className="border-b border-earth-200"><td className="py-2 font-medium text-earth-700">{k.kata}</td><td className="py-2 text-earth-600">{k.artiIndonesia}</td><td className="py-2 font-mono text-earth-600">{k.fonetikIpa ?? "—"}</td></tr>))}</tbody>
              </table>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
