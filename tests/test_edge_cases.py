"""Edge case and mock tests for journal search modules."""

import unittest
from unittest.mock import patch, MagicMock
from modules.search.paper_model import Paper
from modules.search.scoring import compute_composite_score, sort_papers


class TestScoringEdgeCases(unittest.TestCase):
    """Edge cases for scoring module not covered in test_scoring.py."""

    def test_sort_by_relevance(self):
        """relevance should compute composite scores and sort."""
        papers = [
            Paper(title="A", authors=["A"], year=2020, journal="J",
                  doi="10.1/a", url="", source="test", citation_count=10),
            Paper(title="B", authors=["B"], year=2025, journal="J",
                  doi="10.1/b", url="", source="test", citation_count=100),
        ]
        result = sort_papers(papers, sort_by="relevance")
        # B has higher composite (same citations weight but much newer)
        self.assertEqual(result[0].title, "B")

    def test_sort_by_invalid_raises_value_error(self):
        """Invalid sort_by value should raise ValueError."""
        papers = [
            Paper(title="A", authors=["A"], year=2024, journal="J",
                  doi="10.1/a", url="", source="test"),
        ]
        with self.assertRaises(ValueError):
            sort_papers(papers, sort_by="invalid_sort")

    def test_compute_score_empty_list(self):
        """Empty list should return empty list without error."""
        result = compute_composite_score([])
        self.assertEqual(result, [])

    def test_compute_score_all_same_year(self):
        """All papers same year → year_range=0 → recency=0 for all."""
        papers = [
            Paper(title="A", authors=["A"], year=2023, journal="J",
                  doi="10.1/a", url="", source="test", citation_count=100),
            Paper(title="B", authors=["B"], year=2023, journal="J",
                  doi="10.1/b", url="", source="test", citation_count=10),
        ]
        compute_composite_score(papers)
        # A should score higher due to citations (recency is 0 for both)
        self.assertGreater(papers[0].relevance_score, papers[1].relevance_score)

    def test_compute_score_paper_without_year(self):
        """Paper with None year should get norm_recency=0."""
        papers = [
            Paper(title="NoYear", authors=["A"], year=None, journal="J",
                  doi="10.1/a", url="", source="test", citation_count=100),
            Paper(title="NewLow", authors=["B"], year=2025, journal="J",
                  doi="10.1/b", url="", source="test", citation_count=1),
        ]
        compute_composite_score(papers)
        # NoYear has citations advantage but 0 recency
        # NewLow has low citations but max recency
        # With 0.6/0.4 weights, NoYear should still win
        self.assertGreater(papers[0].relevance_score, papers[1].relevance_score)

    def test_compute_score_single_paper(self):
        """Single paper should get max score (1.0) for both metrics."""
        papers = [
            Paper(title="Solo", authors=["A"], year=2024, journal="J",
                  doi="10.1/a", url="", source="test", citation_count=50),
        ]
        compute_composite_score(papers)
        # Single paper: max_citations=50, year_range=0 → both normalized to... 
        # citations: 50/50=1.0, recency: year_range=0 → norm_recency=0
        self.assertAlmostEqual(papers[0].relevance_score, 0.6, places=2)


