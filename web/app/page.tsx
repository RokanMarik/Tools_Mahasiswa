import Link from "next/link";
import { Logo } from "@/components/shared/Logo";

async function getStats() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL ?? "http://localhost:3000"}/api/stats`, { cache: "no-store" });
  if (!res.ok) return null;
  return res.json();
}

export default async function HomePage() {
  const stats = await getStats();
  return (
    <div className="min-h-screen">
      {/* Hero */}
      <section className="bg-gradient-to-b from-earth-100 to-earth-200 py-20 px-4">
        <div className="max-w-3xl mx-auto text-center">
          <div className="flex justify-center mb-6">
            <Logo size="lg" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-earth-700 mb-4">
            Jelajahi Bahasa Nusantara
          </h1>
          <p className="text-lg text-earth-600 mb-8">
            Peta interaktif persebaran bahasa daerah Indonesia.
            Dari Aceh sampai Papua, temukan keragaman linguistik yang membentuk identitas bangsa.
          </p>
          <Link href="/explore/map" className="btn-primary text-lg px-8 py-3 inline-flex items-center gap-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" /></svg>
            Mulai Jelajahi
          </Link>
        </div>
      </section>

      {/* Stats */}
      {stats && (
        <section className="py-12 px-4">
          <div className="max-w-4xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="glass-panel p-6 text-center">
              <div className="text-3xl font-bold text-earth-700">{stats.totalBahasa}</div>
              <div className="text-sm text-earth-600 mt-1">Bahasa</div>
            </div>
            <div className="glass-panel p-6 text-center">
              <div className="text-3xl font-bold text-earth-700">{stats.totalRumpun}</div>
              <div className="text-sm text-earth-600 mt-1">Rumpun</div>
            </div>
            <div className="glass-panel p-6 text-center">
              <div className="text-3xl font-bold text-earth-700">{stats.totalLokasi}</div>
              <div className="text-sm text-earth-600 mt-1">Lokasi</div>
            </div>
            <div className="glass-panel p-6 text-center">
              <div className="text-3xl font-bold text-earth-700">{Object.keys(stats.vitalitasBreakdown).length}</div>
              <div className="text-sm text-earth-600 mt-1">Status Vitalitas</div>
            </div>
          </div>
        </section>
      )}

      {/* CTA */}
      <section className="py-16 px-4 text-center">
        <h2 className="text-2xl font-semibold text-earth-700 mb-4">
          Siap Menjelajahi?
        </h2>
        <p className="text-earth-600 mb-6">
          Lihat peta interaktif dengan marker berwarna per rumpun bahasa.
        </p>
        <Link href="/explore/map" className="btn-primary inline-flex items-center gap-2">
          Buka Peta
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" /></svg>
        </Link>
      </section>
    </div>
  );
}
