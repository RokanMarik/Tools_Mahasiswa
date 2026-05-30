---
name: journal-workflow
description: Orchestrate full journal research workflow: search → review → save to Zotero → citation. Use when user starts a research session from scratch.
---

# Journal Workflow — Meta Skill

Orchestrates the full research workflow across journal-finder and zotero skills.

## Trigger

Natural language detection:
- User starts research from scratch without specifying a single action
- "aku mau riset tentang [topik]"
- "bantu aku cari dan simpan paper tentang [topik]"
- Sequential: user searches, then saves, then asks for citation (workflow detected)

## Workflow Orchestration

### Full Pipeline
```
1. Search    → journal-finder skill (scripts/journal_search.py)
               Multi-source: Garuda + CrossRef + Semantic Scholar (merged, deduped by DOI)
2. Display   → Show papers with numbers
3. Review    → User picks which papers to save
4. Save      → zotero skill (scripts/zotero_save.py)
5. Citation  → Generate APA citation (scripts/citation_generator.py)
6. Done      → Summary of what was saved
```

### Shortcut: Skip to Step
If user already knows what they want:
- "cari jurnal X" → Step 1 only
- "simpan paper 2" → Skip to Step 4
- "citation paper 1" → Skip to Step 5

## State Management

Use agentmemory slots to track workflow state:

```
Slot: journal_search_results  → JSON of last search results
Slot: journal_selected_papers → Indices of user-selected papers
Slot: journal_session_active  → Boolean, whether workflow is in progress
```

### Setting State
After search succeeds, store results:
- Store the full JSON output from journal_search.py in `journal_search_results`
- Set `journal_session_active` to true

### Reading State
When user says "simpan 1 dan 3":
- Read `journal_search_results` to get paper metadata by index
- Pass selected papers to zotero_save.py

### Clearing State
After workflow completes (save done or user abandons):
- Clear `journal_session_active`
- Keep `journal_search_results` for reference (don't clear immediately)

## Error Recovery

If any step fails:
1. Tell user what went wrong in natural language
2. Offer recovery options (retry, skip, abort)
3. Don't lose state — user can retry from the failed step
4. If Zotero fails mid-save, report which papers succeeded and which failed

## Integration Notes

This skill references:
- `journal-finder` skill for search logic (scripts: `scripts/journal_search.py`)
- `zotero` skill for save/citation logic (scripts: `scripts/zotero_save.py`, `scripts/citation_generator.py`)
- Do NOT duplicate code from those skills — reference them

## Script Paths

All scripts are in the project root directory:
- Search: `python scripts/journal_search.py --topic "<topic>" --limit 3`
- Save: `python scripts/zotero_save.py --api-key "$ZOTERO_API_KEY" --papers '<json>'`
- Citation: `python scripts/citation_generator.py --papers '<json>' --style apa`

## Example Conversation

```
User: bantu aku riset tentang federated learning
AI:   Oke, cari paper tentang "federated learning".
      [executes journal_search.py]

      Nemu 3 paper:
      1. [Title] — [Authors]
      2. [Title] — [Authors]
      3. [Title] — [Authors]

      Mau simpan ke Zotero? Ketik nomornya.

User: 1 dan 3
AI:   [executes zotero_save.py for papers 1 and 3]
      ✅ Paper 1 dan 3 berhasil disimpan.

      Citation APA:
      1. [APA citation for paper 1]
      3. [APA citation for paper 3]

      Ada yang mau ditambah?
```
