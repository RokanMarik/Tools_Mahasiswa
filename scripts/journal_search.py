#!/usr/bin/env python3
"""Journal search wrapper script.

Usage:
    python scripts/journal_search.py --topic "machine learning" [--limit 3]

Output: JSON to stdout with paper list.
"""

import argparse
import json
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from importlib import import_module

# Module starts with digit — must use import_module
_journal_finder_mod = import_module("9router_journal_finder")
JournalFinder = _journal_finder_mod.JournalFinder


def search_journals(topic: str, limit: int = 3) -> str:
    """Search for journals on a topic. Returns JSON string.

    Args:
        topic: Search topic.
        limit: Max papers to return (default 3).

    Returns:
        JSON string matching the spec schema:
        {
            "status": "success" | "error",
            "query": "...",
            "papers": [{index, title, authors, year, journal, doi, url, abstract, metadata_source}],
            "error": null | "error message"
        }
    """
    try:
        finder = JournalFinder()

        raw_response = finder.find_journals(topic, limit=limit)
        papers = _parse_journal_response(raw_response, limit)

        return json.dumps({
            "status": "success",
            "query": topic,
            "papers": papers,
            "error": None,
        }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "query": topic,
            "papers": [],
            "error": str(e),
        }, ensure_ascii=False)


def _parse_journal_response(raw: str, limit: int) -> list:
    """Parse raw 9Router response into structured paper list."""
    # Try JSON first (for mocked/test responses)
    try:
        data = json.loads(raw)
        if isinstance(data, dict) and "papers" in data:
            papers = data["papers"]
            result = []
            for i, paper in enumerate(papers[:limit]):
                result.append({**paper, "index": i + 1})
            return result
    except (json.JSONDecodeError, TypeError):
        pass

    # Fall back to raw text parsing
    papers = []
    lines = raw.split("\n")
    current_paper = {}

    for line in lines:
        line = line.strip()
        if not line:
            if current_paper.get("title"):
                papers.append(current_paper)
                current_paper = {}
            continue

        if len(line) >= 2 and line[0].isdigit() and line[1] in ".)":
            if current_paper.get("title"):
                papers.append(current_paper)
            title = line[2:].strip()
            current_paper = {"title": title, "authors": [], "year": None, "journal": "", "doi": "", "url": "", "abstract": "", "metadata_source": "9router"}
            continue

        lower = line.lower()
        if lower.startswith("author"):
            authors_raw = line.split(":", 1)[-1].strip()
            current_paper["authors"] = [a.strip() for a in authors_raw.split(",") if a.strip()]
        elif lower.startswith("year"):
            try:
                current_paper["year"] = int(line.split(":", 1)[-1].strip()[:4])
            except (ValueError, IndexError):
                current_paper["year"] = None
        elif lower.startswith("journal"):
            current_paper["journal"] = line.split(":", 1)[-1].strip()
        elif lower.startswith("doi"):
            current_paper["doi"] = line.split(":", 1)[-1].strip()
        elif lower.startswith("url") or lower.startswith("link") or lower.startswith("http"):
            url_part = line.split(":", 1)[-1].strip() if ":" in line else line
            current_paper["url"] = url_part

    if current_paper.get("title"):
        papers.append(current_paper)

    result = []
    for i, paper in enumerate(papers[:limit]):
        result.append({**paper, "index": i + 1})
    return result


def main():
    parser = argparse.ArgumentParser(description="Search for academic journals")
    parser.add_argument("--topic", required=True, help="Search topic")
    parser.add_argument("--limit", type=int, default=3, help="Max papers to return")
    args = parser.parse_args()

    result = search_journals(args.topic, args.limit)
    print(result)


if __name__ == "__main__":
    main()
