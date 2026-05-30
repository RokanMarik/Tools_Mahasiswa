# Design: Journal Analyzer Skill & Reviewer Upgrade

**Date:** 2026-05-30
**Status:** Draft — awaiting user review

## Overview

Upgrade the Journal Analyzer system to 5/5 rating by:
1. Creating a new `.opencode/skills/journal-analyzer` SKILL.md
2. Upgrading `journal_analyzer/prompts/system/reviewer.md` with comprehensive reviewer competencies
3. Fixing existing SKILL.md files and verifying tests

## Architecture

### Component 1: New `journal-analyzer` SKILL.md

**Location:** `.opencode/skills/journal-analyzer/SKILL.md`

**Purpose:** Make the Journal Analyzer CLI discoverable and usable via natural language.

**Triggers:**
- "review jurnal [file/url]" → `--mode review`
- "baca paper ini" → `--mode read`
- "analisis lengkap" → `--mode full`
- "cari research gap" → `--mode gap`
- "bandingkan paper" → `--mode compare`
- "generate draft artikel" → `--mode generate`
- "analisis data riset" → `--mode data-analysis`

**CLI Mapping:**
```
python journal_analyzer/analyze.py <input> --mode <mode> [--options]
```

**Model Selection (via 9Router config):**
- read → light model (summarization)
- review → heavy model (critical appraisal)
- full → heavy model
- gap → medium model
- generate → heavy model
- compare → heavy model
- data-analysis → medium model

**Output:** Markdown to `output/analysis_<hash>.md` + stdout

### Component 2: Upgraded `reviewer.md` Prompt

**Location:** `journal_analyzer/prompts/system/reviewer.md`

**Current:** 20 lines, 6 basic criteria
**Target:** ~55 lines, full 15-competency framework (minus time management)

**Language:** All output in Bahasa Indonesia. Academic terms retained in English (e.g., "effect size", "p-value", "IMRAD", "self-plagiarism").

**Competency coverage:**

| # | Kompetensi | Section in Format |
|---|---|---|
| 1 | Keahlian domain spesifik | `2. DOMAIN & SCOPE FIT` |
| 2 | Literasi statistik | `4. METHODOLOGY & STATISTICAL VALIDITY` |
| 3 | Pemahaman metodologi (kuant/kual/mixed) | `4. METHODOLOGY & STATISTICAL VALIDITY` |
| 4 | Critical appraisal | `3. KEKUATAN` + `5. MASALAH UTAMA` + `11. REKOMENDASI` |
| 5 | Academic writing (feedback jelas, konstruktif) | Throughout — structured format + Bahasa Indonesia output |
| 6 | Structured writing | 11-section fixed format |
| 7 | Diplomatic tone | Prompt instruction: "kritis namun menghargai karya penulis" |
| 8 | Conflict of interest awareness | `7. ETHICS & INTEGRITY CHECK` |
| 9 | Confidentiality | `7. ETHICS & INTEGRITY CHECK` |
| 10 | Objectivity (merit-based, no bias) | `7. ETHICS & INTEGRITY CHECK` + explicit prompt rule |
| 11 | Standar jurnal (scope, formatting, citation) | `10. PUBLICATION READINESS` |
| 12 | Plagiarism detection | `8. PLAGIARISM & ORIGINALITY` |
| 13 | Tren riset terkini | `9. RESEARCH CONTEXT & TRENDS` |
| 14 | Analytical thinking (kontribusi vs klaim) | `5. MASALAH UTAMA` — "klaim berlebihan tanpa dukungan data" |
| 15 | Attention to detail | `6. MASALAH MINOR` — explicit checklist: referensi, tabel, caption, equation, appendix |
| — | Time management | Skip (N/A untuk AI) |

**New format (11 sections):**
```
1. OVERALL ASSESSMENT (Accept / Minor Revision / Major Revision / Reject)
2. DOMAIN & SCOPE FIT
3. KEKUATAN (3-5 poin)
4. METHODOLOGY & STATISTICAL VALIDITY
5. MASALAH UTAMA (klaim berlebihan, gap logika, kelemahan fatal — dengan justifikasi)
6. MASALAH MINOR (per section + checklist: referensi, tabel, caption, equation, appendix)
7. ETHICS & INTEGRITY CHECK (COI, confidentiality, objectivity)
8. PLAGIARISM & ORIGINALITY (self-plagiarism, citation manipulation, duplicate content)
9. RESEARCH CONTEXT & TRENDS (posisi paper terhadap state-of-the-art bidang ini)
10. PUBLICATION READINESS (citation style consistency, formatting, IMRAD compliance)
11. REKOMENDASI (saran konkret, prioritized: must-fix vs nice-to-have)
```

### Component 3: Fix Existing SKILL.md Files

**`journal-workflow/SKILL.md`:**
- Add explicit script references with full paths
- Clarify that it orchestrates journal-finder + zotero (not journal-analyzer)
- No logic changes — documentation only

**`journal-finder-simple/SKILL.md`:**
- No changes needed (284 lines is acceptable for example-rich skill)

### Component 4: Test Verification

**Action:** Run `python -m pytest tests/ journal_analyzer/tests/ -v --tb=short`
**Expected:** All 22+ tests pass
**If fail:** Fix individual test failures (not refactor)

### Component 5: Unified README.md

**Purpose:** Single entry point that maps user intent → correct tool/skill

**Structure:**
```
# Journal Finder & Analyzer System

## Quick Start
## When to Use Which Tool
  - "I want to FIND papers" → journal-finder skill
  - "I want to REVIEW a paper" → journal-analyzer skill (--mode review)
  - "I want to SAVE papers" → zotero skill
  - "I want FULL research workflow" → journal-workflow skill
## Available Modes (Journal Analyzer)
## Available Skills (Journal Finder)
## Environment Setup
```

## Error Handling

| Scenario | Handling |
|---|---|
| Input file not found | "File tidak ditemukan. Cek path-nya." |
| PDF parsing fails | "Gagal parse PDF. Mungkin encrypted atau scan. Coba copy-paste teksnya." |
| Model unavailable | Fallback to next tier (heavy → medium → light) |
| Token budget exceeded | "Token budget habis. Reset besok 00:00. Atau pakai --no-limit." |
| Cache hit | Use cached result, print "[CACHED]" indicator |

## Non-Goals

- Do NOT refactor existing Python modules
- Do NOT change CLI interface (analyze.py args stay the same)
- Do NOT modify journal-finder-simple SKILL.md
- Do NOT add new Python dependencies

## Success Criteria

1. `journal-analyzer` SKILL.md exists and is loadable by opencode
2. `reviewer.md` covers all 15 competency areas (minus time management) with 11-section review format
3. All existing tests pass
4. README.md provides clear entry point
5. journal-workflow SKILL.md has proper script references
