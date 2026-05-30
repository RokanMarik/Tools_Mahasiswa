import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

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

async function main() {
  console.log("Seeding database...");
  const rumpunMap: Record<string, string> = {};
  const rumpunNames = [...new Set(seedData.map((d) => d.rumpun))];

  for (const nama of rumpunNames) {
    const rumpun = await prisma.rumpunBahasa.create({
      data: { namaRumpun: nama, levelTaksonomi: nama === "Austronesia" ? 2 : 1 },
    });
    rumpunMap[nama] = rumpun.id;
    console.log(`  Rumpun: ${nama}`);
  }

  for (const data of seedData) {
    const bahasa = await prisma.bahasa.create({
      data: {
        namaBahasa: data.namaBahasa,
        namaLokal: data.namaLokal,
        kodeIso639: data.kodeIso639,
        rumpunId: rumpunMap[data.rumpun],
        jumlahPenutur: data.jumlahPenutur,
        statusVitalitas: data.statusVitalitas,
        koordinatPusat: { type: "Point", coordinates: [data.lng, data.lat] },
        lokasi: { create: { provinsi: data.provinsi } },
        fiturLinguistik: { create: { sistemTulisan: data.sistemTulisan, tipeMorfologi: data.tipeMorfologi, urutanKata: data.urutanKata } },
      },
    });
    console.log(`  Bahasa: ${data.namaBahasa}`);
  }

  console.log(`\nSeeded ${seedData.length} languages, ${rumpunNames.length} rumpun.`);
}

main()
  .catch((e) => { console.error(e); process.exit(1); })
  .finally(async () => { await prisma.$disconnect(); });
