"""Semantic Scholar API client for journal search.

Free API - no key required.
Provides: citation count, year, authors, DOI, abstract, venue.
"""

import requests
from typing import List, Dict, Optional

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1"
DEFAULT_FIELDS = "title,year,authors,citationCount,externalIds,abstract,venue,journal,publicationTypes,publicationDate"
DEFAULT_LIMIT = 10


class SemanticScholarClient:
    """Client for Semantic Scholar Academic Graph API."""

    def __init__(self):
        self.base_url = SEMANTIC_SCHOLAR_API
        self.headers = {"Accept": "application/json"}

    def search(self, query: str, limit: int = DEFAULT_LIMIT, year_from: Optional[int] = None, year_to: Optional[int] = None) -> List[Dict]:
        """Search for academic papers."""
        papers = []
        offset = 0

        while len(papers) < limit:
            params = {"query": query, "limit": min(limit - len(papers), 100), "offset": offset, "fields": DEFAULT_FIELDS}

            if year_from or year_to:
                year_filter = f"{year_from or 2000}-{year_to or 2099}"
                params["year"] = year_filter

            try:
                response = requests.get(f"{self.base_url}/paper/search", headers=self.headers, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
            except requests.exceptions.RequestException as e:
                raise Exception(f"Semantic Scholar API error: {e}")

            results = data.get("data", [])
            if not results:
                break

            for paper in results:
                parsed = self._parse_paper(paper)
                if parsed:
                    papers.append(parsed)

            total = data.get("total", 0)
            offset += len(results)
            if offset >= total or offset >= limit:
                break

        return papers[:limit]

    def _parse_paper(self, data: Dict) -> Optional[Dict]:
        """Parse Semantic Scholar API response."""
        title = data.get("title")
        if not title:
            return None

        authors = [a.get("name", "") for a in (data.get("authors", []) or []) if a.get("name")]

        external_ids = data.get("externalIds", {}) or {}
        doi = external_ids.get("DOI", "")
        url = f"https://doi.org/{doi}" if doi else ""

        journal = data.get("venue", "")
        if not journal:
            journal_data = data.get("journal", {}) or {}
            journal = journal_data.get("name", "")

        year = data.get("year")
        if not year:
            pub_date = data.get("publicationDate", "")
            if pub_date:
                year = int(pub_date[:4])

        return {
            "title": title, "authors": authors, "year": year or 0,
            "citations": data.get("citationCount", 0), "doi": doi, "url": url,
            "journal": journal, "abstract": data.get("abstract", ""),
            "source": "semantic-scholar", "publication_types": data.get("publicationTypes", []),
        }
