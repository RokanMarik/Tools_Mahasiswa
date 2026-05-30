---
name: zotero
description: Save papers to Zotero library, generate citations. Use when user asks to save papers, add to library, or generate citations.
---

# Zotero Skill

Save academic papers to Zotero and generate formatted citations (APA style).

## Trigger

Natural language detection:
- "simpan ke zotero"
- "save to zotero"
- "add to library"
- "simpan paper [nomor/judul]"
- "buat citation"
- "generate citation"

## Prerequisites

Requires:
- `ZOTERO_API_KEY` environment variable (or user provides it)
- Zotero desktop running (for local sync)

## Workflow: Save Paper

1. **Get paper metadata** from context (previous search results or user input)
2. **Validate metadata** — title is required, DOI recommended
3. **Execute save**: `python scripts/zotero_save.py --api-key "$ZOTERO_API_KEY" --papers '<json>'`
4. **Parse JSON output** — check `status`, `saved`, `skipped`
5. **Confirm to user** with APA citation

## Workflow: Generate Citation Only

1. **Get paper metadata** from context
2. **Execute**: `python scripts/citation_generator.py --papers '<json>' --style apa`
3. **Display citation** to user

## Script Interfaces

### zotero_save.py
```bash
python scripts/zotero_save.py --api-key "KEY" --papers '[{"title":"...", "authors":["..."], "year":2024, "journal":"...", "doi":"..."}]'
```

Output:
```json
{
  "status": "success",
  "saved": [{"title": "...", "zotero_key": "ABC123", "citation_apa": "..."}],
  "skipped": [],
  "error": null
}
```

### citation_generator.py
```bash
python scripts/citation_generator.py --papers '[{"title":"...", "authors":["..."], "year":2024}]' --style apa
```

Output:
```json
{
  "status": "success",
  "citations": [{"title": "...", "apa": "Author. (Year). Title. Journal. DOI"}],
  "error": null
}
```

## Error Handling

- **No API key**: "API key Zotero belum diset. Set env var `ZOTERO_API_KEY` atau kasih key-nya langsung."
- **Zotero not running**: "Zotero desktop belum dibuka. Buka dulu, terus coba lagi."
- **Invalid metadata**: "Metadata paper ini tidak lengkap. Minimal butuh judul. Mau coba fetch dari DOI?"
- **Duplicate**: "Paper ini sudah ada di Zotero. Mau skip atau buat duplicate?"

## Citation Format

Always use APA style by default:
```
Author, A. A., & Author, B. B. (Year). Title of paper. Journal Name, volume(issue), pages. https://doi.org/xxx
```

Metadata MUST come from verified sources (DOI lookup, journal page, CrossRef API) — NEVER generate citation from AI memory.
