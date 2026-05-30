import { NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getCache, setCache, TTL } from "@/lib/cache";

export async function GET() {
  const cached = getCache("stats");
  if (cached) return NextResponse.json(cached);

  const [totalBahasa, totalRumpun, totalLokasi, vitalitasRaw] = await Promise.all([
    prisma.bahasa.count(),
    prisma.rumpunBahasa.count(),
    prisma.lokasi.count(),
    prisma.bahasa.groupBy({ by: ["statusVitalitas"], _count: true }),
  ]);

  const vitalitasBreakdown: Record<string, number> = {};
  for (const v of vitalitasRaw) {
    if (v.statusVitalitas) vitalitasBreakdown[v.statusVitalitas] = v._count;
  }

  const stats = { totalBahasa, totalRumpun, totalLokasi, vitalitasBreakdown };
  setCache("stats", stats, TTL.STATS);
  return NextResponse.json(stats);
}
