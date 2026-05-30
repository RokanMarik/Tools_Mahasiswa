import Link from "next/link";

export function Header() {
  return (
    <header className="bg-earth-50/90 backdrop-blur-sm border-b border-earth-300 px-4 py-3">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2">
          <span className="text-xl">🗺️</span>
          <span className="font-bold text-earth-700 text-lg">Peta Bahasa Indonesia</span>
        </Link>
        <nav className="flex items-center gap-4">
          <Link href="/explore/map" className="text-sm font-medium text-earth-700 hover:text-earth-600">Jelajahi</Link>
          <span className="text-earth-400 text-sm">|</span>
          <span className="text-sm text-earth-600">Research <span className="text-earth-400">(soon)</span></span>
        </nav>
      </div>
    </header>
  );
}
