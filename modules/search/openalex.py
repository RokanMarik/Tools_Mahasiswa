"""OpenAlex API wrapper for academic paper search."""

import requests
from .paper_model import Paper

OPENALEX_API_URL = "https://api.openalex.org/works"
REQUEST_TIMEOUT = 15


def search(query: str, limit: int = 5) -> list[Paper]:
    """Search OpenAlex API for academic papers."""
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
    authors = []
    for authorship in work.get("authorships", []):
        author = authorship.get("author", {})
        name = author.get("display_name", "")
        if name:
            authors.append(name)

    journal = ""
    primary_location = work.get("primary_location", {}) or {}
    source = primary_location.get("source", {}) or {}
    if source.get("display_name"):
        journal = source["display_name"]

    doi = work.get("doi", "") or ""
    url = work.get("primary_location", {}).get("pdf_url", "") or doi
    citation_count = work.get("cited_by_count", 0) or 0

    year = work.get("publication_year")
    if year:
        try:
            year = int(year)
        except (ValueError, TypeError):
            year = None

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

    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))

    word_positions.sort(key=lambda x: x[0])
    return " ".join(word for _, word in word_positions)
