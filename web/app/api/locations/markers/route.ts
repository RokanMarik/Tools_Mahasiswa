import { NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getCache, setCache, TTL } from "@/lib/cache";
import type { BahasaMarker } from "@/lib/types";

export async function GET() {
  const cached = getCache<BahasaMarker[]>("markers");
  if (cached) return NextResponse.json(cached);

  const bahasaList = await prisma.bahasa.findMany({
    select: {
      id: true, namaBahasa: true, namaLokal: true, kodeIso639: true,
      jumlahPenutur: true, statusVitalitas: true,
      rumpun: { select: { namaRumpun: true } },
      koordinatPusat: true,
    },
  });

  const markers: BahasaMarker[] = bahasaList
    .filter((b) => b.koordinatPusat)
    .map((b) => {
      const coords = b.koordinatPusat as { coordinates: [number, number] };
      return {
        id: b.id, namaBahasa: b.namaBahasa, namaLokal: b.namaLokal,
        kodeIso639: b.kodeIso639, jumlahPenutur: b.jumlahPenutur,
        statusVitalitas: b.statusVitalitas, rumpunNama: b.rumpun?.namaRumpun ?? null,
        lat: coords.coordinates[1], lng: coords.coordinates[0],
      };
    });

  setCache("markers", markers, TTL.MARKERS);
  return NextResponse.json(markers);
}
