"""Tests for scripts/journal_search.py"""

import json
import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestJournalSearch(unittest.TestCase):
    """Test journal_search script with aggregator."""

    @patch("modules.search.aggregator.search")
    def test_search_returns_json_with_papers(self, mock_search):
        """Search should return JSON with paper list."""
        from modules.search.paper_model import Paper
        mock_search.return_value = [
            Paper(title="Test Paper 1", authors=["Smith, J."], year=2024, journal="Test Journal", doi="10.1234/test1", url="https://example.com/paper1", source="garuda", abstract="Test abstract")
        ]

        from scripts.journal_search import search_journals

        result = search_journals("machine learning", limit=1)
        data = json.loads(result)
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["papers"]), 1)
        self.assertEqual(data["papers"][0]["title"], "Test Paper 1")

    @patch("modules.search.aggregator.search")
    def test_search_handles_error(self, mock_search):
        """Search should return JSON error on failure."""
        mock_search.side_effect = RuntimeError("No results from any source")

        from scripts.journal_search import search_journals

        result = search_journals("topic", limit=1)
        data = json.loads(result)
        self.assertEqual(data["status"], "error")
        self.assertIsNotNone(data["error"])

    @patch("modules.search.aggregator.search")
    def test_search_default_limit_is_3(self, mock_search):
        """Default limit should be 3 papers."""
        from modules.search.paper_model import Paper
        mock_search.return_value = []

        from scripts.journal_search import search_journals

        search_journals("topic")
        call_args = mock_search.call_args
        self.assertEqual(call_args.kwargs.get("total_limit"), 3)

    def test_paper_to_dict(self):
        """_paper_to_dict should produce correct dict."""
        from modules.search.paper_model import Paper
        from scripts.journal_search import _paper_to_dict

        paper = Paper(title="Test", authors=["A"], year=2024, journal="J", doi="10.1/x", url="http://x.com", source="crossref", abstract="abs")
        result = _paper_to_dict(paper, 1)
        self.assertEqual(result["index"], 1)
        self.assertEqual(result["title"], "Test")
        self.assertEqual(result["metadata_source"], "crossref")


if __name__ == "__main__":
    unittest.main()
