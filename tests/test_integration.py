"""Integration tests for the journal workflow scripts."""

import json
import unittest

class TestIntegration(unittest.TestCase):
    """Test integration between search results and citation generation."""

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
