# Multi-Source Journal Search Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Extend journal search to aggregate results from Garuda, CrossRef, and Semantic Scholar APIs into a single deduplicated list.

**Architecture:** Modular search modules under `modules/search/`, aggregator for merge/dedup/sort, updated journal_search.py as CLI entry point.

**Tech Stack:** Python 3.14, requests, dataclasses, existing modules pattern.

---

## File Map

| File | Action | Responsibility |
|------|--------|----------------|
| `modules/search/__init__.py` | Create | Package init |
| `modules/search/paper_model.py` | Create | Paper dataclass |
| `modules/search/garuda.py` | Create | Garuda API wrapper |
| `modules/search/crossref.py` | Create | CrossRef API wrapper |
| `modules/search/semantic_scholar.py` | Create | Semantic Scholar API wrapper |
| `modules/search/aggregator.py` | Create | Merge + dedup + sort |
| `scripts/journal_search.py` | Modify | Use aggregator |
| `tests/test_garuda.py` | Create | Garuda tests |
| `tests/test_crossref.py` | Create | CrossRef tests |
| `tests/test_semantic_scholar.py` | Create | Semantic Scholar tests |
| `tests/test_aggregator.py` | Create | Aggregator tests |
| `tests/test_journal_search.py` | Modify | Update integration tests |

---

### Task 1: Paper Model + Garuda Module

**Files:**
- Create: `modules/search/__init__.py`
- Create: `modules/search/paper_model.py`
- Create: `modules/search/garuda.py`
- Test: `tests/test_garuda.py`

- [ ] **Step 1: Create `modules/search/paper_model.py`**

```python
"""Paper data model for multi-source journal search."""

from dataclasses import dataclass, field


@dataclass
class Paper:
    title: str
    authors: list[str]
    year: int | None
    journal: str
    doi: str
    url: str
    source: str
    abstract: str = ""
    relevance_score: float = 0.0
```

- [ ] **Step 2: Create `modules/search/garuda.py`**

```python
"""Garuda Ristekbrin API wrapper."""

import requests
from .paper_model import Paper

GARUDA_API_URL = "https://garuda.ristekbrin.go.id/api/v1/documents"
REQUEST_TIMEOUT = 10


def search(query: str, limit: int = 5) -> list[Paper]:
    """Search Garuda API for academic documents.

    Args:
        query: Search query string.
        limit: Max results to return.

    Returns:
        List of Paper objects from Garuda.
    """
    try:
        response = requests.get(
            GARUDA_API_URL,
            params={"q": query, "format": "json"},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        return [_parse_garuda_doc(doc) for doc in data.get("data", [])[:limit]]
    except requests.RequestException as e:
        raise RuntimeError(f"Garuda API error: {e}") from e


def _parse_garuda_doc(doc: dict) -> Paper:
    """Parse a Garuda API document dict into a Paper object."""
    authors = []
    if doc.get("author"):
        authors = [a.strip() for a in doc["author"].split(",") if a.strip()]
    year = None
    if doc.get("year"):
        try:
            year = int(doc["year"])
        except (ValueError, TypeError):
            pass
    return Paper(
        title=doc.get("title", ""),
        authors=authors,
        year=year,
        journal=doc.get("journal", ""),
        doi=doc.get("doi", ""),
        url=doc.get("url", ""),
        source="garuda",
        abstract=doc.get("abstract", ""),
    )
```

- [ ] **Step 3: Create `tests/test_garuda.py`**

```python
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
```

- [ ] **Step 4: Create `modules/search/__init__.py`**

```python
"""Multi-source journal search modules."""
```

- [ ] **Step 5: Run tests**

Run: `pytest tests/test_garuda.py -v`
Expected: All tests PASS

- [ ] **Step 6: Commit**

```bash
git add modules/search/__init__.py modules/search/paper_model.py modules/search/garuda.py tests/test_garuda.py
git commit -m "feat: add paper model and garuda search module"
```

---

### Task 2: CrossRef Module

**Files:**
- Create: `modules/search/crossref.py`
- Test: `tests/test_crossref.py`

