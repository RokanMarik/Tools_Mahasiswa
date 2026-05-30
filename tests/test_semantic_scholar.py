"""Tests for modules/search/semantic_scholar.py"""

import unittest
from unittest.mock import patch, MagicMock
from modules.search.paper_model import Paper


class TestSemanticScholar(unittest.TestCase):

    @patch("modules.search.semantic_scholar.requests.get")
    def test_search_returns_papers(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [
                {
                    "title": "Test Paper",
                    "authors": [{"name": "John Smith"}, {"name": "Jane Doe"}],
                    "year": 2024,
                    "venue": "Test Conference",
                    "externalIds": {"DOI": "10.1234/test"},
                    "url": "https://example.com",
                    "abstract": "Test abstract",
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        from modules.search.semantic_scholar import search

        papers = search("test", limit=1)
        self.assertEqual(len(papers), 1)
        self.assertIsInstance(papers[0], Paper)
        self.assertEqual(papers[0].title, "Test Paper")
        self.assertEqual(papers[0].source, "semantic_scholar")

    @patch("modules.search.semantic_scholar.requests.get")
    def test_search_handles_error(self, mock_get):
        import requests
        mock_get.side_effect = requests.RequestException("Connection error")

        from modules.search.semantic_scholar import search

        with self.assertRaises(RuntimeError) as ctx:
            search("test")
        self.assertIn("Semantic Scholar API error", str(ctx.exception))

    @patch("modules.search.semantic_scholar.requests.get")
    def test_search_null_external_ids(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [
                {
                    "title": "Paper without DOI",
                    "authors": [],
                    "year": 2023,
                    "venue": "Some Venue",
                    "externalIds": None,
                    "url": "https://example.com",
                    "abstract": "",
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        from modules.search.semantic_scholar import search

        papers = search("test")
        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0].doi, "")


if __name__ == "__main__":
    unittest.main()
