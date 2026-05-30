# Design Doc: Peta Interaktif Bahasa Indonesia

**Tanggal:** 2026-01-28
**Status:** Draft — Menunggu Review
**Project:** Peta Bahasa Indonesia (Interactive Language Map)

---

## 1. Overview

Website interaktif yang menampilkan peta persebaran bahasa daerah di Indonesia. Hybrid mode: **Explore** (publik umum, visual-first) dan **Research** (akademisi, data-detail). Database PostgreSQL + PostGIS dengan 14 tabel yang sudah disiapkan. AI-powered search via 9Router.

### Target Pengguna
- **Mode Explore:** Masyarakat umum, mahasiswa, turis — cari dan eksplor bahasa daerah secara visual
- **Mode Research:** Linguistik, antropolog, peneliti — akses data detail, export, perbandingan

---

## 2. Arsitektur

### Stack
- **Frontend:** Next.js 14+ (App Router) + TypeScript
- **Styling:** Tailwind CSS + Plus Jakarta Sans (single font family)
- **Map:** Leaflet + react-leaflet
- **Charts:** Recharts
- **UI Components:** shadcn/ui
- **Backend:** Next.js API Routes (serverless)
- **ORM:** Prisma
- **Database:** PostgreSQL + PostGIS (Supabase free tier)
- **AI Gateway:** 9Router (localhost:20128)
- **Deploy:** Vercel (free tier), migrasi ke VPS nanti

### Arsitektur Diagram
```
┌─────────────────────────────────────────────┐
│              Vercel (Deploy)                 │
│  ┌───────────────────────────────────────┐  │
│  │            Next.js App                │  │
│  │  ┌────────────┐      ┌────────────┐  │  │
│  │  │  /explore  │      │ /research  │  │  │
│  │  │  (publik)  │      │ (akademisi)│  │  │
│  │  └─────┬──────┘      └─────┬──────┘  │  │
│  │        └──────────┬────────┘         │  │
│  │  ┌────────────────▼────────────────┐ │  │
│  │  │       API Routes (Server)       │ │  │
│  │  │  /api/bahasa  /api/search       │ │  │
│  │  │  /api/summary /api/locations    │ │  │
│  │  └────────────────┬────────────────┘ │  │
│  │                   │ Prisma ORM       │  │
│  └───────────────────┼──────────────────┘  │
└───────────────────────┼─────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────┐
│  PostgreSQL + PostGIS (Supabase)            │
│  14 tabel sesuai schema yang sudah ada      │
└─────────────────────────────────────────────┘
```

---

## 3. Visual Design

### Theme: Earthy Warm
| Elemen | Nilai | Keterangan |
|---|---|---|
| Background | `#f5f0e8` | Warna kertas tua/papyrus |
| Sidebar | `rgba(255,248,235,0.9)` | Glassmorphism hangat |
| Text Primary | `#3d3225` | Coklat tua (bukan hitam) |
| Text Secondary | `#6b5d4f` | Coklat sedang |
| Border | `#e0d5c0` | Coklat muda |

### Warna Rumpun Bahasa
| Rumpun | Hex | Keterangan |
|---|---|---|
| Austronesia | `#c4703f` | Terracotta / tanah liat |
| Papua | `#8b3a3a` | Merah bata |
| Trans-New Guinea | `#5a7247` | Hijau daun |
| Lainnya | `#6b5b8a` | Ungu tua |

### Badge Vitalitas
| Status | Hex |
|---|---|
| Aman | `#22c55e` |
| Rentan | `#eab308` |
| Terancam | `#f97316` |
| Kritis / Punah | `#ef4444` |

### Typography
- **Font Family:** Plus Jakarta Sans (semua elemen)
- **Heading:** weight 600-700
- **Body:** weight 400-500
- **Data/Numbers:** weight 400, tabular-nums

### Map Tiles
- **Default:** CartoDB Voyager (clean, pastel, modern)
- **Dark Mode:** CartoDB Dark Matter (toggle di Research mode)
- **Bukan:** OpenStreetMap default (terlalu rame)

