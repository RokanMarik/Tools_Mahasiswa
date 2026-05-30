"""Tests for modules/search/searxng.py"""

import unittest
import os
from unittest.mock import patch, MagicMock
from modules.search.paper_model import Paper


class TestSearXNG(unittest.TestCase):

    def _mock_requests(self, mock_get, searxng_results=None, ss_results=None, side_effect=None):
        """Helper to mock both SearXNG and Semantic Scholar requests."""
        if side_effect:
            mock_get.side_effect = side_effect
            return

        def side_effect_fn(url, *args, **kwargs):
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            if "searx" in url.lower() or "localhost" in url.lower() or "8888" in url:
                mock_resp.json.return_value = {"results": searxng_results or []}
            else:
                mock_resp.json.return_value = {"data": ss_results or []}
            return mock_resp

        mock_get.side_effect = side_effect_fn

    @patch("modules.search.searxng.requests.get")
    def test_search_returns_papers(self, mock_get):
        self._mock_requests(mock_get, searxng_results=[
            {
                "title": "Test Paper via SearXNG",
                "url": "https://example.com/paper",
                "content": "2024 · Test abstract content",
                "engines": ["arxiv"],
            }
        ])

        os.environ["SEARXNG_URL"] = "http://localhost:8888"
        try:
            from modules.search.searxng import search
            papers = search("test", limit=1)
            self.assertEqual(len(papers), 1)
            self.assertIsInstance(papers[0], Paper)
            self.assertEqual(papers[0].title, "Test Paper via SearXNG")
            self.assertIn("searxng", papers[0].source)
            self.assertEqual(papers[0].year, 2024)
        finally:
            del os.environ["SEARXNG_URL"]

    @patch("modules.search.searxng.requests.get")
    def test_search_extracts_doi_from_url(self, mock_get):
        self._mock_requests(mock_get, searxng_results=[
            {
                "title": "Paper with DOI",
                "url": "https://doi.org/10.1234/test-paper",
                "content": "",
                "engines": ["google scholar"],
            }
        ])

        os.environ["SEARXNG_URL"] = "http://localhost:8888"
        try:
            from modules.search.searxng import search
            papers = search("test")
            self.assertEqual(papers[0].doi, "10.1234")
        finally:
            del os.environ["SEARXNG_URL"]

    @patch("modules.search.searxng.requests.get")
    def test_search_handles_error(self, mock_get):
        import requests
        mock_get.side_effect = requests.RequestException("Connection error")

        os.environ["SEARXNG_URL"] = "http://localhost:8888"
        try:
            from modules.search.searxng import search
            with self.assertRaises(RuntimeError) as ctx:
                search("test")
            self.assertIn("no results", str(ctx.exception).lower())
        finally:
            del os.environ["SEARXNG_URL"]

    @patch("modules.search.searxng.requests.get")
    def test_search_empty_results_raises(self, mock_get):
        self._mock_requests(mock_get, searxng_results=[])

        os.environ["SEARXNG_URL"] = "http://localhost:8888"
        try:
            from modules.search.searxng import search
            with self.assertRaises(RuntimeError):
                search("nonexistent")
        finally:
            del os.environ["SEARXNG_URL"]

    @patch("modules.search.searxng.requests.get")
    def test_search_respects_limit(self, mock_get):
        self._mock_requests(mock_get, searxng_results=[
            {"title": f"Paper {i}", "url": f"https://example.com/{i}", "content": "", "engines": ["arxiv"]}
            for i in range(10)
        ])

        os.environ["SEARXNG_URL"] = "http://localhost:8888"
        try:
            from modules.search.searxng import search
            papers = search("test", limit=3)
            self.assertEqual(len(papers), 3)
        finally:
            del os.environ["SEARXNG_URL"]


if __name__ == "__main__":
    unittest.main()
