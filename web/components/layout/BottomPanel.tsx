import { SearchInput } from "@/components/ui/SearchInput";
import { LanguageCard } from "@/components/ui/LanguageCard";
import { LoadingState } from "@/components/shared/LoadingState";
import Link from "next/link";

interface BottomPanelProps {
  search: string;
  onSearchChange: (v: string) => void;
  onSmartSearch: (query: string) => void;
  searchLoading: boolean;
  searchResultInfo: string | null;
  rumpunFilter: string;
  onRumpunChange: (v: string) => void;
  vitalitasFilter: string;
  onVitalitasChange: (v: string) => void;
  rumpunList: { id: string; namaRumpun: string; bahasaCount: number }[];
  bahasaList: { id: string; namaBahasa: string; namaLokal: string | null; jumlahPenutur: number | null; statusVitalitas: string | null; rumpunNama: string | null; lat: number; lng: number }[];
  loading: boolean;
}

export function BottomPanel({
  search, onSearchChange, onSmartSearch, searchLoading, searchResultInfo,
  rumpunFilter, onRumpunChange, vitalitasFilter, onVitalitasChange,
  rumpunList, bahasaList, loading,
}: BottomPanelProps) {
  return (
    <div className="bg-earth-50/95 backdrop-blur-sm border-t border-earth-300">
      {/* Search + Filters row */}
      <div className="px-4 py-3 border-b border-earth-300">
        <div className="flex gap-2 items-center max-w-4xl mx-auto">
          <div className="flex-1">
            <SearchInput value={search} onChange={onSearchChange} onSearch={onSmartSearch} loading={searchLoading} placeholder="Cari bahasa, daerah, rumpun..." />
          </div>
          <select
            className="input-field w-auto text-sm"
            value={rumpunFilter}
            onChange={(e) => onRumpunChange(e.target.value)}
          >
            <option value="">Rumpun</option>
            {rumpunList.map((r) => (
              <option key={r.id} value={r.namaRumpun}>{r.namaRumpun}</option>
            ))}
          </select>
          <select
            className="input-field w-auto text-sm"
            value={vitalitasFilter}
            onChange={(e) => onVitalitasChange(e.target.value)}
          >
            <option value="">Status</option>
            <option value="aman">Aman</option>
            <option value="rentan">Rentan</option>
            <option value="terancam">Terancam</option>
            <option value="sangat terancam">Sangat terancam</option>
            <option value="kritis">Kritis</option>
          </select>
        </div>
        {searchResultInfo && (
          <p className="text-xs text-earth-600 mt-2 max-w-4xl mx-auto">{searchResultInfo}</p>
        )}
      </div>

      {/* Horizontal scroll cards */}
      <div className="px-4 py-3">
        {loading ? (
          <LoadingState message="Memuat bahasa..." />
        ) : bahasaList.length === 0 ? (
          <p className="text-center text-sm text-earth-600 py-4">Tidak ada bahasa yang sesuai filter.</p>
        ) : (
          <>
            <p className="text-xs text-earth-600 mb-2">{bahasaList.length} bahasa ditemukan</p>
            <div className="flex gap-3 overflow-x-auto pb-2 snap-x snap-mandatory" style={{ scrollbarWidth: 'thin', scrollbarColor: '#d4c5a9 #faf6ed' }}>
              {bahasaList.map((b) => (
                <div key={b.id} className="snap-start flex-shrink-0 w-56">
                  <Link
                    href={`/explore/bahasa/${b.id}`}
                    className="block p-3 rounded-lg border border-earth-300 hover:border-earth-400 hover:bg-earth-50 transition-colors bg-earth-50/50"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="min-w-0">
                        <h3 className="font-semibold text-earth-700 truncate text-sm">{b.namaBahasa}</h3>
                        {b.namaLokal && (
                          <p className="text-xs text-earth-600 truncate">{b.namaLokal}</p>
                        )}
                      </div>
                      {b.statusVitalitas && (
                        <span
                          className="flex-shrink-0 w-2 h-2 rounded-full"
                          style={{
                            backgroundColor:
                              b.statusVitalitas === 'aman' ? '#22c55e' :
                              b.statusVitalitas === 'rentan' ? '#eab308' :
                              b.statusVitalitas === 'terancam' ? '#f97316' :
                              '#ef4444',
                          }}
                        />
                      )}
                    </div>
                    <div className="mt-2 flex items-center gap-2 text-xs text-earth-600">
                      <span>{b.jumlahPenutur ? (b.jumlahPenutur >= 1000000 ? `${(b.jumlahPenutur / 1000000).toFixed(1)}M` : `${(b.jumlahPenutur / 1000).toFixed(0)}K`) : '—'} penutur</span>
                      {b.rumpunNama && (
                        <>
                          <span className="w-1 h-1 rounded-full bg-earth-400" />
                          <span>{b.rumpunNama}</span>
                        </>
                      )}
                    </div>
                  </Link>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
