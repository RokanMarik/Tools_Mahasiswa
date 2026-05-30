from unittest.mock import patch
from models.article_data import StructuredArticleData
from workers.gap_analyzer_worker import GapAnalyzerWorker


def _make_article() -> StructuredArticleData:
    return StructuredArticleData(
        metadata={"title": "AI in Education", "authors": ["Dr. Smith"], "publication_year": 2024},
        sections={
            "abstract": "This study explores AI use in classrooms.",
            "introduction": "AI is transforming education globally.",
            "methodology": "Survey of 500 teachers across 3 countries.",
            "results": "75% reported improved engagement.",
            "discussion": "Results suggest positive impact.",
            "conclusion": "More research needed on long-term effects.",
        },
        methodology_type="kuantitatif",
        key_findings=["75% improved engagement", "AI tools effective"],
        raw_text="Full text.",
    )


def test_gap_analyzer_calls_chat():
    article = _make_article()
    mock_result = "GAP YANG DIIDENTIFIKASI:\n1. Belum ada studi longitudinal."

    with patch.object(GapAnalyzerWorker, "_chat", return_value=mock_result) as mock_chat:
        worker = GapAnalyzerWorker()
        result = worker.run(article)
        mock_chat.assert_called_once()
        assert "gap_text" in result


def test_gap_analyzer_returns_structured_output():
    article = _make_article()
    mock_result = "GAP YANG DIIDENTIFIKASI:\n1. Longitudinal study belum ada."

    with patch.object(GapAnalyzerWorker, "_chat", return_value=mock_result):
        worker = GapAnalyzerWorker()
        result = worker.run(article)
        assert isinstance(result, dict)
        assert "gap_text" in result


def test_gap_analyzer_with_reader_summary():
    article = _make_article()
    mock_result = "GAP: 1. Context Indonesia belum diteliti."

    with patch.object(GapAnalyzerWorker, "_chat", return_value=mock_result) as mock_chat:
        worker = GapAnalyzerWorker()
        result = worker.run(article, reader_summary="AI improves engagement in Western context")
        call_args = mock_chat.call_args
        assert "AI improves engagement in Western context" in call_args[0][1]


def test_gap_analyzer_handles_error():
    article = _make_article()

    with patch.object(GapAnalyzerWorker, "_chat", side_effect=Exception("API down")):
        worker = GapAnalyzerWorker()
        result = worker.run(article)
        assert result is None
