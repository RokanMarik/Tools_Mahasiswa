"""Pretty terminal display."""
from typing import List, Dict
from tabulate import tabulate
from colorama import Fore, Style, init
init(autoreset=True)

class Display:
    def _clean(self, text):
        if not text: return ''
        return text.encode('ascii', 'replace').decode('ascii')

    def display_results(self, papers, query, sort="relevance", show_abstract=False):
        if not papers:
            return f"{Fore.YELLOW}Tidak ada hasil. Coba kata kunci lain.{Style.RESET_ALL}"
        lines = []
        lines.append(f"{Fore.CYAN}Hasil: '{query}' ({len(papers)} paper){Style.RESET_ALL}")
        lines.append("=" * 60)
        for i, p in enumerate(papers, 1):
            lines.append(f"{i}. {self._clean(p.get('title',''))}")
            if p.get('year'): lines.append(f"   Tahun: {p['year']}")
            if p.get('citations'): lines.append(f"   Disitasi: {p['citations']}x")
            if p.get('journal'): lines.append(f"   Jurnal: {p['journal']}")
            if p.get('doi'): lines.append(f"   DOI: {p['doi']}")
            if p.get('url'): lines.append(f"   URL: {p['url']}")
            lines.append(f"   [{p.get('source','')}]")
            lines.append('')
        return chr(10).join(lines)

    def display_balanced(self, foundational, recent, query):
        lines = []
        lines.append(f"{len(foundational)+len(recent)} paper - {len(foundational)} foundational + {len(recent)} terbaru")
        lines.append(f"Query: '{query}'")
        lines.append('=' * 60)
        if foundational:
            lines.append('FOUNDATIONAL (Paling Banyak Disitasi):')
            for i, p in enumerate(foundational, 1):
                lines.append(f"{i}. {p.get('title','')}")
                if p.get('citations'): lines.append(f"   Disitasi: {p['citations']}x")
                lines.append('')
        if recent:
            lines.append('TERBARU:')
            for i, p in enumerate(recent, len(foundational)+1):
                lines.append(f"{i}. {p.get('title','')}")
                if p.get('year'): lines.append(f"   Tahun: {p['year']}")
                lines.append('')
        return chr(10).join(lines)

    def display_table(self, papers):
        if not papers: return 'Tidak ada hasil.'
        rows = [{'No': i, 'Judul': p.get('title','')[:50], 'Tahun': p.get('year',''),
                 'Sitasi': p.get('citations',0), 'Sumber': p.get('source','')}
                for i, p in enumerate(papers, 1)]
        return tabulate(rows, headers='keys', tablefmt='grid')
