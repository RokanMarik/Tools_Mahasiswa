import { SearchInput } from "@/components/ui/SearchInput";
import { FilterPanel } from "@/components/ui/FilterPanel";
import { LanguageCard } from "@/components/ui/LanguageCard";
import { LoadingState } from "@/components/shared/LoadingState";

interface SidebarProps {
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
  bahasaList: { id: string; namaBahasa: string; namaLokal: string | null; jumlahPenutur: number | null; statusVitalitas: string | null; rumpunNama: string | null }[];
  loading: boolean;
}

export function Sidebar({
  search, onSearchChange, onSmartSearch, searchLoading, searchResultInfo,
  rumpunFilter, onRumpunChange, vitalitasFilter, onVitalitasChange,
  rumpunList, bahasaList, loading,
}: SidebarProps) {
  return (
    <div className="w-80 h-full flex flex-col bg-earth-50/95 backdrop-blur-sm border-r border-earth-300">
      <div className="p-4 space-y-4 border-b border-earth-300">
        <SearchInput value={search} onChange={onSearchChange} onSearch={onSmartSearch} loading={searchLoading} />
        {searchResultInfo && (
          <p className="text-xs text-earth-600 italic">{searchResultInfo}</p>
        )}
        <FilterPanel
          rumpunFilter={rumpunFilter} vitalitasFilter={vitalitasFilter}
          onRumpunChange={onRumpunChange} onVitalitasChange={onVitalitasChange}
          rumpunList={rumpunList}
        />
      </div>
      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {loading ? (<LoadingState message="Memuat bahasa..." />) : bahasaList.length === 0 ? (
          <p className="text-center text-sm text-earth-600 py-8">Tidak ada bahasa yang sesuai filter.</p>
        ) : (<>
          <p className="text-xs text-earth-600 px-1">{bahasaList.length} bahasa ditemukan</p>
          {bahasaList.map((b) => (<LanguageCard key={b.id} {...b} />))}
        </>)}
      </div>
    </div>
  );
}
