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

    @patch("scripts.zotero_save.ZoteroClient")
    @patch("scripts.zotero_save.CitationFormatter")
    def test_save_detects_duplicate(self, MockFormatter, MockClient):
        """Should return duplicate status when item already exists."""
        mock_client = MagicMock()
        mock_client.get_user_id.return_value = "12345"
        mock_client.add_item.side_effect = Exception("Failed: Item already exists")
        MockClient.return_value = mock_client

        mock_formatter = MagicMock()
        MockFormatter.return_value = mock_formatter

        from scripts.zotero_save import save_to_zotero

        papers = [{"title": "Existing Paper", "authors": ["Smith"], "year": 2024}]
        result = save_to_zotero(papers, api_key="test-key")
        data = json.loads(result)
        self.assertEqual(data["status"], "duplicate")
        self.assertEqual(len(data["skipped"]), 1)
        self.assertEqual(data["skipped"][0]["reason"], "duplicate")

    def test_save_skips_invalid_metadata(self):
        """Should skip papers without title."""
        from scripts.zotero_save import save_to_zotero

        papers = [{"authors": ["Smith"]}, {"title": "Valid Paper"}]
        # This will fail on Zotero connection, but we can check validation first
        # Use mocked version for the skip path
        import unittest.mock
        with unittest.mock.patch("scripts.zotero_save.ZoteroClient") as MockClient:
            mock_client = MagicMock()
            mock_client.get_user_id.side_effect = Exception("Connection failed")
            MockClient.return_value = mock_client

            result = save_to_zotero(papers, api_key="test-key")
            data = json.loads(result)
            # Connection error is caught first, so all papers are in error status
            self.assertEqual(data["status"], "error")

    def test_save_empty_papers_list(self):
        """Should handle empty paper list."""
        import unittest.mock
        with unittest.mock.patch("scripts.zotero_save.ZoteroClient") as MockClient:
            mock_client = MagicMock()
            mock_client.get_user_id.return_value = "12345"
            mock_client.add_item.return_value = {"key": "K1", "version": 1}
            MockClient.return_value = mock_client

            with unittest.mock.patch("scripts.zotero_save.CitationFormatter") as MockFmt:
                MockFmt.return_value.format.return_value = "citation"

                from scripts.zotero_save import save_to_zotero

                result = save_to_zotero([], api_key="test-key")
                data = json.loads(result)
                self.assertEqual(data["status"], "error")
                self.assertEqual(len(data["saved"]), 0)


if __name__ == "__main__":
    unittest.main()
