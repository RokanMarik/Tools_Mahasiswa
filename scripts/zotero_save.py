#!/usr/bin/env python3
"""Zotero save wrapper script.

Usage:
    python scripts/zotero_save.py --api-key "KEY" --collection "COL_KEY" --papers '{"title": "...", ...}'

Input: Paper metadata as JSON (one or more papers).
Output: JSON to stdout with save results.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.zotero.client import ZoteroClient
from modules.zotero.citation_formatter import CitationFormatter


def save_to_zotero(papers: list, api_key: str, collection_key: str | None = None) -> str:
    """Save papers to Zotero. Returns JSON string.

    Args:
        papers: List of paper dicts with title, authors, year, journal, doi, url.
        api_key: Zotero API key.
        collection_key: Target collection key (None for top-level).

    Returns:
        JSON string matching the spec schema:
        {
            "status": "success" | "error" | "duplicate",
            "saved": [{"title": "...", "zotero_key": "...", "citation_apa": "..."}],
            "skipped": [{"title": "...", "reason": "duplicate"}],
            "error": null | "error message"
        }
    """
    saved = []
    skipped = []
    formatter = CitationFormatter()

    try:
        client = ZoteroClient(api_key=api_key)
        client.library_id = client.get_user_id()
    except Exception as e:
        return json.dumps({
            "status": "error",
            "saved": [],
            "skipped": [],
            "error": f"Zotero connection failed: {e}",
        }, ensure_ascii=False)

    for paper in papers:
        validation = validate_paper_metadata(paper)
        if not validation["valid"]:
            skipped.append({
                "title": paper.get("title", "Unknown"),
                "reason": f"Invalid metadata: {', '.join(validation['errors'])}",
            })
            continue

        item_data = {
            "title": paper["title"],
            "authors": paper.get("authors", []),
            "date": str(paper.get("year", "")),
            "doi": paper.get("doi", ""),
            "url": paper.get("url", ""),
            "journal": paper.get("journal", ""),
            "itemType": "journalArticle",
        }

        try:
            result = client.add_item(collection_key or "", item_data)

            citation = formatter.format(item_data, style="apa")

            saved.append({
                "title": paper["title"],
                "zotero_key": result.get("key", ""),
                "citation_apa": citation,
            })
        except Exception as e:
            error_msg = str(e).lower()
            if "duplicate" in error_msg or "already exists" in error_msg:
                skipped.append({
                    "title": paper["title"],
                    "reason": "duplicate",
                })
            else:
                skipped.append({
                    "title": paper["title"],
                    "reason": f"Save failed: {e}",
                })

    status = "success" if saved else ("duplicate" if skipped else "error")
    return json.dumps({
        "status": status,
        "saved": saved,
        "skipped": skipped,
        "error": None,
    }, ensure_ascii=False)


def validate_paper_metadata(paper: dict) -> dict:
    """Validate paper metadata before saving.

    Args:
        paper: Paper dict with title, authors, etc.

    Returns:
        {valid: bool, errors: list[str]}
    """
    errors = []
    if not paper.get("title"):
        errors.append("title")
    return {"valid": len(errors) == 0, "errors": errors}


def main():
    parser = argparse.ArgumentParser(description="Save papers to Zotero")
    parser.add_argument("--api-key", default=None, help="Zotero API key (or set ZOTERO_API_KEY env var)")
    parser.add_argument("--collection", default=None, help="Collection key (optional)")
    parser.add_argument("--papers", required=True, help="JSON array of paper metadata")
    args = parser.parse_args()

    api_key = args.api_key or os.getenv("ZOTERO_API_KEY")
    if not api_key:
        print(json.dumps({"status": "error", "saved": [], "skipped": [], "error": "No API key provided. Set --api-key or ZOTERO_API_KEY env var."}))
        sys.exit(1)

    try:
        papers = json.loads(args.papers)
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "error", "saved": [], "skipped": [], "error": f"Invalid JSON: {e}"}))
        sys.exit(1)
    if not isinstance(papers, list):
        papers = [papers]

    result = save_to_zotero(papers, api_key=api_key, collection_key=args.collection)
    print(result)


if __name__ == "__main__":
    main()
