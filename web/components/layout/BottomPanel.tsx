import { SearchInput } from "@/components/ui/SearchInput";
import { RUMPUN_COLORS, VITALITAS_COLORS } from "@/lib/types";
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
    <div className="mx-3 mb-3">
      {/* Glassmorphism container */}
      <div className="bg-earth-50/90 backdrop-blur-md rounded-xl border border-earth-300/50 shadow-lg overflow-hidden">
        {/* Search + Filters */}
        <div className="px-4 py-3 border-b border-earth-300/30">
          <div className="flex gap-2 items-center">
            <div className="flex-1">
              <SearchInput value={search} onChange={onSearchChange} onSearch={onSmartSearch} loading={searchLoading} placeholder="Cari bahasa, daerah, rumpun..." />
            </div>
            <select
              className="input-field w-auto text-sm rounded-lg bg-earth-100/50 border-earth-300/30"
              value={rumpunFilter}
              onChange={(e) => onRumpunChange(e.target.value)}
            >
              <option value="">Rumpun</option>
              {rumpunList.map((r) => (
                <option key={r.id} value={r.namaRumpun}>{r.namaRumpun}</option>
              ))}
            </select>
            <select
              className="input-field w-auto text-sm rounded-lg bg-earth-100/50 border-earth-300/30"
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
            <p className="text-xs text-earth-600 mt-1.5">{searchResultInfo}</p>
          )}
        </div>

        {/* Horizontal scroll cards */}
        <div className="px-4 py-3">
          {loading ? (
            <div className="flex items-center justify-center py-6">
              <div className="flex items-center gap-2 text-earth-600">
                <div className="w-4 h-4 border-2 border-earth-400 border-t-earth-700 rounded-full animate-spin" />
                <span className="text-sm">Memuat...</span>
              </div>
            </div>
          ) : bahasaList.length === 0 ? (
            <p className="text-center text-sm text-earth-600 py-4">Tidak ada bahasa yang sesuai filter.</p>
          ) : (
            <>
              <p className="text-xs text-earth-600 mb-2">{bahasaList.length} bahasa</p>
              <div className="flex gap-2.5 overflow-x-auto pb-1 snap-x snap-mandatory" style={{ scrollbarWidth: 'thin' }}>
                {bahasaList.map((b) => {
                  const rumpunColor = RUMPUN_COLORS[b.rumpunNama || ''] || '#6b5b8a';
                  const vitalitasColor = VITALITAS_COLORS[b.statusVitalitas || ''] || '#9ca3af';
                  return (
                    <div key={b.id} className="snap-start flex-shrink-0 w-52">
                      <Link
                        href={`/explore/bahasa/${b.id}`}
                        className="block p-3 rounded-lg border border-earth-300/40 hover:border-earth-400 hover:bg-earth-100/50 transition-all bg-earth-100/30 group"
                      >
                        <div className="flex items-start gap-2.5">
                          {/* Rumpun color dot */}
                          <div
                            className="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center text-white text-xs font-bold"
                            style={{ backgroundColor: rumpunColor }}
                          >
                            {b.namaBahasa.charAt(0)}
                          </div>
                          <div className="min-w-0 flex-1">
                            <h3 className="font-semibold text-earth-700 text-sm truncate group-hover:text-earth-800 transition-colors">{b.namaBahasa}</h3>
                            {b.namaLokal && (
                              <p className="text-xs text-earth-600 truncate italic">{b.namaLokal}</p>
                            )}
                          </div>
                          {/* Vitalitas indicator */}
                          <div
                            className="flex-shrink-0 w-2 h-2 rounded-full mt-1"
                            style={{ backgroundColor: vitalitasColor }}
                            title={b.statusVitalitas || ''}
                          />
                        </div>
                        <div className="mt-2 flex items-center gap-2 text-xs text-earth-600">
                          <span className="font-medium">
                            {b.jumlahPenutur ? (b.jumlahPenutur >= 1000000 ? `${(b.jumlahPenutur / 1000000).toFixed(1)}M` : `${(b.jumlahPenutur / 1000).toFixed(0)}K`) : '—'}
                          </span>
                          <span className="w-1 h-1 rounded-full bg-earth-400" />
                          <span className="truncate">{b.rumpunNama}</span>
                        </div>
                      </Link>
                    </div>
                  );
                })}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
