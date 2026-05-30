from unittest.mock import patch
from workers.comparison_worker import ComparisonWorker


def test_comparison_calls_chat():
    papers = [
        {"title": "Paper 1", "summary": "Summary 1", "methodology": "Quantitative", "key_findings": ["Finding A"]},
        {"title": "Paper 2", "summary": "Summary 2", "methodology": "Qualitative", "key_findings": ["Finding B"]},
    ]
    mock_result = "TABEL PERBANDINGAN:\nPaper 1 vs Paper 2: ..."

    with patch.object(ComparisonWorker, "_chat", return_value=mock_result) as mock_chat:
        worker = ComparisonWorker()
        result = worker.run(papers)
        mock_chat.assert_called_once()
        assert "comparison" in result


def test_comparison_returns_structured_output():
    papers = [{"title": "Test Paper", "summary": "Test"}]
    mock_result = "SYNTHESIS: All papers agree on X."

    with patch.object(ComparisonWorker, "_chat", return_value=mock_result):
        worker = ComparisonWorker()
        result = worker.run(papers)
        assert isinstance(result, dict)
        assert "comparison" in result


def test_comparison_handles_error():
    papers = [{"title": "Paper 1", "summary": "Test 1"}, {"title": "Paper 2", "summary": "Test 2"}]

    with patch.object(ComparisonWorker, "_chat", side_effect=Exception("API down")):
        worker = ComparisonWorker()
        result = worker.run(papers)
        assert result is None
