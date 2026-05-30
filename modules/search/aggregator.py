"""Aggregator: merge, deduplicate, and sort papers from multiple sources."""

from concurrent.futures import ThreadPoolExecutor, as_completed

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
    """Search all sources in parallel and return deduplicated, sorted results.

    Args:
        topic: Search query.
        total_limit: Max papers to return.
        per_source_limit: Max papers per source.
        sort_by: Sort criterion (composite, citations, year, relevance).

    Returns:
        Sorted, deduplicated list of Paper objects.
    """
    all_papers: list[Paper] = []

    with ThreadPoolExecutor(max_workers=len(SOURCES)) as executor:
        future_to_source = {
            executor.submit(_safe_search, source, topic, per_source_limit): source
            for source in SOURCES
        }
        for future in as_completed(future_to_source):
            source = future_to_source[future]
            try:
                papers = future.result()
                all_papers.extend(papers)
            except RuntimeError:
                continue

    if not all_papers:
        raise RuntimeError(f"No results from any source for query: {topic}")

    papers = _deduplicate(all_papers)
    papers = sort_papers(papers, sort_by=sort_by)
    return papers[:total_limit]


def _safe_search(source, topic: str, limit: int) -> list[Paper]:
    """Search a single source, raising RuntimeError on failure."""
    return source.search(topic, limit=limit)


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
