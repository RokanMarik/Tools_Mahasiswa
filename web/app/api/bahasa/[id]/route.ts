import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getCache, setCache, TTL } from "@/lib/cache";

export async function GET(request: NextRequest, { params }: { params: { id: string } }) {
  const cacheKey = `bahasa:${params.id}`;
  const cached = getCache(cacheKey);
  if (cached) return NextResponse.json(cached);

  const bahasa = await prisma.bahasa.findUnique({
    where: { id: params.id },
    include: {
      rumpun: { select: { namaRumpun: true, subRumpun: true } },
      lokasi: { select: { provinsi: true, kabupaten: true, tipeWilayah: true } },
      fiturLinguistik: { select: { sistemTulisan: true, tipeMorfologi: true, urutanKata: true, jumlahVokal: true, jumlahKonsonan: true } },
      kosakata: { select: { kata: true, artiIndonesia: true, fonetikIpa: true }, take: 20 },
    },
  });

  if (!bahasa) return NextResponse.json({ error: "Bahasa not found" }, { status: 404 });

  setCache(cacheKey, bahasa, TTL.DETAIL);
  return NextResponse.json(bahasa);
}
