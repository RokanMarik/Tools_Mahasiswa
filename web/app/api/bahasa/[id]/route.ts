import { NextResponse } from "next/server";
import { supabase } from "@/lib/supabase";

export async function GET(request: Request, { params }: { params: { id: string } }) {
  const { data: bahasa, error } = await supabase
    .from("bahasa")
    .select("*, rumpun_bahasa(nama_rumpun, sub_rumpun), lokasi(provinsi, kabupaten, tipe_wilayah), fitur_linguistik(sistem_tulisan, tipe_morfologi, urutan_kata, jumlah_vokal, jumlah_konsonan), kosakata(kata, arti_indonesia, fonetik_ipa)")
    .eq("id", params.id)
    .single();

  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  if (!bahasa) return NextResponse.json({ error: "Bahasa not found" }, { status: 404 });

  const formatted = {
    id: bahasa.id,
    namaBahasa: bahasa.nama_bahasa,
    namaLokal: bahasa.nama_lokal,
    kodeIso639: bahasa.kode_iso_639,
    autoSummary: bahasa.auto_summary,
    jumlahPenutur: bahasa.jumlah_penutur,
    statusVitalitas: bahasa.status_vitalitas,
    rumpun: bahasa.rumpun_bahasa,
    lokasi: bahasa.lokasi || [],
    fiturLinguistik: bahasa.fitur_linguistik,
    kosakata: (bahasa.kosakata || []).map((k: any) => ({
      kata: k.kata,
      artiIndonesia: k.arti_indonesia,
      fonetikIpa: k.fonetik_ipa,
    })),
  };

  return NextResponse.json(formatted);
}
