import { NextResponse } from "next/server";
import { supabase } from "@/lib/supabase";

export async function GET() {
  const { data: stats, error: s1 } = await supabase.from("bahasa").select("*", { count: "exact", head: true });
  const { count: rumpunCount } = await supabase.from("rumpun_bahasa").select("*", { count: "exact", head: true });
  const { count: lokasiCount } = await supabase.from("lokasi").select("*", { count: "exact", head: true });
  const { data: vitalitasRaw } = await supabase.from("bahasa").select("status_vitalitas");

  if (s1) return NextResponse.json({ error: s1.message }, { status: 500 });

  const vitalitasBreakdown: Record<string, number> = {};
  for (const v of vitalitasRaw || []) {
    if (v.status_vitalitas) {
      vitalitasBreakdown[v.status_vitalitas] = (vitalitasBreakdown[v.status_vitalitas] || 0) + 1;
    }
  }

  return NextResponse.json({
    totalBahasa: stats?.length ?? 0,
    totalRumpun: rumpunCount ?? 0,
    totalLokasi: lokasiCount ?? 0,
    vitalitasBreakdown,
  });
}
