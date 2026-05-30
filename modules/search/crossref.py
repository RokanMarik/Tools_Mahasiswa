"""CrossRef API wrapper."""

import requests
from .paper_model import Paper

CROSSREF_API_URL = "https://api.crossref.org/works"
REQUEST_TIMEOUT = 10


def search(query: str, limit: int = 5) -> list[Paper]:
    """Search CrossRef API for academic works."""
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
