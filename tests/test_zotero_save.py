"""Tests for scripts/zotero_save.py"""

import json
import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestZoteroSave(unittest.TestCase):
    """Test zotero_save script functions."""

    @patch("scripts.zotero_save.ZoteroClient")
    @patch("scripts.zotero_save.CitationFormatter")
    def test_save_returns_json_on_success(self, MockFormatter, MockClient):
        """Save should return JSON with saved papers and citations."""
        mock_client = MagicMock()
        mock_client.get_user_id.return_value = "12345"
        mock_client.add_item.return_value = {"key": "ABC123", "version": 1}
        MockClient.return_value = mock_client

        mock_formatter = MagicMock()
        mock_formatter.format.return_value = "Smith, J. (2024). Test Paper. Test Journal. https://doi.org/10.1234"
        MockFormatter.return_value = mock_formatter

        from scripts.zotero_save import save_to_zotero

        papers = [
            {
                "title": "Test Paper",
                "authors": ["John Smith"],
                "year": 2024,
                "journal": "Test Journal",
                "doi": "10.1234/test",
                "url": "https://example.com",
            }
        ]

        result = save_to_zotero(papers, api_key="test-key", collection_key="COL1")
        data = json.loads(result)
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["saved"]), 1)
        self.assertEqual(data["saved"][0]["title"], "Test Paper")

    @patch("scripts.zotero_save.ZoteroClient")
    def test_save_handles_connection_error(self, MockClient):
        """Save should return JSON error on connection failure."""
        mock_client = MagicMock()
        mock_client.get_user_id.side_effect = Exception("Connection refused")
        MockClient.return_value = mock_client

        from scripts.zotero_save import save_to_zotero

        papers = [{"title": "Test"}]
        result = save_to_zotero(papers, api_key="test-key")
        data = json.loads(result)
        self.assertEqual(data["status"], "error")
        self.assertIsNotNone(data["error"])

    def test_validate_paper_metadata_requires_title(self):
        """Validation should fail if title is missing."""
        from scripts.zotero_save import validate_paper_metadata

        result = validate_paper_metadata({"authors": ["Smith"]})
        self.assertFalse(result["valid"])
        self.assertIn("title", result["errors"])

    def test_validate_paper_metadata_passes_with_title(self):
        """Validation should pass with at least a title."""
        from scripts.zotero_save import validate_paper_metadata

        result = validate_paper_metadata({"title": "Test Paper"})
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])


if __name__ == "__main__":
    unittest.main()
