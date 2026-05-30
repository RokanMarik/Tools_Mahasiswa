import { NextResponse } from "next/server";
import { supabase } from "@/lib/supabase";
import { getCache, setCache, TTL } from "@/lib/cache";

export async function GET() {
  const cached = getCache("markers");
  if (cached) return NextResponse.json(cached);

  const { data: bahasa, error } = await supabase
    .from("bahasa")
    .select("id, nama_bahasa, nama_lokal, kode_iso_639, jumlah_penutur, status_vitalitas, koordinat_pusat, rumpun_bahasa(nama_rumpun)");

  if (error) return NextResponse.json({ error: error.message }, { status: 500 });

  const markers = bahasa
    .filter((b: any) => b.koordinat_pusat)
    .map((b: any) => ({
      id: b.id,
      namaBahasa: b.nama_bahasa,
      namaLokal: b.nama_lokal,
      kodeIso639: b.kode_iso_639,
      jumlahPenutur: b.jumlah_penutur,
      statusVitalitas: b.status_vitalitas,
      rumpunNama: b.rumpun_bahasa?.nama_rumpun ?? null,
      lat: b.koordinat_pusat.coordinates[1],
      lng: b.koordinat_pusat.coordinates[0],
    }));

  setCache("markers", markers, TTL.MARKERS);
  return NextResponse.json(markers);
}
