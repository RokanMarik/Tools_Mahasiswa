"""Tests for modules/search/aggregator.py"""

import unittest
from unittest.mock import patch, MagicMock
from modules.search.paper_model import Paper


class TestAggregator(unittest.TestCase):

    @patch("modules.search.aggregator.semantic_scholar.search")
    @patch("modules.search.aggregator.crossref.search")
    @patch("modules.search.aggregator.garuda.search")
    def test_search_merges_sources(self, mock_garuda, mock_crossref, mock_ss):
        mock_garuda.return_value = [
            Paper(title="Garuda Paper", authors=["A"], year=2024, journal="J", doi="", url="", source="garuda")
        ]
        mock_crossref.return_value = [
            Paper(title="CrossRef Paper", authors=["B"], year=2023, journal="J", doi="10.1/x", url="", source="crossref")
        ]
        mock_ss.return_value = [
            Paper(title="SS Paper", authors=["C"], year=2022, journal="J", doi="10.2/y", url="", source="semantic_scholar")
        ]

        from modules.search.aggregator import search

        papers = search("test", total_limit=10)
        self.assertEqual(len(papers), 3)
        sources = {p.source for p in papers}
        self.assertIn("garuda", sources)
        self.assertIn("crossref", sources)
        self.assertIn("semantic_scholar", sources)

    @patch("modules.search.aggregator.semantic_scholar.search")
    @patch("modules.search.aggregator.crossref.search")
    @patch("modules.search.aggregator.garuda.search")
    def test_search_deduplicates_by_doi(self, mock_garuda, mock_crossref, mock_ss):
        mock_garuda.return_value = [
            Paper(title="Same Paper", authors=["A"], year=2024, journal="J", doi="10.1/dup", url="url1", source="garuda")
        ]
        mock_crossref.return_value = [
            Paper(title="Same Paper", authors=["B"], year=2024, journal="J", doi="10.1/dup", url="url2", source="crossref")
        ]
        mock_ss.return_value = []

        from modules.search.aggregator import search

        papers = search("test", total_limit=10)
        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0].source, "garuda")

    @patch("modules.search.aggregator.semantic_scholar.search")
    @patch("modules.search.aggregator.crossref.search")
    @patch("modules.search.aggregator.garuda.search")
    def test_search_handles_source_failure(self, mock_garuda, mock_crossref, mock_ss):
        mock_garuda.side_effect = RuntimeError("Garuda down")
        mock_crossref.return_value = [
            Paper(title="CrossRef Paper", authors=["A"], year=2024, journal="J", doi="10.1/x", url="", source="crossref")
        ]
        mock_ss.return_value = [
            Paper(title="SS Paper", authors=["B"], year=2023, journal="J", doi="10.2/y", url="", source="semantic_scholar")
        ]

        from modules.search.aggregator import search

        papers = search("test", total_limit=10)
        self.assertEqual(len(papers), 2)

    @patch("modules.search.aggregator.semantic_scholar.search")
    @patch("modules.search.aggregator.crossref.search")
    @patch("modules.search.aggregator.garuda.search")
    def test_search_raises_when_all_fail(self, mock_garuda, mock_crossref, mock_ss):
        mock_garuda.side_effect = RuntimeError("Down")
        mock_crossref.side_effect = RuntimeError("Down")
        mock_ss.side_effect = RuntimeError("Down")

        from modules.search.aggregator import search

        with self.assertRaises(RuntimeError):
            search("test")

    @patch("modules.search.aggregator.semantic_scholar.search")
    @patch("modules.search.aggregator.crossref.search")
    @patch("modules.search.aggregator.garuda.search")
    def test_search_respects_total_limit(self, mock_garuda, mock_crossref, mock_ss):
        mock_garuda.return_value = [
            Paper(title=f"Garuda {i}", authors=["A"], year=2024, journal="J", doi=f"10.1/g{i}", url="", source="garuda")
            for i in range(5)
        ]
        mock_crossref.return_value = []
        mock_ss.return_value = []

        from modules.search.aggregator import search

        papers = search("test", total_limit=3)
        self.assertEqual(len(papers), 3)


if __name__ == "__main__":
    unittest.main()
