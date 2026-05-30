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
    <span className={`inline-flex items-center gap-1.5 rounded-full font-medium text-white ${sizeClasses}`} style={{ backgroundColor: color }}>
      <span className="w-1.5 h-1.5 rounded-full bg-white/60" />
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  );
}
