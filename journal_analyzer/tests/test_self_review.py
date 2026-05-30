from unittest.mock import patch
from workers.self_review_worker import SelfReviewWorker


def test_self_review_calls_chat():
    mock_result = "QUALITY SCORE: 8/10\n\nSTRENGTHS: Good structure."

    with patch.object(SelfReviewWorker, "_chat", return_value=mock_result) as mock_chat:
        worker = SelfReviewWorker()
        result = worker.run(
            draft_article="# DRAFT ARTIKEL\n\n## ABSTRAK\nTest abstract.",
            research_topic="AI in Education",
        )
        mock_chat.assert_called_once()
        assert "review" in result


def test_self_review_returns_structured_output():
    mock_result = "QUALITY SCORE: 7\n\nISSUES: Need more references."

    with patch.object(SelfReviewWorker, "_chat", return_value=mock_result):
        worker = SelfReviewWorker()
        result = worker.run(draft_article="# DRAFT\nTest")
        assert isinstance(result, dict)
        assert "review" in result


def test_self_review_handles_error():
    with patch.object(SelfReviewWorker, "_chat", side_effect=Exception("API down")):
        worker = SelfReviewWorker()
        result = worker.run(draft_article="# DRAFT\nTest")
        assert result is None
