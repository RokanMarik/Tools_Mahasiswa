import Link from "next/link";
import { Logo } from "./Logo";

export function Header() {
  return (
    <header className="absolute top-0 left-0 right-0 z-[1000] px-4 py-2">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
          <div className="bg-earth-50/90 backdrop-blur-md rounded-lg px-3 py-1.5 border border-earth-300/50 shadow-sm">
            <Logo size="sm" />
          </div>
        </Link>
        <nav className="flex items-center gap-1 bg-earth-50/90 backdrop-blur-md rounded-lg px-2 py-1.5 border border-earth-300/50 shadow-sm">
          <Link href="/explore/map" className="text-sm font-medium text-earth-700 hover:text-earth-600 transition-colors px-3 py-1 rounded-md hover:bg-earth-200/50">Peta</Link>
          <span className="text-earth-400 text-xs">·</span>
          <span className="text-sm text-earth-600 px-3 py-1 opacity-50">Research</span>
        </nav>
      </div>
    </header>
  );
}
