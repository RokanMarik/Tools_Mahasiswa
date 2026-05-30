# Peta Bahasa Indonesia — Fase 1a (MVP Core) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build MVP website with interactive Leaflet map, sidebar filters, keyword search, language detail pages, and deploy to Vercel.

**Architecture:** Monolithic Next.js App Router with API routes, Prisma ORM connecting to Supabase PostgreSQL. Earthy Warm visual theme with Plus Jakarta Sans font. Seed data of 20 Indonesian languages.

**Tech Stack:** Next.js 14+, TypeScript, Tailwind CSS, Leaflet, react-leaflet, Prisma, PostgreSQL+PostGIS, shadcn/ui, Plus Jakarta Sans, 9Router (localhost:20128).

---

## File Structure

```
Mencari_Jurnal_Ilmiah/
├── web/                                    # Next.js app (NEW)
│   ├── app/
│   │   ├── layout.tsx                      # Root layout + fonts + theme
│   │   ├── page.tsx                        # Landing page
│   │   ├── globals.css                     # Tailwind + custom theme
│   │   ├── explore/
│   │   │   ├── page.tsx                    # Landing redirect
│   │   │   ├── map/
│   │   │   │   └── page.tsx               # Interactive map page
│   │   │   └── bahasa/
│   │   │       └── [slug]/
│   │   │           └── page.tsx           # Language detail page
│   │   └── api/
│   │       ├── bahasa/
│   │       │   ├── route.ts               # GET list (paginated)
│   │       │   └── [id]/
│   │       │       └── route.ts           # GET single detail
│   │       ├── locations/
│   │       │   └── markers/
│   │       │       └── route.ts           # GET coordinates
│   │       ├── rumpun/
│   │       │   └── route.ts               # GET rumpun list
│   │       └── stats/
│   │           └── route.ts               # GET global stats
│   ├── components/
│   │   ├── map/
│   │   │   ├── LanguageMap.tsx             # Leaflet wrapper
│   │   │   ├── LanguageMarkers.tsx         # Marker layer
│   │   │   └── MapPopup.tsx                # Popup content
│   │   ├── layout/
│   │   │   ├── Header.tsx                  # Site header
│   │   │   └── Sidebar.tsx                 # Filter + search sidebar
│   │   ├── ui/
│   │   │   ├── VitalityBadge.tsx           # Status badge
│   │   │   ├── LanguageCard.tsx            # Card for list
│   │   │   ├── SearchInput.tsx             # Search bar
│   │   │   └── FilterPanel.tsx             # Filter controls
│   │   └── shared/
│   │       └── LoadingState.tsx            # Loading skeletons
│   ├── lib/
│   │   ├── prisma.ts                       # Prisma client singleton
│   │   ├── cache.ts                        # In-memory cache
│   │   ├── types.ts                        # Shared TypeScript types
│   │   └── utils.ts                        # Utility functions
│   ├── prisma/
│   │   ├── schema.prisma                   # Prisma schema
│   │   └── seed.ts                         # Seed 20 languages
│   ├── public/
│   │   └── fonts/                          # Plus Jakarta Sans (optional)
│   ├── scripts/
│   │   └── deploy-schema.sql               # SQL for Supabase
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── postcss.config.mjs
│   ├── next.config.js
│   └── .env.local                          # Local env vars
├── docs/
│   └── superpowers/
│       ├── specs/2026-01-28-peta-bahasa-indonesia-design.md
│       └── plans/2026-01-28-peta-bahasa-mvp-core.md
└── (existing Python project files)
```

---

## Task 1: Project Setup — Next.js + TypeScript + Tailwind

**Files:**
- Create: `web/package.json`
- Create: `web/tsconfig.json`
- Create: `web/next.config.js`
- Create: `web/tailwind.config.ts`
- Create: `web/postcss.config.mjs`
- Create: `web/.gitignore`

- [ ] **Step 1: Create package.json**

Create `web/package.json`:

```json
{
  "name": "peta-bahasa-indonesia",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "db:generate": "prisma generate",
    "db:push": "prisma db push",
    "db:seed": "tsx prisma/seed.ts"
  },
  "dependencies": {
    "next": "^14.2.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "@prisma/client": "^5.14.0",
    "leaflet": "^1.9.0",
    "react-leaflet": "^4.2.0",
    "@types/leaflet": "^1.9.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.3.0"
  },
  "devDependencies": {
    "typescript": "^5.4.0",
    "@types/node": "^20.12.0",
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "prisma": "^5.14.0",
    "tsx": "^4.7.0",
    "eslint": "^8.57.0",
    "eslint-config-next": "^14.2.0"
  }
}
```

- [ ] **Step 2: Create tsconfig.json**

Create `web/tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

- [ ] **Step 3: Create next.config.js**

Create `web/next.config.js`:

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
};

module.exports = nextConfig;
```

- [ ] **Step 4: Create Tailwind config**

Create `web/tailwind.config.ts`:

```ts
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Earthy Warm theme
        earth: {
          50: "#faf6ed",
          100: "#f5f0e8",  // Background
          200: "#e8e0d0",
          300: "#e0d5c0",  // Border
          400: "#d4c5a9",
          500: "#c4b08a",
          600: "#6b5d4f",  // Text secondary
          700: "#3d3225",  // Text primary
          800: "#2a2218",
          900: "#1a1510",
        },
        // Rumpun colors
        rumpun: {
          austronesia: "#c4703f",
          papua: "#8b3a3a",
          transNewGuinea: "#5a7247",
          lainnya: "#6b5b8a",
        },
        // Vitalitas colors
        vitalitas: {
          aman: "#22c55e",
          rentan: "#eab308",
          terancam: "#f97316",
          kritis: "#ef4444",
        },
      },
      fontFamily: {
        sans: ["Plus Jakarta Sans", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
```

- [ ] **Step 5: Create PostCSS config**

Create `web/postcss.config.mjs`:

```js
/** @type {import('postcss-load-config').Config} */
const config = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};

export default config;
```

- [ ] **Step 6: Create .gitignore**

Create `web/.gitignore`:

```
node_modules/
.next/
out/
.env*.local
*.tsbuildinfo
```

- [ ] **Step 7: Install dependencies**

Run: `cd web && npm install`
Expected: All packages installed, no errors.

- [ ] **Step 8: Verify project structure**

Run: `cd web && npx next info`
Expected: Shows Next.js version, Node.js version, no errors.

- [ ] **Step 9: Commit**

```bash
git add web/package.json web/tsconfig.json web/next.config.js web/tailwind.config.ts web/postcss.config.mjs web/.gitignore
git commit -m "feat: setup Next.js project with TypeScript and Tailwind"
```

---

## Task 2: Global Styles + Layout + Font

**Files:**
- Create: `web/app/globals.css`
- Create: `web/app/layout.tsx`

- [ ] **Step 1: Create globals.css**

Create `web/app/globals.css`:

```css
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  * {
    @apply border-earth-300;
  }

  body {
    @apply bg-earth-100 text-earth-700 font-sans antialiased;
  }
}

@layer components {
  .glass-panel {
    @apply bg-earth-50/90 backdrop-blur-sm border border-earth-300 rounded-lg shadow-sm;
  }

  .btn-primary {
    @apply px-4 py-2 bg-earth-700 text-earth-100 rounded-lg hover:bg-earth-800 transition-colors font-medium;
  }

  .btn-secondary {
    @apply px-4 py-2 bg-earth-200 text-earth-700 rounded-lg hover:bg-earth-300 transition-colors font-medium;
  }

  .input-field {
    @apply w-full px-3 py-2 bg-earth-50 border border-earth-400 rounded-lg text-earth-700 placeholder-earth-600 focus:outline-none focus:ring-2 focus:ring-earth-500 focus:border-transparent;
  }
}

/* Leaflet overrides for Earthy Warm theme */
.leaflet-container {
  font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
}

.leaflet-popup-content-wrapper {
  @apply bg-earth-50 text-earth-700 rounded-lg shadow-md;
}

.leaflet-popup-tip {
  @apply bg-earth-50;
}

.leaflet-popup-content {
  @apply m-3;
}
```

- [ ] **Step 2: Create root layout**

Create `web/app/layout.tsx`:

