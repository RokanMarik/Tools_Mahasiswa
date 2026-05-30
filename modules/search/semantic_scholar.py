"""Semantic Scholar API wrapper."""

import requests
from .paper_model import Paper

SEMANTIC_SCHOLAR_API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
REQUEST_TIMEOUT = 10


def search(query: str, limit: int = 5) -> list[Paper]:
    """Search Semantic Scholar API for papers."""
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
