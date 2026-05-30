// Seed data via Supabase REST API (HTTPS port 443 - not blocked)
// Usage: node seed-via-api.js

const SUPABASE_URL = "https://hkeheukewxsvaarxaket.supabase.co";
const SUPABASE_KEY = process.argv[2]; // service_role key from Dashboard → Settings → API

if (!SUPABASE_KEY) {
  console.log("Usage: node seed-via-api.js <SERVICE_ROLE_KEY>");
  console.log("Get key from: Supabase Dashboard → Settings → API → service_role key");
  process.exit(1);
}

const headers = {
  "Content-Type": "application/json",
  "apikey": SUPABASE_KEY,
  "Authorization": `Bearer ${SUPABASE_KEY}`,
  "Prefer": "return=minimal",
};

async function apiPost(table, data) {
  const res = await fetch(`${SUPABASE_URL}/rest/v1/${table}`, {
    method: "POST",
    headers,
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`${table}: ${res.status} ${err}`);
  }
}

const seedData = [
  { namaBahasa: "Jawa", namaLokal: "Basa Jawa", kodeIso639: "jav", rumpun: "Austronesia", jumlahPenutur: 98000000, statusVitalitas: "rentan", lat: -7.5, lng: 110.5, provinsi: "Jawa Tengah", sistemTulisan: "Latin, Hanacaraka", tipeMorfologi: "aglutinatif", urutanKata: "SVO" },
  { namaBahasa: "Sunda", namaLokal: "Basa Sunda", kodeIso639: "sun", rumpun: "Austronesia", jumlahPenutur: 42000000, statusVitalitas: "rentan", lat: -6.9, lng: 107.6, provinsi: "Jawa Barat", sistemTulisan: "Latin", tipeMorfologi: "aglutinatif", urutanKata: "SVO" },
  { namaBahasa: "Madura", namaLokal: "Bâsa Madhurâ", kodeIso639: "mad", rumpun: "Austronesia", jumlahPenutur: 13700000, statusVitalitas: "rentan", lat: -7.0, lng: 113.3, provinsi: "Jawa Timur", sistemTulisan: "Latin", tipeMorfologi: "aglutinatif", urutanKata: "SVO" },
  { namaBahasa: "Batak Toba", namaLokal: "Hata Batak Toba", kodeIso639: "bbc", rumpun: "Austronesia", jumlahPenutur: 2000000, statusVitalitas: "rentan", lat: 2.5, lng: 99.0, provinsi: "Sumatera Utara", sistemTulisan: "Latin, Surat Batak", tipeMorfologi: "aglutinatif", urutanKata: "VSO" },
  { namaBahasa: "Batak Karo", namaLokal: "Hata Karo", kodeIso639: "btx", rumpun: "Austronesia", jumlahPenutur: 600000, statusVitalitas: "rentan", lat: 3.0, lng: 98.5, provinsi: "Sumatera Utara", sistemTulisan: "Latin", tipeMorfologi: "aglutinatif", urutanKata: "VSO" },
  { namaBahasa: "Minangkabau", namaLokal: "Baso Minangkabau", kodeIso639: "min", rumpun: "Austronesia", jumlahPenutur: 6500000, statusVitalitas: "rentan", lat: -0.5, lng: 100.5, provinsi: "Sumatera Barat", sistemTulisan: "Latin, Jawi", tipeMorfologi: "aglutinatif", urutanKata: "SVO" },
  { namaBahasa: "Bugis", namaLokal: "Basa Ugi", kodeIso639: "bug", rumpun: "Austronesia", jumlahPenutur: 5000000, statusVitalitas: "rentan", lat: -4.0, lng: 120.0, provinsi: "Sulawesi Selatan", sistemTulisan: "Latin, Lontara", tipeMorfologi: "aglutinatif", urutanKata: "SVO" },
  { namaBahasa: "Makassar", namaLokal: "Basa Mangkasara'", kodeIso639: "mak", rumpun: "Austronesia", jumlahPenutur: 2100000, statusVitalitas: "rentan", lat: -5.1, lng: 119.4, provinsi: "Sulawesi Selatan", sistemTulisan: "Latin, Lontara", tipeMorfologi: "aglutinatif", urutanKata: "SVO" },
  { namaBahasa: "Bali", namaLokal: "Basa Bali", kodeIso639: "ban", rumpun: "Austronesia", jumlahPenutur: 3300000, statusVitalitas: "rentan", lat: -8.4, lng: 115.1, provinsi: "Bali", sistemTulisan: "Latin, Balinese", tipeMorfologi: "aglutinatif", urutanKata: "SVO" },
  { namaBahasa: "Sasak", namaLokal: "Basa Sasak", kodeIso639: "sas", rumpun: "Austronesia", jumlahPenutur: 2700000, statusVitalitas: "rentan", lat: -8.6, lng: 116.3, provinsi: "Nusa Tenggara Barat", sistemTulisan: "Latin", tipeMorfologi: "aglutinatif", urutanKata: "SVO" },
  { namaBahasa: "Banjar", namaLokal: "Bahasa Banjar", kodeIso639: "bjn", rumpun: "Austronesia", jumlahPenutur: 6300000, statusVitalitas: "rentan", lat: -3.3, lng: 114.6, provinsi: "Kalimantan Selatan", sistemTulisan: "Latin", tipeMorfologi: "aglutinatif", urutanKata: "SVO" },
  { namaBahasa: "Dayak Ngaju", namaLokal: "Basa Ngaju", kodeIso639: "nij", rumpun: "Austronesia", jumlahPenutur: 890000, statusVitalitas: "rentan", lat: -1.7, lng: 113.5, provinsi: "Kalimantan Tengah", sistemTulisan: "Latin", tipeMorfologi: "aglutinatif", urutanKata: "SVO" },
  { namaBahasa: "Dayak Iban", namaLokal: "Jaku Iban", kodeIso639: "ibl", rumpun: "Austronesia", jumlahPenutur: 1200000, statusVitalitas: "rentan", lat: 1.0, lng: 111.5, provinsi: "Kalimantan Barat", sistemTulisan: "Latin", tipeMorfologi: "aglutinatif", urutanKata: "SVO" },
  { namaBahasa: "Gorontalo", namaLokal: "Bahasa Hulontalo", kodeIso639: "gor", rumpun: "Austronesia", jumlahPenutur: 900000, statusVitalitas: "rentan", lat: 0.5, lng: 122.2, provinsi: "Gorontalo", sistemTulisan: "Latin", tipeMorfologi: "aglutinatif", urutanKata: "SVO" },
  { namaBahasa: "Toraja", namaLokal: "Basa Toraja", kodeIso639: "sda", rumpun: "Austronesia", jumlahPenutur: 650000, statusVitalitas: "rentan", lat: -3.0, lng: 119.8, provinsi: "Sulawesi Selatan", sistemTulisan: "Latin", tipeMorfologi: "aglutinatif", urutanKata: "SVO" },
  { namaBahasa: "Bima", namaLokal: "Basa Mbojo", kodeIso639: "bhp", rumpun: "Austronesia", jumlahPenutur: 500000, statusVitalitas: "rentan", lat: -8.5, lng: 118.7, provinsi: "Nusa Tenggara Barat", sistemTulisan: "Latin", tipeMorfologi: "aglutinatif", urutanKata: "SVO" },
  { namaBahasa: "Batak Simalungun", namaLokal: "Hata Simalungun", kodeIso639: "bts", rumpun: "Austronesia", jumlahPenutur: 1300000, statusVitalitas: "rentan", lat: 2.8, lng: 99.3, provinsi: "Sumatera Utara", sistemTulisan: "Latin", tipeMorfologi: "aglutinatif", urutanKata: "VSO" },
  { namaBahasa: "Asmat", namaLokal: "Asmat", kodeIso639: "asm", rumpun: "Papua", jumlahPenutur: 65000, statusVitalitas: "sangat terancam", lat: -5.3, lng: 138.5, provinsi: "Papua", sistemTulisan: "Latin", tipeMorfologi: "aglutinatif", urutanKata: "SOV" },
  { namaBahasa: "Dani", namaLokal: "Dani", kodeIso639: "dna", rumpun: "Trans-New Guinea", jumlahPenutur: 200000, statusVitalitas: "rentan", lat: -4.1, lng: 139.0, provinsi: "Papua", sistemTulisan: "Latin", tipeMorfologi: "aglutinatif", urutanKata: "SOV" },
  { namaBahasa: "Melayu", namaLokal: "Bahasa Melayu", kodeIso639: "msa", rumpun: "Austronesia", jumlahPenutur: 77000000, statusVitalitas: "aman", lat: 1.0, lng: 104.0, provinsi: "Kepulauan Riau", sistemTulisan: "Latin, Jawi", tipeMorfologi: "aglutinatif", urutanKata: "SVO" },
];

