#!/usr/bin/env python3
"""Citation generator wrapper script.

Usage:
    python scripts/citation_generator.py --papers '{"title": "...", ...}' [--style apa]

Output: JSON to stdout with formatted citations.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.zotero.citation_formatter import CitationFormatter


def generate_citations(papers: list[dict], style: str = "apa") -> str:
    """Generate citations for papers. Returns JSON string.

    Args:
        papers: List of paper dicts with title, authors, year, journal, doi.
        style: Citation style (apa, ieee, mla, chicago). Defaults to apa.

    Returns:
        JSON string matching the spec schema:
        {
            "status": "success" | "error",
            "citations": [{"title": "...", "apa": "..."}],
            "error": null | "error message"
        }
    """
    try:
        formatter = CitationFormatter()
        if style not in formatter.STYLES:
            style = "apa"

        citations = []
        for paper in papers:
            item = {
                "title": paper.get("title", "Untitled"),
                "authors": paper.get("authors", []),
                "date": str(paper.get("year", "n.d.")),
                "journal": paper.get("journal", ""),
                "doi": paper.get("doi", ""),
            }
            citation_text = formatter.format(item, style=style)
            citations.append({
                "title": paper.get("title", "Untitled"),
                style: citation_text,
            })

        return json.dumps({
            "status": "success",
            "citations": citations,
            "error": None,
        }, ensure_ascii=False)

    except (ValueError, TypeError, AttributeError) as e:
        return json.dumps({
            "status": "error",
            "citations": [],
            "error": str(e),
        }, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Generate citations")
    parser.add_argument("--papers", required=True, help="JSON array of paper metadata")
    parser.add_argument("--style", default="apa", help="Citation style (apa, ieee, mla, chicago)")
    args = parser.parse_args()

    try:
        papers = json.loads(args.papers)
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "error", "citations": [], "error": f"Invalid JSON: {e}"}))
        sys.exit(1)
    if not isinstance(papers, list):
        papers = [papers]

    result = generate_citations(papers, style=args.style)
    print(result)


if __name__ == "__main__":
    main()
