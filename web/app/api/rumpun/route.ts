import { NextResponse } from "next/server";
import { supabase } from "@/lib/supabase";

export async function GET() {
  const { data: rumpun, error } = await supabase
    .from("rumpun_bahasa")
    .select("id, nama_rumpun, sub_rumpun, bahasa(id)");

  if (error) return NextResponse.json({ error: error.message }, { status: 500 });

  const result = (rumpun || []).map((r: any) => ({
    id: r.id,
    namaRumpun: r.nama_rumpun,
    subRumpun: r.sub_rumpun,
    bahasaCount: r.bahasa?.length ?? 0,
  }));

  return NextResponse.json(result);
}