```tsx
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Peta Bahasa Indonesia",
  description: "Peta interaktif persebaran bahasa daerah di Indonesia. Jelajahi 700+ bahasa dari Aceh sampai Papua.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="id">
      <body className="min-h-screen">
        {children}
      </body>
    </html>
  );
}
```

- [ ] **Step 3: Verify build**

Run: `cd web && npm run build`
Expected: Build succeeds (may show route warnings — that's OK, pages not created yet).

- [ ] **Step 4: Commit**

```bash
git add web/app/globals.css web/app/layout.tsx
git commit -m "feat: add global styles, Earthy Warm theme, Plus Jakarta Sans font"
```

---

## Task 3: Prisma Schema + Database Setup

**Files:**
- Create: `web/prisma/schema.prisma`
- Create: `web/.env.local`
- Create: `web/lib/prisma.ts`
- Create: `web/lib/types.ts`

- [ ] **Step 1: Create .env.local**

Create `web/.env.local`:

```env
# Get this from Supabase Dashboard → Settings → Database → Connection string
DATABASE_URL="postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT].supabase.co:5432/postgres"

# 9Router (existing)
NINEROUTER_URL="http://localhost:20128"
NINEROUTER_KEY="sk-2ce0b3116b58ede3-4v2kkj-033fc842"
```

Note: User must replace with actual Supabase connection string. For local development, can also use local PostgreSQL.

- [ ] **Step 2: Create Prisma schema**

Create `web/prisma/schema.prisma`:

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// Rumpun Bahasa — Taxonomy tree (self-referencing)
model RumpunBahasa {
  id              String       @id @default(uuid()) @db.Uuid
  namaRumpun      String       @map("nama_rumpun") @db.VarChar(100)
  subRumpun       String?      @map("sub_rumpun") @db.VarChar(100)
  parentId        String?      @map("parent_id") @db.Uuid
  parent          RumpunBahasa? @relation("RumpunHierarchy", fields: [parentId], references: [id])
  children        RumpunBahasa[] @relation("RumpunHierarchy")
  levelTaksonomi  Int?         @map("level_taksonomi")
  referensi       String?      @map("referensi") @db.Text
  dibuatPada      DateTime     @default(now()) @map("dibuat_pada")
  diperbaruiPada  DateTime     @default(now()) @updatedAt @map("diperbarui_pada")
  bahasa          Bahasa[]

  @@map("rumpun_bahasa")
}

// Bahasa — Main entity
model Bahasa {
  id                 String            @id @default(uuid()) @db.Uuid
  namaBahasa         String            @map("nama_bahasa") @db.VarChar(150)
  namaLokal          String?           @map("nama_lokal") @db.VarChar(150)
  kodeIso639         String?           @unique @map("kode_iso_639") @db.Char(3)
  rumpunId           String?           @map("rumpun_id") @db.Uuid
  rumpun             RumpunBahasa?     @relation(fields: [rumpunId], references: [id])
  jumlahPenutur      Int?              @map("jumlah_penutur")
  statusVitalitas    String?           @map("status_vitalitas") @db.VarChar(30)
  tanggalDokumentasi DateTime?         @map("tanggal_dokumentasi") @db.Date
  // Store coordinates as JSON (PostGIS GEOGRAPHY not native in Prisma)
  koordinatPusat     Json?             @map("koordinat_pusat")
  geojsonWilayah     Json?             @map("geojson_wilayah")
  catatan            String?           @map("catatan") @db.Text
  autoSummary        String?           @map("auto_summary") @db.Text
  dibuatPada         DateTime          @default(now()) @map("dibuat_pada")
  diperbaruiPada     DateTime          @default(now()) @updatedAt @map("diperbarui_pada")
  lokasi             Lokasi[]
  fiturLinguistik    FiturLinguistik?
  kosakata           Kosakata[]
  statusPreservasi   StatusPreservasi?
  manuskrip          Manuskrip[]

  @@index([kodeIso639])
  @@index([statusVitalitas])
  @@index([rumpunId])
  @@map("bahasa")
}

// Lokasi — Geographic distribution
model Lokasi {
  id             String   @id @default(uuid()) @db.Uuid
  bahasaId       String   @map("bahasa_id") @db.Uuid
  bahasa         Bahasa   @relation(fields: [bahasaId], references: [id], onDelete: Cascade)
  provinsi       String?  @db.VarChar(100)
  kabupaten      String?  @db.VarChar(100)
  kecamatan      String?  @db.VarChar(100)
  tipeWilayah    String?  @map("tipe_wilayah") @db.VarChar(30)
  polygonGeojson Json?    @map("polygon_geojson")
  luasKm2        Decimal? @map("luas_km2") @db.Decimal(12, 2)
  dibuatPada     DateTime @default(now()) @map("dibuat_pada")

  @@index([bahasaId])
  @@map("lokasi")
}

// Fitur Linguistik — One per bahasa
model FiturLinguistik {
  id              String   @id @default(uuid()) @db.Uuid
  bahasaId        String   @unique @map("bahasa_id") @db.Uuid
  bahasa          Bahasa   @relation(fields: [bahasaId], references: [id], onDelete: Cascade)
  sistemTulisan   String?  @map("sistem_tulisan") @db.VarChar(60)
  tipeMorfologi   String?  @map("tipe_morfologi") @db.VarChar(30)
  urutanKata      String?  @map("urutan_kata") @db.Char(3)
  jumlahVokal     Int?     @map("jumlah_vokal")
  jumlahKonsonan  Int?     @map("jumlah_konsonan")
  memilikiNada    Boolean  @default(false) @map("memiliki_nada")
  memilikiRegister Boolean @default(false) @map("memiliki_register")
  catatanFonologi String?  @map("catatan_fonologi") @db.Text
  dibuatPada      DateTime @default(now()) @map("dibuat_pada")
  diperbaruiPada  DateTime @default(now()) @updatedAt @map("diperbarui_pada")

  @@map("fitur_linguistik")
}

// Kosakata — Vocabulary entries
model Kosakata {
  id              String   @id @default(uuid()) @db.Uuid
  bahasaId        String   @map("bahasa_id") @db.Uuid
  bahasa          Bahasa   @relation(fields: [bahasaId], references: [id], onDelete: Cascade)
  kata            String   @db.VarChar(200)
  artiIndonesia   String   @map("arti_indonesia") @db.VarChar(200)
  fonetikIpa      String?  @map("fonetik_ipa") @db.VarChar(200)
  dalamSwadesh    Boolean  @default(false) @map("dalam_swadesh")
  nomorSwadesh    Int?     @map("nomor_swadesh")
  audioUrl        String?  @map("audio_url")
  catatan         String?  @db.Text
  dibuatPada      DateTime @default(now()) @map("dibuat_pada")

  @@index([bahasaId])
  @@index([bahasaId, dalamSwadesh])
  @@map("kosakata")
}

// Status Preservasi — One per bahasa
model StatusPreservasi {
  id                String   @id @default(uuid()) @db.Uuid
  bahasaId          String   @unique @map("bahasa_id") @db.Uuid
  bahasa            Bahasa   @relation(fields: [bahasaId], references: [id], onDelete: Cascade)
  skalaUnesco       Int?     @map("skala_unesco")
  ancamanUtama      String[] @map("ancaman_utama")
  programAktif      String?  @map("program_aktif") @db.Text
  lembagaPelestari  String?  @map("lembaga_pelestari") @db.VarChar(200)
  tahunPenilaian    Int?     @map("tahun_penilaian")
  urlLaporan        String?  @map("url_laporan")
  dibuatPada        DateTime @default(now()) @map("dibuat_pada")
  diperbaruiPada    DateTime @default(now()) @updatedAt @map("diperbarui_pada")

  @@map("status_preservasi")
}

// Manuskrip — Manuscripts and artifacts
model Manuskrip {
  id                String   @id @default(uuid()) @db.Uuid
  bahasaId          String   @map("bahasa_id") @db.Uuid
  bahasa            Bahasa   @relation(fields: [bahasaId], references: [id], onDelete: Cascade)
  judul             String   @db.VarChar(300)
  abad              String?  @db.VarChar(20)
  jenisAksara       String?  @map("jenis_aksara") @db.VarChar(100)
  bahasaDigunakan   String?  @map("bahasa_digunakan") @db.VarChar(100)
  lokasiSimpan      String?  @map("lokasi_simpan") @db.VarChar(200)
  kondisi           String?  @db.VarChar(20)
  urlDigitalisasi   String?  @map("url_digitalisasi")
  catatan           String?  @db.Text
  dibuatPada        DateTime @default(now()) @map("dibuat_pada")

  @@index([bahasaId])
  @@map("manuskrip")
}
```

Note: This schema covers the core tables needed for MVP. Additional tables (kontributor, media_dokumen, peristiwa_sejarah, etc.) will be added in Fase 2.

- [ ] **Step 3: Create Prisma client singleton**

Create `web/lib/prisma.ts`:

```ts
import { PrismaClient } from "@prisma/client";

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === "development" ? ["query", "error", "warn"] : ["error"],
  });

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;
```

- [ ] **Step 4: Create shared types**

Create `web/lib/types.ts`:

```ts
export interface BahasaMarker {
  id: string;
  namaBahasa: string;
  namaLokal: string | null;
  kodeIso639: string | null;
  jumlahPenutur: number | null;
  statusVitalitas: string | null;
  rumpunNama: string | null;
  lat: number;
  lng: number;
}

