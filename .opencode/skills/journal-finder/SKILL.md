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
```

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
      "metadata_source": "crossref"
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
   Year: {year} | Journal: {journal}
   DOI: {doi}
   {url}
```

## State

After search, remember results for potential Zotero save. The AI should track which papers were found so user can reference them by number ("simpan 1 dan 3").
