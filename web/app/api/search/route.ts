import { NextRequest, NextResponse } from "next/server";
import { supabase } from "@/lib/supabase";
import { getCache, setCache, TTL } from "@/lib/cache";

async function call9Router(query: string) {
  const ninerouterUrl = process.env.NINEROUTER_URL || "http://localhost:20128";
  const ninerouterKey = process.env.NINEROUTER_KEY || "";

  const prompt = `Convert this Indonesian language search query into database filters. Return ONLY valid JSON, no explanation.

Query: "${query}"

Available filters:
- vitalitas: ["aman", "rentan", "terancam", "sangat terancam", "kritis"]
- rumpun: ["Austronesia", "Papua", "Trans-New Guinea"]
- provinsi: any Indonesian province name
- tipe_wilayah: ["pesisir", "pegunungan", "dataran", "kepulauan", "perkotaan"]
- sort: ["nama", "penutur_asc", "penutur_desc"]
- search: string for name matching

Example response format:
{"vitalitas": ["kritis", "sangat terancam"], "provinsi": ["Papua", "Papua Barat"], "sort": "penutur_asc"}

Respond with JSON only:`;

  const response = await fetch(`${ninerouterUrl}/v1/chat/completions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${ninerouterKey}`,
    },
    body: JSON.stringify({
      model: "kr/claude-sonnet-4.5",
      messages: [{ role: "user", content: prompt }],
      temperature: 0.1,
      max_tokens: 200,
    }),
    signal: AbortSignal.timeout(8000),
  });

  if (!response.ok) throw new Error(`9Router error: ${response.status}`);

  const data = await response.json();
  const content = data.choices?.[0]?.message?.content || "";

  // Extract JSON from response
  const jsonMatch = content.match(/\{[^}]+\}/s);
  if (!jsonMatch) throw new Error("No JSON in response");

  return JSON.parse(jsonMatch[0]);
}

async function keywordFallback(query: string) {
  const q = query.toLowerCase();
  const { data: bahasa, error } = await supabase
    .from("bahasa")
    .select("id, nama_bahasa, nama_lokal, kode_iso_639, jumlah_penutur, status_vitalitas, koordinat_pusat, rumpun_bahasa(nama_rumpun)")
    .or(`nama_bahasa.ilike.%${q}%,nama_lokal.ilike.%${q}%`)
    .order("nama_bahasa", { ascending: true })
    .limit(20);

  if (error) throw error;

  return (bahasa || []).map((b: any) => ({
    id: b.id,
    namaBahasa: b.nama_bahasa,
    namaLokal: b.nama_lokal,
    kodeIso639: b.kode_iso_639,
    jumlahPenutur: b.jumlah_penutur,
    statusVitalitas: b.status_vitalitas,
    rumpunNama: b.rumpun_bahasa?.nama_rumpun ?? null,
    lat: b.koordinat_pusat?.coordinates?.[1] ?? null,
    lng: b.koordinat_pusat?.coordinates?.[0] ?? null,
  })).filter((b: any) => b.lat && b.lng);
}

export async function POST(request: NextRequest) {
  const { query } = await request.json();
  if (!query || typeof query !== "string") {
    return NextResponse.json({ error: "Query required" }, { status: 400 });
  }

  // Check cache
  const cacheKey = `search:${query.toLowerCase().trim()}`;
  const cached = getCache(cacheKey);
  if (cached) return NextResponse.json(cached);

  let filters: any = null;
  let usedAI = true;

  try {
    filters = await call9Router(query);
  } catch {
    // Fallback to keyword search
    usedAI = false;
    const results = await keywordFallback(query);
    const response = { results, usedAI, query };
    setCache(cacheKey, response, TTL.MARKERS);
    return NextResponse.json(response);
  }

  // Build Supabase query with AI filters
  let supabaseQuery = supabase
    .from("bahasa")
    .select("id, nama_bahasa, nama_lokal, kode_iso_639, jumlah_penutur, status_vitalitas, koordinat_pusat, rumpun_bahasa(nama_rumpun)");

  if (filters.vitalitas?.length) {
    supabaseQuery = supabaseQuery.in("status_vitalitas", filters.vitalitas);
  }
  if (filters.rumpun?.length) {
    supabaseQuery = supabaseQuery.in("rumpun_bahasa.nama_rumpun", filters.rumpun);
  }
  if (filters.provinsi?.length) {
    // Need to join with lokasi
    const { data: lokasiIds } = await supabase
      .from("lokasi")
      .select("bahasa_id")
      .in("provinsi", filters.provinsi);

    if (lokasiIds?.length) {
      supabaseQuery = supabaseQuery.in("id", lokasiIds.map((l: any) => l.bahasa_id));
    }
  }
  if (filters.tipe_wilayah) {
    const { data: lokasiIds } = await supabase
      .from("lokasi")
      .select("bahasa_id")
      .eq("tipe_wilayah", filters.tipe_wilayah);

    if (lokasiIds?.length) {
      supabaseQuery = supabaseQuery.in("id", lokasiIds.map((l: any) => l.bahasa_id));
    }
  }
  if (filters.search) {
    const q = filters.search;
    supabaseQuery = supabaseQuery.or(`nama_bahasa.ilike.%${q}%,nama_lokal.ilike.%${q}%`);
  }

  // Apply sort
  if (filters.sort === "penutur_asc") {
    supabaseQuery = supabaseQuery.order("jumlah_penutur", { ascending: true, nullsLast: true });
  } else if (filters.sort === "penutur_desc") {
    supabaseQuery = supabaseQuery.order("jumlah_penutur", { ascending: false, nullsLast: true });
  } else {
    supabaseQuery = supabaseQuery.order("nama_bahasa", { ascending: true });
  }

  supabaseQuery = supabaseQuery.limit(50);

  const { data: bahasa, error } = await supabaseQuery;
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });

  const results = (bahasa || [])
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

  const response = { results, usedAI, filters, query };
  setCache(cacheKey, response, TTL.MARKERS);
  return NextResponse.json(response);
}
