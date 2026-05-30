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
