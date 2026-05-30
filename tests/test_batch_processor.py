import os
import sys
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.batch_processor import BatchProcessor


def test_process_batch_returns_dict():
    """Test that process_batch returns aggregated results"""
    processor = BatchProcessor()
    
    questions = ["What is machine learning?"]
    results = processor.process_batch(questions)
    
    assert isinstance(results, dict)
    assert "questions" in results
    assert "total_papers_found" in results
    print("[PASS] test_process_batch_returns_dict passed")


def test_process_batch_multiple_questions():
    """Test processing multiple questions"""
    with patch('modules.batch_processor.WebSearchOptimizer') as mock_optimizer_class, \
         patch('modules.batch_processor.ContentFetcher') as mock_fetcher_class:
        
        mock_optimizer_instance = MagicMock()
        mock_optimizer_instance.optimize_and_search.return_value = [
            {"title": "Paper 1", "url": "http://example.com/1"}
        ]
        mock_optimizer_class.return_value = mock_optimizer_instance
        
        mock_fetcher_instance = MagicMock()
        mock_fetcher_instance.fetch_papers.return_value = [
            {"title": "Paper 1", "content": "Content"}
        ]
        mock_fetcher_class.return_value = mock_fetcher_instance
        
        processor = BatchProcessor()
        questions = ["Question 1", "Question 2"]
        results = processor.process_batch(questions)
        
        assert len(results["questions"]) == 2
        assert results["total_papers_found"] >= 0
        print("[PASS] test_process_batch_multiple_questions passed")


def test_process_single_question_with_error():
    """Test error handling in single question processing"""
    with patch('modules.batch_processor.WebSearchOptimizer') as mock_optimizer_class:
        mock_optimizer_instance = MagicMock()
        mock_optimizer_instance.optimize_and_search.side_effect = Exception("API Error")
        mock_optimizer_class.return_value = mock_optimizer_instance
        
        processor = BatchProcessor()
        result = processor._process_single_question("test question")
        
        assert result["status"] == "error"
        assert len(result["errors"]) > 0
        print("[PASS] test_process_single_question_with_error passed")


def test_process_single_question_success():
    """Test successful single question processing"""
    with patch('modules.batch_processor.WebSearchOptimizer') as mock_optimizer_class, \
         patch('modules.batch_processor.ContentFetcher') as mock_fetcher_class:
        
        mock_optimizer_instance = MagicMock()
        mock_optimizer_instance.optimize_and_search.return_value = [
            {"title": "Paper 1", "url": "http://example.com/1"}
        ]
        mock_optimizer_class.return_value = mock_optimizer_instance
        
        mock_fetcher_instance = MagicMock()
        mock_fetcher_instance.fetch_papers.return_value = [
            {"title": "Paper 1", "content": "Content", "url": "http://example.com/1"}
        ]
        mock_fetcher_class.return_value = mock_fetcher_instance
        
        processor = BatchProcessor()
        result = processor._process_single_question("test question")
        
        assert result["status"] == "success"
        assert len(result["papers"]) > 0
        print("[PASS] test_process_single_question_success passed")


def test_retry_search_with_fallback():
    """Test fallback search retry"""
    with patch('modules.batch_processor.WebSearchOptimizer') as mock_optimizer_class:
        mock_optimizer_instance = MagicMock()
        mock_optimizer_instance.optimize_and_search.return_value = [
            {"title": "Fallback Paper", "url": "http://example.com/fallback"}
        ]
        mock_optimizer_class.return_value = mock_optimizer_instance
        
        processor = BatchProcessor()
        results = processor._retry_search_with_fallback("test question with many words")
        
        assert len(results) > 0
        assert results[0]["title"] == "Fallback Paper"
        print("[PASS] test_retry_search_with_fallback passed")


if __name__ == "__main__":
    test_process_batch_returns_dict()
    test_process_batch_multiple_questions()
    test_process_single_question_with_error()
    test_process_single_question_success()
    test_retry_search_with_fallback()
    print("\n[SUCCESS] All BatchProcessor tests passed!")
