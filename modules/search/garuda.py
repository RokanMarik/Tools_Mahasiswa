"""Garuda Ristekbrin API wrapper."""

import requests
from .paper_model import Paper

GARUDA_API_URL = "https://garuda.ristekbrin.go.id/api/v1/documents"
REQUEST_TIMEOUT = 10


def search(query: str, limit: int = 5) -> list[Paper]:
    """Search Garuda API for academic documents."""
    try:
        response = requests.get(
            GARUDA_API_URL,
            params={"q": query, "format": "json"},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        return [_parse_garuda_doc(doc) for doc in data.get("data", [])[:limit]]
    except requests.RequestException as e:
        raise RuntimeError(f"Garuda API error: {e}") from e


def _parse_garuda_doc(doc: dict) -> Paper:
    """Parse a Garuda API document dict into a Paper object."""
    authors = []
    if doc.get("author"):
        authors = [a.strip() for a in doc["author"].split(",") if a.strip()]
    year = None
    if doc.get("year"):
        try:
            year = int(doc["year"])
        except (ValueError, TypeError):
            pass
    return Paper(
        title=doc.get("title", ""),
        authors=authors,
        year=year,
        journal=doc.get("journal", ""),
        doi=doc.get("doi", ""),
        url=doc.get("url", ""),
        source="garuda",
        abstract=doc.get("abstract", ""),
    )
