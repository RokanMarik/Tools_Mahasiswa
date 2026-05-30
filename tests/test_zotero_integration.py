"""Integration tests for the full Zotero pipeline."""

import unittest
import importlib
from modules.zotero.citation_formatter import CitationFormatter


class TestZoteroIntegration(unittest.TestCase):
    def setUp(self):
        self.finder = importlib.import_module("9router_journal_finder").JournalFinder()

    def test_check_duplicates_returns_list(self):
        """Test that check_duplicates returns a list."""
        items = [
            {"key": "1", "title": "Paper A", "doi": "10.1/a", "authors": [], "journal": "", "date": "", "item_type": ""},
            {"key": "2", "title": "Paper B", "doi": "10.2/b", "authors": [], "journal": "", "date": "", "item_type": ""},
        ]
        result = self.finder.check_duplicates(items)
        self.assertIsInstance(result, list)

    def test_analyze_gaps_returns_list(self):
        """Test that analyze_gaps returns a list."""
        items = [
            {"title": "Machine Learning in Medicine", "journal": "", "authors": [], "doi": "", "key": "", "date": "", "item_type": ""},
        ]
        result = self.finder.analyze_gaps(items)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    def test_recommend_related_returns_list(self):
        """Test that recommend_related returns a list even without API."""
        gaps = [{"topic": "NLP", "status": "missing", "count": 0}]
        result = self.finder.recommend_related(gaps, [])
        self.assertIsInstance(result, list)


class TestEndToEnd(unittest.TestCase):
    """End-to-end tests for the full pipeline."""

    def test_full_pipeline_with_mock_data(self):
        """Test the full analysis pipeline with mock data."""
        finder = importlib.import_module("9router_journal_finder").JournalFinder()

        items = [
            {"title": "Deep Learning for Medical Imaging", "journal": "Medical AI", "authors": ["John Smith"], "doi": "10.1/ml", "key": "1", "date": "2024", "item_type": "journalArticle"},
            {"title": "Neural Networks for Diagnosis", "journal": "AI Medicine", "authors": ["Jane Doe"], "doi": "10.2/nn", "key": "2", "date": "2023", "item_type": "journalArticle"},
            {"title": "NLP for Clinical Notes", "journal": "NLP Journal", "authors": ["Bob Lee"], "doi": "10.3/nlp", "key": "3", "date": "2024", "item_type": "journalArticle"},
        ]

        # Check no crashes on each step
        dups = finder.check_duplicates(items)
        self.assertIsInstance(dups, list)

        gaps = finder.analyze_gaps(items)
        self.assertIsInstance(gaps, list)

        # Recommendations may be empty without API, but should not crash
        recs = finder.recommend_related(gaps, ["Medical AI"])
        self.assertIsInstance(recs, list)

    def test_citation_formatting_in_pipeline(self):
        """Test that citation formatting works with pipeline data."""
        formatter = CitationFormatter()
        item = {
            "title": "Test Paper",
            "authors": ["John Smith"],
            "date": "2024",
            "doi": "10.1/test",
            "journal": "Test Journal",
            "volume": "1",
            "issue": "1",
            "pages": "1-10",
        }

        for style in CitationFormatter.STYLES:
            result = formatter.format(item, style=style)
            self.assertIsInstance(result, str)
            self.assertTrue(len(result) > 0)


if __name__ == "__main__":
    unittest.main()
