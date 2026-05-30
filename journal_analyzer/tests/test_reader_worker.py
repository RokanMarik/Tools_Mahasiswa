from unittest.mock import patch, MagicMock
from models.article_data import StructuredArticleData
from workers.reader_worker import ReaderWorker


def _make_article() -> StructuredArticleData:
    return StructuredArticleData(
        metadata={"title": "Test Paper", "authors": ["Test Author"]},
        sections={"abstract": "Test abstract", "introduction": "Test intro"},
        raw_text="Test full text",
    )


def test_reader_calls_chat():
    article = _make_article()
    mock_result = "LATAR BELAKANG: Test.\nTUJUAN: Test.\nMETODE: Test."

    with patch.object(ReaderWorker, "_chat", return_value=mock_result) as mock_chat:
        worker = ReaderWorker(ninerouter_url="http://test", ninerouter_key="key")
        result = worker.run(article)
        mock_chat.assert_called_once()
        assert "summary" in result
        assert "LATAR BELAKANG" in result["summary"]


def test_reader_returns_structured_output():
    article = _make_article()
    mock_result = "LATAR BELAKANG: Test context.\nTUJUAN: Test goal."

    with patch.object(ReaderWorker, "_chat", return_value=mock_result):
        worker = ReaderWorker(ninerouter_url="http://test", ninerouter_key="key")
        result = worker.run(article)
        assert isinstance(result, dict)
        assert "summary" in result


def test_reader_handles_error():
    article = _make_article()

    with patch.object(ReaderWorker, "_chat", side_effect=Exception("API down")):
        worker = ReaderWorker(ninerouter_url="http://test", ninerouter_key="key")
        result = worker.run(article)
        assert result is None
