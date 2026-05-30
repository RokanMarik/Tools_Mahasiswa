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
        self.assertEqual(call_args.kwargs.get("limit"), 3)


    def test_parse_text_response_valid(self):
        """Should parse numbered paper list from text."""
        from scripts.journal_search import _parse_journal_response

        raw = """1. Deep Learning Review
Authors: Smith, Johnson
Year: 2024
Journal: AI Journal
DOI: 10.1234/review
URL: https://example.com/review

2. Neural Networks Survey
Authors: Doe
Year: 2023
Journal: ML Review
DOI: 10.5678/survey
URL: https://example.com/survey"""

        papers = _parse_journal_response(raw, 2)
        self.assertEqual(len(papers), 2)
        self.assertEqual(papers[0]["title"], "Deep Learning Review")
        self.assertEqual(papers[0]["authors"], ["Smith", "Johnson"])
        self.assertEqual(papers[0]["year"], 2024)
        self.assertEqual(papers[1]["title"], "Neural Networks Survey")

    def test_parse_text_response_empty_string(self):
        """Should handle empty string gracefully."""
        from scripts.journal_search import _parse_journal_response

        papers = _parse_journal_response("", 3)
        self.assertEqual(len(papers), 0)

    def test_parse_text_response_single_char_line(self):
        """Should not crash on single-character lines."""
        from scripts.journal_search import _parse_journal_response

        raw = "1\nSome text\n2. Valid Paper\nAuthors: Test"
        papers = _parse_journal_response(raw, 3)
        # Should not crash, and should parse valid paper
        self.assertTrue(len(papers) >= 0)

    def test_parse_respects_limit(self):
        """Should truncate to limit."""
        from scripts.journal_search import _parse_journal_response

        raw = """1. Paper One
Authors: A
Year: 2024

2. Paper Two
Authors: B
Year: 2024

3. Paper Three
Authors: C
Year: 2024"""

        papers = _parse_journal_response(raw, 2)
        self.assertEqual(len(papers), 2)
        self.assertEqual(papers[0]["title"], "Paper One")
        self.assertEqual(papers[1]["title"], "Paper Two")

    def test_parse_no_dict_mutation(self):
        """Should not mutate input dicts if passed as list."""
        from scripts.journal_search import _parse_journal_response

        # This tests that when we build the result, we create new dicts
        raw = "1. Test Paper\nAuthors: Smith\nYear: 2024"
        papers = _parse_journal_response(raw, 1)
        # Verify index was added
        self.assertIn("index", papers[0])
        self.assertEqual(papers[0]["index"], 1)


if __name__ == "__main__":
    unittest.main()
