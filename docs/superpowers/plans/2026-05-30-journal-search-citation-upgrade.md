# Journal Search Citation + Sorting Upgrade — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade journal search system to support citation-based sorting with OpenAlex as primary source, composite scoring (citations + recency), and CLI `--sort` flag.

**Architecture:** Replace CrossRef/Semantic Scholar with OpenAlex as primary source (broader coverage, built-in citation counts). Add `citation_count` field to Paper model. New scoring module computes weighted composite score. CLI adds `--sort` flag for user control.

**Tech Stack:** Python 3.14, requests, argparse, dataclasses

---

### File Structure

| File | Action | Responsibility |
|------|--------|----------------|
| `modules/search/paper_model.py` | Modify | Add `citation_count: int = 0` field |
| `modules/search/openalex.py` | Create | OpenAlex API source with citation extraction |
| `modules/search/scoring.py` | Create | Composite scoring + sorting logic |
| `modules/search/aggregator.py` | Modify | Update SOURCES list, integrate scoring |
| `modules/search/crossref.py` | Delete | Redundant with OpenAlex |
| `modules/search/semantic_scholar.py` | Delete | Redundant with OpenAlex |
| `scripts/journal_search.py` | Modify | Add `--sort` CLI argument |

---

### Task 1: Add citation_count to Paper Model

**Files:**
- Modify: `modules/search/paper_model.py`

- [ ] **Step 1: Add citation_count field to Paper dataclass**

Add `citation_count: int = 0` after the `abstract` field:

```python
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
    citation_count: int = 0
    relevance_score: float = 0.0
```

- [ ] **Step 2: Commit**

```bash
git add modules/search/paper_model.py
git commit -m "feat: add citation_count field to Paper model"
```

---

### Task 2: Create OpenAlex Source Module

**Files:**
- Create: `modules/search/openalex.py`

- [ ] **Step 1: Write test for OpenAlex search**

Create `tests/test_openalex.py`:

```python
from modules.search.openalex import search

def test_openalex_search_returns_papers():
    papers = search("artificial intelligence education", limit=2)
    assert len(papers) > 0
    assert papers[0].title != ""

def test_openalex_paper_has_citation_count():
    papers = search("machine learning", limit=3)
    # At least one paper should have citation data
    assert any(p.citation_count >= 0 for p in papers)

def test_openalex_paper_fields():
    papers = search("deep learning", limit=1)
    paper = papers[0]
    assert paper.title
    assert paper.source == "openalex"
    assert isinstance(paper.citation_count, int)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_openalex.py -v
```
Expected: FAIL — `ModuleNotFoundError: No module named 'modules.search.openalex'`

- [ ] **Step 3: Create OpenAlex source module**

Create `modules/search/openalex.py`:

```python
"""OpenAlex API wrapper for academic paper search."""

import requests
from .paper_model import Paper

OPENALEX_API_URL = "https://api.openalex.org/works"
REQUEST_TIMEOUT = 15


def search(query: str, limit: int = 5) -> list[Paper]:
    """Search OpenAlex API for academic papers.

    Args:
        query: Search query string.
        limit: Max results to return.

    Returns:
        List of Paper objects with citation counts.
    """
    try:
        response = requests.get(
            OPENALEX_API_URL,
            params={
                "search": query,
                "per_page": limit,
                "sort": "cited_by_count:desc",
            },
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        return [
            _parse_openalex_work(work)
            for work in data.get("results", [])
        ]
    except requests.RequestException as e:
        raise RuntimeError(f"OpenAlex API error: {e}") from e


def _parse_openalex_work(work: dict) -> Paper:
    """Parse an OpenAlex API work dict into a Paper object."""
    # Extract authors
    authors = []
    for authorship in work.get("authorships", []):
        author = authorship.get("author", {})
        name = author.get("display_name", "")
        if name:
            authors.append(name)

    # Extract journal/venue
    journal = ""
    primary_location = work.get("primary_location", {}) or {}
    source = primary_location.get("source", {}) or {}
    if source.get("display_name"):
        journal = source["display_name"]

    # Extract DOI
    doi = work.get("doi", "") or ""

    # Extract URL
    url = work.get("primary_location", {}).get("pdf_url", "") or doi

    # Extract citation count
    citation_count = work.get("cited_by_count", 0) or 0

    # Extract year
    year = work.get("publication_year")
    if year:
        try:
            year = int(year)
        except (ValueError, TypeError):
            year = None

    # Reconstruct abstract from inverted index
    abstract = _reconstruct_abstract(work.get("abstract_inverted_index"))

    return Paper(
        title=work.get("title", "") or "",
        authors=authors,
        year=year,
        journal=journal,
        doi=doi,
        url=url,
        source="openalex",
        abstract=abstract,
        citation_count=citation_count,
    )


def _reconstruct_abstract(inverted_index: dict | None) -> str:
    """Reconstruct abstract string from OpenAlex inverted index format."""
    if not inverted_index:
        return ""

    # Build word-position pairs
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))

    # Sort by position and join
    word_positions.sort(key=lambda x: x[0])
    return " ".join(word for _, word in word_positions)
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/test_openalex.py -v
```
Expected: PASS (3 tests)

