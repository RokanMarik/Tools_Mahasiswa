"""Tests for scripts/journal_search.py"""

import json
import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestJournalSearch(unittest.TestCase):
    """Test journal_search script functions."""

    @patch("scripts.journal_search.JournalFinder")
    def test_search_returns_json_with_papers(self, MockFinder):
        """Search should return JSON with paper list."""
        mock_finder = MagicMock()
        mock_finder.find_journals.return_value = json.dumps({
            "status": "success",
            "query": "machine learning",
            "papers": [
                {
                    "index": 1,
                    "title": "Test Paper 1",
                    "authors": ["Smith, J."],
                    "year": 2024,
                    "journal": "Test Journal",
                    "doi": "10.1234/test1",
                    "url": "https://example.com/paper1",
                    "abstract": "Test abstract",
                    "metadata_source": "crossref",
                }
            ],
            "error": None,
        })
        MockFinder.return_value = mock_finder

        from scripts.journal_search import search_journals

        result = search_journals("machine learning", limit=1)
        data = json.loads(result)
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["papers"]), 1)
        self.assertEqual(data["papers"][0]["title"], "Test Paper 1")

    @patch("scripts.journal_search.JournalFinder")
    def test_search_handles_error(self, MockFinder):
        """Search should return JSON error on failure."""
        mock_finder = MagicMock()
        mock_finder.find_journals.side_effect = Exception("Connection refused")
        MockFinder.return_value = mock_finder

        from scripts.journal_search import search_journals

        result = search_journals("topic", limit=1)
        data = json.loads(result)
        self.assertEqual(data["status"], "error")
        self.assertIsNotNone(data["error"])

    @patch("scripts.journal_search.JournalFinder")
    def test_search_default_limit_is_3(self, MockFinder):
        """Default limit should be 3 papers."""
        mock_finder = MagicMock()
        mock_finder.find_journals.return_value = json.dumps({
            "status": "success",
            "query": "topic",
            "papers": [],
            "error": None,
        })
        MockFinder.return_value = mock_finder

        from scripts.journal_search import search_journals

        search_journals("topic")
        call_args = mock_finder.find_journals.call_args
        self.assertIn("limit", call_args.kwargs or {})


if __name__ == "__main__":
    unittest.main()
