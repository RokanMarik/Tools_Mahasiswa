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
3. **Ask for collection** — ALWAYS ask where to save before proceeding:
   - Fetch collections via `CollectionPicker.display_collections()`
   - Show numbered list:
     ```
     Koleksi Zotero kamu:
       1. Semester Satu (15 items)
       2. Semester Dua (8 items)
       3. Skripsi (3 items)
     
     Simpan di koleksi mana? (ketik nomor atau nama)
     ```
   - User picks by number (e.g. "2") or name (e.g. "semester dua")
   - If no collection exists, offer: "Belum ada koleksi. Mau simpan di root library atau bikin koleksi baru?"
4. **Execute save**: `python scripts/zotero_save.py --api-key "$ZOTERO_API_KEY" --collection "COLLECTION_KEY" --papers '<json>'`
5. **Parse JSON output** — check `status`, `saved`, `skipped`
6. **Confirm to user** with APA citation + collection name

## Workflow: Generate Citation Only

1. **Get paper metadata** from context
2. **Execute**: `python scripts/citation_generator.py --papers '<json>' --style apa`
3. **Display citation** to user

## Script Interfaces

### zotero_save.py
```bash
python scripts/zotero_save.py --api-key "KEY" --collection "COL_KEY" --papers '[{"title":"...", "authors":["..."], "year":2024, "journal":"...", "doi":"..."}]'
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
- **No collections**: "Belum ada koleksi di Zotero. Simpan di root library? (ketik 'ya' atau bikin koleksi baru dulu di Zotero)"

## Citation Format

Always use APA style by default:

```
Author, A. A., & Author, B. B. (Year). Title of the article. *Journal Name*, *Volume*(Issue), Page range. https://doi.org/xxx
```

## Example Conversation

### Save to Specific Collection

```
User: "Simpan paper flipped classroom ke Zotero"
Agent: "Koleksi Zotero kamu:
  1. Semester Satu (15 items)
  2. Semester Dua (8 items)
  3. Skripsi (3 items)

Simpan di koleksi mana?"
User: "2"
Agent: "✅ Berhasil disimpan ke 'Semester Dua':

Smith, J., & Lee, K. (2024). Flipped classroom in higher education. *Frontiers in Education*, 9, 1412683. https://doi.org/10.3389/feduc.2024.1412683"
```

### Save to Root (No Collections)

```
User: "Simpan paper ini"
Agent: "Belum ada koleksi di Zotero. Simpan di root library?"
User: "ya"
Agent: "✅ Berhasil disimpan ke library kamu:

Author. (Year). Title. *Journal*. DOI"
```

---

**Last Updated:** 2026-05-31
**Version:** 2.0 (collection picker mandatory before save)
