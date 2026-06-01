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
        """Explain WHY people cite this paper."""
        citations = p.get('citations', 0) or 0
        year = p.get('year', 0) or 0
        title = p.get('title', '').lower()
        age = (2025 - year) if year else 0
        doi = p.get('doi', '').lower()

        # Check both title AND journal for paper type
        text = title + ' ' + p.get('journal', '').lower()
        # Primary reason based on paper type
        if 'review' in text or 'survey' in text or 'meta-analysis' in text:
            primary = 'Review komprehensif — orang nyitasi ini karena rangkuman lengkap penelitian sebelumnya'
        elif 'introduction' in text or 'guide' in text or 'handbook' in text:
            primary = 'Buku panduan/pengenalan topik — jadi rujukan standar buat yang baru belajar'
        elif 'framework' in text or 'model' in text or 'theory' in text:
            primary = 'Menawarkan framework/model — peneliti lain pakai sebagai dasar teori'
        elif 'impact' in text or 'effect' in text or 'influence' in text:
            primary = 'Studi tentang dampak/efek — jadi referensi bukti empiris di bidang ini'
        elif 'method' in text or 'approach' in text or 'design' in text:
            primary = 'Menawarkan metode baru — peneliti lain mengadopsi pendekatannya'
        elif 'challenge' in text or 'barrier' in text or 'problem' in text:
            primary = 'Mengidentifikasi masalah/kendala — jadi acuan diskusi tantangan di bidang ini'
        elif 'best practice' in text or 'strategy' in text or 'technique' in text:
            primary = 'Rekomendasi strategi/best practice — dirujuk sebagai panduan praktis'
        elif 'case study' in text or 'implementation' in text:
            primary = 'Studi kasus implementasi — jadi contoh nyata yang bisa ditiru peneliti lain'
        else:
            # Generic but informative
            if citations >= 50:
                primary = 'Topik yang sangat relevan — banyak peneliti merujuk ke paper ini sebagai dasar'
            elif citations >= 10:
                primary = 'Penelitian penting di topik ini — jadi acuan utama dalam literatur'
            elif citations >= 1:
                primary = 'Kontribusi spesifik di bidangnya — peneliti lain menganggap relevan untuk dirujuk'
            else:
                primary = 'Belum ada sitasi — tapi topik ini relevan, berpotensi jadi referensi di masa depan'

        # Additional context
        extras = []
        if citations >= 100:
            extras.append('Sudah jadi standar rujukan di bidang ini')
        if age > 10:
            extras.append('Karya klasik — sudah bertahan lebih dari 10 tahun sebagai referensi')
        elif age <= 2 and citations > 0:
            extras.append('Baru tapi langsung impactful — menunjukkan kualitas tinggi')
        if p.get('journal', ''):
            j = p['journal'].lower()
            if any(k in j for k in ['handbook', 'encyclopedia', 'annual review']):
                extras.append('Terbit di sumber referensi bergengsi')

        parts = [primary] + extras
        return '; '.join(parts)

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

        # Citation reason (always shown)
        reason = self._citation_reason(p)
        if reason:
            color = Fore.GREEN if citations > 0 else Fore.LIGHTBLACK_EX
            lines.append(f"     {color}Kenapa disitasi:{Style.RESET_ALL} {reason}")

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
