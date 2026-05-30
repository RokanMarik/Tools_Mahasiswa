import Link from "next/link";
import { VitalityBadge } from "@/components/ui/VitalityBadge";
import type { BahasaMarker } from "@/lib/types";

export function MapPopup({ marker }: { marker: BahasaMarker }) {
  const penutur = marker.jumlahPenutur ? marker.jumlahPenutur.toLocaleString("id-ID") : "Tidak diketahui";
  return (
    <div className="min-w-[220px]">
      <div className="flex items-center gap-2 mb-2">
        <div
          className="w-3 h-3 rounded-full flex-shrink-0"
          style={{ backgroundColor: marker.rumpunNama === "Papua" ? "#8b3a3a" : marker.rumpunNama === "Trans-New Guinea" ? "#5a7247" : "#c4703f" }}
        />
        <h3 className="font-semibold text-earth-700 text-base">{marker.namaBahasa}</h3>
      </div>
      {marker.namaLokal && <p className="text-sm text-earth-600 italic mb-3">{marker.namaLokal}</p>}
      <div className="space-y-1.5 text-sm">
        <div className="flex justify-between items-center">
          <span className="text-earth-600">Penutur</span>
          <span className="font-semibold text-earth-700">{penutur}</span>
        </div>
        {marker.rumpunNama && (
          <div className="flex justify-between items-center">
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
        className="mt-3 block text-center text-sm text-rumpun-austronesia hover:underline font-medium transition-colors"
      >
        Lihat detail →
      </Link>
    </div>
  );
}
