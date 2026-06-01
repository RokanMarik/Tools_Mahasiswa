#!/usr/bin/env python3
"""Tools Mahasiswa - Journal search & Zotero integration CLI."""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.search.engine import SearchEngine, SORT_CITATIONS, SORT_YEAR, SORT_RELEVANCE, SOURCE_ALL
from modules.zotero.client import ZoteroClient
from modules.zotero.citation_formatter import CitationFormatter
from modules.export.csv_export import CsvExporter
from modules.export.bibtex_export import BibtexExporter
from modules.export.ris_export import RisExporter
from modules.ui.display import Display

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def cmd_search(args):
    engine = SearchEngine()
    display = Display()
    sources = [s.strip() for s in args.source.split(',')] if args.source else [SOURCE_ALL]

    if args.balanced:
        result = engine.get_balanced_results(query=args.query, limit=args.limit or 6, year_from=args.year_from, year_to=args.year_to)
        print(display.display_balanced(result["foundational"], result["recent"], args.query))
    else:
        papers = engine.search(query=args.query, sources=sources, sort=args.sort or SORT_RELEVANCE, limit=args.limit or 6, year_from=args.year_from, year_to=args.year_to)
        if args.format == "json":
            print(json.dumps(papers, indent=2, ensure_ascii=False))
        elif args.format == "table":
            print(display.display_table(papers))
        else:
            print(display.display_results(papers, args.query, show_abstract=args.abstract))

        if args.export:
            content = _export(papers, args.export)
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f: f.write(content)
                print(f"Exported to {args.output}")
            else:
                print(content)


def cmd_save(args):
    api_key = args.api_key or os.getenv('ZOTERO_API_KEY')
    if not api_key:
        print(json.dumps({"status": "error", "error": "Set --api-key or ZOTERO_API_KEY"}))
        sys.exit(1)
    try:
        papers = json.loads(args.papers)
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "error", "error": str(e)}))
        sys.exit(1)
    if not isinstance(papers, list): papers = [papers]
    client = ZoteroClient(api_key=api_key)
    client.library_id = client.get_user_id()
    formatter = CitationFormatter()
    saved, skipped = [], []
    for paper in papers:
        item = {"title": paper.get('title',''), "authors": paper.get('authors',[]), "date": str(paper.get('year','')), "doi": paper.get('doi',''), "url": paper.get('url',''), "journal": paper.get('journal',''), "itemType": "journalArticle"}
        try:
            result = client.add_item(args.collection or '', item)
            saved.append({"title": paper.get('title',''), "citation_apa": formatter.format(item, 'apa')})
        except Exception as e:
            skipped.append({"title": paper.get('title',''), "reason": str(e)})
    print(json.dumps({"status": "success" if saved else "error", "saved": saved, "skipped": skipped}, indent=2, ensure_ascii=False))


def cmd_citation(args):
    try:
        papers = json.loads(args.papers)
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "error", "error": str(e)}))
        sys.exit(1)
    if not isinstance(papers, list): papers = [papers]
    formatter = CitationFormatter()
    citations = []
    for p in papers:
        item = {"title": p.get('title','Untitled'), "authors": p.get('authors',[]), "date": str(p.get('year','n.d.')), "journal": p.get('journal',''), "doi": p.get('doi','')}
        citations.append({"title": p.get('title',''), args.style or 'apa': formatter.format(item, args.style or 'apa')})
    print(json.dumps({"status": "success", "citations": citations}, indent=2, ensure_ascii=False))


def cmd_collections(args):
    api_key = args.api_key or os.getenv('ZOTERO_API_KEY')
    if not api_key:
        print('Error: Set --api-key or ZOTERO_API_KEY')
        sys.exit(1)
    client = ZoteroClient(api_key=api_key)
    client.library_id = client.get_user_id()
    collections = client.get_collections()
    for c in collections:
        print(f"{c.get('name','')} (key: {c.get('key','')})")


def cmd_export(args):
    try:
        papers = json.loads(args.papers)
    except json.JSONDecodeError as e:
        print(f'Error: {e}')
        sys.exit(1)
    if not isinstance(papers, list): papers = [papers]
    content = _export(papers, args.format)
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f: f.write(content)
        print(f'Exported {len(papers)} papers to {args.output}')
    else:
        print(content)


def _export(papers, fmt):
    if fmt == 'csv': return CsvExporter().export(papers)
    if fmt == 'bibtex': return BibtexExporter().export(papers)
    if fmt == 'ris': return RisExporter().export(papers)
    return json.dumps(papers, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description='Tools Mahasiswa - Journal search & Zotero')
    sub = parser.add_subparsers(dest='command')

    sp = sub.add_parser('search', help='Search journals')
    sp.add_argument('query')
    sp.add_argument('--source', default='all')
    sp.add_argument('--sort', choices=['citations','year','relevance'], default='relevance')
    sp.add_argument('--limit', type=int, default=6)
    sp.add_argument('--year-from', type=int)
    sp.add_argument('--year-to', type=int)
    sp.add_argument('--balanced', action='store_true')
    sp.add_argument('--abstract', action='store_true')
    sp.add_argument('--format', choices=['table','json','pretty'], default='pretty')
    sp.add_argument('--export', choices=['csv','bibtex','ris','json'])
    sp.add_argument('--output')

    sp = sub.add_parser('save', help='Save to Zotero')
    sp.add_argument('--papers', required=True)
    sp.add_argument('--api-key')
    sp.add_argument('--collection')

    sp = sub.add_parser('citation', help='Generate citations')
    sp.add_argument('--papers', required=True)
    sp.add_argument('--style', choices=['apa','ieee','mla','chicago'], default='apa')

    sp = sub.add_parser('collections', help='List Zotero collections')
    sp.add_argument('--api-key')

    sp = sub.add_parser('export', help='Export papers')
    sp.add_argument('--papers', required=True)
    sp.add_argument('--format', required=True, choices=['csv','bibtex','ris','json'])
    sp.add_argument('--output')

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmds = {'search': cmd_search, 'save': cmd_save, 'citation': cmd_citation, 'collections': cmd_collections, 'export': cmd_export}
    cmds[args.command](args)


if __name__ == '__main__':
    main()
