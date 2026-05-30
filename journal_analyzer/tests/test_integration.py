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


def test_gap_analysis_pipeline():
    """Test: parse → reader → gap analyzer → aggregate."""
    from unittest.mock import patch
    text = """## ABSTRACT
This study examines AI in education with a survey of 500 teachers.

## INTRODUCTION
AI is transforming education globally.

## METHODOLOGY
Quantitative survey method.

## RESULTS
75% reported improved engagement.

## CONCLUSION
More longitudinal research is needed.
"""
    from parsers.text_parser import TextParser
    parser = TextParser()
    article = parser.parse(text)

    reader_summary = "AI improves engagement in education."

    from workers.reader_worker import ReaderWorker
    from workers.gap_analyzer_worker import GapAnalyzerWorker
    from core.output_aggregator import OutputAggregator

    with patch.object(ReaderWorker, "_chat", return_value=reader_summary):
        reader = ReaderWorker(prompts_dir="journal_analyzer/prompts")
        reader_result = reader.run(article)

    gap_text = "GAP: 1. Studi longitudinal belum ada. 2. Konteks Asia Tenggara kurang diteliti."

    with patch.object(GapAnalyzerWorker, "_chat", return_value=gap_text):
        gap_worker = GapAnalyzerWorker(prompts_dir="journal_analyzer/prompts")
        gap_result = gap_worker.run(article, reader_summary=reader_summary)
        assert gap_result is not None
        assert "gap_text" in gap_result

    agg = OutputAggregator()
    output = agg.aggregate({
        "reader": {"status": "success", "data": reader_result},
        "gap_analyzer": {"status": "success", "data": gap_result},
    })
    assert "# Ringkasan Jurnal" in output
    assert "## Research Gap" in output
    assert "longitudinal" in output


def test_data_analysis_pipeline():
    """Test: data analysis worker → aggregate."""
    from unittest.mock import patch
    from workers.data_analysis_worker import DataAnalysisWorker
    from core.output_aggregator import OutputAggregator

    interp_text = "RINGKASAN DESKRIPTIF:\nMean = 75.3, SD = 12.1\n\nINTERPRETASI: H0 ditolak (p < 0.05)."

    with patch.object(DataAnalysisWorker, "_chat", return_value=interp_text):
        worker = DataAnalysisWorker(prompts_dir="journal_analyzer/prompts")
        result = worker.run(
            research_question="Pengaruh metode X terhadap hasil belajar",
            dataset_description="n=200, pretest-posttest design",
        )
        assert result is not None
        assert "interpretation" in result

    agg = OutputAggregator()
    output = agg.aggregate({
        "data_analysis": {"status": "success", "data": result},
    })
    assert "## Analisis Data" in output
    assert "H0 ditolak" in output


def test_generate_pipeline():
    """Test: parse → reader → gap analyzer → generator → self-review → aggregate."""
    from unittest.mock import patch
    text = """## ABSTRACT
This study examines AI use in education.

## INTRODUCTION
AI is transforming education.

## METHODOLOGY
Survey of 500 teachers.

## RESULTS
75% reported improved engagement.

## CONCLUSION
More research needed.
"""
    from parsers.text_parser import TextParser
    parser = TextParser()
    article = parser.parse(text)

    from workers.reader_worker import ReaderWorker
    from workers.gap_analyzer_worker import GapAnalyzerWorker
    from workers.generator_worker import GeneratorWorker
    from workers.self_review_worker import SelfReviewWorker
    from core.output_aggregator import OutputAggregator

    # Mock reader
    with patch.object(ReaderWorker, "_chat", return_value="AI improves engagement."):
        reader = ReaderWorker(prompts_dir="journal_analyzer/prompts")
        reader_result = reader.run(article)

    # Mock gap analyzer
    with patch.object(GapAnalyzerWorker, "_chat", return_value="GAP: Longitudinal studies needed."):
        gap_worker = GapAnalyzerWorker(prompts_dir="journal_analyzer/prompts")
        gap_result = gap_worker.run(article, reader_summary="AI improves engagement.")

    # Mock generator
    draft = "# DRAFT ARTIKEL\n\n## ABSTRAK\nAI in education improves engagement.\n\n## DATA DIBUTUHKAN: Empirical results."
    with patch.object(GeneratorWorker, "_chat", return_value=draft):
        gen_worker = GeneratorWorker(prompts_dir="journal_analyzer/prompts")
        gen_result = gen_worker.run(
            research_topic="AI in Education",
            reader_summaries=["AI improves engagement."],
            gap_analysis="GAP: Longitudinal studies needed.",
        )
        assert gen_result is not None
        assert "draft" in gen_result

    # Mock self-review
    review = "QUALITY SCORE: 8/10\n\nSTRENGTHS: Good structure.\nISSUES: Need to fill data placeholders."
    with patch.object(SelfReviewWorker, "_chat", return_value=review):
        review_worker = SelfReviewWorker(prompts_dir="journal_analyzer/prompts")
        review_result = review_worker.run(draft_article=draft, research_topic="AI in Education")
        assert review_result is not None
        assert "review" in review_result

    # Aggregate
    agg = OutputAggregator()
    output = agg.aggregate({
        "reader": {"status": "success", "data": reader_result},
        "gap_analyzer": {"status": "success", "data": gap_result},
        "generator": {"status": "success", "data": gen_result},
        "self_review": {"status": "success", "data": review_result},
    })
    assert "# Ringkasan Jurnal" in output
    assert "## Research Gap" in output
    assert "## Draft Artikel" in output
    assert "## Self-Review" in output
    assert "8/10" in output


def test_compare_pipeline():
    """Test: parse multiple papers → comparison → aggregate."""
    from unittest.mock import patch
    text1 = """## ABSTRACT
Paper 1 about AI in education using quantitative method."""
    text2 = """## ABSTRACT
Paper 2 about AI in education using qualitative method."""

    from parsers.text_parser import TextParser
    article1 = TextParser().parse(text1)
    article2 = TextParser().parse(text2)

    from workers.comparison_worker import ComparisonWorker
    from core.output_aggregator import OutputAggregator

    comp_text = "TABEL PERBANDINGAN:\nPaper 1: Kuantitatif\nPaper 2: Kualitatif\n\nSYNTHESIS: Both show positive impact."

    with patch.object(ComparisonWorker, "_chat", return_value=comp_text):
        worker = ComparisonWorker(prompts_dir="journal_analyzer/prompts")
        papers = [
            {"title": article1.metadata.get("title", "Paper 1"), "summary": article1.sections.get("abstract", "")},
            {"title": article2.metadata.get("title", "Paper 2"), "summary": article2.sections.get("abstract", "")},
        ]
        result = worker.run(papers)
        assert result is not None
        assert "comparison" in result

    agg = OutputAggregator()
    output = agg.aggregate({
        "comparison": {"status": "success", "data": result},
    })
    assert "## Perbandingan Paper" in output
    assert "Kuantitatif" in output
    assert "Kualitatif" in output


if __name__ == "__main__":
    unittest.main()
