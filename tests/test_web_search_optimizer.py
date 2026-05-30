import os
import sys
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.web_search_optimizer import WebSearchOptimizer
from modules.search_cache import SearchCache


def test_generate_search_query():
    """Test that search query is generated from research question"""
    optimizer = WebSearchOptimizer(
        ninerouter_url="http://localhost:20128",
        ninerouter_key="test-key"
    )
    
    research_question = "How does deep learning improve cancer detection?"
    
    # Mock the requests.post call
    with patch('modules.web_search_optimizer.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "deep learning cancer detection medical imaging"}}]
        }
        mock_post.return_value = mock_response
        
        query = optimizer._generate_search_query(research_question)
        
        assert isinstance(query, str)
        assert len(query) > 0
        print("[PASS] test_generate_search_query passed")


def test_optimize_and_search_uses_cache():
    """Test that cached results are returned without new search"""
    cache = Mock()
    cache.get.return_value = [{"title": "Cached Paper", "url": "http://example.com"}]
    
    optimizer = WebSearchOptimizer(cache=cache)
    results = optimizer.optimize_and_search("test question")
    
    assert results == [{"title": "Cached Paper", "url": "http://example.com"}]
    cache.get.assert_called_once_with("test question")
    print("[PASS] test_optimize_and_search_uses_cache passed")


def test_optimize_and_search_executes_search():
    """Test that search is executed when cache miss"""
    with patch('modules.web_search_optimizer.requests.post') as mock_post:
        # Mock chat response for query generation
        chat_response = MagicMock()
        chat_response.json.return_value = {
            "choices": [{"message": {"content": "test query"}}]
        }
        
        # Mock search response
        search_response = MagicMock()
        search_response.json.return_value = {
            "results": [
                {
                    "title": "Paper 1",
                    "url": "http://example.com/1",
                    "snippet": "Abstract...",
                    "source": "arxiv"
                }
            ]
        }
        
        # Set up mock to return different responses for chat and search
        mock_post.side_effect = [chat_response, search_response]
        
        cache = Mock()
        cache.get.return_value = None
        
        optimizer = WebSearchOptimizer(cache=cache)
        results = optimizer.optimize_and_search("test question")
        
        assert len(results) > 0
        assert results[0]["title"] == "Paper 1"
        cache.set.assert_called_once()
        print("[PASS] test_optimize_and_search_executes_search passed")


def test_optimize_and_search_handles_error():
    """Test that search handles errors gracefully"""
    with patch('modules.web_search_optimizer.requests.post') as mock_post:
        # Mock chat response
        chat_response = MagicMock()
        chat_response.json.return_value = {
            "choices": [{"message": {"content": "test query"}}]
        }
        
        # Mock search error
        mock_post.side_effect = [chat_response, Exception("API Error")]
        
        cache = Mock()
        cache.get.return_value = None
        
        optimizer = WebSearchOptimizer(cache=cache)
        results = optimizer.optimize_and_search("test question")
        
        assert results == []
        print("[PASS] test_optimize_and_search_handles_error passed")


if __name__ == "__main__":
    test_generate_search_query()
    test_optimize_and_search_uses_cache()
    test_optimize_and_search_executes_search()
    test_optimize_and_search_handles_error()
    print("\n[SUCCESS] All WebSearchOptimizer tests passed!")
