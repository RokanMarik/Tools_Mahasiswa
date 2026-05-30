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