- [ ] **Step 1: Create `modules/search/crossref.py`**

```python
"""CrossRef API wrapper."""

import requests
from .paper_model import Paper

CROSSREF_API_URL = "https://api.crossref.org/works"
REQUEST_TIMEOUT = 10


def search(query: str, limit: int = 5) -> list[Paper]:
    """Search CrossRef API for academic works.

    Args:
        query: Search query string.
        limit: Max results to return.

    Returns:
        List of Paper objects from CrossRef.
    """
    try:
        response = requests.get(
            CROSSREF_API_URL,
            params={
                "query": query,
                "select": "title,author,DOI,url,published,container-title",
                "rows": limit,
            },
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        return [_parse_crossref_item(item) for item in data.get("message", {}).get("item", [])]
    except requests.RequestException as e:
        raise RuntimeError(f"CrossRef API error: {e}") from e


def _parse_crossref_item(item: dict) -> Paper:
    """Parse a CrossRef API item dict into a Paper object."""
    title = ""
    if item.get("title"):
        title = item["title"][0] if isinstance(item["title"], list) else item["title"]

    authors = []
    for author in item.get("author", []):
        name_parts = []
        if author.get("given"):
            name_parts.append(author["given"])
        if author.get("family"):
            name_parts.append(author["family"])
        if name_parts:
            authors.append(" ".join(name_parts))

    year = None
    published = item.get("published", {})
    date_parts = published.get("date-parts", [])
    if date_parts and date_parts[0]:
        try:
            year = int(date_parts[0][0])
        except (ValueError, IndexError, TypeError):
            pass

    return Paper(
        title=title,
        authors=authors,
        year=year,
        journal=item.get("container-title", [""])[0] if item.get("container-title") else "",
        doi=item.get("DOI", ""),
        url=item.get("URL", ""),
        source="crossref",
    )
```

- [ ] **Step 2: Create `tests/test_crossref.py`**

```python
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
```

- [ ] **Step 3: Run tests**

Run: `pytest tests/test_crossref.py -v`

- [ ] **Step 4: Commit**

```bash
git add modules/search/crossref.py tests/test_crossref.py
git commit -m "feat: add crossref search module"
```

---

### Task 3: Semantic Scholar Module

**Files:**
- Create: `modules/search/semantic_scholar.py`
- Test: `tests/test_semantic_scholar.py`

- [ ] **Step 1: Create `modules/search/semantic_scholar.py`**

```python
"""Semantic Scholar API wrapper."""

import requests
from .paper_model import Paper

SEMANTIC_SCHOLAR_API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
REQUEST_TIMEOUT = 10


def search(query: str, limit: int = 5) -> list[Paper]:
    """Search Semantic Scholar API for papers.

    Args:
        query: Search query string.
        limit: Max results to return.

    Returns:
        List of Paper objects from Semantic Scholar.
    """
    try:
        response = requests.get(
            SEMANTIC_SCHOLAR_API_URL,
            params={
                "query": query,
                "fields": "title,authors,year,venue,externalIds,url,abstract",
                "limit": limit,
            },
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        return [_parse_ss_paper(paper) for paper in data.get("data", [])]
    except requests.RequestException as e:
        raise RuntimeError(f"Semantic Scholar API error: {e}") from e


def _parse_ss_paper(paper: dict) -> Paper:
    """Parse a Semantic Scholar API paper dict into a Paper object."""
    authors = []
    for author in paper.get("authors", []):
        if author.get("name"):
            authors.append(author["name"])

    external_ids = paper.get("externalIds", {}) or {}
    doi = external_ids.get("DOI", "")

    return Paper(
        title=paper.get("title", ""),
        authors=authors,
        year=paper.get("year"),
        journal=paper.get("venue", ""),
        doi=doi,
        url=paper.get("url", ""),
        source="semantic_scholar",
        abstract=paper.get("abstract", ""),
    )
```

- [ ] **Step 2: Create `tests/test_semantic_scholar.py`**

