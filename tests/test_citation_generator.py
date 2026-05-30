"""Tests for scripts/citation_generator.py"""

import json
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestCitationGenerator(unittest.TestCase):
    """Test citation_generator script functions."""

    def test_generate_apa_citation(self):
        """Should generate APA citation from paper metadata."""
        from scripts.citation_generator import generate_citations

        papers = [
            {
                "title": "Deep Learning for Medical Imaging",
                "authors": ["John Smith", "Jane Doe"],
                "year": 2024,
                "journal": "Journal of Medical AI",
                "doi": "10.1234/test",
            }
        ]

        result = generate_citations(papers, style="apa")
        data = json.loads(result)
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["citations"]), 1)
        citation = data["citations"][0]["apa"]
        self.assertIn("Smith", citation)
        self.assertIn("2024", citation)
        self.assertIn("Deep Learning", citation)

    def test_generate_citation_missing_authors(self):
        """Should handle papers with no authors."""
        from scripts.citation_generator import generate_citations

        papers = [{"title": "Untitled Paper", "year": 2024}]
        result = generate_citations(papers, style="apa")
        data = json.loads(result)
        self.assertEqual(data["status"], "success")
        citation = data["citations"][0]["apa"]
        self.assertIn("Unknown Author", citation)

    def test_generate_citation_empty_list(self):
        """Should handle empty paper list."""
        from scripts.citation_generator import generate_citations

        result = generate_citations([], style="apa")
        data = json.loads(result)
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["citations"]), 0)

    def test_generate_citation_unsupported_style_defaults_to_apa(self):
        """Unsupported style should default to APA."""
        from scripts.citation_generator import generate_citations

        papers = [{"title": "Test", "authors": ["Smith"], "year": 2024}]
        result = generate_citations(papers, style="harvard")
        data = json.loads(result)
        self.assertEqual(data["status"], "success")
        self.assertIn("apa", data["citations"][0])


    def test_generate_multiple_papers(self):
        """Should handle multiple papers."""
        from scripts.citation_generator import generate_citations

        papers = [
            {"title": "Paper A", "authors": ["Smith"], "year": 2024},
            {"title": "Paper B", "authors": ["Doe"], "year": 2023},
        ]
        result = generate_citations(papers, style="apa")
        data = json.loads(result)
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["citations"]), 2)

    def test_generate_citation_error_path(self):
        """Should return error JSON on unexpected failure."""
        from scripts.citation_generator import generate_citations

        # Pass invalid data that triggers an error in CitationFormatter
        result = generate_citations(None, style="apa")  # type: ignore
        data = json.loads(result)
        self.assertEqual(data["status"], "error")
        self.assertIsNotNone(data["error"])

    def test_generate_citation_with_style_key(self):
        """Output key should match the requested style."""
        from scripts.citation_generator import generate_citations

        papers = [{"title": "Test", "authors": ["Smith"], "year": 2024}]
        result = generate_citations(papers, style="ieee")
        data = json.loads(result)
        self.assertIn("ieee", data["citations"][0])
        self.assertNotIn("apa", data["citations"][0])


if __name__ == "__main__":
    unittest.main()
