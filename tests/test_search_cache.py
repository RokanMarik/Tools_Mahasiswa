import os
import json
import tempfile
import sys

# Add parent directory to path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.search_cache import SearchCache


def test_cache_initialization():
    """Test that cache initializes with empty dict"""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_file = os.path.join(tmpdir, "cache.json")
        cache = SearchCache(cache_file)
        assert cache.cache == {}
        print("[PASS] test_cache_initialization passed")


def test_cache_set_and_get():
    """Test setting and getting cache"""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_file = os.path.join(tmpdir, "cache.json")
        cache = SearchCache(cache_file)
        
        test_results = [{"title": "Paper 1", "url": "http://example.com"}]
        cache.set("test query", test_results)
        
        retrieved = cache.get("test query")
        assert retrieved == test_results
        print("[PASS] test_cache_set_and_get passed")


def test_cache_persistence():
    """Test that cache persists to file"""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_file = os.path.join(tmpdir, "cache.json")
        
        # Create and populate cache
        cache1 = SearchCache(cache_file)
        test_results = [{"title": "Paper 1"}]
        cache1.set("query1", test_results)
        
        # Create new cache instance and verify data persists
        cache2 = SearchCache(cache_file)
        assert cache2.get("query1") == test_results
        print("[PASS] test_cache_persistence passed")


def test_cache_clear():
    """Test clearing cache"""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache_file = os.path.join(tmpdir, "cache.json")
        cache = SearchCache(cache_file)
        cache.set("query1", [{"title": "Paper"}])
        cache.clear()
        assert cache.get("query1") is None
        print("[PASS] test_cache_clear passed")


if __name__ == "__main__":
    test_cache_initialization()
    test_cache_set_and_get()
    test_cache_persistence()
    test_cache_clear()
    print("\n[SUCCESS] All SearchCache tests passed!")
