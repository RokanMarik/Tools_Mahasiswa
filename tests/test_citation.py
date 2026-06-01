"""Tests for citation formatter."""
import pytest
from modules.zotero.citation_formatter import CitationFormatter


class TestCitationFormatter:
    def setup_method(self):
        self.formatter = CitationFormatter()
        self.item = {
            "title": "Test Paper Title",
            "authors": ["Smith, John", "Doe, Jane"],
            "date": "2024",
            "journal": "Test Journal",
        }

    def test_apa_format(self):
        result = self.formatter.format(self.item, "apa")
        assert "Smith, J." in result or "John, S." in result
        assert "2024" in result
        assert "Test Paper Title" in result

    def test_ieee_format(self):
        result = self.formatter.format(self.item, "ieee")
        assert "2024" in result

    def test_mla_format(self):
        result = self.formatter.format(self.item, "mla")
        assert "2024" in result

    def test_chicago_format(self):
        result = self.formatter.format(self.item, "chicago")
        assert "2024" in result