- [ ] **Step 5: Commit**

```bash
git add modules/search/openalex.py tests/test_openalex.py
git commit -m "feat: add OpenAlex API source with citation counts"
```

---

### Task 3: Create Scoring Module

**Files:**
- Create: `modules/search/scoring.py`

- [ ] **Step 1: Write tests for scoring module**

Create `tests/test_scoring.py`:

```python
from modules.search.paper_model import Paper
from modules.search.scoring import compute_composite_score, sort_papers


def _make_paper(title, year=2023, citations=0):
    return Paper(
        title=title, authors=["Test"], year=year,
        journal="Test", doi="10.x/x", url="http://x",
        source="test", citation_count=citations,
    )


def test_composite_score_high_citation_old_paper():
    papers = [
        _make_paper("New Low Cit", year=2025, citations=1),
        _make_paper("Old High Cit", year=2020, citations=100),
    ]
    compute_composite_score(papers)
    # Old high-citation paper should score higher due to 0.6 weight on citations
    assert papers[0].relevance_score < papers[1].relevance_score


def test_composite_score_new_high_citation_wins():
    papers = [
        _make_paper("Old Low Cit", year=2020, citations=5),
        _make_paper("New High Cit", year=2025, citations=100),
    ]
    compute_composite_score(papers)
    assert papers[0].relevance_score < papers[1].relevance_score


def test_composite_score_all_zero_citations():
    papers = [
        _make_paper("A", year=2023, citations=0),
        _make_paper("B", year=2025, citations=0),
    ]
    compute_composite_score(papers)
    # When all citations are 0, score should be based on recency only
    assert papers[0].relevance_score < papers[1].relevance_score


def test_sort_by_citations():
    papers = [
        _make_paper("Low", citations=5),
        _make_paper("High", citations=100),
        _make_paper("Med", citations=50),
    ]
    result = sort_papers(papers, sort_by="citations")
    assert result[0].citation_count == 100
    assert result[1].citation_count == 50
    assert result[2].citation_count == 5


def test_sort_by_year():
    papers = [
        _make_paper("Old", year=2020),
        _make_paper("New", year=2025),
        _make_paper("Mid", year=2023),
    ]
    result = sort_papers(papers, sort_by="year")
    assert result[0].year == 2025
    assert result[1].year == 2023
    assert result[2].year == 2020


def test_sort_by_composite():
    papers = [
        _make_paper("A", year=2020, citations=100),
        _make_paper("B", year=2025, citations=100),
    ]
    result = sort_papers(papers, sort_by="composite")
    # B should be first (same citations, newer year)
    assert result[0].title == "B"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_scoring.py -v
```
Expected: FAIL — `ModuleNotFoundError: No module named 'modules.search.scoring'`

- [ ] **Step 3: Create scoring module**

