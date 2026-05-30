"""Citation formatting for Zotero items (APA, IEEE, MLA, Chicago)."""

from typing import Dict, List


class CitationFormatter:
    STYLES = ["apa", "ieee", "mla", "chicago"]

    def format(self, item: Dict, style: str = "apa", number: int = None) -> str:
        """Format an item into a citation string.

        Args:
            item: Item dict with title, authors, date, doi, journal, etc.
            style: Citation style ('apa', 'ieee', 'mla', 'chicago').
            number: Item number (used by IEEE for [1], [2], etc.).

        Returns:
            Formatted citation string.
        """
        if style not in self.STYLES:
            style = "apa"  # Default to APA

        method = getattr(self, f"_format_{style}")
        return method(item, number)

    def _format_authors_apa(self, authors: List[str]) -> str:
        """Format authors in APA style: Smith, J., & Doe, J."""
        if not authors:
            return "Unknown Author"

        formatted = []
        for author in authors:
            parts = author.strip().split()
            if len(parts) >= 2:
                last = parts[-1]
                initials = ". ".join([p[0] + "." for p in parts[:-1]])
                formatted.append(f"{last}, {initials}")
            elif len(parts) == 1:
                formatted.append(parts[0])
            else:
                formatted.append(author)

        if len(formatted) == 1:
            return formatted[0]
        elif len(formatted) == 2:
            return f"{formatted[0]}, & {formatted[1]}"
        else:
            return ", ".join(formatted[:-1]) + ", & " + formatted[-1]

    def _format_authors_ieee(self, authors: List[str]) -> str:
        """Format authors in IEEE style: J. Smith and J. Doe."""
        if not authors:
            return "Unknown Author"

        formatted = []
        for author in authors:
            parts = author.strip().split()
            if len(parts) >= 2:
                initials = " ".join([p[0] + "." for p in parts[:-1]])
                last = parts[-1]
                formatted.append(f"{initials} {last}")
            elif len(parts) == 1:
                formatted.append(parts[0])
            else:
                formatted.append(author)

        if len(formatted) == 1:
            return formatted[0]
        else:
            return " and ".join([", ".join(formatted[:-1]), formatted[-1]])

    def _format_authors_mla_chicago(self, authors: List[str]) -> str:
        """Format authors in MLA/Chicago style: Smith, John, and Jane Doe."""
        if not authors:
            return "Unknown Author"

        formatted = []
        for author in authors:
            parts = author.strip().split()
            if len(parts) >= 2:
                last = parts[-1]
                first = " ".join(parts[:-1])
                formatted.append(f"{last}, {first}")
            else:
                formatted.append(author)

        if len(formatted) == 1:
            return formatted[0]
        elif len(formatted) == 2:
            return f"{formatted[0]}, and {formatted[1]}"
        else:
            return ", ".join(formatted[:-1]) + ", and " + formatted[-1]

    def _format_apa(self, item: Dict, number: int = None) -> str:
        title = item.get("title", "Untitled")
        authors = self._format_authors_apa(item.get("authors", []))
        date = item.get("date", "n.d.")
        journal = item.get("journal", "")
        volume = item.get("volume", "")
        issue = item.get("issue", "")
        pages = item.get("pages", "")
        doi = item.get("doi", "")

        citation = f"{authors}. ({date}). {title}."
        if journal:
            citation += f" {journal}"
            if volume:
                citation += f", {volume}"
                if issue:
                    citation += f"({issue})"
            if pages:
                citation += f", {pages}"
            citation += "."
        if doi:
            citation += f" https://doi.org/{doi}"

        return citation

    def _format_ieee(self, item: Dict, number: int = None) -> str:
        title = item.get("title", "Untitled")
        authors = self._format_authors_ieee(item.get("authors", []))
        journal = item.get("journal", "")
        volume = item.get("volume", "")
        issue = item.get("issue", "")
        pages = item.get("pages", "")
        date = item.get("date", "")
        doi = item.get("doi", "")

        prefix = f"[{number}] " if number else ""
        citation = f'{prefix}{authors}, "{title},"'
        if journal:
            citation += f" {journal}"
            if volume:
                citation += f", vol. {volume}"
            if issue:
                citation += f", no. {issue}"
            if pages:
                citation += f", pp. {pages}"
            if date:
                citation += f", {date}"
            citation += "."
        if doi:
            citation += f" doi: {doi}."

        return citation

    def _format_mla(self, item: Dict, number: int = None) -> str:
        title = item.get("title", "Untitled")
        authors = self._format_authors_mla_chicago(item.get("authors", []))
        journal = item.get("journal", "")
        volume = item.get("volume", "")
        issue = item.get("issue", "")
        pages = item.get("pages", "")
        date = item.get("date", "")
        doi = item.get("doi", "")

        citation = f'{authors}. "{title}."'
        if journal:
            citation += f" {journal}"
            if volume:
                citation += f", vol. {volume}"
            if issue:
                citation += f", no. {issue}"
            if date:
                citation += f", {date}"
            if pages:
                citation += f", pp. {pages}"
            citation += "."
        if doi:
            citation += f" https://doi.org/{doi}"

        return citation

    def _format_chicago(self, item: Dict, number: int = None) -> str:
        title = item.get("title", "Untitled")
        authors = self._format_authors_mla_chicago(item.get("authors", []))
        journal = item.get("journal", "")
        volume = item.get("volume", "")
        issue = item.get("issue", "")
        pages = item.get("pages", "")
        date = item.get("date", "")
        doi = item.get("doi", "")

        citation = f'{authors}. "{title}."'
        if journal:
            citation += f" {journal}"
            if volume and date:
                citation += f" {volume}, no. {issue} ({date})"
            elif volume:
                citation += f" {volume}"
                if issue:
                    citation += f" ({issue})"
                if date:
                    citation += f" ({date})"
            elif date:
                citation += f" ({date})"
            if pages:
                citation += f": {pages}"
            citation += "."
        if doi:
            citation += f" https://doi.org/{doi}"

        return citation
