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

export function FilterPanel({ rumpunFilter, vitalitasFilter, onRumpunChange, onVitalitasChange, rumpunList }: FilterPanelProps) {
  return (
    <div className="space-y-4">
      <div>
        <label className="text-sm font-medium text-earth-700 mb-1.5 block">Rumpun Bahasa</label>
        <select className="input-field" value={rumpunFilter} onChange={(e) => onRumpunChange(e.target.value)}>
          <option value="">Semua rumpun</option>
          {rumpunList.map((r) => (<option key={r.id} value={r.namaRumpun}>{r.namaRumpun} ({r.bahasaCount})</option>))}
        </select>
      </div>
      <div>
        <label className="text-sm font-medium text-earth-700 mb-1.5 block">Status Vitalitas</label>
        <select className="input-field" value={vitalitasFilter} onChange={(e) => onVitalitasChange(e.target.value)}>
          {VITALITAS_OPTIONS.map((opt) => (<option key={opt.value} value={opt.value}>{opt.label}</option>))}
        </select>
      </div>
    </div>
  );
}
