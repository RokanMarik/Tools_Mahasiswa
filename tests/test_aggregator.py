"""Tests for modules/search/aggregator.py"""

import unittest
from unittest.mock import patch, MagicMock
from modules.search.paper_model import Paper


class TestAggregator(unittest.TestCase):

    @patch("modules.search.aggregator.openalex.search")
    @patch("modules.search.aggregator.garuda.search")
    def test_search_merges_sources(self, mock_garuda, mock_openalex):
        mock_garuda.return_value = [
            Paper(title="Garuda Paper", authors=["A"], year=2024, journal="J", doi="", url="", source="garuda")
        ]
        mock_openalex.return_value = [
            Paper(title="OpenAlex Paper", authors=["B"], year=2023, journal="J", doi="10.1/x", url="", source="openalex")
        ]

        from modules.search.aggregator import search

        papers = search("test", total_limit=10)
        self.assertEqual(len(papers), 2)
        sources = {p.source for p in papers}
        self.assertIn("garuda", sources)
        self.assertIn("openalex", sources)

    @patch("modules.search.aggregator.openalex.search")
    @patch("modules.search.aggregator.garuda.search")
    def test_search_deduplicates_by_doi(self, mock_garuda, mock_openalex):
        mock_garuda.return_value = [
            Paper(title="Same Paper", authors=["A"], year=2024, journal="J", doi="10.1/dup", url="url1", source="garuda")
        ]
        mock_openalex.return_value = [
            Paper(title="Same Paper", authors=["B"], year=2024, journal="J", doi="10.1/dup", url="url2", source="openalex")
        ]

        from modules.search.aggregator import search

        papers = search("test", total_limit=10)
        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0].source, "garuda")

    @patch("modules.search.aggregator.openalex.search")
    @patch("modules.search.aggregator.garuda.search")
    def test_search_handles_source_failure(self, mock_garuda, mock_openalex):
        mock_garuda.side_effect = RuntimeError("Garuda down")
        mock_openalex.return_value = [
            Paper(title="OpenAlex Paper", authors=["A"], year=2024, journal="J", doi="10.1/x", url="", source="openalex")
        ]

        from modules.search.aggregator import search

        papers = search("test", total_limit=10)
        self.assertEqual(len(papers), 1)

    @patch("modules.search.aggregator.openalex.search")
    @patch("modules.search.aggregator.garuda.search")
    def test_search_raises_when_all_fail(self, mock_garuda, mock_openalex):
        mock_garuda.side_effect = RuntimeError("Down")
        mock_openalex.side_effect = RuntimeError("Down")

        from modules.search.aggregator import search

        with self.assertRaises(RuntimeError):
            search("test")

    @patch("modules.search.aggregator.openalex.search")
    @patch("modules.search.aggregator.garuda.search")
    def test_search_respects_total_limit(self, mock_garuda, mock_openalex):
        mock_garuda.return_value = [
            Paper(title=f"Garuda {i}", authors=["A"], year=2024, journal="J", doi=f"10.1/g{i}", url="", source="garuda")
            for i in range(5)
        ]
        mock_openalex.return_value = []

        from modules.search.aggregator import search

        papers = search("test", total_limit=3)
        self.assertEqual(len(papers), 3)


if __name__ == "__main__":
    unittest.main()
