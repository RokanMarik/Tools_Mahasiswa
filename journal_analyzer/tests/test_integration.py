"""Integration tests for the journal workflow scripts."""

import json
import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(__file__))


def test_full_pipeline_text_input():
    """Test: text input → parse → reader → reviewer → aggregate."""
    text = """## ABSTRACT
This paper investigates the impact of AI on education.

## INTRODUCTION
AI is transforming education. This study explores how.

## METHODOLOGY
We conducted a survey of 500 teachers using quantitative methods.

## RESULTS
80% of teachers reported improved student engagement.

## DISCUSSION
Results suggest AI has significant positive impact.

## CONCLUSION
More research is needed on long-term effects.
"""
    # Parse
    from parsers.text_parser import TextParser
    parser = TextParser()
    article = parser.parse(text)
    assert article.sections["abstract"] == "This paper investigates the impact of AI on education."
    assert article.word_count > 0

    # Reader (mocked)
    from workers.reader_worker import ReaderWorker
    reader_summary = "LATAR BELAKANG: AI di pendidikan sedang berkembang.\nTUJUAN: Meneliti dampak AI.\nMETODE: Survei 500 guru.\nHASIL: 80% engagement meningkat.\nIMPLIKASI: AI berdampak positif."

    with patch.object(ReaderWorker, "_chat", return_value=reader_summary):
        reader = ReaderWorker(prompts_dir="journal_analyzer/prompts")
        reader_result = reader.run(article)
        assert reader_result is not None
        assert "summary" in reader_result

    # Reviewer (mocked)
    from workers.reviewer_worker import ReviewerWorker
    review_text = "OVERALL ASSESSMENT: Minor Revision\n\nKEKUATAN:\n1. Metodologi jelas\n2. Sample size cukup\n\nMASALAH MINOR:\n1. Tambahkan effect size"

    with patch.object(ReviewerWorker, "_chat", return_value=review_text):
        reviewer = ReviewerWorker(prompts_dir="journal_analyzer/prompts")
        reviewer_result = reviewer.run(article, reader_summary=reader_summary)
        assert reviewer_result is not None
        assert reviewer_result["assessment"] == "Minor Revision"

    # Aggregate
    from core.output_aggregator import OutputAggregator
    agg = OutputAggregator()
    output = agg.aggregate({
        "reader": {"status": "success", "data": reader_result},
        "reviewer": {"status": "success", "data": reviewer_result},
    })
    assert "# Ringkasan Jurnal" in output
    assert "## Review Peer" in output
    assert "Minor Revision" in output


class TestIntegration(unittest.TestCase):
    """Test full workflow: search → save → citation."""

    @patch("modules.search.aggregator.search")
    @patch("scripts.zotero_save.ZoteroClient")
    @patch("scripts.zotero_save.CitationFormatter")
    def test_full_workflow_search_then_save(self, MockFormatter, MockClient, mock_search):
        """Full workflow: search papers, then save selected ones."""
        from modules.search.paper_model import Paper
        mock_search.return_value = [
            Paper(title="Paper A", authors=["Smith"], year=2024, journal="J1", doi="10.1/a", url="https://a.com", source="openalex", abstract=""),
            Paper(title="Paper B", authors=["Doe"], year=2023, journal="J2", doi="10.2/b", url="https://b.com", source="openalex", abstract=""),
        ]

        mock_client = MagicMock()
        mock_client.get_user_id.return_value = "12345"
        mock_client.add_item.return_value = {"key": "KEY1", "version": 1}
        MockClient.return_value = mock_client

        mock_formatter = MagicMock()
        mock_formatter.format.return_value = "Smith. (2024). Paper A. J1. https://doi.org/10.1/a"
        MockFormatter.return_value = mock_formatter

        from scripts.journal_search import search_journals
        search_result = json.loads(search_journals("test topic"))
        self.assertEqual(search_result["status"], "success")
        self.assertEqual(len(search_result["papers"]), 2)

        selected = [search_result["papers"][0]]

        from scripts.zotero_save import save_to_zotero
        save_result = json.loads(save_to_zotero(selected, api_key="test-key"))
        self.assertEqual(save_result["status"], "success")
        self.assertEqual(len(save_result["saved"]), 1)
        self.assertEqual(save_result["saved"][0]["title"], "Paper A")

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