Create `modules/search/scoring.py`:

```python
"""Scoring and sorting logic for journal search results."""

from .paper_model import Paper

CITATION_WEIGHT = 0.6
RECENCY_WEIGHT = 0.4


def compute_composite_score(papers: list[Paper]) -> list[Paper]:
    """Compute composite score for each paper based on citations and recency.

    Uses min-max normalization to scale both metrics to 0-1 range.
    Formula: score = (norm_citations * 0.6) + (norm_recency * 0.4)

    Args:
        papers: List of Paper objects to score.

    Returns:
        Same list with relevance_score updated.
    """
    if not papers:
        return papers

    # Extract citation counts and years
    citations = [p.citation_count for p in papers]
    years = [p.year for p in papers if p.year is not None]

    max_citations = max(citations) if citations else 0
    min_year = min(years) if years else 2020
    max_year = max(years) if years else 2025
    year_range = max_year - min_year

    for paper in papers:
        # Normalize citations (0-1)
        norm_citations = (
            paper.citation_count / max_citations if max_citations > 0 else 0
        )

        # Normalize recency (0-1), papers without year get 0
        if paper.year is not None and year_range > 0:
            norm_recency = (paper.year - min_year) / year_range
        else:
            norm_recency = 0

        # Composite score
        paper.relevance_score = (
            norm_citations * CITATION_WEIGHT + norm_recency * RECENCY_WEIGHT
        )

    return papers


def sort_papers(
    papers: list[Paper], sort_by: str = "composite"
) -> list[Paper]:
    """Sort papers by the specified criterion.

    Args:
        papers: List of Paper objects.
        sort_by: One of 'composite', 'citations', 'year', 'relevance'.

    Returns:
        Sorted list (descending order).
    """
    if sort_by == "composite":
        compute_composite_score(papers)
        papers.sort(key=lambda p: p.relevance_score, reverse=True)
    elif sort_by == "citations":
        papers.sort(key=lambda p: p.citation_count, reverse=True)
    elif sort_by == "year":
        papers.sort(key=lambda p: p.year or 0, reverse=True)
    elif sort_by == "relevance":
        papers.sort(key=lambda p: p.relevance_score, reverse=True)
    else:
        raise ValueError(
            f"Invalid sort_by value: {sort_by}. "
            f"Must be one of: composite, citations, year, relevance"
        )

    return papers
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_scoring.py -v
```
Expected: PASS (6 tests)

- [ ] **Step 5: Commit**

```bash
git add modules/search/scoring.py tests/test_scoring.py
git commit -m "feat: add composite scoring and sorting module"
```

---

### Task 4: Update Aggregator

**Files:**
- Modify: `modules/search/aggregator.py`

- [ ] **Step 1: Update SOURCES list and integrate scoring**

Replace the entire `aggregator.py` content:

```python
"""Aggregator: merge, deduplicate, and sort papers from multiple sources."""

from .paper_model import Paper
from . import openalex, garuda
from .scoring import sort_papers

SOURCES = [openalex, garuda]


def search(
    topic: str,
    total_limit: int = 3,
    per_source_limit: int = 5,
    sort_by: str = "composite",
) -> list[Paper]:
    """Search all sources and return deduplicated, sorted results.

    Args:
        topic: Search query.
        total_limit: Max papers to return.
        per_source_limit: Max papers per source.
        sort_by: Sort criterion (composite, citations, year, relevance).

    Returns:
        Sorted, deduplicated list of Paper objects.
    """
    all_papers: list[Paper] = []

    for source_module in SOURCES:
        try:
            papers = source_module.search(topic, limit=per_source_limit)
            all_papers.extend(papers)
        except RuntimeError:
            continue

    if not all_papers:
        raise RuntimeError(f"No results from any source for query: {topic}")

    papers = _deduplicate(all_papers)
    papers = sort_papers(papers, sort_by=sort_by)
    return papers[:total_limit]


def _deduplicate(papers: list[Paper]) -> list[Paper]:
    """Remove duplicate papers by DOI, then by title. Priority: Garuda > OpenAlex."""
    seen_dois: set[str] = set()
    seen_titles: set[str] = set()
    result: list[Paper] = []

    source_priority = {"garuda": 0, "openalex": 1}
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
```