async function seed() {
  console.log("Seeding via Supabase REST API...\n");

  try {
    // 1. Check if rumpun exist, create if not
    console.log("1. Checking rumpun...");
    let rumpunRes = await fetch(`${SUPABASE_URL}/rest/v1/rumpun_bahasa?select=nama_rumpun`, {
      headers: { "apikey": SUPABASE_KEY, "Authorization": `Bearer ${SUPABASE_KEY}`, "Prefer": "return=minimal" },
    });

    if (!rumpunRes.ok || (await rumpunRes.json()).length === 0) {
      console.log("   Creating 3 rumpun...");
      await apiPost("rumpun_bahasa", [{ nama_rumpun: "Austronesia", level_taksonomi: 2 }]);
      await apiPost("rumpun_bahasa", [{ nama_rumpun: "Papua", level_taksonomi: 1 }]);
      await apiPost("rumpun_bahasa", [{ nama_rumpun: "Trans-New Guinea", level_taksonomi: 2 }]);
    } else {
      console.log("   Rumpun already exist, skipping create.");
    }

    // 2. Get rumpun IDs
    console.log("2. Fetching rumpun IDs...");
    const rumpunIdRes = await fetch(`${SUPABASE_URL}/rest/v1/rumpun_bahasa?select=id,nama_rumpun`, { headers });
    const rumpunList = await rumpunIdRes.json();
    const rumpunMap = {};
    rumpunList.forEach(r => { rumpunMap[r.nama_rumpun] = r.id; });
    console.log("   Rumpun map:", JSON.stringify(rumpunMap, null, 2));

    // 3. Create bahasa, then lokasi and fitur separately
    console.log("\n3. Creating 20 languages...");

    // Check existing bahasa
    const existingRes = await fetch(`${SUPABASE_URL}/rest/v1/bahasa?select=nama_bahasa`, {
      headers: { "apikey": SUPABASE_KEY, "Authorization": `Bearer ${SUPABASE_KEY}` },
    });
    const existing = existingRes.ok ? (await existingRes.json()).map(b => b.nama_bahasa) : [];
    const toSeed = seedData.filter(d => !existing.includes(d.namaBahasa));
    console.log(`   ${existing.length} already exist, ${toSeed.length} to create.\n`);

    for (const d of toSeed) {
      // Insert bahasa
      const bahasaBody = {
        nama_bahasa: d.namaBahasa,
        nama_lokal: d.namaLokal,
        kode_iso_639: d.kodeIso639,
        rumpun_id: rumpunMap[d.rumpun],
        jumlah_penutur: d.jumlahPenutur,
        status_vitalitas: d.statusVitalitas,
        koordinat_pusat: { type: "Point", coordinates: [d.lng, d.lat] },
      };

      const bahasaRes = await fetch(`${SUPABASE_URL}/rest/v1/bahasa`, {
        method: "POST",
        headers: { ...headers, "Prefer": "return=representation" },
        body: JSON.stringify([bahasaBody]),
      });
      if (!bahasaRes.ok) {
        const err = await bahasaRes.text();
        throw new Error(`bahasa (${d.namaBahasa}): ${bahasaRes.status} ${err}`);
      }
      const bahasaResult = await bahasaRes.json();
      const bahasaId = bahasaResult[0].id;

      // Insert lokasi
      await apiPost("lokasi", [{ bahasa_id: bahasaId, provinsi: d.provinsi }]);

      // Insert fitur_linguistik
      await apiPost("fitur_linguistik", [{
        bahasa_id: bahasaId,
        sistem_tulisan: d.sistemTulisan,
        tipe_morfologi: d.tipeMorfologi,
        urutan_kata: d.urutanKata,
      }]);

      console.log(`   ✓ ${d.namaBahasa}`);
      await new Promise(r => setTimeout(r, 100));
    }

    console.log("\n✅ All 20 languages seeded successfully!");
  } catch (err) {
    console.error("\n❌ Error:", err.message);
    process.exit(1);
  }
}

seed();
