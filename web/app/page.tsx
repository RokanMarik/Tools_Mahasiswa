import Link from "next/link";

async function getStats() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL ?? "http://localhost:3000"}/api/stats`, { cache: "no-store" });
  if (!res.ok) return null;
  return res.json();
}

export default async function HomePage() {
  const stats = await getStats();
  return (
    <div className="min-h-screen">
      <section className="bg-gradient-to-b from-earth-100 to-earth-200 py-20 px-4">
        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl font-bold text-earth-700 mb-4">Peta Bahasa Indonesia</h1>
          <p className="text-lg text-earth-600 mb-8">Jelajahi persebaran bahasa daerah dari Aceh sampai Papua. Temukan keragaman linguistik Nusantara dalam satu peta interaktif.</p>
          <Link href="/explore/map" className="btn-primary text-lg px-8 py-3">Mulai Jelajahi →</Link>
        </div>
      </section>
      {stats && (
        <section className="py-12 px-4">
          <div className="max-w-4xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="glass-panel p-6 text-center"><div className="text-3xl font-bold text-earth-700">{stats.totalBahasa}</div><div className="text-sm text-earth-600 mt-1">Bahasa</div></div>
            <div className="glass-panel p-6 text-center"><div className="text-3xl font-bold text-earth-700">{stats.totalRumpun}</div><div className="text-sm text-earth-600 mt-1">Rumpun</div></div>
            <div className="glass-panel p-6 text-center"><div className="text-3xl font-bold text-earth-700">{stats.totalLokasi}</div><div className="text-sm text-earth-600 mt-1">Lokasi</div></div>
            <div className="glass-panel p-6 text-center"><div className="text-3xl font-bold text-earth-700">{Object.keys(stats.vitalitasBreakdown).length}</div><div className="text-sm text-earth-600 mt-1">Status Vitalitas</div></div>
          </div>
        </section>
      )}
      <section className="py-16 px-4 text-center">
        <h2 className="text-2xl font-semibold text-earth-700 mb-4">Siap Menjelajahi?</h2>
        <p className="text-earth-600 mb-6">Lihat peta interaktif dengan marker berwarna per rumpun bahasa.</p>
        <Link href="/explore/map" className="btn-primary">Buka Peta →</Link>
      </section>
    </div>
  );
}
