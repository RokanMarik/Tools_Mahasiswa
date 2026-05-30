#!/usr/bin/env python3
"""Journal search wrapper script.

Uses multi-source aggregator (OpenAlex + Garuda).

Usage:
    python scripts/journal_search.py --topic "machine learning" [--limit 3]

Output: JSON to stdout with paper list.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.search import aggregator


def search_journals(topic: str, limit: int = 3, sort_by: str = "composite") -> str:
    """Search for journals on a topic using multi-source aggregator.

    Args:
        topic: Search topic.
        limit: Max papers to return (default 3).
        sort_by: Sort criterion (composite, citations, year, relevance).

    Returns:
        JSON string with paper list.
    """
    try:
        papers = aggregator.search(topic, total_limit=limit, sort_by=sort_by)
        paper_dicts = [_paper_to_dict(p, i + 1) for i, p in enumerate(papers)]

        return json.dumps({
            "status": "success",
            "query": topic,
            "papers": paper_dicts,
            "error": None,
        }, ensure_ascii=False)

    except RuntimeError as e:
        return json.dumps({
            "status": "error",
            "query": topic,
            "papers": [],
            "error": str(e),
        }, ensure_ascii=False)


def _paper_to_dict(paper, index: int) -> dict:
    """Convert Paper dataclass to dict for JSON serialization."""
    return {
        "index": index,
        "title": paper.title,
        "authors": paper.authors,
        "year": paper.year,
        "journal": paper.journal,
        "doi": paper.doi,
        "url": paper.url,
        "abstract": paper.abstract,
        "citation_count": paper.citation_count,
        "metadata_source": paper.source,
    }


def main():
    parser = argparse.ArgumentParser(description="Search for academic journals")
    parser.add_argument("--topic", required=True, help="Search topic")
    parser.add_argument("--limit", type=int, default=3, help="Max papers to return")
    parser.add_argument(
        "--sort",
        choices=["composite", "citations", "year", "relevance"],
        default="composite",
        help="Sort criterion (default: composite)",
    )
    args = parser.parse_args()

    result = search_journals(args.topic, args.limit, args.sort)
    print(result)


if __name__ == "__main__":
    main()
