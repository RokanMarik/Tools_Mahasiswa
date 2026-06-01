"""Tests for display module."""
import pytest
from modules.ui.display import Display


class TestDisplay:
    def setup_method(self):
        self.display = Display()
        self.papers = [
            {"title": "Test Paper", "authors": ["Smith, J"], "year": 2024, "citations": 42, "doi": "10.1234/test", "journal": "Test J", "source": "crossref"},
        ]

    def test_display_results_not_empty(self):
        result = self.display.display_results(self.papers, "test")
        assert "Test Paper" in result

    def test_display_results_no_papers(self):
        result = self.display.display_results([], "test")
        assert len(result) > 0  # Should show no results message

    def test_display_table_not_empty(self):
        result = self.display.display_table(self.papers)
        assert "Test Paper" in result

    def test_display_balanced(self):
        result = self.display.display_balanced(
            foundational=[{"title": "Foundational", "citations": 100}],
            recent=[{"title": "Recent", "year": 2024}],
            query="test"
        )
        assert "Foundational" in result
        assert "Recent" in result
