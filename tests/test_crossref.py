"""Tests for modules/search/crossref.py"""

import unittest
from unittest.mock import patch, MagicMock
from modules.search.paper_model import Paper


class TestCrossRef(unittest.TestCase):

    @patch("modules.search.crossref.requests.get")
    def test_search_returns_papers(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "message": {
                "item": [
                    {
                        "title": ["Test Paper Title"],
                        "author": [{"given": "John", "family": "Smith"}],
                        "DOI": "10.1234/test",
                        "URL": "https://example.com/test",
                        "published": {"date-parts": [[2024, 1, 15]]},
                        "container-title": ["Test Journal"],
                    }
                ]
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        from modules.search.crossref import search

        papers = search("test", limit=1)
        self.assertEqual(len(papers), 1)
        self.assertIsInstance(papers[0], Paper)
        self.assertEqual(papers[0].title, "Test Paper Title")
        self.assertEqual(papers[0].source, "crossref")
        self.assertEqual(papers[0].year, 2024)

    @patch("modules.search.crossref.requests.get")
    def test_search_handles_error(self, mock_get):
        import requests
        mock_get.side_effect = requests.RequestException("Connection error")

        from modules.search.crossref import search

        with self.assertRaises(RuntimeError) as ctx:
            search("test")
        self.assertIn("CrossRef API error", str(ctx.exception))

    @patch("modules.search.crossref.requests.get")
    def test_search_missing_fields(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "message": {
                "item": [
                    {"title": ["Minimal Paper"]}
                ]
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        from modules.search.crossref import search

        papers = search("test")
        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0].title, "Minimal Paper")
        self.assertEqual(papers[0].authors, [])
        self.assertIsNone(papers[0].year)


if __name__ == "__main__":
    unittest.main()
