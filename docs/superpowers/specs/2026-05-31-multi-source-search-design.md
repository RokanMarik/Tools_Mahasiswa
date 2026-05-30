# Multi-Source Journal Search Enhancement

**Date:** 2026-05-31
**Status:** Approved
**Type:** Feature Enhancement (extends existing journal_search.py)

---

## Overview

Extend journal search to aggregate results from 3 free sources (Garuda, CrossRef, Semantic Scholar), combining Indonesian and international journals into a single deduplicated, relevance-sorted list. No Docker needed — all sources are free REST APIs requiring no authentication.

---

## Architecture

### New Files

```
modules/search/
├── __init__.py
├── paper_model.py         ← Paper dataclass
├── garuda.py              ← Garuda Ristek API
├── crossref.py            ← CrossRef API
├── semantic_scholar.py    ← Semantic Scholar API
├── aggregator.py          ← Merge + dedup + sort
tests/
├── test_garuda.py
├── test_crossref.py
├── test_semantic_scholar.py
├── test_aggregator.py
```

### Modified Files

- `scripts/journal_search.py` — import aggregator, keep same CLI interface

### Existing Files (reused, not modified)

- `9router_journal_finder.py` — JournalFinder class (still used for AI-modeled search)

---

## Paper Model

```python
@dataclass
class Paper:
    title: str
    authors: list[str]
    year: int | None
    journal: str
    doi: str
    url: str
    source: str  # "garuda", "crossref", "semantic_scholar"
    abstract: str = ""
    relevance_score: float = 0.0
```

---

## Source Specifications

### Garuda API
- **Endpoint:** `https://garuda.ristekbrin.go.id/api/v1/documents?q={query}&format=json`
- **Auth:** None
- **Response:** JSON with document list
- **Fields:** title, author, year, journal, DOI, URL, abstract

### CrossRef API
- **Endpoint:** `https://api.crossref.org/works?query={query}&select=title,author,DOI,url,published,container-title&rows={limit}`
- **Auth:** None (optional mailto for polite pool)
- **Response:** JSON with `message.items`
- **Fields:** title, author (given/family), DOI, URL, published-print/date-parts, container-title

### Semantic Scholar API
- **Endpoint:** `https://api.semanticscholar.org/graph/v1/paper/search?query={query}&fields=title,authors,year,venue,externalIds,url,abstract&limit={limit}`
- **Auth:** None
- **Rate limit:** 100 requests per 5 minutes
- **Response:** JSON with `data` array
- **Fields:** title, authors (name), year, venue, externalIds (DOI), url, abstract

---

## Aggregator Logic

1. Call all 3 sources sequentially (each with 10s timeout)
2. Collect results as `List[Paper]`
3. Deduplicate:
   - Primary: match by DOI (case-insensitive)
   - Secondary: match by lowercase title (if DOI missing)
   - Priority: keep Garuda version if both sources have same paper
4. Sort by relevance_score (currently: simple — Garuda items first, then others by year desc)
5. Return top N papers

### Error Handling
- If one source fails, skip it and continue with others
- If all sources fail, raise exception with error details
- Each source call has 10-second timeout

---

## CLI Interface (unchanged)

```bash
python scripts/journal_search.py --topic "machine learning" --limit 3
```

Output JSON schema (same as before, now populated from 3 sources):
```json
{
  "status": "success",
  "query": "machine learning",
  "papers": [{index, title, authors, year, journal, doi, url, abstract, metadata_source}],
  "error": null
}
```

---

## Implementation Phases

### Phase 1: Core modules
- `modules/search/paper_model.py` — Paper dataclass
- `modules/search/garuda.py` — Garuda API wrapper
- `modules/search/crossref.py` — CrossRef API wrapper
- `modules/search/semantic_scholar.py` — Semantic Scholar API wrapper
- Tests for each module

### Phase 2: Aggregator
- `modules/search/aggregator.py` — merge + dedup + sort
- Tests for aggregator (dedup, sort, error handling)

### Phase 3: Integration
- Modify `scripts/journal_search.py` to use aggregator
- Update existing tests
- Integration tests
