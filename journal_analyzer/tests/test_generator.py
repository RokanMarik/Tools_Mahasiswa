from unittest.mock import patch
from workers.generator_worker import GeneratorWorker


def test_generator_calls_chat():
    mock_result = "# DRAFT ARTIKEL\n\n## ABSTRAK\nTest abstract."

    with patch.object(GeneratorWorker, "_chat", return_value=mock_result) as mock_chat:
        worker = GeneratorWorker()
        result = worker.run(
            research_topic="AI in Education",
            reader_summaries=["Summary 1", "Summary 2"],
        )
        mock_chat.assert_called_once()
        assert "draft" in result


def test_generator_returns_structured_output():
    mock_result = "# DRAFT ARTIKEL\n\n## ABSTRAK\nTest."

    with patch.object(GeneratorWorker, "_chat", return_value=mock_result):
        worker = GeneratorWorker()
        result = worker.run(research_topic="Test topic")
        assert isinstance(result, dict)
        assert "draft" in result


def test_generator_with_gap_analysis():
    mock_result = "# DRAFT\n\nAddressing the gap in longitudinal studies."

    with patch.object(GeneratorWorker, "_chat", return_value=mock_result) as mock_chat:
        worker = GeneratorWorker()
        result = worker.run(
            research_topic="Test",
            gap_analysis="Gap: longitudinal studies needed",
        )
        call_args = mock_chat.call_args
        assert "longitudinal studies needed" in call_args[0][1]


def test_generator_handles_error():
    with patch.object(GeneratorWorker, "_chat", side_effect=Exception("API down")):
        worker = GeneratorWorker()
        result = worker.run(research_topic="Test")
        assert result is None
