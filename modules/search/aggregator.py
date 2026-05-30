"""Aggregator: merge, deduplicate, and sort papers from multiple sources."""

from .paper_model import Paper
from . import garuda, crossref, semantic_scholar

SOURCES = [garuda, crossref, semantic_scholar]


def search(topic: str, total_limit: int = 3, per_source_limit: int = 5) -> list[Paper]:
    """Search all sources and return deduplicated, sorted results."""
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
    papers = _sort_and_score(papers, topic)
    return papers[:total_limit]


def _deduplicate(papers: list[Paper]) -> list[Paper]:
    """Remove duplicate papers by DOI, then by title. Priority: Garuda > CrossRef > Semantic Scholar."""
    seen_dois: set[str] = set()
    seen_titles: set[str] = set()
    result: list[Paper] = []

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
    """Score and sort papers by relevance."""
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