---

## 4. Frontend Structure

### Route: `/explore`
| Route | Deskripsi |
|---|---|
| `/` | Landing page + quick search + statistik global |
| `/map` | Peta interaktif (halaman utama) |
| `/bahasa/[slug]` | Detail bahasa (mode publik) |
| `/rumpun/[slug]` | Filter per rumpun |

### Route: `/research`
| Route | Deskripsi |
|---|---|
| `/bahasa/[slug]/linguistik` | Fitur linguistik lengkap |
| `/bahasa/[slug]/sejarah` | Timeline + tren penutur |
| `/bahasa/[slug]/kosakata` | Swadesh list + sampel |
| `/bahasa/[slug]/manuskrip` | Galeri manuskrip |
| `/compare` | Perbandingan 2-5 bahasa |
| `/export` | Export CSV/JSON/GeoJSON |

### Komponen Utama
| Komponen | Fungsi |
|---|---|
| `Map` | Leaflet instance + marker + polygon + clustering |
| `Sidebar` | Filter + search + scrollable list |
| `LanguageCard` | Info singkat di popup/sidebar |
| `SearchBar` | Natural language input (AI-powered) |
| `VitalityBadge` | Badge warna per status vitalitas |
| `DataTable` | Tabel sortable (kosakata, lokasi) |
| `TimelineChart` | Line chart tren penutur |
| `ComparisonTable` | Side-by-side comparison |

---

## 5. API Structure

### Endpoints
| Endpoint | Method | Deskripsi | Cache |
|---|---|---|---|
| `/api/bahasa` | GET | List bahasa (paginated, filterable) | 5 menit |
| `/api/bahasa/[id]` | GET | Detail satu bahasa (join 6 tabel) | 1 jam |
| `/api/search` | POST | Smart Search (9Router AI) | 5 menit |
| `/api/summary` | POST | Auto-Summary (9Router AI, background) | Permanen (DB) |
| `/api/locations/markers` | GET | Koordinat semua bahasa (Leaflet) | 5 menit |
| `/api/locations/polygons` | GET | GeoJSON wilayah | 24 jam |
| `/api/rumpun` | GET | List rumpun + count | 1 jam |
| `/api/stats` | GET | Statistik global | 1 jam |

### Query Strategy
- **Query ringan (<100ms):** Prisma, langsung eksekusi
- **Query berat (1-5s):** Cache di memori, TTL sesuai tabel
- **AI calls:** Background job, hasil simpan di DB (bukan real-time)
- **Spatial queries:** Raw SQL (PostGIS tidak native di Prisma)

### Caching
```
In-memory (per API route):
├── markers → TTL 5 menit
├── stats → TTL 1 jam
├── rumpun → TTL 1 jam
└── detail bahasa → TTL 1 jam

Database-level:
├── bahasa.auto_summary → generated sekali, permanen
└── polygons GeoJSON → cache 24 jam
```

---

## 6. Database

### Provider: Supabase (Free Tier)
- Storage: 500MB
- Unlimited API requests
- Include PostGIS
- Auto backup harian
- Mudah migrate ke VPS

### Schema
Menggunakan schema yang sudah ada di `bahasa_indonesia_schema.sql` (14 tabel):
1. `rumpun_bahasa` — Taksonomi linguistik (self-referencing tree)
2. `bahasa` — Entitas utama
3. `lokasi` — Wilayah sebaran (PostGIS polygon)
4. `kontributor` — Peneliti/dokumentator
5. `media_dokumen` — Audio, video, PDF
6. `fitur_linguistik` — Fonologi, morfologi, sintaksis
7. `kosakata` — Swadesh list + sampel
8. `status_preservasi` — UNESCO scale, ancaman
9. `sumber_referensi` — Sumber data
10. `peristiwa_sejarah` — Timeline historis
11. `pengaruh_bahasa_lain` — Serakan kosakata
12. `penutur_historis` — Tren jumlah penutur
13. `riwayat_nama` — Evolusi nama/ejaan
14. `manuskrip` — Artefak tulis