export interface BahasaDetail {
  id: string;
  namaBahasa: string;
  namaLokal: string | null;
  kodeIso639: string | null;
  rumpunNama: string | null;
  subRumpun: string | null;
  jumlahPenutur: number | null;
  statusVitalitas: string | null;
  autoSummary: string | null;
  fiturLinguistik: {
    sistemTulisan: string | null;
    tipeMorfologi: string | null;
    urutanKata: string | null;
    jumlahVokal: number | null;
    jumlahKonsonan: number | null;
  } | null;
  lokasi: {
    provinsi: string | null;
    kabupaten: string | null;
    tipeWilayah: string | null;
  }[];
  kosakata: {
    kata: string;
    artiIndonesia: string;
    fonetikIpa: string | null;
  }[];
}

export interface RumpunCount {
  id: string;
  namaRumpun: string;
  subRumpun: string | null;
  bahasaCount: number;
}

export interface GlobalStats {
  totalBahasa: number;
  totalRumpun: number;
  totalLokasi: number;
  vitalitasBreakdown: Record<string, number>;
}

export const VITALITAS_COLORS: Record<string, string> = {
  aman: "#22c55e",
  rentan: "#eab308",
  terancam: "#f97316",
  kritis: "#ef4444",
  "sangat terancam": "#f97316",
  punah: "#ef4444",
};

export const RUMPUN_COLORS: Record<string, string> = {
  Austronesia: "#c4703f",
  "Melayu-Polinesia": "#c4703f",
  Papua: "#8b3a3a",
  "Trans-New Guinea": "#5a7247",
};
```

- [ ] **Step 5: Generate Prisma client**

Run: `cd web && npm run db:generate`
Expected: Prisma client generated at `node_modules/@prisma/client`, no errors.

- [ ] **Step 6: Commit**

```bash
git add web/prisma/schema.prisma web/.env.local web/lib/prisma.ts web/lib/types.ts
git commit -m "feat: add Prisma schema for core tables, types, and DB client"
```

---

## Task 4: Seed Database — 20 Languages

**Files:**
- Create: `web/prisma/seed.ts`

- [ ] **Step 1: Create seed script**

Create `web/prisma/seed.ts`:

```ts
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

const seedData = [
  {
    namaBahasa: "Jawa",
    namaLokal: "Basa Jawa",
    kodeIso639: "jav",
    rumpun: "Austronesia",
    jumlahPenutur: 98000000,
    statusVitalitas: "rentan",
    lat: -7.5,
    lng: 110.5,
    provinsi: "Jawa Tengah",
    sistemTulisan: "Latin, Hanacaraka",
    tipeMorfologi: "aglutinatif",
    urutanKata: "SVO",
  },
  {
    namaBahasa: "Sunda",
    namaLokal: "Basa Sunda",
    kodeIso639: "sun",
    rumpun: "Austronesia",
    jumlahPenutur: 42000000,
    statusVitalitas: "rentan",
    lat: -6.9,
    lng: 107.6,
    provinsi: "Jawa Barat",
    sistemTulisan: "Latin",
    tipeMorfologi: "aglutinatif",
    urutanKata: "SVO",
  },
  {
    namaBahasa: "Madura",
    namaLokal: "Bâsa Madhurâ",
    kodeIso639: "mad",
    rumpun: "Austronesia",
    jumlahPenutur: 13700000,
    statusVitalitas: "rentan",
    lat: -7.0,
    lng: 113.3,
    provinsi: "Jawa Timur",
    sistemTulisan: "Latin",
    tipeMorfologi: "aglutinatif",
    urutanKata: "SVO",
  },
  {
    namaBahasa: "Batak Toba",
    namaLokal: "Hata Batak Toba",
    kodeIso639: "bbc",
    rumpun: "Austronesia",
    jumlahPenutur: 2000000,
    statusVitalitas: "rentan",
    lat: 2.5,
    lng: 99.0,
    provinsi: "Sumatera Utara",
    sistemTulisan: "Latin, Surat Batak",
    tipeMorfologi: "aglutinatif",
    urutanKata: "VSO",
  },
  {
    namaBahasa: "Batak Karo",
    namaLokal: "Hata Karo",
    kodeIso639: "btx",
    rumpun: "Austronesia",
    jumlahPenutur: 600000,
    statusVitalitas: "rentan",
    lat: 3.0,
    lng: 98.5,
    provinsi: "Sumatera Utara",
    sistemTulisan: "Latin",
    tipeMorfologi: "aglutinatif",
    urutanKata: "VSO",
  },
  {
    namaBahasa: "Minangkabau",
    namaLokal: "Baso Minangkabau",
    kodeIso639: "min",
    rumpun: "Austronesia",
    jumlahPenutur: 6500000,
    statusVitalitas: "rentan",
    lat: -0.5,
    lng: 100.5,
    provinsi: "Sumatera Barat",
    sistemTulisan: "Latin, Jawi",
    tipeMorfologi: "aglutinatif",
    urutanKata: "SVO",
  },
  {
    namaBahasa: "Bugis",
    namaLokal: "Basa Ugi",
    kodeIso639: "bug",
    rumpun: "Austronesia",
    jumlahPenutur: 5000000,
    statusVitalitas: "rentan",
    lat: -4.0,
    lng: 120.0,
    provinsi: "Sulawesi Selatan",
    sistemTulisan: "Latin, Lontara",
    tipeMorfologi: "aglutinatif",
    urutanKata: "SVO",
  },
  {
    namaBahasa: "Makassar",
    namaLokal: "Basa Mangkasara'",
    kodeIso639: "mak",
    rumpun: "Austronesia",
    jumlahPenutur: 2100000,
    statusVitalitas: "rentan",
    lat: -5.1,
    lng: 119.4,
    provinsi: "Sulawesi Selatan",
    sistemTulisan: "Latin, Lontara",
    tipeMorfologi: "aglutinatif",
    urutanKata: "SVO",
  },
  {
    namaBahasa: "Bali",
    namaLokal: "Basa Bali",
    kodeIso639: "ban",
    rumpun: "Austronesia",
    jumlahPenutur: 3300000,
    statusVitalitas: "rentan",
    lat: -8.4,
    lng: 115.1,
    provinsi: "Bali",
    sistemTulisan: "Latin, Balinese",
    tipeMorfologi: "aglutinatif",
    urutanKata: "SVO",
  },
  {
    namaBahasa: "Sasak",
    namaLokal: "Basa Sasak",
    kodeIso639: "sas",
    rumpun: "Austronesia",
    jumlahPenutur: 2700000,
    statusVitalitas: "rentan",
    lat: -8.6,
    lng: 116.3,
    provinsi: "Nusa Tenggara Barat",
    sistemTulisan: "Latin",
    tipeMorfologi: "aglutinatif",
    urutanKata: "SVO",
  },
  {
    namaBahasa: "Banjar",
    namaLokal: "Bahasa Banjar",
    kodeIso639: "bjn",
    rumpun: "Austronesia",
    jumlahPenutur: 6300000,
    statusVitalitas: "rentan",
    lat: -3.3,
    lng: 114.6,
    provinsi: "Kalimantan Selatan",
    sistemTulisan: "Latin",
    tipeMorfologi: "aglutinatif",
    urutanKata: "SVO",
  },
  {
    namaBahasa: "Dayak Ngaju",
    namaLokal: "Basa Ngaju",
    kodeIso639: "nij",
    rumpun: "Austronesia",
    jumlahPenutur: 890000,
    statusVitalitas: "rentan",
    lat: -1.7,
    lng: 113.5,
    provinsi: "Kalimantan Tengah",
    sistemTulisan: "Latin",
    tipeMorfologi: "aglutinatif",
    urutanKata: "SVO",
  },
  {
    namaBahasa: "Dayak Iban",
    namaLokal: "Jaku Iban",
    kodeIso639: "ibl",
    rumpun: "Austronesia",
    jumlahPenutur: 1200000,
    statusVitalitas: "rentan",
    lat: 1.0,
    lng: 111.5,
    provinsi: "Kalimantan Barat",
    sistemTulisan: "Latin",
    tipeMorfologi: "aglutinatif",
    urutanKata: "SVO",
  },
  {
    namaBahasa: "Gorontalo",
    namaLokal: "Bahasa Hulontalo",
    kodeIso639: "gor",
    rumpun: "Austronesia",
    jumlahPenutur: 900000,
    statusVitalitas: "rentan",
    lat: 0.5,
    lng: 122.2,
    provinsi: "Gorontalo",
    sistemTulisan: "Latin",
    tipeMorfologi: "aglutinatif",
    urutanKata: "SVO",
  },
  {
    namaBahasa: "Toraja",
    namaLokal: "Basa Toraja",
    kodeIso639: "sda",
    rumpun: "Austronesia",
    jumlahPenutur: 650000,
    statusVitalitas: "rentan",
    lat: -3.0,
    lng: 119.8,
    provinsi: "Sulawesi Selatan",
    sistemTulisan: "Latin",
    tipeMorfologi: "aglutinatif",
    urutanKata: "SVO",
  },
  {
    namaBahasa: "Bima",
    namaLokal: "Basa Mbojo",
    kodeIso639: "bhp",
    rumpun: "Austronesia",
    jumlahPenutur: 500000,
    statusVitalitas: "rentan",
    lat: -8.5,
    lng: 118.7,
    provinsi: "Nusa Tenggara Barat",
    sistemTulisan: "Latin",
    tipeMorfologi: "aglutinatif",
    urutanKata: "SVO",
  },
  {
    namaBahasa: "Batak Simalungun",
    namaLokal: "Hata Simalungun",
    kodeIso639: "bts",
    rumpun: "Austronesia",
    jumlahPenutur: 1300000,
    statusVitalitas: "rentan",
    lat: 2.8,
    lng: 99.3,
    provinsi: "Sumatera Utara",
    sistemTulisan: "Latin",
    tipeMorfologi: "aglutinatif",
    urutanKata: "VSO",
  },
  {
    namaBahasa: "Asmat",
    namaLokal: "Asmat",
    kodeIso639: "asm",
    rumpun: "Papua",
    jumlahPenutur: 65000,
    statusVitalitas: "sangat terancam",
    lat: -5.3,
    lng: 138.5,
    provinsi: "Papua",
    sistemTulisan: "Latin",
    tipeMorfologi: "aglutinatif",
    urutanKata: "SOV",
  },
  {
    namaBahasa: "Dani",
    namaLokal: "Dani",
    kodeIso639: "dna",
    rumpun: "Trans-New Guinea",
    jumlahPenutur: 200000,
    statusVitalitas: "rentan",
    lat: -4.1,
    lng: 139.0,
    provinsi: "Papua",
    sistemTulisan: "Latin",
    tipeMorfologi: "aglutinatif",
    urutanKata: "SOV",
  },
  {
    namaBahasa: "Melayu",
    namaLokal: "Bahasa Melayu",
    kodeIso639: "msa",
    rumpun: "Austronesia",
    jumlahPenutur: 77000000,
    statusVitalitas: "aman",
    lat: 1.0,
    lng: 104.0,
    provinsi: "Kepulauan Riau",
    sistemTulisan: "Latin, Jawi",
    tipeMorfologi: "aglutinatif",
    urutanKata: "SVO",
  },
];