```python
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
        self.assertEqual(papers[0].year, 2024)

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
        """Handle papers with null externalIds."""
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
```

- [ ] **Step 3: Run tests**

Run: `pytest tests/test_semantic_scholar.py -v`

- [ ] **Step 4: Commit**

```bash
git add modules/search/semantic_scholar.py tests/test_semantic_scholar.py
git commit -m "feat: add semantic scholar search module"
```

---

### Task 4: Aggregator Module

**Files:**
- Create: `modules/search/aggregator.py`
- Test: `tests/test_aggregator.py`

- [ ] **Step 1: Create `modules/search/aggregator.py`**

```python
"""Aggregator: merge, deduplicate, and sort papers from multiple sources."""

from .paper_model import Paper
from . import garuda, crossref, semantic_scholar

SOURCES = [garuda, crossref, semantic_scholar]
REQUEST_TIMEOUT = 10


def search(topic: str, total_limit: int = 3, per_source_limit: int = 5) -> list[Paper]:
    """Search all sources and return deduplicated, sorted results.

    Args:
        topic: Search query.
        total_limit: Max papers to return overall.
        per_source_limit: Max papers per source.

    Returns:
        List of unique Paper objects, sorted by relevance.
    """
    all_papers: list[Paper] = []

    for source_module in SOURCES:
        try:
            papers = source_module.search(topic, limit=per_source_limit)
            all_papers.extend(papers)
        except RuntimeError:
            # Source failed, skip silently and try next
            continue

    if not all_papers:
        raise RuntimeError(f"No results from any source for query: {topic}")

    papers = _deduplicate(all_papers)
    papers = _sort_and_score(papers, topic)
    return papers[:total_limit]


def _deduplicate(papers: list[Paper]) -> list[Paper]:
    """Remove duplicate papers by DOI, then by title.

    Priority: Garuda > CrossRef > Semantic Scholar.
    """
    seen_dois: set[str] = set()
    seen_titles: set[str] = set()
    result: list[Paper] = []

    # Sort so Garuda comes first (higher priority)
    source_priority = {"garuda": 0, "crossref": 1, "semantic_scholar": 2}
    papers.sort(key=lambda p: source_priority.get(p.source, 99))

    for paper in papers:
        doi_key = paper.doi.lower().strip() if paper.doi else ""
        title_key = paper.title.lower().strip() if paper.title else ""

        if doi_key and doi_key in seen_dois:
            continue
        if title_key and not doi_key and title_key in seen_titles:
            continue

        if doi_key:
            seen_dois.add(doi_key)
        if title_key:
            seen_titles.add(title_key)

        result.append(paper)

    return result


def _sort_and_score(papers: list[Paper], topic: str) -> list[Paper]:
    """Score and sort papers by relevance.

    Scoring:
    - Has DOI: +1
    - Has authors: +1
    - Has year: +1
    - Year is recent (within 5 years): +1
    - Topic words in title: +1 per match
    - Garuda source: +0.5 (user preference for Indonesian content)
    """
    topic_words = set(topic.lower().split())

    for paper in papers:
        score = 0.0
        if paper.doi:
            score += 1
        if paper.authors:
            score += 1
        if paper.year:
            score += 1
            if paper.year >= 2021:
                score += 1
        if paper.title:
            title_words = set(paper.title.lower().split())
            score += len(topic_words & title_words)
        if paper.source == "garuda":
            score += 0.5
        paper.relevance_score = score

    papers.sort(key=lambda p: p.relevance_score, reverse=True)
    return papers
```

- [ ] **Step 2: Create `tests/test_aggregator.py`**

