from unittest.mock import patch
from workers.data_analysis_worker import DataAnalysisWorker


def test_data_analysis_basic():
    mock_result = "RINGKASAN DESKRIPTIF:\nMean = 75.3, SD = 12.1"

    with patch.object(DataAnalysisWorker, "_chat", return_value=mock_result) as mock_chat:
        worker = DataAnalysisWorker()
        result = worker.run(
            research_question="Pengaruh metode X terhadap hasil belajar",
            dataset_description="n=200, variabel: skor_pretest, skor_posttest",
            statistical_results="t(199) = 5.67, p < 0.001, Cohen's d = 0.85",
        )
        mock_chat.assert_called_once()
        assert "interpretation" in result


def test_data_analysis_with_hypothesis():
    mock_result = "INTERPRETASI: H0 ditolak."

    with patch.object(DataAnalysisWorker, "_chat", return_value=mock_result):
        worker = DataAnalysisWorker()
        result = worker.run(
            research_question="Perbedaan skor antara grup A dan B",
            hypothesis="Grup A > Grup B",
            statistical_results="t = 2.34, p = 0.02",
        )
        assert "interpretation" in result


def test_data_analysis_handles_error():
    with patch.object(DataAnalysisWorker, "_chat", side_effect=Exception("API down")):
        worker = DataAnalysisWorker()
        result = worker.run(
            research_question="Test question",
            dataset_description="Test data",
        )
        assert result is None
