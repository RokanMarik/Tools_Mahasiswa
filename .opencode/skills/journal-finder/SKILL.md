---
name: journal-finder
description: Search for academic journals via 9Router. Use when user asks to find papers, search journals, or look up research.
---

# Journal Finder Skill

Search for academic journals and papers via 9Router. Returns structured paper metadata.

## Trigger

Natural language detection:
- "cari jurnal [topik]"
- "find papers about [topic]"
- "search for journals on [topic]"
- "cari paper tentang [topik]"

**Multi-source search:** This skill searches multiple APIs:
- **OpenAlex** (api.openalex.org) — 250M+ papers with citation counts, ingests CrossRef + many sources
- **Garuda** (garuda.ristekbrin.go.id) — Indonesian academic journals
- **SearXNG + Google Scholar** (optional) — Finds Indonesian journals not indexed in OpenAlex (iicls.org, etc.)

Results are merged, deduplicated by DOI, and sorted by composite score (citations 60% + recency 40%). No API keys needed.

**Enable SearXNG (for Indonesian journal coverage):**
```bash
# Start SearXNG via Docker (port 8888)
docker run -d --name searxng -p 8888:8080 searxng/searxng
# OR restart existing container
docker start searxng

# Set environment variable
set SEARXNG_URL=http://localhost:8888
```
SearXNG searches Google Scholar + CrossRef + Semantic Scholar. Citations enriched via Semantic Scholar API.

## Workflow

1. **Parse topic** from user request
2. **Clarify if needed** — if topic is too broad, ask one brief clarification question
3. **Select model** based on context:
   - `Mencari_Jurnal_Ilmiah` → journal search and recommendation
   - `Merangkum_Memperjelas_Catatan` → paper analysis/summarization
   - `kr/claude-sonnet-4.5` → general questions about research
4. **Execute search**: `python scripts/journal_search.py --topic "<topic>" --limit 3`
5. **Parse JSON output** and display papers to user in readable format
6. **Offer next steps**: "Mau simpan ke Zotero?", "Mau analisis paper tertentu?", atau "Cari lagi?"

## Script Interface

```bash
python scripts/journal_search.py --topic "machine learning" --limit 3
python scripts/journal_search.py --topic "machine learning" --limit 5 --sort citations
python scripts/journal_search.py --topic "machine learning" --limit 5 --sort year
python scripts/journal_search.py --topic "machine learning" --limit 5 --sort composite  # default
```

`--sort` options: `composite` (default), `citations`, `year`, `relevance`

Output JSON:
```json
{
  "status": "success",
  "query": "machine learning",
  "papers": [
    {
      "index": 1,
      "title": "...",
      "authors": ["..."],
      "year": 2024,
      "journal": "...",
      "doi": "10.xxxx/xxxxx",
      "url": "https://...",
      "abstract": "...",
      "citation_count": 42,
      "metadata_source": "openalex"
    }
  ],
  "error": null
}
```

## Error Handling

- **9Router not running**: "9Router belum jalan. Nyalakan dulu, lalu coba lagi."
- **No results**: "Nggak nemu paper untuk topik itu. Coba kata kunci lain atau topik yang lebih spesifik?"
- **JSON parse error**: Retry once, then report error to user

## Display Format

Show papers as:
```
Nemu {n} paper:

1. {title}
   Authors: {authors}
   Year: {year} | Journal: {journal} | Citations: {citation_count}
   DOI: {doi}
   {url}
```

## State

After search, remember results for potential Zotero save. The AI should track which papers were found so user can reference them by number ("simpan 1 dan 3").
