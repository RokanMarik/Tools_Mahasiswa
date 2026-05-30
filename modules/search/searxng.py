"""SearXNG meta-search engine wrapper for academic papers.

Uses public SearXNG instances (no API key needed) to search Google Scholar,
CrossRef, and other academic sources. Provides broader coverage for
Indonesian journals that may not be indexed in OpenAlex.
"""

import os
import re
import requests
from .paper_model import Paper

# Public SearXNG instances (fallback order)
SEARXNG_INSTANCES = [
    "https://searx.be",
    "https://search.onon.top",
    "https://searx.tiekoetter.com",
    "https://searx.ng",
]

REQUEST_TIMEOUT = 15


def _get_base_url() -> str:
    """Get SearXNG base URL — env override or first working public instance."""
    env_url = os.getenv("SEARXNG_URL")
    if env_url:
        return env_url.rstrip("/")
    return SEARXNG_INSTANCES[0]


def search(query: str, limit: int = 5) -> list[Paper]:
    """Search SearXNG for academic papers.

    Tries multiple instances if the first one fails.

    Args:
        query: Search query string.
        limit: Max results to return.

    Returns:
        List of Paper objects from SearXNG results.
    """
    base_url = _get_base_url()

    for instance in [base_url] + SEARXNG_INSTANCES:
        if instance != base_url and base_url in SEARXNG_INSTANCES:
            pass  # skip duplicate
        try:
            response = requests.get(
                f"{instance}/search",
                params={
                    "q": query,
                    "format": "json",
                    "categories": "general,science",
                    "engines": "google scholar,crossref,google,duckduckgo",
                    "language": "en,id",
                },
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])[:limit]
            if results:
                return [_parse_searxng_result(r) for r in results]
        except (requests.RequestException, ValueError):
            continue

    raise RuntimeError(
        f"SearXNG: no results from any instance for query: {query}"
    )


def _parse_searxng_result(result: dict) -> Paper:
    """Parse a SearXNG result dict into a Paper object."""
    url = result.get("url", "")
    title = result.get("title", "")
    content = result.get("content", "")

    # Extract DOI from URL
    doi = ""
    if "doi.org" in url:
        doi = url.split("doi.org/")[-1].split("/")[0].split("?")[0]

    # Extract year from content or publishedDate
    year = _extract_year(content, result.get("publishedDate", ""))

    # Extract authors if present in content
    authors = _extract_authors(content)

    # Determine source engine
    engines = result.get("engines", [])
    source_engine = engines[0] if engines else "searxng"

    # Detect Indonesian journals from URL/domain
    journal = _detect_journal(url, content)

    return Paper(
        title=title,
        authors=authors,
        year=year,
        journal=journal,
        doi=doi,
        url=url,
        source=f"searxng:{source_engine}",
        abstract=_clean_abstract(content),
    )


def _extract_year(content: str, published_date: str) -> int | None:
    """Extract year from content text or published date."""
    if published_date:
        try:
            return int(published_date[:4])
        except (ValueError, TypeError):
            pass

    # Look for year pattern in content (e.g., "2025" or "(2025)")
    if content:
        match = re.search(r"\b(20[2-3]\d)\b", content)
        if match:
            return int(match.group(1))

    return None


def _extract_authors(content: str) -> list[str]:
    """Try to extract author names from content snippet."""
    if not content:
        return []

    # Common patterns: "Author1, Author2 - Journal, Year"
    # or "by Author1, Author2"
    patterns = [
        r"^([^–\-]+)[–\-]",  # Before dash
        r"by\s+([^,]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            author_str = match.group(1).strip()
            if len(author_str) < 100:  # sanity check
                return [a.strip() for a in author_str.split(",") if a.strip()]

    return []


def _detect_journal(url: str, content: str) -> str:
    """Detect journal name from URL or content."""
    # Common Indonesian journal domains
    domain_journal_map = {
        "iicls.org": "EDU RESEARCH (IICLS)",
        "garuda.ristekbrin": "Garuda (BRIN)",
        "jurnal.ugm.ac.id": "UGM Journal",
        "journal.uny.ac.id": "UNY Journal",
        "ejournal.upi.edu": "UPI E-Journal",
        "jurnal.unipar.ac.id": "UNIPAR Journal",
        "jbasic.org": "Jurnal Basicedu",
    }

    for domain, journal in domain_journal_map.items():
        if domain in url:
            return journal

    return ""


def _clean_abstract(content: str) -> str:
    """Clean up abstract/content snippet."""
    if not content:
        return ""
    # Remove HTML entities and excessive whitespace
    content = re.sub(r"&\w+;", " ", content)
    content = re.sub(r"\s+", " ", content).strip()
    return content[:500]  # truncate
