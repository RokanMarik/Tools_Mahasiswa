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
