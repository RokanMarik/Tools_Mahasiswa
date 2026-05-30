import { NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getCache, setCache, TTL } from "@/lib/cache";

export async function GET() {
  const cached = getCache("rumpun");
  if (cached) return NextResponse.json(cached);

  const rumpunList = await prisma.rumpunBahasa.findMany({
    select: { id: true, namaRumpun: true, subRumpun: true, _count: { select: { bahasa: true } } },
    orderBy: { namaRumpun: "asc" },
  });

  const result = rumpunList.map((r) => ({
    id: r.id, namaRumpun: r.namaRumpun, subRumpun: r.subRumpun, bahasaCount: r._count.bahasa,
  }));

  setCache("rumpun", result, TTL.RUMPUN);
  return NextResponse.json(result);
}
