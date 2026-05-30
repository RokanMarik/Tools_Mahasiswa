import os
import json
import tempfile
from core.cache import AnalysisCache


def test_set_and_get_parsed():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = AnalysisCache(cache_dir=tmpdir)
        cache.set_parsed("abc123", {"title": "Test Paper"})
        result = cache.get_parsed("abc123")
        assert result == {"title": "Test Paper"}


def test_get_parsed_missing():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = AnalysisCache(cache_dir=tmpdir)
        result = cache.get_parsed("nonexistent")
        assert result is None


def test_set_and_get_analysis():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = AnalysisCache(cache_dir=tmpdir)
        cache.set_analysis("abc123", "reader", {"summary": "Test"})
        result = cache.get_analysis("abc123", "reader")
        assert result == {"summary": "Test"}


def test_analysis_cache_miss():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = AnalysisCache(cache_dir=tmpdir)
        result = cache.get_analysis("abc123", "reviewer")
        assert result is None


def test_clear_analysis():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = AnalysisCache(cache_dir=tmpdir)
        cache.set_analysis("abc123", "reader", {"summary": "Test"})
        cache.clear_analysis("abc123")
        result = cache.get_analysis("abc123", "reader")
        assert result is None


def test_analysis_cache_ttl_expiration():
    """Verify that analysis cache entries expire after TTL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Use 0-day TTL so entries expire immediately
        cache = AnalysisCache(cache_dir=tmpdir, ttl_days=0)
        cache.set_analysis("abc123", "reader", {"summary": "Test"})
        # Wait a tiny bit to ensure TTL has passed
        import time
        time.sleep(0.01)
        result = cache.get_analysis("abc123", "reader")
        assert result is None


def test_analysis_cache_persistence():
    """Verify cache persists across new instances."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache1 = AnalysisCache(cache_dir=tmpdir)
        cache1.set_parsed("abc123", {"title": "Persistent Paper"})
        cache1.set_analysis("abc123", "reader", {"summary": "Persistent summary"})

        # New instance pointing at same directory
        cache2 = AnalysisCache(cache_dir=tmpdir)
        assert cache2.get_parsed("abc123") == {"title": "Persistent Paper"}
        assert cache2.get_analysis("abc123", "reader") == {"summary": "Persistent summary"}
