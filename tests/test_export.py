"""Tests for export modules."""
import pytest
from modules.export.csv_export import CsvExporter
from modules.export.bibtex_export import BibtexExporter
from modules.export.ris_export import RisExporter


SAMPLE_PAPERS = [
    {"title": "Test Paper", "authors": ["Smith, John"], "year": 2024, "citations": 42, "doi": "10.1234/test", "journal": "Test J", "source": "crossref"},
    {"title": "Another Paper", "authors": ["Doe, Jane", "Lee, Bob"], "year": 2023, "citations": 10, "journal": "Other J", "source": "semantic-scholar"},
]


class TestCsvExporter:
    def test_export_contains_header(self):
        output = CsvExporter().export(SAMPLE_PAPERS)
        assert "title,authors,year,citations,doi,url,journal,source" in output

    def test_export_contains_data(self):
        output = CsvExporter().export(SAMPLE_PAPERS)
        assert "Test Paper" in output
        assert "Another Paper" in output


class TestBibtexExporter:
    def test_export_contains_article(self):
        output = BibtexExporter().export(SAMPLE_PAPERS)
        assert "@article{paper1," in output
        assert "@article{paper2," in output

    def test_export_contains_title(self):
        output = BibtexExporter().export(SAMPLE_PAPERS)
        assert "Test Paper" in output


class TestRisExporter:
    def test_export_contains_type(self):
        output = RisExporter().export(SAMPLE_PAPERS)
        assert "TY  - JOUR" in output

    def test_export_contains_end(self):
        output = RisExporter().export(SAMPLE_PAPERS)
        assert "ER  - " in output

    def test_export_contains_authors(self):
        output = RisExporter().export(SAMPLE_PAPERS)
        assert "AU  - Smith, John" in output
