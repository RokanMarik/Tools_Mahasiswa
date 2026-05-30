import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const limit = parseInt(searchParams.get("limit") ?? "50");
  const offset = parseInt(searchParams.get("offset") ?? "0");
  const rumpun = searchParams.get("rumpun");
  const vitalitas = searchParams.get("vitalitas");
  const search = searchParams.get("search");

  const where: Record<string, unknown> = {};
  if (rumpun) where.rumpun = { namaRumpun: rumpun };
  if (vitalitas) where.statusVitalitas = vitalitas;
  if (search) {
    where.OR = [
      { namaBahasa: { contains: search, mode: "insensitive" as const } },
      { namaLokal: { contains: search, mode: "insensitive" as const } },
    ];
  }

  const [data, total] = await Promise.all([
    prisma.bahasa.findMany({
      where, select: { id: true, namaBahasa: true, namaLokal: true, kodeIso639: true, jumlahPenutur: true, statusVitalitas: true, rumpun: { select: { namaRumpun: true } } },
      orderBy: { namaBahasa: "asc" }, take: limit, skip: offset,
    }),
    prisma.bahasa.count({ where }),
  ]);

  return NextResponse.json({ data, total, limit, offset });
}
