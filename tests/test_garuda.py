"""Tests for modules/search/garuda.py"""

import unittest
from unittest.mock import patch, MagicMock
from modules.search.paper_model import Paper


class TestGaruda(unittest.TestCase):

    @patch("modules.search.garuda.requests.get")
    def test_search_returns_papers(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [
                {
                    "title": "Test Paper",
                    "author": "John Smith, Jane Doe",
                    "year": "2024",
                    "journal": "Test Journal",
                    "doi": "10.1234/test",
                    "url": "https://example.com",
                    "abstract": "Test abstract",
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        from modules.search.garuda import search

        papers = search("test", limit=1)
        self.assertEqual(len(papers), 1)
        self.assertIsInstance(papers[0], Paper)
        self.assertEqual(papers[0].title, "Test Paper")
        self.assertEqual(papers[0].source, "garuda")
        self.assertEqual(papers[0].year, 2024)

    @patch("modules.search.garuda.requests.get")
    def test_search_handles_error(self, mock_get):
        import requests
        mock_get.side_effect = requests.RequestException("Connection error")

        from modules.search.garuda import search

        with self.assertRaises(RuntimeError) as ctx:
            search("test")
        self.assertIn("Garuda API error", str(ctx.exception))

    @patch("modules.search.garuda.requests.get")
    def test_search_empty_results(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": []}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        from modules.search.garuda import search

        papers = search("nonexistent")
        self.assertEqual(len(papers), 0)

    @patch("modules.search.garuda.requests.get")
    def test_search_respects_limit(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [{"title": f"Paper {i}", "author": "A", "year": "2024", "journal": "J", "doi": "", "url": "", "abstract": ""} for i in range(10)]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        from modules.search.garuda import search

        papers = search("test", limit=3)
        self.assertEqual(len(papers), 3)


if __name__ == "__main__":
    unittest.main()
