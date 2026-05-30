"""Tests for GapAnalyzer."""

import unittest
from modules.zotero.gap_analyzer import GapAnalyzer


class TestGapAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = GapAnalyzer()
        self.sample_items = [
            {"title": "Deep Learning for Medical Imaging", "journal": "Medical AI Journal", "authors": [], "doi": "", "key": "", "date": "", "item_type": ""},
            {"title": "Machine Learning in Healthcare", "journal": "Health Informatics", "authors": [], "doi": "", "key": "", "date": "", "item_type": ""},
            {"title": "Neural Networks for Diagnosis", "journal": "AI Medicine", "authors": [], "doi": "", "key": "", "date": "", "item_type": ""},
            {"title": "NLP for Clinical Notes", "journal": "NLP Journal", "authors": [], "doi": "", "key": "", "date": "", "item_type": ""},
        ]

    def test_missing_topic(self):
        """Test topic with 0 papers is classified as missing."""
        results = self.analyzer.analyze(self.sample_items)
        robotics = [r for r in results if r["topic"] == "Robotics"]
        self.assertEqual(len(robotics), 1)
        self.assertEqual(robotics[0]["status"], "missing")
        self.assertEqual(robotics[0]["count"], 0)

    def test_empty_items(self):
        """Test with empty item list -- all topics should be missing."""
        results = self.analyzer.analyze([])
        self.assertTrue(all(r["status"] == "missing" for r in results))

    def test_sorting_order(self):
        """Test that results are sorted: missing first, then low, then covered."""
        results = self.analyzer.analyze(self.sample_items)
        status_order = {"missing": 0, "low": 1, "covered": 2}
        statuses = [status_order[r["status"]] for r in results]
        self.assertEqual(statuses, sorted(statuses))

    def test_returns_all_topics(self):
        """Test that all predefined topics are in results."""
        results = self.analyzer.analyze(self.sample_items)
        self.assertEqual(len(results), len(self.analyzer._get_topics_for_field("AI")))

    def test_topic_matching_case_insensitive(self):
        """Test that topic matching is case insensitive."""
        items = [{"title": "DEEP LEARNING IS GREAT", "journal": "", "authors": [], "doi": "", "key": "", "date": "", "item_type": ""}]
        results = self.analyzer.analyze(items)
        dl = [r for r in results if r["topic"].lower() == "deep learning"]
        self.assertEqual(dl[0]["count"], 1)


if __name__ == "__main__":
    unittest.main()
