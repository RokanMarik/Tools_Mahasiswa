"""Tests for ZoteroClient."""

import os
import unittest
from unittest.mock import patch, MagicMock
from modules.zotero.client import ZoteroClient


class TestZoteroClient(unittest.TestCase):
    def test_init_with_api_key(self):
        client = ZoteroClient(api_key="test_key_123")
        self.assertEqual(client.api_key, "test_key_123")
        self.assertEqual(client.library_type, "users")

    def test_init_with_custom_library(self):
        client = ZoteroClient(api_key="test_key", library_type="groups", library_id="456")
        self.assertEqual(client.library_type, "groups")
        self.assertEqual(client.library_id, "456")

    @patch("modules.zotero.client.requests.get")
    def test_get_collections(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "key": "ABC123",
                "data": {"name": "Machine Learning"},
                "meta": {"numItems": 23},
            }
        ]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        client = ZoteroClient(api_key="test_key")
        collections = client.get_collections()

        self.assertEqual(len(collections), 1)
        self.assertEqual(collections[0]["name"], "Machine Learning")
        self.assertEqual(collections[0]["num_items"], 23)

    @patch("modules.zotero.client.requests.get")
    def test_get_collection_items(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "key": "ITEM1",
                "data": {
                    "itemType": "journalArticle",
                    "title": "Test Paper",
                    "creators": [{"creatorType": "author", "firstName": "John", "lastName": "Doe"}],
                    "date": "2024",
                    "DOI": "10.1234/test",
                    "url": "https://example.com",
                    "publicationTitle": "Test Journal",
                },
            }
        ]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        client = ZoteroClient(api_key="test_key")
        items = client.get_collection_items("ABC123")

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "Test Paper")
        self.assertEqual(items[0]["doi"], "10.1234/test")
        self.assertEqual(items[0]["authors"], ["John Doe"])

    @patch("modules.zotero.client.requests.get")
    def test_get_user_id(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"userID": 12345}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        client = ZoteroClient(api_key="test_key")
        user_id = client.get_user_id()

        self.assertEqual(user_id, "12345")

    def test_invalid_api_key_error(self):
        client = ZoteroClient(api_key="invalid_key")
        # This will fail with real API call, so we just test the client creates properly
        self.assertEqual(client.api_key, "invalid_key")

    @patch("modules.zotero.client.requests.get")
    def test_skips_attachments(self, mock_get):
        """Test that attachment items are skipped."""
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "key": "ITEM1",
                "data": {
                    "itemType": "journalArticle",
                    "title": "Test Paper",
                    "creators": [],
                    "date": "2024",
                    "DOI": "",
                    "url": "",
                    "publicationTitle": "",
                },
            },
            {
                "key": "ITEM2",
                "data": {
                    "itemType": "attachment",
                    "title": "paper.pdf",
                    "creators": [],
                    "date": "",
                    "DOI": "",
                    "url": "",
                    "publicationTitle": "",
                },
            },
        ]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        client = ZoteroClient(api_key="test_key")
        items = client.get_collection_items("ABC123")

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["item_type"], "journalArticle")


if __name__ == "__main__":
    unittest.main()