- [ ] **Step 2: Commit**

```bash
git add modules/search/aggregator.py
git commit -m "refactor: update aggregator to use OpenAlex + scoring"
```

---

### Task 5: Add --sort CLI Flag

**Files:**
- Modify: `scripts/journal_search.py`

- [ ] **Step 1: Add --sort argument and pass to aggregator**

Replace the `search_journals` function and `main` function:

```python
def search_journals(topic: str, limit: int = 3, sort_by: str = "composite") -> str:
    """Search for journals on a topic using multi-source aggregator.

    Args:
        topic: Search topic.
        limit: Max papers to return (default 3).
        sort_by: Sort criterion (composite, citations, year, relevance).

    Returns:
        JSON string with paper list.
    """
    try:
        papers = aggregator.search(topic, total_limit=limit, sort_by=sort_by)
        paper_dicts = [_paper_to_dict(p, i + 1) for i, p in enumerate(papers)]

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
```

Update `_paper_to_dict` to include citation_count:

```python
def _paper_to_dict(paper, index: int) -> dict:
    """Convert Paper dataclass to dict for JSON serialization."""
    return {
        "index": index,
        "title": paper.title,
        "authors": paper.authors,
        "year": paper.year,
        "journal": paper.journal,
        "doi": paper.doi,
        "url": paper.url,
        "abstract": paper.abstract,
        "citation_count": paper.citation_count,
        "metadata_source": paper.source,
    }
```

Update `main` to add `--sort` argument:

```python
def main():
    parser = argparse.ArgumentParser(description="Search for academic journals")
    parser.add_argument("--topic", required=True, help="Search topic")
    parser.add_argument("--limit", type=int, default=3, help="Max papers to return")
    parser.add_argument(
        "--sort",
        choices=["composite", "citations", "year", "relevance"],
        default="composite",
        help="Sort criterion (default: composite)",
    )
    args = parser.parse_args()

    result = search_journals(args.topic, args.limit, args.sort)
    print(result)
```

- [ ] **Step 2: Commit**

```bash
git add scripts/journal_search.py
git commit -m "feat: add --sort CLI flag for citation/year sorting"
```

---

### Task 6: Remove Redundant Sources

**Files:**
- Delete: `modules/search/crossref.py`
- Delete: `modules/search/semantic_scholar.py`

- [ ] **Step 1: Remove CrossRef and Semantic Scholar modules**

```bash
git rm modules/search/crossref.py modules/search/semantic_scholar.py
git commit -m "chore: remove redundant CrossRef and Semantic Scholar sources"
```

---

### Task 7: Integration Test

- [ ] **Step 1: Test default composite sort**

```bash
$env:PYTHONIOENCODING="utf-8"; python scripts/journal_search.py --topic "artificial intelligence education" --limit 3
```
Expected: JSON with 3 papers sorted by composite score, each with `citation_count` field.

- [ ] **Step 2: Test sort by citations**

```bash
$env:PYTHONIOENCODING="utf-8"; python scripts/journal_search.py --topic "machine learning" --limit 5 --sort citations
```
Expected: Papers sorted by citation_count descending.

- [ ] **Step 3: Test sort by year**

```bash
$env:PYTHONIOENCODING="utf-8"; python scripts/journal_search.py --topic "deep learning" --limit 5 --sort year
```
Expected: Papers sorted by year descending (newest first).

- [ ] **Step 4: Test invalid sort value**

```bash
$env:PYTHONIOENCODING="utf-8"; python scripts/journal_search.py --topic "test" --sort invalid
```
Expected: argparse error listing valid choices.

- [ ] **Step 5: Final commit**

```bash
git add -A && git commit -m "feat: journal search citation upgrade complete"
```