### Views
- `v_bahasa_ringkasan` — Summary untuk popup peta
- `v_tren_penutur` — Data untuk grafik timeline

### Data Strategy
- **MVP:** Seed ~20 bahasa contoh:
  Jawa, Sunda, Madura, Batak Toba, Batak Karo, Batak Simalungun,
  Minangkabau, Melayu, Bugis, Makassar, Bali, Sasak, Bima,
  Dayak Ngaju, Dayak Iban, Banjar, Gorontalo, Toraja,
  Asmat, Dani
- **Fase 2:** Data collection pipeline via 9Router (Ethnologue, Glottolog, Wikipedia)
  Target: ~700 bahasa (estimasi dari Ethnologue untuk Indonesia)

---

## 7. AI Integration (9Router)

### Smart Search
```
User: "bahasa yang hampir punah di pedalaman Kalimantan"
   ↓
POST /api/search { query: "..." }
   ↓
9Router chat → convert to JSON filter:
{
  "vitalitas": ["terancam", "sangat terancam", "kritis"],
  "provinsi": ["Kalimantan Barat", ...],
  "tipe_wilayah": ["pegunungan"],
  "sort": "jumlah_penutur ASC"
}
   ↓
Prisma query → return results
```

**Fallback:** Kalau 9Router error → keyword search biasa (LIKE)

### Auto-Summary
```
Script: scripts/generate_summaries.py
├── Loop semua bahasa
├── 9Router chat → generate 3-paragraf summary
├── Simpan ke bahasa.auto_summary
└── Delay 2 detik per bahasa (rate limit)

Estimasi: 700 bahasa × 2 detik = ~23 menit
Dijalankan sekali, hasil permanen di DB
```

---

## 8. Deployment

### Development
```
Local:    npm run dev (localhost:3000)
Database: Supabase cloud (free)
9Router:  localhost:20128 (existing)
```

### Production (Vercel)
```
Push → GitHub → Auto deploy → Vercel
Env vars:
  DATABASE_URL     → Supabase connection string
  NINEROUTER_URL   → 9Router URL
  NINEROUTER_KEY   → 9Router API key
```

### Migrasi ke VPS (Fase 2)
```
1. npm run build → standalone output
2. Setup PM2 (process manager)
3. Setup nginx (reverse proxy)
4. Setup SSL (Let's Encrypt)
5. Database: tetap Supabase atau migrate
```

---

## 9. Roadmap

### Fase 1a — MVP Core (Minggu 1)
- [ ] Setup Next.js + TypeScript + Tailwind
- [ ] Setup Supabase + Prisma + schema deploy
- [ ] Seed 20 bahasa contoh
- [ ] Leaflet map + markers + popup
- [ ] Sidebar + filter + search (keyword)
- [ ] Halaman detail bahasa
- [ ] Deploy ke Vercel

### Fase 1b — Polish (Minggu 2)
- [ ] Earthy Warm theme + Plus Jakarta Sans
- [ ] Smart Search (9Router integration)
- [ ] Marker clustering + polygon layer
- [ ] Auto-Summary generation
- [ ] Responsive / touch optimization

### Fase 2 — Extended (Minggu 3+)
- [ ] Research mode (linguistik, sejarah, kosakata)
- [ ] Comparison tool
- [ ] Export (CSV, JSON, GeoJSON)
- [ ] Data collection pipeline (700+ bahasa)
- [ ] Dark mode toggle
- [ ] Admin panel (jika perlu)

---

## 10. Technical Notes

### PostGIS + Prisma
Prisma tidak native support tipe `GEOGRAPHY` PostGIS. Solusi:
- Gunakan raw SQL untuk spatial queries
- Simpan koordinat sebagai `Json` di Prisma schema
- Convert di application layer

### Serverless Timeout (Vercel)
- Hobby tier: 10 detik timeout
- Mitigasi: cache agresif, pagination, split AI call (async)

### Rate Limiting 9Router
- Delay 2 detik antar request untuk summary generation
- Smart search: cache hasil 5 menit untuk query yang sama