async function main() {
  console.log("Seeding database...");

  // Create rumpun
  const rumpunMap: Record<string, string> = {};
  const rumpunNames = [...new Set(seedData.map((d) => d.rumpun))];

  for (const nama of rumpunNames) {
    const rumpun = await prisma.rumpunBahasa.create({
      data: {
        namaRumpun: nama,
        levelTaksonomi: nama === "Austronesia" ? 2 : 1,
      },
    });
    rumpunMap[nama] = rumpun.id;
    console.log(`  Rumpun: ${nama} (${rumpun.id})`);
  }

  // Create bahasa with lokasi and fitur
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
        lokasi: {
          create: {
            provinsi: data.provinsi,
          },
        },
        fiturLinguistik: {
          create: {
            sistemTulisan: data.sistemTulisan,
            tipeMorfologi: data.tipeMorfologi,
            urutanKata: data.urutanKata,
          },
        },
      },
    });
    console.log(`  Bahasa: ${data.namaBahasa} (${bahasa.id})`);
  }

  console.log(`\nSeeded ${seedData.length} languages, ${rumpunNames.length} rumpun.`);
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
```

- [ ] **Step 2: Push schema to database**

Prerequisite: User must set `DATABASE_URL` in `web/.env.local` to actual Supabase connection string.

Run: `cd web && npm run db:push`
Expected: All tables created in Supabase. Output shows table names.

- [ ] **Step 3: Run seed**

Run: `cd web && npm run db:seed`
Expected: Output shows each rumpun and bahasa created. Final line: "Seeded 20 languages, 3 rumpun."

- [ ] **Step 4: Verify data**

Run a quick Prisma query or check Supabase dashboard to confirm 20 bahasa entries exist.

- [ ] **Step 5: Commit**

```bash
git add web/prisma/seed.ts
git commit -m "feat: add seed data for 20 Indonesian languages"
```

---

## Task 5: API Routes — Bahasa, Locations, Stats

**Files:**
- Create: `web/app/api/bahasa/route.ts`
- Create: `web/app/api/bahasa/[id]/route.ts`
- Create: `web/app/api/locations/markers/route.ts`
- Create: `web/app/api/rumpun/route.ts`
- Create: `web/app/api/stats/route.ts`
- Create: `web/lib/cache.ts`

- [ ] **Step 1: Create in-memory cache**

Create `web/lib/cache.ts`:

```ts
interface CacheEntry<T> {
  data: T;
  expiry: number;
}

const cache = new Map<string, CacheEntry<unknown>>();

export function getCache<T>(key: string): T | null {
  const entry = cache.get(key);
  if (!entry) return null;
  if (Date.now() > entry.expiry) {
    cache.delete(key);
    return null;
  }
  return entry.data as T;
}

export function setCache<T>(key: string, data: T, ttlMs: number): void {
  cache.set(key, { data, expiry: Date.now() + ttlMs });
}

export function clearCache(): void {
  cache.clear();
}

// TTL constants
export const TTL = {
  MARKERS: 5 * 60 * 1000,       // 5 minutes
  STATS: 60 * 60 * 1000,        // 1 hour
  RUMPUN: 60 * 60 * 1000,       // 1 hour
  DETAIL: 60 * 60 * 1000,       // 1 hour
} as const;
```

- [ ] **Step 2: Create markers API**

Create `web/app/api/locations/markers/route.ts`:

```ts
import { NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getCache, setCache, TTL } from "@/lib/cache";
import type { BahasaMarker } from "@/lib/types";

