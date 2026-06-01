"""Pretty terminal display."""
from typing import List, Dict
from tabulate import tabulate
from colorama import Fore, Style, init
init(autoreset=True)


class Display:
    def _clean(self, text):
        if not text: return ''
        return text.encode('ascii', 'replace').decode('ascii')

    def _citation_reason(self, p):
        """Give reason why a paper is highly cited."""
        citations = p.get('citations', 0) or 0
        year = p.get('year', 0) or 0
        title = p.get('title', '').lower()

        reasons = []
        if citations >= 100:
            reasons.append('Paper referensi utama di bidangnya')
        elif citations >= 50:
            reasons.append('Sering jadi rujukan penting')
        elif citations >= 10:
            reasons.append('Banyak dikutip peneliti lain')
        elif citations >= 1:
            reasons.append('Mulai banyak dirujuk')

        if year and (2025 - year) > 10:
            reasons.append('Sudah lama terbit, banyak waktu untuk disitasi')
        elif year and (2025 - year) <= 2:
            reasons.append('Baru terbit tapi sudah langsung banyak disitasi')

        if 'review' in title or 'survey' in title:
            reasons.append('Jenis review article, memang sering disitasi')

        if not reasons and citations > 0:
            reasons.append('Topik relevan dan banyak diteliti')

        return '; '.join(reasons) if reasons else ''

    def _format_paper(self, p, n):
        """Format a single paper with full details."""
        title = self._clean(p.get('title', 'Untitled'))
        lines = [f"  {Fore.WHITE}{n}. {title}{Style.RESET_ALL}"]

        if p.get('year'):
            lines.append(f"     {Fore.LIGHTBLACK_EX}Tahun:{Style.RESET_ALL} {p['year']}")

        citations = p.get('citations', 0) or 0
        if citations:
            lines.append(f"     {Fore.LIGHTBLACK_EX}Disitasi:{Style.RESET_ALL} {Fore.YELLOW}{citations}x{Style.RESET_ALL}")

        if p.get('quality_score') is not None:
            qs = p['quality_score']
            color = Fore.GREEN if qs > 60 else (Fore.YELLOW if qs > 40 else Fore.RED)
            lines.append(f"     {Fore.LIGHTBLACK_EX}Skor kualitas:{Style.RESET_ALL} {color}{qs}/100{Style.RESET_ALL}")

        if p.get('journal'):
            lines.append(f"     {Fore.LIGHTBLACK_EX}Jurnal:{Style.RESET_ALL} {p['journal']}")

        # Link (DOI URL)
        doi = p.get('doi', '')
        url = p.get('url', '')
        if doi:
            lines.append(f"     {Fore.LIGHTBLACK_EX}Link:{Style.RESET_ALL} https://doi.org/{doi}")
        elif url:
            lines.append(f"     {Fore.LIGHTBLACK_EX}Link:{Style.RESET_ALL} {url}")

        # Citation reason
        if citations > 0:
            reason = self._citation_reason(p)
            if reason:
                lines.append(f"     {Fore.GREEN}Kenapa disitasi:{Style.RESET_ALL} {reason}")

        if p.get('summary'):
            lines.append(f"     {Fore.CYAN}Ringkasan:{Style.RESET_ALL} {p['summary']}")

        badges = {"semantic-scholar": "[Semantic Scholar]", "crossref": "[Crossref]", "garuda": "[Garuda]"}
        badge = badges.get(p.get('source', ''), p.get('source', ''))
        lines.append(f"     {Fore.MAGENTA}{badge}{Style.RESET_ALL}")
        return "\n".join(lines)

    def display_results(self, papers, query, sort="relevance", show_abstract=False, show_quality=True):
        if not papers:
            return f"{Fore.YELLOW}Tidak ada hasil. Coba kata kunci lain.{Style.RESET_ALL}"
        lines = [
            f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}",
            f"{Fore.CYAN}Hasil: '{query}' ({len(papers)} paper){Style.RESET_ALL}",
            f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}",
            ""
        ]
        for i, p in enumerate(papers, 1):
            lines.append(self._format_paper(p, i))
            lines.append("")
        return "\n".join(lines)

    def display_balanced(self, foundational, recent, query):
        lines = [
            f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}",
            f"{Fore.CYAN}{len(foundational)+len(recent)} paper - {len(foundational)} foundational + {len(recent)} terbaru{Style.RESET_ALL}",
            f"{Fore.CYAN}Query: '{query}'{Style.RESET_ALL}",
            f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}",
            ""
        ]
        if foundational:
            lines.append(f"{Fore.YELLOW}FOUNDATIONAL (Paling Banyak Disitasi):{Style.RESET_ALL}")
            lines.append("")
            for i, p in enumerate(foundational, 1):
                lines.append(self._format_paper(p, i))
                lines.append(f"  {Fore.GREEN}-> Alasan disitasi banyak: {self._citation_reason(p)}{Style.RESET_ALL}")
                lines.append("")
        if recent:
            lines.append(f"{Fore.BLUE}TERBARU:{Style.RESET_ALL}")
            lines.append("")
            n = len(foundational) + 1
            for i, p in enumerate(recent, n):
                lines.append(self._format_paper(p, i))
                lines.append("")
        return "\n".join(lines)

    def display_table(self, papers):
        if not papers: return 'Tidak ada hasil.'
        rows = [{'No': i, 'Judul': self._clean(p.get('title',''))[:60], 'Tahun': p.get('year',''),
                 'Sitasi': p.get('citations',0), 'Skor': p.get('quality_score',''), 'Sumber': p.get('source','')}
                for i, p in enumerate(papers, 1)]
        return tabulate(rows, headers='keys', tablefmt='grid')
