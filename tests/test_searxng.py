"""Tests for modules/search/searxng.py"""

import unittest
from unittest.mock import patch, MagicMock
from modules.search.paper_model import Paper


class TestSearXNG(unittest.TestCase):

    @patch("modules.search.searxng.requests.get")
    def test_search_returns_papers(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [
                {
                    "title": "Test Paper via SearXNG",
                    "url": "https://example.com/paper",
                    "content": "Test abstract content",
                    "engines": ["arxiv"],
                    "publishedDate": "2024-01-15T00:00:00Z",
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        from modules.search.searxng import search

        papers = search("test", limit=1)
        self.assertEqual(len(papers), 1)
        self.assertIsInstance(papers[0], Paper)
        self.assertEqual(papers[0].title, "Test Paper via SearXNG")
        self.assertIn("searxng", papers[0].source)
        self.assertEqual(papers[0].year, 2024)

    @patch("modules.search.searxng.requests.get")
    def test_search_extracts_doi_from_url(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [
                {
                    "title": "Paper with DOI",
                    "url": "https://doi.org/10.1234/test-paper",
                    "content": "",
                    "engines": ["google scholar"],
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        from modules.search.searxng import search

        papers = search("test")
        self.assertEqual(papers[0].doi, "10.1234")

    @patch("modules.search.searxng.requests.get")
    def test_search_handles_error(self, mock_get):
        import requests
        mock_get.side_effect = requests.RequestException("Connection error")

        from modules.search.searxng import search

        with self.assertRaises(RuntimeError) as ctx:
            search("test")
        self.assertIn("SearXNG API error", str(ctx.exception))

    @patch("modules.search.searxng.requests.get")
    def test_search_empty_results(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": []}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        from modules.search.searxng import search

        papers = search("nonexistent")
        self.assertEqual(len(papers), 0)

    @patch("modules.search.searxng.requests.get")
    def test_search_respects_limit(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [
                {"title": f"Paper {i}", "url": f"https://example.com/{i}", "content": "", "engines": ["arxiv"]}
                for i in range(10)
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        from modules.search.searxng import search

        papers = search("test", limit=3)
        self.assertEqual(len(papers), 3)


if __name__ == "__main__":
    unittest.main()