export async function GET() {
  const cached = getCache<BahasaMarker[]>("markers");
  if (cached) {
    return NextResponse.json(cached);
  }

  const bahasaList = await prisma.bahasa.findMany({
    select: {
      id: true,
      namaBahasa: true,
      namaLokal: true,
      kodeIso639: true,
      jumlahPenutur: true,
      statusVitalitas: true,
      rumpun: { select: { namaRumpun: true } },
      koordinatPusat: true,
    },
  });

  const markers: BahasaMarker[] = bahasaList
    .filter((b) => b.koordinatPusat)
    .map((b) => {
      const coords = b.koordinatPusat as { coordinates: [number, number] };
      return {
        id: b.id,
        namaBahasa: b.namaBahasa,
        namaLokal: b.namaLokal,
        kodeIso639: b.kodeIso639,
        jumlahPenutur: b.jumlahPenutur,
        statusVitalitas: b.statusVitalitas,
        rumpunNama: b.rumpun?.namaRumpun ?? null,
        lat: coords.coordinates[1],
        lng: coords.coordinates[0],
      };
    });

  setCache("markers", markers, TTL.MARKERS);
  return NextResponse.json(markers);
}
```

- [ ] **Step 3: Create bahasa list API**

Create `web/app/api/bahasa/route.ts`:

```ts
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
      where,
      select: {
        id: true,
        namaBahasa: true,
        namaLokal: true,
        kodeIso639: true,
        jumlahPenutur: true,
        statusVitalitas: true,
        rumpun: { select: { namaRumpun: true } },
      },
      orderBy: { namaBahasa: "asc" },
      take: limit,
      skip: offset,
    }),
    prisma.bahasa.count({ where }),
  ]);

  return NextResponse.json({ data, total, limit, offset });
}
```

- [ ] **Step 4: Create bahasa detail API**

Create `web/app/api/bahasa/[id]/route.ts`:

```ts
import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getCache, setCache, TTL } from "@/lib/cache";

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const cacheKey = `bahasa:${params.id}`;
  const cached = getCache(cacheKey);
  if (cached) {
    return NextResponse.json(cached);
  }

  const bahasa = await prisma.bahasa.findUnique({
    where: { id: params.id },
    include: {
      rumpun: { select: { namaRumpun: true, subRumpun: true } },
      lokasi: { select: { provinsi: true, kabupaten: true, tipeWilayah: true } },
      fiturLinguistik: {
        select: {
          sistemTulisan: true,
          tipeMorfologi: true,
          urutanKata: true,
          jumlahVokal: true,
          jumlahKonsonan: true,
        },
      },
      kosakata: {
        select: { kata: true, artiIndonesia: true, fonetikIpa: true },
        take: 20,
      },
    },
  });

  if (!bahasa) {
    return NextResponse.json({ error: "Bahasa not found" }, { status: 404 });
  }

  setCache(cacheKey, bahasa, TTL.DETAIL);
  return NextResponse.json(bahasa);
}
```

- [ ] **Step 5: Create stats API**

Create `web/app/api/stats/route.ts`:

```ts
import { NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getCache, setCache, TTL } from "@/lib/cache";

export async function GET() {
  const cached = getCache("stats");
  if (cached) {
    return NextResponse.json(cached);
  }

  const [totalBahasa, totalRumpun, totalLokasi, vitalitasRaw] = await Promise.all([
    prisma.bahasa.count(),
    prisma.rumpunBahasa.count(),
    prisma.lokasi.count(),
    prisma.bahasa.groupBy({
      by: ["statusVitalitas"],
      _count: true,
    }),
  ]);

  const vitalitasBreakdown: Record<string, number> = {};
  for (const v of vitalitasRaw) {
    if (v.statusVitalitas) {
      vitalitasBreakdown[v.statusVitalitas] = v._count;
    }
  }

  const stats = { totalBahasa, totalRumpun, totalLokasi, vitalitasBreakdown };
  setCache("stats", stats, TTL.STATS);
  return NextResponse.json(stats);
}
```

- [ ] **Step 6: Create rumpun API**

Create `web/app/api/rumpun/route.ts`:

```ts
import { NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getCache, setCache, TTL } from "@/lib/cache";

export async function GET() {
  const cached = getCache("rumpun");
  if (cached) {
    return NextResponse.json(cached);
  }

  const rumpunList = await prisma.rumpunBahasa.findMany({
    select: {
      id: true,
      namaRumpun: true,
      subRumpun: true,
      _count: { select: { bahasa: true } },
    },
    orderBy: { namaRumpun: "asc" },
  });

  const result = rumpunList.map((r) => ({
    id: r.id,
    namaRumpun: r.namaRumpun,
    subRumpun: r.subRumpun,
    bahasaCount: r._count.bahasa,
  }));

  setCache("rumpun", result, TTL.RUMPUN);
  return NextResponse.json(result);
}
```

- [ ] **Step 7: Test API routes**

Run: `cd web && npm run dev`
Open: `http://localhost:3000/api/stats`
Expected: JSON with `totalBahasa: 20`, `totalRumpun: 3`, `totalLokasi: 20`, `vitalitasBreakdown`.

Open: `http://localhost:3000/api/locations/markers`
Expected: JSON array of 20 markers with lat/lng.

- [ ] **Step 8: Commit**

```bash
git add web/lib/cache.ts web/app/api/ web/lib/prisma.ts web/lib/types.ts
git commit -m "feat: add API routes for bahasa, markers, stats, rumpun with caching"
```

---

## Task 6: Shared UI Components

**Files:**
- Create: `web/components/ui/VitalityBadge.tsx`
- Create: `web/components/ui/LanguageCard.tsx`
- Create: `web/components/ui/SearchInput.tsx`
- Create: `web/components/ui/FilterPanel.tsx`
- Create: `web/components/shared/LoadingState.tsx`

- [ ] **Step 1: Create VitalityBadge**

Create `web/components/ui/VitalityBadge.tsx`:

```tsx
import { VITALITAS_COLORS } from "@/lib/types";

interface VitalityBadgeProps {
  status: string | null;
  size?: "sm" | "md";
}

export function VitalityBadge({ status, size = "sm" }: VitalityBadgeProps) {
  if (!status) return null;

  const color = VITALITAS_COLORS[status] ?? "#9ca3af";
  const sizeClasses = size === "sm" ? "text-xs px-2 py-0.5" : "text-sm px-3 py-1";

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full font-medium text-white ${sizeClasses}`}
      style={{ backgroundColor: color }}
    >
      <span className="w-1.5 h-1.5 rounded-full bg-white/60" />
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  );
}
```

- [ ] **Step 2: Create LanguageCard**

Create `web/components/ui/LanguageCard.tsx`:

```tsx
import Link from "next/link";
import { VitalityBadge } from "./VitalityBadge";

interface LanguageCardProps {
  id: string;
  namaBahasa: string;
  namaLokal: string | null;
  jumlahPenutur: number | null;
  statusVitalitas: string | null;
  rumpunNama: string | null;
}

export function LanguageCard({
  id,
  namaBahasa,
  namaLokal,
  jumlahPenutur,
  statusVitalitas,
  rumpunNama,
}: LanguageCardProps) {
  const penuturFormatted = jumlahPenutur
    ? jumlahPenutur >= 1000000
      ? `${(jumlahPenutur / 1000000).toFixed(1)}M`
      : `${(jumlahPenutur / 1000).toFixed(0)}K`
    : "—";

  return (
    <Link
      href={`/explore/bahasa/${id}`}
      className="block p-3 rounded-lg border border-earth-300 hover:border-earth-400 hover:bg-earth-50 transition-colors"
    >
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <h3 className="font-semibold text-earth-700 truncate">{namaBahasa}</h3>
          {namaLokal && (
            <p className="text-sm text-earth-600 truncate">{namaLokal}</p>
          )}
        </div>
        <VitalityBadge status={statusVitalitas} />
      </div>
      <div className="mt-2 flex items-center gap-3 text-sm text-earth-600">
        <span>{penuturFormatted} penutur</span>
        {rumpunNama && (
          <>
            <span className="w-1 h-1 rounded-full bg-earth-400" />
            <span>{rumpunNama}</span>
          </>
        )}
      </div>
    </Link>
  );
}
```

- [ ] **Step 3: Create SearchInput**

Create `web/components/ui/SearchInput.tsx`:

```tsx
interface SearchInputProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}

export function SearchInput({
  value,
  onChange,
  placeholder = "Cari bahasa...",
}: SearchInputProps) {
  return (
    <div className="relative">
      <svg
        className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-earth-600"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
        />
      </svg>
      <input
        type="text"
        className="input-field pl-10"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
      />
    </div>
  );
}
```

- [ ] **Step 4: Create FilterPanel**

Create `web/components/ui/FilterPanel.tsx`:

```tsx
interface FilterPanelProps {
  rumpunFilter: string;
  vitalitasFilter: string;
  onRumpunChange: (value: string) => void;
  onVitalitasChange: (value: string) => void;
  rumpunList: { id: string; namaRumpun: string; bahasaCount: number }[];
}

