import Link from "next/link";
import { VitalityBadge } from "@/components/ui/VitalityBadge";
import type { BahasaMarker } from "@/lib/types";

export function MapPopup({ marker }: { marker: BahasaMarker }) {
  const penutur = marker.jumlahPenutur ? marker.jumlahPenutur.toLocaleString("id-ID") : "Tidak diketahui";
  return (
    <div className="min-w-[200px]">
      <h3 className="font-semibold text-earth-700 text-base">{marker.namaBahasa}</h3>
      {marker.namaLokal && <p className="text-sm text-earth-600 italic">{marker.namaLokal}</p>}
      <div className="mt-2 space-y-1 text-sm">
        <div className="flex justify-between"><span className="text-earth-600">Penutur</span><span className="font-medium text-earth-700">{penutur}</span></div>
        {marker.rumpunNama && (<div className="flex justify-between"><span className="text-earth-600">Rumpun</span><span className="font-medium text-earth-700">{marker.rumpunNama}</span></div>)}
        <div className="flex justify-between items-center"><span className="text-earth-600">Status</span><VitalityBadge status={marker.statusVitalitas} /></div>
      </div>
      <Link href={`/explore/bahasa/${marker.id}`} className="mt-3 block text-center text-sm text-rumpun-austronesia hover:underline font-medium">Lihat detail →</Link>
    </div>
  );
}
