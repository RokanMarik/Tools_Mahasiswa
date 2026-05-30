"""Integration tests for the journal workflow scripts."""

import json
import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(__file__))


class TestIntegration(unittest.TestCase):
    """Test full workflow: search → save → citation."""

    @patch("scripts.journal_search.JournalFinder")
    @patch("scripts.zotero_save.ZoteroClient")
    @patch("scripts.zotero_save.CitationFormatter")
    def test_full_workflow_search_then_save(self, MockFormatter, MockClient, MockFinder):
        """Full workflow: search papers, then save selected ones."""
        mock_finder = MagicMock()
        mock_finder.find_journals.return_value = json.dumps({
            "status": "success",
            "query": "test topic",
            "papers": [
                {"index": 1, "title": "Paper A", "authors": ["Smith"], "year": 2024, "journal": "J1", "doi": "10.1/a", "url": "https://a.com", "abstract": "", "metadata_source": "crossref"},
                {"index": 2, "title": "Paper B", "authors": ["Doe"], "year": 2023, "journal": "J2", "doi": "10.2/b", "url": "https://b.com", "abstract": "", "metadata_source": "crossref"},
            ],
            "error": None,
        })
        MockFinder.return_value = mock_finder

        mock_client = MagicMock()
        mock_client.get_user_id.return_value = "12345"
        mock_client.add_item.return_value = {"key": "KEY1", "version": 1}
        MockClient.return_value = mock_client

        mock_formatter = MagicMock()
        mock_formatter.format.return_value = "Smith. (2024). Paper A. J1. https://doi.org/10.1/a"
        MockFormatter.return_value = mock_formatter

        from scripts.journal_search import search_journals
        search_result = json.loads(search_journals("test topic"))
        self.assertEqual(search_result["status"], "success")
        self.assertEqual(len(search_result["papers"]), 2)

        selected = [search_result["papers"][0]]

        from scripts.zotero_save import save_to_zotero
        save_result = json.loads(save_to_zotero(selected, api_key="test-key"))
        self.assertEqual(save_result["status"], "success")
        self.assertEqual(len(save_result["saved"]), 1)
        self.assertEqual(save_result["saved"][0]["title"], "Paper A")

    def test_citation_from_search_result(self):
        """Citation should work with data from search results."""
        from scripts.citation_generator import generate_citations

        paper = {
            "title": "Test Paper",
            "authors": ["Jane Doe", "John Smith"],
            "year": 2024,
            "journal": "Test Journal",
            "doi": "10.9999/test",
        }

        result = json.loads(generate_citations([paper], style="apa"))
        self.assertEqual(result["status"], "success")
        citation = result["citations"][0]["apa"]
        self.assertIn("Doe", citation)
        self.assertIn("2024", citation)
        self.assertIn("Test Paper", citation)


if __name__ == "__main__":
    unittest.main()