class TestOpenAlexMock(unittest.TestCase):
    """Mock tests for OpenAlex that don't hit the real API."""

    @patch("modules.search.openalex.requests.get")
    def test_search_returns_papers(self, mock_get):
        """OpenAlex search should parse results correctly."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [
                {
                    "title": "Test Paper",
                    "doi": "10.1/test",
                    "publication_year": 2024,
                    "cited_by_count": 42,
                    "authorships": [{"author": {"display_name": "Test Author"}}],
                    "primary_location": {
                        "source": {"display_name": "Test Journal"},
                        "pdf_url": "https://example.com/paper.pdf",
                    },
                    "abstract_inverted_index": None,
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        from modules.search.openalex import search

        papers = search("test", limit=1)
        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0].title, "Test Paper")
        self.assertEqual(papers[0].citation_count, 42)
        self.assertEqual(papers[0].year, 2024)
        self.assertEqual(papers[0].source, "openalex")

    @patch("modules.search.openalex.requests.get")
    def test_search_raises_runtime_error_on_failure(self, mock_get):
        """OpenAlex search should raise RuntimeError on API failure."""
        import requests
        mock_get.side_effect = requests.RequestException("API down")

        from modules.search.openalex import search

        with self.assertRaises(RuntimeError):
            search("test", limit=1)

    @patch("modules.search.openalex.requests.get")
    def test_search_empty_results(self, mock_get):
        """OpenAlex search should return empty list for no results."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        from modules.search.openalex import search

        papers = search("nonexistent_topic_xyz", limit=1)
        self.assertEqual(papers, [])

    @patch("modules.search.openalex.requests.get")
    def test_abstract_reconstruction(self, mock_get):
        """OpenAlex should reconstruct abstract from inverted index."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [
                {
                    "title": "Test",
                    "doi": "10.1/test",
                    "publication_year": 2024,
                    "cited_by_count": 0,
                    "authorships": [],
                    "primary_location": {"source": None, "pdf_url": ""},
                    "abstract_inverted_index": {
                        "This": [0],
                        "is": [1],
                        "a": [2],
                        "test": [3],
                        "abstract": [4],
                    },
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        from modules.search.openalex import search

        papers = search("test", limit=1)
        self.assertEqual(papers[0].abstract, "This is a test abstract")


class TestSearXNGMock(unittest.TestCase):
    """Mock tests for SearXNG citation enrichment."""

    @patch("modules.search.searxng.requests.get")
    def test_searxng_enriches_citations(self, mock_get):
        """SearXNG should enrich papers with citation counts from Semantic Scholar."""
        # Mock SearXNG response
        searxng_response = {
            "results": [
                {
                    "title": "Artificial Intelligence in Education Review",
                    "url": "https://example.com/paper",
                    "content": "2023 · AI in education review paper",
                    "engines": ["google scholar"],
                }
            ]
        }
        # Mock Semantic Scholar response
        ss_response = {
            "data": [
                {"title": "Artificial Intelligence in Education Review", "citationCount": 42, "year": 2023}
            ]
        }

        def side_effect(url, *args, **kwargs):
            mock_resp = unittest.mock.MagicMock()
            mock_resp.status_code = 200
            if "searx" in url.lower() or "localhost" in url.lower() or "8888" in url:
                mock_resp.json.return_value = searxng_response
            else:
                mock_resp.json.return_value = ss_response
            return mock_resp

        mock_get.side_effect = side_effect

        import os
        os.environ["SEARXNG_URL"] = "http://localhost:8888"

        from modules.search import searxng

        papers = searxng.search("test", limit=1)
        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0].title, "Artificial Intelligence in Education Review")
        self.assertEqual(papers[0].citation_count, 42)
        self.assertIn("google", papers[0].source)

        del os.environ["SEARXNG_URL"]


class TestAggregatorParallel(unittest.TestCase):
    """Tests for parallel aggregator behavior."""

    @patch("modules.search.aggregator.openalex.search")
    @patch("modules.search.aggregator.garuda.search")
    def test_parallel_search_merges_sources(self, mock_garuda, mock_openalex):
        """Parallel search should merge results from both sources."""
        mock_garuda.return_value = [
            Paper(title="Garuda Paper", authors=["A"], year=2024, journal="J",
                  doi="10.1/g", url="", source="garuda", citation_count=10)
        ]
        mock_openalex.return_value = [
            Paper(title="OpenAlex Paper", authors=["B"], year=2023, journal="J",
                  doi="10.1/o", url="", source="openalex", citation_count=50)
        ]

        from modules.search.aggregator import search

        papers = search("test", total_limit=10)
        self.assertEqual(len(papers), 2)
        sources = {p.source for p in papers}
        self.assertIn("garuda", sources)
        self.assertIn("openalex", sources)

    @patch("modules.search.aggregator.openalex.search")
    @patch("modules.search.aggregator.garuda.search")
    def test_parallel_handles_sort_by(self, mock_garuda, mock_openalex):
        """Parallel search should respect sort_by parameter."""
        mock_garuda.return_value = [
            Paper(title="Old", authors=["A"], year=2020, journal="J",
                  doi="10.1/a", url="", source="garuda", citation_count=10)
        ]
        mock_openalex.return_value = [
            Paper(title="New", authors=["B"], year=2024, journal="J",
                  doi="10.1/b", url="", source="openalex", citation_count=100)
        ]

        from modules.search.aggregator import search

        # Sort by year should put 2024 first
        papers = search("test", total_limit=10, sort_by="year")
        self.assertEqual(papers[0].year, 2024)

        # Sort by citations should put 100 first
        papers = search("test", total_limit=10, sort_by="citations")
        self.assertEqual(papers[0].citation_count, 100)


if __name__ == "__main__":
    unittest.main()
