import Link from "next/link";
import { Logo } from "@/components/shared/Logo";

export function Header() {
  return (
    <header className="bg-earth-50/90 backdrop-blur-sm border-b border-earth-300 px-4 py-3">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
          <Logo size="sm" />
        </Link>
        <nav className="flex items-center gap-4">
          <Link href="/explore/map" className="text-sm font-medium text-earth-700 hover:text-earth-600 transition-colors">Jelajahi</Link>
          <span className="text-earth-400 text-sm">|</span>
          <span className="text-sm text-earth-600">Research <span className="text-earth-400">(soon)</span></span>
        </nav>
      </div>
    </header>
  );
}