const VITALITAS_OPTIONS = [
  { value: "", label: "Semua status" },
  { value: "aman", label: "Aman" },
  { value: "rentan", label: "Rentan" },
  { value: "terancam", label: "Terancam" },
  { value: "sangat terancam", label: "Sangat terancam" },
  { value: "kritis", label: "Kritis" },
];

export function FilterPanel({
  rumpunFilter,
  vitalitasFilter,
  onRumpunChange,
  onVitalitasChange,
  rumpunList,
}: FilterPanelProps) {
  return (
    <div className="space-y-4">
      <div>
        <label className="text-sm font-medium text-earth-700 mb-1.5 block">
          Rumpun Bahasa
        </label>
        <select
          className="input-field"
          value={rumpunFilter}
          onChange={(e) => onRumpunChange(e.target.value)}
        >
          <option value="">Semua rumpun</option>
          {rumpunList.map((r) => (
            <option key={r.id} value={r.namaRumpun}>
              {r.namaRumpun} ({r.bahasaCount})
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className="text-sm font-medium text-earth-700 mb-1.5 block">
          Status Vitalitas
        </label>
        <select
          className="input-field"
          value={vitalitasFilter}
          onChange={(e) => onVitalitasChange(e.target.value)}
        >
          {VITALITAS_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
```

- [ ] **Step 5: Create LoadingState**

Create `web/components/shared/LoadingState.tsx`:

```tsx
export function LoadingState({ message = "Memuat..." }: { message?: string }) {
  return (
    <div className="flex items-center justify-center py-8">
      <div className="flex items-center gap-3 text-earth-600">
        <div className="w-5 h-5 border-2 border-earth-400 border-t-earth-700 rounded-full animate-spin" />
        <span className="text-sm">{message}</span>
      </div>
    </div>
  );
}
```

- [ ] **Step 6: Commit**

```bash
git add web/components/
git commit -m "feat: add shared UI components (VitalityBadge, LanguageCard, SearchInput, FilterPanel)"
```

---

## Task 7: Map Page — Leaflet + Markers + Sidebar

**Files:**
- Create: `web/components/map/LanguageMap.tsx`
- Create: `web/components/map/LanguageMarkers.tsx`
- Create: `web/components/map/MapPopup.tsx`
- Create: `web/components/layout/Header.tsx`
- Create: `web/components/layout/Sidebar.tsx`
- Create: `web/app/explore/map/page.tsx`

- [ ] **Step 1: Create Leaflet map wrapper (client component)**

Create `web/components/map/LanguageMap.tsx`:

```tsx
"use client";

import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { LanguageMarkers } from "./LanguageMarkers";
import type { BahasaMarker } from "@/lib/types";

interface LanguageMapProps {
  markers: BahasaMarker[];
  center?: [number, number];
  zoom?: number;
}

export function LanguageMap({
  markers,
  center = [-2.5, 118.0], // Center of Indonesia
  zoom = 5,
}: LanguageMapProps) {
  return (
    <MapContainer
      center={center}
      zoom={zoom}
      className="w-full h-full"
      zoomControl={true}
    >
      <TileLayer
        attribution='&copy; <a href="https://carto.com/">CARTO</a>'
        url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
      />
      <LanguageMarkers markers={markers} />
    </MapContainer>
  );
}
```

- [ ] **Step 2: Create marker layer**

Create `web/components/map/LanguageMarkers.tsx`:

```tsx
"use client";

import { Marker, Popup, useMap } from "react-leaflet";
import { Icon } from "leaflet";
import { MapPopup } from "./MapPopup";
import type { BahasaMarker } from "@/lib/types";

// Custom marker icon with rumpun color
function createMarkerIcon(rumpunNama: string | null): Icon {
  const color = rumpunNama === "Papua"
    ? "#8b3a3a"
    : rumpunNama === "Trans-New Guinea"
    ? "#5a7247"
    : "#c4703f";

  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="36" viewBox="0 0 24 36">
      <path d="M12 0C5.4 0 0 5.4 0 12c0 9 12 24 12 24s12-15 12-24C24 5.4 18.6 0 12 0z"
        fill="${color}" stroke="white" stroke-width="1.5"/>
      <circle cx="12" cy="12" r="5" fill="white" opacity="0.9"/>
    </svg>
  `;

  return new Icon({
    iconUrl: `data:image/svg+xml;base64,${btoa(svg)}`,
    iconSize: [24, 36],
    iconAnchor: [12, 36],
    popupAnchor: [0, -36],
  });
}

interface LanguageMarkersProps {
  markers: BahasaMarker[];
}

export function LanguageMarkers({ markers }: LanguageMarkersProps) {
  const map = useMap();

  return (
    <>
      {markers.map((m) => (
        <Marker
          key={m.id}
          position={[m.lat, m.lng]}
          icon={createMarkerIcon(m.rumpunNama)}
          eventHandlers={{
            click: () => {
              map.flyTo([m.lat, m.lng], 8, { duration: 1 });
            },
          }}
        >
          <Popup>
            <MapPopup marker={m} />
          </Popup>
        </Marker>
      ))}
    </>
  );
}
```

- [ ] **Step 3: Create popup content**

Create `web/components/map/MapPopup.tsx`:

```tsx
import Link from "next/link";
import { VitalityBadge } from "@/components/ui/VitalityBadge";
import type { BahasaMarker } from "@/lib/types";

interface MapPopupProps {
  marker: BahasaMarker;
}

export function MapPopup({ marker }: MapPopupProps) {
  const penutur = marker.jumlahPenutur
    ? marker.jumlahPenutur.toLocaleString("id-ID")
    : "Tidak diketahui";

  return (
    <div className="min-w-[200px]">
      <h3 className="font-semibold text-earth-700 text-base">{marker.namaBahasa}</h3>
      {marker.namaLokal && (
        <p className="text-sm text-earth-600 italic">{marker.namaLokal}</p>
      )}
      <div className="mt-2 space-y-1 text-sm">
        <div className="flex justify-between">
          <span className="text-earth-600">Penutur</span>
          <span className="font-medium text-earth-700">{penutur}</span>
        </div>
        {marker.rumpunNama && (
          <div className="flex justify-between">
            <span className="text-earth-600">Rumpun</span>
            <span className="font-medium text-earth-700">{marker.rumpunNama}</span>
          </div>
        )}
        <div className="flex justify-between items-center">
          <span className="text-earth-600">Status</span>
          <VitalityBadge status={marker.statusVitalitas} />
        </div>
      </div>
      <Link
        href={`/explore/bahasa/${marker.id}`}
        className="mt-3 block text-center text-sm text-rumpun-austronesia hover:underline font-medium"
      >
        Lihat detail →
      </Link>
    </div>
  );
}
```

- [ ] **Step 4: Create Header**

Create `web/components/layout/Header.tsx`:

```tsx
import Link from "next/link";

export function Header() {
  return (
    <header className="bg-earth-50/90 backdrop-blur-sm border-b border-earth-300 px-4 py-3">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2">
          <span className="text-xl">🗺️</span>
          <span className="font-bold text-earth-700 text-lg">
            Peta Bahasa Indonesia
          </span>
        </Link>
        <nav className="flex items-center gap-4">
          <Link
            href="/explore/map"
            className="text-sm font-medium text-earth-700 hover:text-earth-600"
          >
            Jelajahi
          </Link>
          <span className="text-earth-400 text-sm">|</span>
          <span className="text-sm text-earth-600">
            Research <span className="text-earth-400">(soon)</span>
          </span>
        </nav>
      </div>
    </header>
  );
}
```

- [ ] **Step 5: Create Sidebar**

Create `web/components/layout/Sidebar.tsx`:

```tsx
import { SearchInput } from "@/components/ui/SearchInput";
import { FilterPanel } from "@/components/ui/FilterPanel";
import { LanguageCard } from "@/components/ui/LanguageCard";
import { LoadingState } from "@/components/shared/LoadingState";

interface SidebarProps {
  search: string;
  onSearchChange: (v: string) => void;
  rumpunFilter: string;
  onRumpunChange: (v: string) => void;
  vitalitasFilter: string;
  onVitalitasChange: (v: string) => void;
  rumpunList: { id: string; namaRumpun: string; bahasaCount: number }[];
  bahasaList: {
    id: string;
    namaBahasa: string;
    namaLokal: string | null;
    jumlahPenutur: number | null;
    statusVitalitas: string | null;
    rumpunNama: string | null;
  }[];
  loading: boolean;
}

export function Sidebar({
  search,
  onSearchChange,
  rumpunFilter,
  onRumpunChange,
  vitalitasFilter,
  onVitalitasChange,
  rumpunList,
  bahasaList,
  loading,
}: SidebarProps) {
  return (
    <div className="w-80 h-full flex flex-col bg-earth-50/95 backdrop-blur-sm border-r border-earth-300">
      <div className="p-4 space-y-4 border-b border-earth-300">
        <SearchInput value={search} onChange={onSearchChange} />
        <FilterPanel
          rumpunFilter={rumpunFilter}
          vitalitasFilter={vitalitasFilter}
          onRumpunChange={onRumpunChange}
          onVitalitasChange={onVitalitasChange}
          rumpunList={rumpunList}
        />
      </div>

      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {loading ? (
          <LoadingState message="Memuat bahasa..." />
        ) : bahasaList.length === 0 ? (
          <p className="text-center text-sm text-earth-600 py-8">
            Tidak ada bahasa yang sesuai filter.
          </p>
        ) : (
          <>
            <p className="text-xs text-earth-600 px-1">
              {bahasaList.length} bahasa ditemukan
            </p>
            {bahasaList.map((b) => (
              <LanguageCard key={b.id} {...b} />
            ))}
          </>
        )}
      </div>
    </div>
  );
}
```

- [ ] **Step 6: Create map page**

Create `web/app/explore/map/page.tsx`:

```tsx
"use client";

import { useState, useEffect } from "react";
import dynamic from "next/dynamic";
import { Header } from "@/components/layout/Header";
import { Sidebar } from "@/components/layout/Sidebar";
import type { BahasaMarker } from "@/lib/types";

// Dynamic import for Leaflet (SSR incompatible)
const LanguageMap = dynamic(
  () => import("@/components/map/LanguageMap").then((m) => ({ default: m.LanguageMap })),
  { ssr: false, loading: () => <div className="flex-1 bg-earth-200 flex items-center justify-center">Memuat peta...</div> }
);

export default function MapPage() {
  const [markers, setMarkers] = useState<BahasaMarker[]>([]);
  const [bahasaList, setBahasaList] = useState<BahasaMarker[]>([]);
  const [rumpunList, setRumpunList] = useState<{ id: string; namaRumpun: string; bahasaCount: number }[]>([]);
  const [search, setSearch] = useState("");
  const [rumpunFilter, setRumpunFilter] = useState("");
  const [vitalitasFilter, setVitalitasFilter] = useState("");
  const [loading, setLoading] = useState(true);

  // Fetch markers
  useEffect(() => {
    fetch("/api/locations/markers")
      .then((r) => r.json())
      .then((data) => {
        setMarkers(data);
        setBahasaList(data);
      })
      .finally(() => setLoading(false));
  }, []);

  // Fetch rumpun
  useEffect(() => {
    fetch("/api/rumpun")
      .then((r) => r.json())
      .then((data) => setRumpunList(data));
  }, []);

  // Apply filters
  useEffect(() => {
    let filtered = markers;

    if (search) {
      const q = search.toLowerCase();
      filtered = filtered.filter(
        (b) =>
          b.namaBahasa.toLowerCase().includes(q) ||
          b.namaLokal?.toLowerCase().includes(q)
      );
    }

    if (rumpunFilter) {
      filtered = filtered.filter((b) => b.rumpunNama === rumpunFilter);
    }

    if (vitalitasFilter) {
      filtered = filtered.filter((b) => b.statusVitalitas === vitalitasFilter);
    }

    setBahasaList(filtered);
  }, [search, rumpunFilter, vitalitasFilter, markers]);

  return (
    <div className="h-screen flex flex-col">
      <Header />
      <div className="flex-1 flex overflow-hidden">
        <Sidebar
          search={search}
          onSearchChange={setSearch}
          rumpunFilter={rumpunFilter}
          onRumpunChange={setRumpunFilter}
          vitalitasFilter={vitalitasFilter}
          onVitalitasChange={setVitalitasFilter}
          rumpunList={rumpunList}
          bahasaList={bahasaList.map((b) => ({
            id: b.id,
            namaBahasa: b.namaBahasa,
            namaLokal: b.namaLokal,
            jumlahPenutur: b.jumlahPenutur,
            statusVitalitas: b.statusVitalitas,
            rumpunNama: b.rumpunNama,
          }))}
          loading={loading}
        />
        <div className="flex-1">
          <LanguageMap markers={bahasaList} />
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 7: Test map page**

Run: `cd web && npm run dev`
Open: `http://localhost:3000/explore/map`
Expected: Full-screen map with Leaflet (CARTO Voyager tiles), 20 colored markers, sidebar with search + filters + language list. Clicking a marker zooms in and shows popup.

- [ ] **Step 8: Commit**

```bash
git add web/components/map/ web/components/layout/ web/app/explore/
git commit -m "feat: add interactive map page with Leaflet, markers, sidebar, filters"
```

---

## Task 8: Landing Page + Language Detail Page

**Files:**
- Create: `web/app/page.tsx`
- Create: `web/app/explore/page.tsx`
- Create: `web/app/explore/bahasa/[slug]/page.tsx`

- [ ] **Step 1: Create landing page**

Create `web/app/page.tsx`:

```tsx
import Link from "next/link";

async function getStats() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL ?? "http://localhost:3000"}/api/stats`, {
    cache: "no-store",
  });
  if (!res.ok) return null;
  return res.json();
}

export default async function HomePage() {
  const stats = await getStats();

  return (
    <div className="min-h-screen">
      {/* Hero */}
      <section className="bg-gradient-to-b from-earth-100 to-earth-200 py-20 px-4">
        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl font-bold text-earth-700 mb-4">
            Peta Bahasa Indonesia
          </h1>
          <p className="text-lg text-earth-600 mb-8">
            Jelajahi persebaran bahasa daerah dari Aceh sampai Papua.
            Temukan keragaman linguistik Nusantara dalam satu peta interaktif.
          </p>
          <Link href="/explore/map" className="btn-primary text-lg px-8 py-3">
            Mulai Jelajahi →
          </Link>
        </div>
      </section>

      {/* Stats */}
      {stats && (
        <section className="py-12 px-4">
          <div className="max-w-4xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="glass-panel p-6 text-center">
              <div className="text-3xl font-bold text-earth-700">{stats.totalBahasa}</div>
              <div className="text-sm text-earth-600 mt-1">Bahasa</div>
            </div>
            <div className="glass-panel p-6 text-center">
              <div className="text-3xl font-bold text-earth-700">{stats.totalRumpun}</div>
              <div className="text-sm text-earth-600 mt-1">Rumpun</div>
            </div>
            <div className="glass-panel p-6 text-center">
              <div className="text-3xl font-bold text-earth-700">{stats.totalLokasi}</div>
              <div className="text-sm text-earth-600 mt-1">Lokasi</div>
            </div>
            <div className="glass-panel p-6 text-center">
              <div className="text-3xl font-bold text-earth-700">
                {Object.keys(stats.vitalitasBreakdown).length}
              </div>
              <div className="text-sm text-earth-600 mt-1">Status Vitalitas</div>
            </div>
          </div>
        </section>
      )}

      {/* CTA */}
      <section className="py-16 px-4 text-center">
        <h2 className="text-2xl font-semibold text-earth-700 mb-4">
          Siap Menjelajahi?
        </h2>
        <p className="text-earth-600 mb-6">
          Lihat peta interaktif dengan marker berwarna per rumpun bahasa.
        </p>
        <Link href="/explore/map" className="btn-primary">
          Buka Peta →
        </Link>
      </section>
    </div>
  );
}
```

- [ ] **Step 2: Create explore redirect page**

Create `web/app/explore/page.tsx`:

```tsx
import { redirect } from "next/navigation";

export default function ExplorePage() {
  redirect("/explore/map");
}
```

- [ ] **Step 3: Create language detail page**

Create `web/app/explore/bahasa/[slug]/page.tsx`:

```tsx
import { notFound } from "next/navigation";
import Link from "next/link";
import { Header } from "@/components/layout/Header";
import { VitalityBadge } from "@/components/ui/VitalityBadge";

interface BahasaDetailData {
  id: string;
  namaBahasa: string;
  namaLokal: string | null;
  kodeIso639: string | null;
  autoSummary: string | null;
  jumlahPenutur: number | null;
  statusVitalitas: string | null;
  rumpun: { namaRumpun: string | null; subRumpun: string | null } | null;
  lokasi: { provinsi: string | null; kabupaten: string | null; tipeWilayah: string | null }[];
  fiturLinguistik: {
    sistemTulisan: string | null;
    tipeMorfologi: string | null;
    urutanKata: string | null;
    jumlahVokal: number | null;
    jumlahKonsonan: number | null;
  } | null;
  kosakata: { kata: string; artiIndonesia: string; fonetikIpa: string | null }[];
}

async function getBahasa(id: string): Promise<BahasaDetailData | null> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL ?? "http://localhost:3000"}/api/bahasa/${id}`, {
    cache: "no-store",
  });
  if (!res.ok) return null;
  return res.json();
}

export default async function BahasaDetailPage({
  params,
}: {
  params: { slug: string };
}) {
  const bahasa = await getBahasa(params.slug);
  if (!bahasa) notFound();

  const penuturFormatted = bahasa.jumlahPenutur
    ? bahasa.jumlahPenutur.toLocaleString("id-ID")
    : "Tidak diketahui";

  return (
    <div className="min-h-screen">
      <Header />

      <main className="max-w-4xl mx-auto px-4 py-8">
        {/* Back button */}
        <Link
          href="/explore/map"
          className="inline-flex items-center gap-1 text-sm text-earth-600 hover:text-earth-700 mb-6"
        >
          ← Kembali ke peta
        </Link>

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold text-earth-700">{bahasa.namaBahasa}</h1>
              {bahasa.namaLokal && (
                <p className="text-lg text-earth-600 italic mt-1">{bahasa.namaLokal}</p>
              )}
            </div>
            <VitalityBadge status={bahasa.statusVitalitas} size="md" />
          </div>
        </div>

        {/* Info Grid */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <div className="glass-panel p-5">
            <h2 className="font-semibold text-earth-700 mb-3">Informasi Dasar</h2>
            <dl className="space-y-2 text-sm">
              <div className="flex justify-between">
                <dt className="text-earth-600">ISO 639-3</dt>
                <dd className="font-mono text-earth-700">{bahasa.kodeIso639 ?? "—"}</dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-earth-600">Rumpun</dt>
                <dd className="text-earth-700">{bahasa.rumpun?.namaRumpun ?? "—"}</dd>
              </div>
              {bahasa.rumpun?.subRumpun && (
                <div className="flex justify-between">
                  <dt className="text-earth-600">Sub-rumpun</dt>
                  <dd className="text-earth-700">{bahasa.rumpun.subRumpun}</dd>
                </div>
              )}
              <div className="flex justify-between">
                <dt className="text-earth-600">Jumlah Penutur</dt>
                <dd className="font-semibold text-earth-700">{penuturFormatted}</dd>
              </div>
            </dl>
          </div>

          <div className="glass-panel p-5">
            <h2 className="font-semibold text-earth-700 mb-3">Fitur Linguistik</h2>
            {bahasa.fiturLinguistik ? (
              <dl className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <dt className="text-earth-600">Sistem Tulisan</dt>
                  <dd className="text-earth-700">{bahasa.fiturLinguistik.sistemTulisan ?? "—"}</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-earth-600">Tipe Morfologi</dt>
                  <dd className="text-earth-700">{bahasa.fiturLinguistik.tipeMorfologi ?? "—"}</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-earth-600">Urutan Kata</dt>
                  <dd className="font-mono text-earth-700">{bahasa.fiturLinguistik.urutanKata ?? "—"}</dd>
                </div>
              </dl>
            ) : (
              <p className="text-sm text-earth-600">Data fitur linguistik belum tersedia.</p>
            )}
          </div>
        </div>

        {/* Lokasi */}
        {bahasa.lokasi.length > 0 && (
          <div className="glass-panel p-5 mb-8">
            <h2 className="font-semibold text-earth-700 mb-3">Lokasi Sebaran</h2>
            <div className="flex flex-wrap gap-2">
              {bahasa.lokasi.map((loc, i) => (
                <span
                  key={i}
                  className="px-3 py-1 bg-earth-200 text-earth-700 rounded-full text-sm"
                >
                  {loc.provinsi}
                  {loc.kabupaten && `, ${loc.kabupaten}`}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Summary (AI-generated, optional) */}
        {bahasa.autoSummary && (
          <div className="glass-panel p-5 mb-8">
            <h2 className="font-semibold text-earth-700 mb-3">Ringkasan</h2>
            <div className="prose prose-sm text-earth-600">
              {bahasa.autoSummary.split("\n").map((p, i) => (
                <p key={i}>{p}</p>
              ))}
            </div>
          </div>
        )}

        {/* Kosakata */}
        {bahasa.kosakata.length > 0 && (
          <div className="glass-panel p-5">
            <h2 className="font-semibold text-earth-700 mb-3">Kosakata Sampel</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-earth-300">
                    <th className="text-left py-2 text-earth-600 font-medium">Kata</th>
                    <th className="text-left py-2 text-earth-600 font-medium">Arti</th>
                    <th className="text-left py-2 text-earth-600 font-medium">Fonetik (IPA)</th>
                  </tr>
                </thead>
                <tbody>
                  {bahasa.kosakata.map((k, i) => (
                    <tr key={i} className="border-b border-earth-200">
                      <td className="py-2 font-medium text-earth-700">{k.kata}</td>
                      <td className="py-2 text-earth-600">{k.artiIndonesia}</td>
                      <td className="py-2 font-mono text-earth-600">{k.fonetikIpa ?? "—"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
```

- [ ] **Step 4: Test all pages**

Run: `cd web && npm run dev`
Open: `http://localhost:3000` → Landing page with stats
Open: `http://localhost:3000/explore/map` → Map page
Click any marker → Popup → "Lihat detail" → Detail page
Expected: All pages render correctly, data flows from API → components.

- [ ] **Step 5: Commit**

```bash
git add web/app/page.tsx web/app/explore/page.tsx web/app/explore/bahasa/
git commit -m "feat: add landing page and language detail page"
```

---

## Task 9: Deploy to Vercel

**Files:**
- Modify: `web/.env.local` (add production vars)

- [ ] **Step 1: Prepare for deployment**

Ensure `web/package.json` has the correct build script (already done in Task 1).

Add to `web/.env.local` for production:
```env
DATABASE_URL="postgresql://..."
NINEROUTER_URL="http://localhost:20128"
NINEROUTER_KEY="sk-..."
```

- [ ] **Step 2: Push to GitHub**

```bash
cd web
git add .
git commit -m "feat: complete MVP - ready for deployment"
git push origin main
```

- [ ] **Step 3: Deploy to Vercel**

Option A — CLI:
```bash
cd web
npx vercel --prod
```

Option B — Web UI:
1. Go to vercel.com
2. Import repository → select `web` folder as root
3. Set environment variables: `DATABASE_URL`, `NINEROUTER_URL`, `NINEROUTER_KEY`
4. Deploy

- [ ] **Step 4: Verify production**

Open the Vercel deployment URL.
Expected: Landing page loads, map page works, all API endpoints respond.

- [ ] **Step 5: Commit**

```bash
git add web/
git commit -m "deploy: MVP deployed to Vercel"
```

---

## Summary

| Task | Deliverable | Status |
|------|-------------|--------|
| 1 | Next.js project setup | ☐ |
| 2 | Global styles + font + theme | ☐ |
| 3 | Prisma schema + DB connection | ☐ |
| 4 | Seed 20 languages | ☐ |
| 5 | API routes + cache | ☐ |
| 6 | UI components | ☐ |
| 7 | Map page (Leaflet + sidebar) | ☐ |
| 8 | Landing + detail pages | ☐ |
| 9 | Deploy to Vercel | ☐ |

**Total estimated commits:** 9 (one per task)
**Total estimated time:** 2-3 hours (experienced developer)
