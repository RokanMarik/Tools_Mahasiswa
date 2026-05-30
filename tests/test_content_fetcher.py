import os
import sys
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.content_fetcher import ContentFetcher
from modules.search_cache import SearchCache


def test_fetch_papers_returns_list():
    """Test that fetch_papers returns list of papers"""
    fetcher = ContentFetcher(
        ninerouter_url="http://localhost:20128",
        ninerouter_key="test-key"
    )
    
    urls = ["http://example.com/paper1.pdf"]
    results = fetcher.fetch_papers(urls, max_papers=1)
    
    assert isinstance(results, list)
    print("[PASS] test_fetch_papers_returns_list passed")


def test_fetch_single_paper_success():
    """Test successful paper fetch"""
    with patch('modules.content_fetcher.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "title": "Test Paper",
            "content": "This is the paper content...",
            "source": "arxiv"
        }
        mock_post.return_value = mock_response
        
        cache = Mock()
        cache.get.return_value = None
        
        fetcher = ContentFetcher(cache=cache)
        result = fetcher._fetch_single_paper("http://example.com/paper.pdf")
        
        assert result is not None
        assert result["title"] == "Test Paper"
        assert "content" in result
        print("[PASS] test_fetch_single_paper_success passed")


def test_fetch_papers_respects_max_papers():
    """Test that fetch_papers respects max_papers limit"""
    fetcher = ContentFetcher()
    
    urls = [f"http://example.com/paper{i}.pdf" for i in range(10)]
    
    # Mock the _fetch_single_paper method
    fetcher._fetch_single_paper = Mock(return_value={"title": "Paper", "content": "Content"})
    
    results = fetcher.fetch_papers(urls, max_papers=3)
    
    assert fetcher._fetch_single_paper.call_count == 3
    print("[PASS] test_fetch_papers_respects_max_papers passed")


def test_fetch_papers_uses_cache():
    """Test that fetch_papers uses cache for content"""
    cache = Mock()
    cache.get.return_value = {"title": "Cached Paper", "content": "Cached content"}
    
    fetcher = ContentFetcher(cache=cache)
    result = fetcher._fetch_single_paper("http://example.com/paper.pdf")
    
    assert result["title"] == "Cached Paper"
    cache.get.assert_called_once_with("content:http://example.com/paper.pdf")
    print("[PASS] test_fetch_papers_uses_cache passed")


def test_fetch_papers_handles_error():
    """Test that fetch_papers handles errors gracefully"""
    with patch('modules.content_fetcher.requests.post') as mock_post:
        mock_post.side_effect = Exception("Network Error")
        
        cache = Mock()
        cache.get.return_value = None
        
        fetcher = ContentFetcher(cache=cache)
        result = fetcher._fetch_single_paper("http://example.com/paper.pdf")
        
        assert result is None
        print("[PASS] test_fetch_papers_handles_error passed")


if __name__ == "__main__":
    test_fetch_papers_returns_list()
    test_fetch_single_paper_success()
    test_fetch_papers_respects_max_papers()
    test_fetch_papers_uses_cache()
    test_fetch_papers_handles_error()
    print("\n[SUCCESS] All ContentFetcher tests passed!")
