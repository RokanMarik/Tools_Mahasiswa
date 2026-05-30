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

export function LanguageCard({ id, namaBahasa, namaLokal, jumlahPenutur, statusVitalitas, rumpunNama }: LanguageCardProps) {
  const penuturFormatted = jumlahPenutur
    ? jumlahPenutur >= 1000000 ? `${(jumlahPenutur / 1000000).toFixed(1)}M` : `${(jumlahPenutur / 1000).toFixed(0)}K`
    : "—";

  return (
    <Link href={`/explore/bahasa/${id}`} className="block p-3 rounded-lg border border-earth-300 hover:border-earth-400 hover:bg-earth-50 transition-colors">
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <h3 className="font-semibold text-earth-700 truncate">{namaBahasa}</h3>
          {namaLokal && <p className="text-sm text-earth-600 truncate">{namaLokal}</p>}
        </div>
        <VitalityBadge status={statusVitalitas} />
      </div>
      <div className="mt-2 flex items-center gap-3 text-sm text-earth-600">
        <span>{penuturFormatted} penutur</span>
        {rumpunNama && (<><span className="w-1 h-1 rounded-full bg-earth-400" /><span>{rumpunNama}</span></>)}
      </div>
    </Link>
  );
}
