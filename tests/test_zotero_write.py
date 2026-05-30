"""Tests for create_collection and add_item."""

import unittest
from unittest.mock import patch, MagicMock
from modules.zotero.client import ZoteroClient


class TestCreateCollection(unittest.TestCase):
    @patch("modules.zotero.client.requests.post")
    def test_create_collection_top_level(self, mock_post):
        """Test creating a top-level collection."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "successful": {"0": {"key": "ABC123", "version": 1}},
            "failed": {},
        }
        mock_response.headers = {}
        mock_post.return_value = mock_response

        client = ZoteroClient(api_key="test_key")
        result = client.create_collection("Test Collection")

        self.assertEqual(result["key"], "ABC123")
        self.assertEqual(result["name"], "Test Collection")

    @patch("modules.zotero.client.requests.post")
    def test_create_collection_with_parent(self, mock_post):
        """Test creating a child collection."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "successful": {"0": {"key": "XYZ789", "version": 2}},
            "failed": {},
        }
        mock_response.headers = {}
        mock_post.return_value = mock_response

        client = ZoteroClient(api_key="test_key")
        result = client.create_collection("Sub Collection", parent_key="PARENT1")

        self.assertEqual(result["key"], "XYZ789")
        # Verify parent was sent in payload
        call_args = mock_post.call_args
        payload = call_args[1]["json"]
        self.assertEqual(payload[0]["parentCollection"], "PARENT1")


class TestAddItem(unittest.TestCase):
    @patch("modules.zotero.client.requests.post")
    def test_add_item_to_collection(self, mock_post):
        """Test adding an item to a collection."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "successful": {"0": {"key": "ITEM123", "version": 5}},
            "failed": {},
        }
        mock_post.return_value = mock_response

        client = ZoteroClient(api_key="test_key")
        item_data = {
            "title": "Test Paper",
            "authors": ["John Smith", "Jane Doe"],
            "date": "2024",
            "doi": "10.1234/test",
            "url": "https://example.com",
            "journal": "Test Journal",
        }

        result = client.add_item("COLL1", item_data)

        self.assertEqual(result["key"], "ITEM123")

        # Verify payload structure
        call_args = mock_post.call_args
        payload = call_args[1]["json"]
        self.assertEqual(payload[0]["title"], "Test Paper")
        self.assertEqual(payload[0]["collections"], ["COLL1"])
        self.assertEqual(len(payload[0]["creators"]), 2)

    @patch("modules.zotero.client.requests.post")
    def test_add_item_single_author(self, mock_post):
        """Test adding item with single author."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "successful": {"0": {"key": "ITEM456", "version": 1}},
            "failed": {},
        }
        mock_post.return_value = mock_response

        client = ZoteroClient(api_key="test_key")
        item_data = {
            "title": "Solo Paper",
            "authors": ["Alice Johnson"],
            "date": "2023",
        }

        result = client.add_item("COLL2", item_data)

        self.assertEqual(result["key"], "ITEM456")
        call_args = mock_post.call_args
        payload = call_args[1]["json"]
        self.assertEqual(payload[0]["creators"][0]["lastName"], "Johnson")
        self.assertEqual(payload[0]["creators"][0]["firstName"], "Alice")


if __name__ == "__main__":
    unittest.main()
