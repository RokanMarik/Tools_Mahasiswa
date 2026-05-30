"""Tests for CollectionPicker."""

import unittest
from unittest.mock import MagicMock, patch
from modules.zotero.collection_picker import CollectionPicker


class TestCollectionPicker(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_client.get_collections.return_value = [
            {"key": "KEY1", "name": "Machine Learning", "num_items": 23},
            {"key": "KEY2", "name": "Medical AI", "num_items": 15},
            {"key": "KEY3", "name": "NLP", "num_items": 9},
        ]
        self.picker = CollectionPicker(self.mock_client)

    def test_display_collections(self):
        """Test that collections are formatted correctly."""
        picker = CollectionPicker(self.mock_client)
        result = picker.display_collections()
        self.assertIn("Machine Learning", result)
        self.assertIn("23 items", result)

    def test_select_by_number(self):
        """Test selecting collection by number."""
        self.picker._collections = self.mock_client.get_collections.return_value
        result = self.picker.select_by_number(2)
        self.assertEqual(result["name"], "Medical AI")

    def test_select_by_name(self):
        """Test selecting collection by name (case-insensitive)."""
        self.picker._collections = self.mock_client.get_collections.return_value
        result = self.picker.select_by_name("nlp")
        self.assertEqual(result["name"], "NLP")

    def test_select_by_number_out_of_range(self):
        """Test selecting invalid number returns None."""
        self.picker._collections = self.mock_client.get_collections.return_value
        result = self.picker.select_by_number(99)
        self.assertIsNone(result)

    def test_select_by_name_not_found(self):
        """Test selecting non-existent name returns None."""
        self.picker._collections = self.mock_client.get_collections.return_value
        result = self.picker.select_by_name("Nonexistent")
        self.assertIsNone(result)

    def test_empty_collections(self):
        """Test handling of empty collection list."""
        self.mock_client.get_collections.return_value = []
        picker = CollectionPicker(self.mock_client)
        result = picker.display_collections()
        self.assertIn("Tidak ada koleksi", result)


if __name__ == "__main__":
    unittest.main()