```python
"""Tests for modules/search/aggregator.py"""

import unittest
from unittest.mock import patch, MagicMock
from modules.search.paper_model import Paper


class TestAggregator(unittest.TestCase):

    @patch("modules.search.aggregator.semantic_scholar.search")
    @patch("modules.search.aggregator.crossref.search")
    @patch("modules.search.aggregator.garuda.search")
    def test_search_merges_sources(self, mock_garuda, mock_crossref, mock_ss):
        """Should merge results from all sources."""
        mock_garuda.return_value = [
            Paper(title="Garuda Paper", authors=["A"], year=2024, journal="J", doi="", url="", source="garuda")
        ]
        mock_crossref.return_value = [
            Paper(title="CrossRef Paper", authors=["B"], year=2023, journal="J", doi="10.1/x", url="", source="crossref")
        ]
        mock_ss.return_value = [
            Paper(title="SS Paper", authors=["C"], year=2022, journal="J", doi="10.2/y", url="", source="semantic_scholar")
        ]

        from modules.search.aggregator import search

        papers = search("test", total_limit=10)
        self.assertEqual(len(papers), 3)
        sources = {p.source for p in papers}
        self.assertIn("garuda", sources)
        self.assertIn("crossref", sources)
        self.assertIn("semantic_scholar", sources)

    @patch("modules.search.aggregator.semantic_scholar.search")
    @patch("modules.search.aggregator.crossref.search")
    @patch("modules.search.aggregator.garuda.search")
    def test_search_deduplicates_by_doi(self, mock_garuda, mock_crossref, mock_ss):
        """Same DOI should result in one paper."""
        mock_garuda.return_value = [
            Paper(title="Same Paper", authors=["A"], year=2024, journal="J", doi="10.1/dup", url="url1", source="garuda")
        ]
        mock_crossref.return_value = [
            Paper(title="Same Paper", authors=["B"], year=2024, journal="J", doi="10.1/dup", url="url2", source="crossref")
        ]
        mock_ss.return_value = []

        from modules.search.aggregator import search

        papers = search("test", total_limit=10)
        self.assertEqual(len(papers), 1)
        # Garuda version should be kept (higher priority)
        self.assertEqual(papers[0].source, "garuda")

    @patch("modules.search.aggregator.semantic_scholar.search")
    @patch("modules.search.aggregator.crossref.search")
    @patch("modules.search.aggregator.garuda.search")
    def test_search_handles_source_failure(self, mock_garuda, mock_crossref, mock_ss):
        """If one source fails, others should still work."""
        import requests
        mock_garuda.side_effect = RuntimeError("Garuda down")
        mock_crossref.return_value = [
            Paper(title="CrossRef Paper", authors=["A"], year=2024, journal="J", doi="10.1/x", url="", source="crossref")
        ]
        mock_ss.return_value = [
            Paper(title="SS Paper", authors=["B"], year=2023, journal="J", doi="10.2/y", url="", source="semantic_scholar")
        ]

        from modules.search.aggregator import search

        papers = search("test", total_limit=10)
        self.assertEqual(len(papers), 2)

    @patch("modules.search.aggregator.semantic_scholar.search")
    @patch("modules.search.aggregator.crossref.search")
    @patch("modules.search.aggregator.garuda.search")
    def test_search_raises_when_all_fail(self, mock_garuda, mock_crossref, mock_ss):
        """Should raise if all sources fail."""
        mock_garuda.side_effect = RuntimeError("Down")
        mock_crossref.side_effect = RuntimeError("Down")
        mock_ss.side_effect = RuntimeError("Down")

        from modules.search.aggregator import search

        with self.assertRaises(RuntimeError):
            search("test")

    @patch("modules.search.aggregator.semantic_scholar.search")
    @patch("modules.search.aggregator.crossref.search")
    @patch("modules.search.aggregator.garuda.search")
    def test_search_respects_total_limit(self, mock_garuda, mock_crossref, mock_ss):
        """Should truncate to total_limit."""
        mock_garuda.return_value = [
            Paper(title=f"Garuda {i}", authors=["A"], year=2024, journal="J", doi=f"10.1/g{i}", url="", source="garuda")
            for i in range(5)
        ]
        mock_crossref.return_value = []
        mock_ss.return_value = []

        from modules.search.aggregator import search

        papers = search("test", total_limit=3)
        self.assertEqual(len(papers), 3)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run tests**

Run: `pytest tests/test_aggregator.py -v`

- [ ] **Step 4: Commit**

```bash
git add modules/search/aggregator.py tests/test_aggregator.py
git commit -m "feat: add aggregator module with dedup and scoring"
```

---

### Task 5: Integrate with journal_search.py

**Files:**
- Modify: `scripts/journal_search.py`
- Modify: `tests/test_journal_search.py`

- [ ] **Step 1: Modify `scripts/journal_search.py`**

Replace the `_parse_journal_response` function and update `search_journals()` to use the aggregator:

```python
#!/usr/bin/env python3
"""Journal search wrapper script.

Usage:
    python scripts/journal_search.py --topic "machine learning" [--limit 3]

Output: JSON to stdout with paper list.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.search import aggregator


def search_journals(topic: str, limit: int = 3) -> str:
    """Search for journals on a topic using multi-source aggregator.

    Args:
        topic: Search topic.
        limit: Max papers to return (default 3).

    Returns:
        JSON string with paper list.
    """
    try:
        papers = aggregator.search(topic, total_limit=limit)
        paper_dicts = [_paper_to_dict(p) for p in papers]

        return json.dumps({
            "status": "success",
            "query": topic,
            "papers": paper_dicts,
            "error": None,
        }, ensure_ascii=False)

    except RuntimeError as e:
        return json.dumps({
            "status": "error",
            "query": topic,
            "papers": [],
            "error": str(e),
        }, ensure_ascii=False)


def _paper_to_dict(paper) -> dict:
    """Convert Paper dataclass to dict for JSON serialization."""
    return {
        "index": 0,  # Will be set by caller
        "title": paper.title,
        "authors": paper.authors,
        "year": paper.year,
        "journal": paper.journal,
        "doi": paper.doi,
        "url": paper.url,
        "abstract": paper.abstract,
        "metadata_source": paper.source,
    }


def main():
    parser = argparse.ArgumentParser(description="Search for academic journals")
    parser.add_argument("--topic", required=True, help="Search topic")
    parser.add_argument("--limit", type=int, default=3, help="Max papers to return")
    args = parser.parse_args()

    result = search_journals(args.topic, args.limit)
    # Add index numbers
    data = json.loads(result)
    if data["status"] == "success":
        for i, paper in enumerate(data["papers"]):
            paper["index"] = i + 1
    print(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Update `tests/test_journal_search.py`**

Update tests to work with the new aggregator-based implementation. Replace the `@patch("scripts.journal_search.JournalFinder")` mocks with `@patch("modules.search.aggregator.search")`.

- [ ] **Step 3: Run ALL tests**

Run: `pytest tests/ -v`
Expected: ALL tests PASS (existing + new)

- [ ] **Step 4: Commit**

```bash
git add scripts/journal_search.py tests/test_journal_search.py
git commit -m "feat: integrate multi-source aggregator into journal_search"
```

---

### Task 6: Update SKILL.md and spec

**Files:**
- Modify: `.opencode/skills/journal-finder/SKILL.md`
- Modify: `.opencode/skills/journal-workflow/SKILL.md`

- [ ] **Step 1: Update journal-finder SKILL.md**

Add note about multi-source search: "Searches Garuda (Indonesia), CrossRef (global), and Semantic Scholar (global) APIs simultaneously."

- [ ] **Step 2: Commit**

```bash
git add .opencode/skills/journal-finder/SKILL.md .opencode/skills/journal-workflow/SKILL.md
git commit -m "docs: update skills with multi-source search info"
```

---

## Self-Review

- [ ] **Spec coverage:** All requirements from multi-source-search-design.md covered?
  - ✅ Garuda module → Task 1
  - ✅ CrossRef module → Task 2
  - ✅ Semantic Scholar module → Task 3
  - ✅ Aggregator (merge + dedup + sort) → Task 4
  - ✅ journal_search.py updated → Task 5
  - ✅ Tests for all modules → Tasks 1-5
  - ✅ SKILL.md updated → Task 6

- [ ] **No placeholders:** All code is explicit, no TBD/TODO

- [ ] **Type consistency:** Paper dataclass used consistently across all modules
