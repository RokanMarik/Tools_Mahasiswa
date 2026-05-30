from unittest.mock import patch
from models.article_data import StructuredArticleData
from workers.reviewer_worker import ReviewerWorker


def _make_article() -> StructuredArticleData:
    return StructuredArticleData(
        metadata={"title": "Test Paper", "authors": ["Test Author"], "publication_year": 2024},
        sections={
            "abstract": "Test abstract about methodology.",
            "introduction": "Background and research question.",
            "methodology": "We used quantitative survey method with n=200.",
            "results": "Significant correlation found (p<0.05).",
            "discussion": "Results support the hypothesis.",
            "conclusion": "Further research needed.",
        },
        methodology_type="kuantitatif",
        raw_text="Full text.",
    )


def test_reviewer_calls_chat_with_context():
    article = _make_article()
    mock_result = "OVERALL ASSESSMENT: Major Revision\n\nKEKUATAN: 1. Good methodology"

    with patch.object(ReviewerWorker, "_chat", return_value=mock_result) as mock_chat:
        worker = ReviewerWorker(ninerouter_url="http://test", ninerouter_key="key")
        result = worker.run(article, reader_summary="Summary context")
        mock_chat.assert_called_once()
        assert "assessment" in result
        assert "review_text" in result


def test_reviewer_extracts_assessment():
    article = _make_article()
    mock_result = "OVERALL ASSESSMENT: Minor Revision\n\nSome review text here."

    with patch.object(ReviewerWorker, "_chat", return_value=mock_result):
        worker = ReviewerWorker(ninerouter_url="http://test", ninerouter_key="key")
        result = worker.run(article)
        assert result["assessment"] == "Minor Revision"


def test_reviewer_handles_no_assessment():
    article = _make_article()
    mock_result = "This paper is good."

    with patch.object(ReviewerWorker, "_chat", return_value=mock_result):
        worker = ReviewerWorker(ninerouter_url="http://test", ninerouter_key="key")
        result = worker.run(article)
        assert result["assessment"] == "N/A"
        assert result["review_text"] == "This paper is good."


def test_reviewer_handles_error():
    article = _make_article()

    with patch.object(ReviewerWorker, "_chat", side_effect=Exception("API down")):
        worker = ReviewerWorker(ninerouter_url="http://test", ninerouter_key="key")
        result = worker.run(article)
        assert result is None
