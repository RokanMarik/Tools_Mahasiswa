# Tools Mahasiswa

Journal search engine with Zotero integration for Indonesian & international scientific articles.

## Features

- Multi-source search: Semantic Scholar (international), Crossref (DOI-based), Garuda (Indonesian)
- Citation count & publication year display
- Sort by: most cited, newest, relevance
- Balanced mode: foundational (high citations) + recent papers
- Direct Zotero API integration
- Export: CSV, BibTeX, RIS, JSON
- Citation generation: APA, IEEE, MLA, Chicago

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Search Journals
```bash
# Basic search (all sources)
python main.py search "machine learning"

# Sort by most cited
python main.py search "AI" --sort citations --limit 10

# Indonesian journals only
python main.py search "pembelajaran" --source garuda

# Balanced: foundational + recent
python main.py search "flipped classroom" --balanced

# Filter by year range
python main.py search "deep learning" --year-from 2020 --year-to 2025
```

### Save to Zotero
```bash
python main.py save --papers '''[{"title":"Test","authors":["Author"],"year":2024}]''' --api-key YOUR_KEY
```

### Generate Citations
```bash
python main.py citation --papers '''[{"title":"Test","authors":["Author"],"year":2024}]''' --style apa
```

### Export
```bash
python main.py export --papers '''[...]''' --format bibtex --output refs.bib
```

## Architecture

```
modules/
  search/       Multi-source search engine
    semantic_scholar.py  Semantic Scholar API
    crossref.py          Crossref API
    garuda.py            Garuda (Indonesian)
    engine.py            Orchestrator + dedup + sort
  zotero/       Zotero API integration
    client.py            Direct API client
    citation_formatter.py APA/IEEE/MLA/Chicago
    collection_picker.py  Collection management
  export/       Export formats
    csv_export.py
    bibtex_export.py
    ris_export.py
  ui/           Terminal display
    display.py
```

## API Sources

| Source | Region | Citations | Free |
|--------|--------|-----------|------|
| Semantic Scholar | International | Yes | Yes |
| Crossref | International | Yes | Yes |
| Garuda | Indonesia | No | Yes |

## License

MIT
