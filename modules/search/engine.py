"""Main search engine orchestrator."""

from typing import List, Dict, Optional
from .semantic_scholar import SemanticScholarClient
from .crossref import CrossrefClient
from .garuda import GarudaClient

SOURCE_SEMANTIC = "semantic-scholar"
SOURCE_CROSSREF = "crossref"
SOURCE_GARUDA = "garuda"
SOURCE_ALL = "all"
VALID_SOURCES = [SOURCE_SEMANTIC, SOURCE_CROSSREF, SOURCE_GARUDA, SOURCE_ALL]

SORT_CITATIONS = "citations"
SORT_YEAR = "year"
SORT_RELEVANCE = "relevance"
VALID_SORTS = [SORT_CITATIONS, SORT_YEAR, SORT_RELEVANCE]


class SearchEngine:
    """Multi-source journal search engine."""

    def __init__(self):
        self.semantic = SemanticScholarClient()
        self.crossref = CrossrefClient()
        self.garuda = GarudaClient()

    def search(self, query, sources=None, sort=SORT_RELEVANCE, limit=6, year_from=None, year_to=None):
        if sources is None: sources = [SOURCE_ALL]
        if SOURCE_ALL in sources: sources = [SOURCE_SEMANTIC, SOURCE_CROSSREF, SOURCE_GARUDA]
        sources = [s for s in sources if s in VALID_SOURCES]

        all_papers = []
        for source in sources:
            try:
                papers = self._search_source(source, query, limit, year_from, year_to)
                all_papers.extend(papers)
            except Exception:
                continue

        papers = self._deduplicate(all_papers)
        papers = self._sort(papers, sort)
        return papers[:limit]

    def _search_source(self, source, query, limit, year_from, year_to):
        if source == SOURCE_SEMANTIC:
            return self.semantic.search(query, limit=limit, year_from=year_from, year_to=year_to)
        elif source == SOURCE_CROSSREF:
            return self.crossref.search(query, limit=limit, year_from=year_from, year_to=year_to)
        elif source == SOURCE_GARUDA:
            return self.garuda.search(query, limit=limit, year_from=year_from, year_to=year_to)
        return []

    def _deduplicate(self, papers):
        import re
        seen_dois = set()
        seen_titles = set()
        unique = []
        for paper in papers:
            doi = paper.get("doi", "").lower().strip()
            title = paper.get("title", "").lower().strip()
            title_key = re.sub(r"[^\w\s]", "", title).strip()
            if doi and doi in seen_dois: continue
            if title_key in seen_titles: continue
            if doi: seen_dois.add(doi)
            if title_key: seen_titles.add(title_key)
            unique.append(paper)
        return unique

    def _sort(self, papers, sort):
        if sort == SORT_CITATIONS:
            return sorted(papers, key=lambda p: p.get("citations", 0), reverse=True)
        elif sort == SORT_YEAR:
            return sorted(papers, key=lambda p: p.get("year", 0), reverse=True)
        return papers

    def get_balanced_results(self, query, limit=6, year_from=None, year_to=None):
        all_papers = self.search(query, sources=[SOURCE_ALL], sort=SORT_CITATIONS, limit=limit*3, year_from=year_from, year_to=year_to)
        if not all_papers: return {"foundational": [], "recent": []}
        half = limit // 2
        by_cit = sorted(all_papers, key=lambda p: p.get("citations", 0), reverse=True)
        foundational = by_cit[:half]
        by_year = sorted(all_papers, key=lambda p: p.get("year", 0), reverse=True)
        recent = []
        seen = {p.get("doi") or p.get("title") for p in foundational}
        for p in by_year:
            key = p.get("doi") or p.get("title")
            if key not in seen and len(recent) < half:
                recent.append(p)
                seen.add(key)
        return {"foundational": foundational, "recent": recent}
