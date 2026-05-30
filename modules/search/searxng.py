"""SearXNG API wrapper via 9Router."""

import os
import requests
from .paper_model import Paper

REQUEST_TIMEOUT = 10


def _get_searxng_url() -> str:
    """Get SearXNG search endpoint URL from 9Router."""
    base = os.getenv("NINEROUTER_URL", "http://localhost:20128")
    return f"{base}/v1/search"


def search(query: str, limit: int = 5) -> list[Paper]:
    """Search SearXNG via 9Router for academic papers.

    Args:
        query: Search query string.
        limit: Max results to return.

    Returns:
        List of Paper objects from SearXNG.
    """
    try:
        response = requests.get(
            _get_searxng_url(),
            params={
                "q": query,
                "format": "json",
                "categories": "science",
            },
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        return [_parse_searxng_result(r) for r in data.get("results", [])[:limit]]
    except requests.RequestException as e:
        raise RuntimeError(f"SearXNG API error: {e}") from e


def _parse_searxng_result(result: dict) -> Paper:
    """Parse a SearXNG result dict into a Paper object."""
    # Extract DOI from URL if present
    doi = ""
    url = result.get("url", "")
    if "doi.org" in url:
        doi = url.split("doi.org/")[-1].split("/")[0].split("?")[0]

    # Try to extract year from publishedDate
    year = None
    published = result.get("publishedDate", "")
    if published:
        try:
            year = int(published[:4])
        except (ValueError, TypeError):
            pass

    # Get engine name
    engines = result.get("engines", [])
    source_engine = engines[0] if engines else "searxng"

    return Paper(
        title=result.get("title", ""),
        authors=[],  # SearXNG doesn't typically provide authors in search results
        year=year,
        journal="",  # Not available from SearXNG
        doi=doi,
        url=url,
        source=f"searxng:{source_engine}",
        abstract=result.get("content", ""),
    )
