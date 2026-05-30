"""Tests for CitationFormatter."""

import unittest
from modules.zotero.citation_formatter import CitationFormatter


class TestCitationFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = CitationFormatter()
        self.sample_paper = {
            "title": "Deep Learning for Medical Imaging",
            "authors": ["John Smith", "Jane Doe"],
            "date": "2024",
            "doi": "10.1234/abc",
            "journal": "Journal of Medical AI",
            "volume": "15",
            "issue": "3",
            "pages": "123-145",
        }

    def test_apa_format(self):
        result = self.formatter.format(self.sample_paper, style="apa")
        self.assertIn("Smith, J.", result)
        self.assertIn("(2024)", result)
        self.assertIn("Deep Learning for Medical Imaging", result)
        self.assertIn("10.1234/abc", result)

    def test_ieee_format(self):
        result = self.formatter.format(self.sample_paper, style="ieee", number=1)
        self.assertIn("[1]", result)
        self.assertIn("J. Smith", result)
        self.assertIn("Deep Learning for Medical Imaging", result)
        self.assertIn("vol. 15", result)

    def test_mla_format(self):
        result = self.formatter.format(self.sample_paper, style="mla")
        self.assertIn("Smith, John", result)
        self.assertIn("Doe, Jane", result)
        self.assertIn("Deep Learning for Medical Imaging", result)
        self.assertIn("2024", result)

    def test_chicago_format(self):
        result = self.formatter.format(self.sample_paper, style="chicago")
        self.assertIn("Smith, John", result)
        self.assertIn("Doe, Jane", result)
        self.assertIn("Deep Learning for Medical Imaging", result)
        self.assertIn("15", result)
        self.assertIn("2024", result)

    def test_unknown_style_defaults_to_apa(self):
        result = self.formatter.format(self.sample_paper, style="unknown")
        self.assertIn("(2024)", result)  # APA uses year in parentheses

    def test_missing_fields(self):
        paper = {
            "title": "No DOI Paper",
            "authors": ["Bob Lee"],
            "date": "2023",
            "doi": "",
            "journal": "",
            "volume": "",
            "issue": "",
            "pages": "",
        }
        result = self.formatter.format(paper, style="apa")
        self.assertNotIn("10.", result)  # No DOI should appear

    def test_single_author(self):
        paper = {
            "title": "Single Author Paper",
            "authors": ["Alice Johnson"],
            "date": "2024",
            "doi": "",
            "journal": "",
            "volume": "",
            "issue": "",
            "pages": "",
        }
        result = self.formatter.format(paper, style="apa")
        self.assertIn("Johnson, A.", result)

    def test_no_authors(self):
        paper = {
            "title": "No Author Paper",
            "authors": [],
            "date": "2024",
            "doi": "",
            "journal": "",
            "volume": "",
            "issue": "",
            "pages": "",
        }
        result = self.formatter.format(paper, style="apa")
        self.assertIn("Unknown Author", result)


if __name__ == "__main__":
    unittest.main()
