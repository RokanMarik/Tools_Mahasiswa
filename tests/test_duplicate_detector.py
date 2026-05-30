"""Tests for DuplicateDetector."""

import unittest
from modules.zotero.duplicate_detector import DuplicateDetector


class TestDuplicateDetector(unittest.TestCase):
    def setUp(self):
        self.detector = DuplicateDetector()
        self.sample_items = [
            {
                "key": "ITEM1",
                "title": "Deep Learning for Medical Imaging",
                "authors": ["John Smith"],
                "doi": "10.1234/abc",
                "journal": "Medical AI Journal",
                "date": "2024",
                "item_type": "journalArticle",
            },
            {
                "key": "ITEM2",
                "title": "Deep Learning for Medical Imaging",
                "authors": ["John Smith"],
                "doi": "10.1234/abc",
                "journal": "Medical AI Journal",
                "date": "2024",
                "item_type": "journalArticle",
            },
            {
                "key": "ITEM3",
                "title": "AI in Healthcare: A Review",
                "authors": ["Jane Doe"],
                "doi": "10.5678/def",
                "journal": "Healthcare Review",
                "date": "2023",
                "item_type": "journalArticle",
            },
            {
                "key": "ITEM4",
                "title": "AI in Healthcare Review",
                "authors": ["Jane Doe"],
                "doi": "10.9999/ghi",
                "journal": "Healthcare Review",
                "date": "2023",
                "item_type": "journalArticle",
            },
            {
                "key": "ITEM5",
                "title": "Unique Paper Title",
                "authors": ["Bob Lee"],
                "doi": "10.1111/jkl",
                "journal": "Unique Journal",
                "date": "2022",
                "item_type": "journalArticle",
            },
        ]

    def test_no_duplicates(self):
        """Test with items that have no duplicates."""
        items = self.sample_items[4:]  # Just the unique one
        result = self.detector.find_duplicates(items)
        self.assertEqual(len(result), 0)

    def test_exact_doi_match(self):
        """Test detection of exact DOI duplicates."""
        result = self.detector.find_duplicates(self.sample_items)
        doi_groups = [g for g in result if g["reason"] == "same_doi"]
        self.assertEqual(len(doi_groups), 1)
        self.assertEqual(len(doi_groups[0]["group"]), 2)

    def test_similar_title_match(self):
        """Test detection of similar title duplicates."""
        result = self.detector.find_duplicates(self.sample_items)
        title_groups = [g for g in result if g["reason"] == "similar_title"]
        self.assertEqual(len(title_groups), 1)
        self.assertEqual(len(title_groups[0]["group"]), 2)

    def test_empty_items(self):
        """Test with empty list."""
        result = self.detector.find_duplicates([])
        self.assertEqual(len(result), 0)

    def test_single_item(self):
        """Test with single item (no duplicates possible)."""
        result = self.detector.find_duplicates([self.sample_items[0]])
        self.assertEqual(len(result), 0)

    def test_items_without_doi(self):
        """Test items with empty DOI are not matched by DOI."""
        items = [
            {"key": "A", "title": "Paper A", "doi": "", "authors": [], "journal": "", "date": "", "item_type": ""},
            {"key": "B", "title": "Paper B", "doi": "", "authors": [], "journal": "", "date": "", "item_type": ""},
        ]
        result = self.detector.find_duplicates(items)
        doi_groups = [g for g in result if g["reason"] == "same_doi"]
        self.assertEqual(len(doi_groups), 0)


if __name__ == "__main__":
    unittest.main()
