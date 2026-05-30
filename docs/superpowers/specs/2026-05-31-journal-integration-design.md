# Journal Integration Design

**Date:** 2026-05-31
**Status:** Approved
**Approach:** OpenCode Custom Skills (Phased C: separate skills + meta skill)

---

## Overview

Integrate three existing systems (Journal Finder, 9Router, Zotero) into OpenCode as native skills so users can search for academic papers, review results, and save to Zotero — all through natural language in the OpenCode chat, without opening a terminal.

---

## Architecture

### File Structure

```
.opencode/
├── skills/
│   ├── journal-finder/
│   │   └── SKILL.md              ← How AI searches journals via 9Router
│   ├── zotero/
│   │   └── SKILL.md              ← How AI saves to / reads from Zotero
│   ├── journal-workflow/
│   │   └── SKILL.md              ← Meta skill: orchestrates journal-finder + zotero
│   └── journal-help/
│       └── SKILL.md              ← Cheat sheet (? / /help)
│
scripts/
├── journal_search.py             ← Wrapper for 9Router + search APIs
├── zotero_save.py                ← Wrapper for Zotero CLI
└── citation_generator.py         ← Generate APA citation from metadata

modules/zotero/                   ← Existing, reused
├── client.py
├── citation_formatter.py
├── collection_picker.py
└── ...
```

### Workflow

```
User: "cari jurnal tentang federated learning"
  → AI detect intent → load journal-finder
  → Execute scripts/journal_search.py
  → Display 3-5 papers (link, author, year, DOI, abstract)
  → "Mau simpan ke Zotero?"
User: "1 dan 3"
  → AI validate metadata (DOI check)
  → Execute scripts/zotero_save.py
  → Confirm + generate APA citation
```

---

## Skill Specifications

### journal-finder/SKILL.md

**Trigger:** User requests journal search (keywords: "cari jurnal", "find papers", "search paper")

**AI Behavior:**
1. Parse topic from user request
2. If topic too broad, ask brief clarification
3. Select 9Router model based on context (journal-finder for search, analysis model for analysis, general for questions)
4. Execute `scripts/journal_search.py` with topic + parameters
5. Display results (3-5 papers with links + metadata)
6. Offer next step: save to Zotero / analyze / search again

### zotero/SKILL.md

**Trigger:** User requests save to Zotero (keywords: "simpan zotero", "save to zotero", "add to library")

**AI Behavior:**
1. Get metadata of user-selected papers
2. Validate DOI/metadata before save
3. Execute `scripts/zotero_save.py` with verified metadata
4. Confirm success + display APA citation
5. Offer: save more / create bibliography / done

### journal-workflow/SKILL.md (Meta Skill)

**Trigger:** User starts full research workflow from the beginning

**AI Behavior:**
1. Orchestrate: journal-finder → review → zotero → citation
2. Maintain state across steps (which papers are selected)
3. Handle mid-workflow errors (search failed / Zotero down / invalid metadata)
4. Offer shortcuts: if user knows what they want, skip to specific step

### journal-help/SKILL.md (Cheat Sheet)

**Trigger:** User types `?`, `/help`, or "bantuan"

**Content:** List of available commands with examples

---

## Data Flow

### Script Execution

AI uses Bash tool to run Python scripts:
```bash
python scripts/journal_search.py --topic "federated learning" --limit 3
```

Script output is JSON → AI parses → displays to user in readable format.

### Script Output Schema

**`journal_search.py` output:**
```json
{
  "status": "success" | "error",
  "query": "federated learning",
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
      "metadata_source": "crossref" | "publisher" | "semantic_scholar"
    }
  ],
  "error": null
}
```

**`zotero_save.py` output:**
```json
{
  "status": "success" | "error" | "duplicate",
  "saved": [{"title": "...", "zotero_key": "...", "citation_apa": "..."}],
  "skipped": [{"title": "...", "reason": "duplicate"}],
  "error": null
}
```

**`citation_generator.py` output:**
```json
{
  "status": "success" | "error",
  "citations": [{"title": "...", "apa": "Author. (Year). Title. Journal. DOI"}],
  "error": null
}
```

### State Management

AI uses memory slots to track state:
- `journal_search_results` → latest search results
- `journal_selected_papers` → papers user selected
- `journal_session_active` → whether workflow is in progress

### Model Selection (9Router)

Automatic routing based on task:
- `Mencari_Jurnal_Ilmiah` → journal search and recommendation
- `Merangkum_Memperjelas_Catatan` → paper analysis and summarization
- `kr/claude-sonnet-4.5` → general purpose questions

---

## Error Handling

| Scenario | User Message | Recovery |
|----------|-------------|----------|
| 9Router down | "9Router belum jalan. Nyalakan dulu, lalu coba lagi." | Wait for user to start 9Router |
| No results | "Nggak nemu paper. Coba kata kunci lain?" | New search with different keywords |
| Invalid DOI | "Metadata tidak valid. Skip atau fetch ulang?" | User chooses skip or retry |
| Zotero not running | "Zotero desktop belum dibuka." | User opens Zotero, retry |
| Topic change mid-workflow | Detect intent change → reset state → start fresh |
| Duplicate in Zotero | "Paper ini sudah ada. Skip atau buat duplicate?" | User decides |
| Session timeout | Slot expired → auto-reset | User starts new workflow |

### Principles
- AI always explains errors in natural language
- AI offers recovery options, not just error messages
- No silent failures

---

## User Experience

### Cheat Sheet

```
📚 Journal Finder — Perintah Tersedia

Cari Jurnal:
  "cari jurnal [topik]"          → Cari 3-5 paper (mode cepat)
  "cari jurnal lengkap [topik]"  → Cari + analisis + report

Simpan ke Zotero:
  "simpan [nomor/judul]"         → Simpan paper ke Zotero
  "simpan semua"                 → Simpan semua hasil pencarian

Citation:
  "citation [nomor/judul]"       → Generate APA citation
  "citation semua"               → Citation semua paper yang dipilih

Lainnya:
  "analisis paper [judul/link]"  → AI analisis paper
  "cari lagi [topik]"            → Pencarian baru
  "?" atau "/help"               → Tampilkan contekannya ini

Tips:
  - Gak perlu hafal, tinggal ngomong aja
  - AI bakal tanya kalau butuh klarifikasi
```

### UX Principles
- Natural language first
- Proactive guidance (AI suggests next steps)
- Minimal friction (brief confirmations)
- Token efficient (only load needed skills)

---

## Citation Format

- **Style:** APA (Author, Year, Title, Journal, DOI)
- **Source:** Metadata from original paper source (DOI, CrossRef API, journal page) — NOT AI-generated from memory
- **Verification:** Metadata validated before citation generation

---

## Implementation Phases

### Phase 1: Individual Skills
- Create `journal-finder` SKILL.md
- Create `zotero` SKILL.md
- Create `journal-help` SKILL.md
- Create wrapper scripts (`journal_search.py`, `zotero_save.py`, `citation_generator.py`)

### Phase 2: Meta Skill
- Create `journal-workflow` SKILL.md
- Implement state management via memory slots
- Test full end-to-end workflow

### Phase 3: Polish
- Error handling refinement
- Token usage optimization
- User testing and feedback iteration
