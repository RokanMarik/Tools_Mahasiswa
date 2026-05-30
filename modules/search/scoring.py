"""Scoring and sorting logic for journal search results."""

import datetime

from .paper_model import Paper

CITATION_WEIGHT = 0.6
RECENCY_WEIGHT = 0.4
_CURRENT_YEAR = datetime.date.today().year


def compute_composite_score(papers: list[Paper]) -> list[Paper]:
    """Compute composite score for each paper based on citations and recency.

    Uses min-max normalization to scale both metrics to 0-1 range.
    Formula: score = (norm_citations * 0.6) + (norm_recency * 0.4)
    """
    if not papers:
        return papers

    citations = [p.citation_count for p in papers]
    years = [p.year for p in papers if p.year is not None]

    max_citations = max(citations) if citations else 0
    min_year = min(years) if years else _CURRENT_YEAR - 5
    max_year = max(years) if years else _CURRENT_YEAR
    year_range = max_year - min_year

    for paper in papers:
        norm_citations = (
            paper.citation_count / max_citations if max_citations > 0 else 0
        )

        if paper.year is not None and year_range > 0:
            norm_recency = (paper.year - min_year) / year_range
        else:
            norm_recency = 0

        paper.relevance_score = (
            norm_citations * CITATION_WEIGHT + norm_recency * RECENCY_WEIGHT
        )

    return papers


def sort_papers(
    papers: list[Paper], sort_by: str = "composite"
) -> list[Paper]:
    """Sort papers by the specified criterion."""
    if sort_by == "composite":
        compute_composite_score(papers)
        papers.sort(key=lambda p: p.relevance_score, reverse=True)
    elif sort_by == "citations":
        papers.sort(key=lambda p: p.citation_count, reverse=True)
    elif sort_by == "year":
        papers.sort(key=lambda p: p.year or 0, reverse=True)
    elif sort_by == "relevance":
        # Alias for composite — compute scores then sort
        compute_composite_score(papers)
        papers.sort(key=lambda p: p.relevance_score, reverse=True)
    else:
        raise ValueError(
            f"Invalid sort_by value: {sort_by}. "
            f"Must be one of: composite, citations, year, relevance"
        )

    return papers
