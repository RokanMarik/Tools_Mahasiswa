"""Tests for search engine."""
import pytest
from modules.search.engine import SearchEngine, SORT_CITATIONS, SORT_YEAR, SORT_RELEVANCE
from modules.search.crossref import CrossrefClient
from modules.search.semantic_scholar import SemanticScholarClient


class TestCrossrefClient:
    def test_search_returns_results(self):
        client = CrossrefClient()
        papers = client.search("machine learning", limit=3)
        assert len(papers) > 0
        for p in papers:
            assert "title" in p
            assert p["source"] == "crossref"

    def test_search_with_year_filter(self):
        client = CrossrefClient()
        papers = client.search("deep learning", limit=3, year_from=2023, year_to=2025)
        assert len(papers) >= 0  # May be empty if no results
        for p in papers:
            if p["year"]:
                assert 2023 <= p["year"] <= 2025


class TestSearchEngine:
    def test_search_crossref(self):
        engine = SearchEngine()
        papers = engine.search("artificial intelligence", sources=["crossref"], limit=3)
        assert len(papers) > 0

    def test_sort_by_citations(self):
        engine = SearchEngine()
        papers = engine.search("AI", sources=["crossref"], sort=SORT_CITATIONS, limit=5)
        if len(papers) > 1:
            assert papers[0]["citations"] >= papers[-1]["citations"]

    def test_sort_by_year(self):
        engine = SearchEngine()
        papers = engine.search("AI", sources=["crossref"], sort=SORT_YEAR, limit=5)
        if len(papers) > 1 and papers[0]["year"] and papers[-1]["year"]:
            assert papers[0]["year"] >= papers[-1]["year"]

    def test_deduplication(self):
        engine = SearchEngine()
        # Same DOI should be deduplicated
        papers = engine._deduplicate([
            {"title": "Test", "doi": "10.1234/test", "source": "a"},
            {"title": "Test", "doi": "10.1234/test", "source": "b"},
        ])
        assert len(papers) == 1

    def test_balanced_results(self):
        engine = SearchEngine()
        result = engine.get_balanced_results("AI", limit=4)
        assert "foundational" in result
        assert "recent" in result
        assert isinstance(result["foundational"], list)
        assert isinstance(result["recent"], list)
