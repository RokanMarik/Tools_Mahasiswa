"""Crossref API client for journal search."""

import requests
from typing import List, Dict, Optional

CROSSREF_API = "https://api.crossref.org"
USER_AGENT = "ToolsMahasiswa/1.0"


class CrossrefClient:
    """Client for Crossref REST API."""

    def __init__(self):
        self.base_url = CROSSREF_API
        self.headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}

    def search(self, query, limit=20, year_from=None, year_to=None):
        """Search for academic works."""
        papers = []
        offset = 0

        while len(papers) < limit:
            params = {"query": query, "rows": min(limit - len(papers), 100), "offset": offset, "sort": "relevance"}

            if year_from or year_to:
                params["filter"] = f"from-pub-date:{year_from or 2000},until-pub-date:{year_to or 2099}"

            try:
                response = requests.get(f"{self.base_url}/works", headers=self.headers, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
            except requests.exceptions.RequestException as e:
                raise Exception(f"Crossref API error: {e}")

            msg = data.get("message", {})
            items = msg.get("items", [])  # FIXED: items not item
            if not items:
                break

            for item in items:
                parsed = self._parse_work(item)
                if parsed:
                    papers.append(parsed)

            total = msg.get("total-results", 0)
            offset += len(items)
            if offset >= total or offset >= limit:
                break

        return papers[:limit]

    def _parse_work(self, data):
        """Parse Crossref API response."""
        title_list = data.get("title", [])
        title = title_list[0] if title_list else None
        if not title:
            return None

        authors = []
        for author in (data.get("author", []) or []):
            parts = []
            if author.get("given"): parts.append(author["given"])
            if author.get("family"): parts.append(author["family"])
            if parts: authors.append(" ".join(parts))

        year = 0
        for field in ["published-print", "published-online", "created"]:
            d = data.get(field, {})
            if d and d.get("date-parts"):
                p = d["date-parts"][0]
                if p and p[0]: year = p[0]; break

        journal_list = data.get("container-title", [])
        journal = journal_list[0] if journal_list else ""
        doi = data.get("DOI", "")

        return {
            "title": title, "authors": authors, "year": year,
            "citations": data.get("is-referenced-by-count", 0) or 0,
            "doi": doi, "url": f"https://doi.org/{doi}" if doi else "",
            "journal": journal, "abstract": data.get("abstract", ""),
            "source": "crossref", "type": data.get("type", ""),
        }
