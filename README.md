# Journal Finder & Analyzer System

Sistem lengkap untuk mencari, menganalisis, me-review, dan menyimpan jurnal ilmiah. Didukung oleh 9Router AI gateway.

**Status:** Production Ready | **Tests:** 213 passed

---

## Quick Start

**"Saya mau cari paper tentang topik X"** → Pakai skill `journal-finder`
**"Saya mau review paper yang sudah saya punya"** → Pakai skill `journal-analyzer`
**"Saya mau simpan paper ke Zotero"** → Pakai skill `zotero`
**"Saya mau workflow lengkap dari cari sampai simpan"** → Pakai skill `journal-workflow`

---

## Kapan Pakai Apa

| Kebutuhan | Skill / Tool | Cara Pakai |
|---|---|---|
| Cari paper/jurnal | `journal-finder` | Bilang aja: "cari paper tentang machine learning" |
| Review paper (peer review Q1/Q2) | `journal-analyzer` --mode review | `python journal_analyzer/analyze.py paper.pdf --mode review` |
| Ringkas paper | `journal-analyzer` --mode read | `python journal_analyzer/analyze.py paper.pdf --mode read` |
| Analisis lengkap (read + review) | `journal-analyzer` --mode full | `python journal_analyzer/analyze.py paper.pdf --mode full` |
| Cari research gap | `journal-analyzer` --mode gap | `python journal_analyzer/analyze.py paper.pdf --mode gap` |
| Generate draft artikel | `journal-analyzer` --mode generate | `python journal_analyzer/analyze.py --mode generate --prompt "topik"` |
| Bandingkan paper | `journal-analyzer` --mode compare | `python journal_analyzer/analyze.py p1.pdf --mode compare --compare p2.pdf` |
| Simpan ke Zotero | `zotero` | Bilang: "simpan paper 1 dan 3" |
| Generate citation | `zotero` | Bilang: "citation paper 1" |
| Workflow lengkap (cari → simpan → citation) | `journal-workflow` | Bilang: "bantu riset tentang federated learning" |

---

## Journal Analyzer — 7 Mode

### `--mode read` — Baca & Ringkas
Input: PDF, URL, atau teks. Output: Ringkasan paper (abstrak, temuan kunci, metodologi).

### `--mode review` — Peer Review (Q1/Q2)
Input: PDF, URL, atau teks. Output: Review 11 section lengkap:
1. Overall Assessment (Accept/Minor/Major/Reject)
2. Domain & Scope Fit
3. Kekuatan
4. Methodology & Statistical Validity
5. Masalah Utama
6. Masalah Minor (+ checklist)
7. Ethics & Integrity Check
8. Plagiarism & Originality
9. Research Context & Trends
10. Publication Readiness
11. Rekomendasi (prioritized)

### `--mode full` — Analisis Lengkap
Kombinasi read + review. Output: Ringkasan + full peer review.

### `--mode gap` — Research Gap Analysis
Input: PDF. Output: Gap dalam riset yang bisa jadi peluang paper baru.

### `--mode generate` — Generate Draft Artikel
Input: Topik riset. Output: Draft artikel ilmiah + self-review.
```bash
python journal_analyzer/analyze.py --mode generate --prompt "federated learning di healthcare"
```

### `--mode compare` — Bandingkan Paper
Input: 2+ file PDF. Output: Perbandingan sistematis.
```bash
python journal_analyzer/analyze.py paper1.pdf --mode compare --compare paper2.pdf paper3.pdf
```

### `--mode data-analysis` — Analisis Data Riset
Input: Research question + dataset (CSV/Excel). Output: Analisis statistik.
```bash
python journal_analyzer/analyze.py --mode data-analysis --research-question "..." --dataset data.csv
```

---

## Skills (opencode)

| Skill | Deskripsi | Trigger |
|---|---|---|
| `journal-finder` | Cari paper via OpenAlex + Garuda + SearXNG | "cari jurnal [topik]" |
| `journal-finder-simple` | Cari cepat, 3 link open access | "cari jurnal dong" |
| `journal-analyzer` | Analisis/review/generate paper | "review jurnal.pdf" |
| `zotero` | Simpan paper + generate citation | "simpan ke zotero" |
| `journal-workflow` | Orchestrate: cari → review → simpan → citation | "bantu riset tentang [topik]" |
| `journal-help` | Cheat sheet perintah | "?" atau "/help" |

---

## Environment Setup

```powershell
# Windows PowerShell
$env:NINEROUTER_URL = "http://localhost:20128"
$env:NINEROUTER_KEY = "sk-your-key-here"

# Untuk Zotero (opsional)
$env:ZOTERO_API_KEY = "your-zotero-api-key"
```

```bash
# Linux/Mac
export NINEROUTER_URL="http://localhost:20128"
export NINEROUTER_KEY="sk-your-key-here"
export ZOTERO_API_KEY="your-zotero-api-key"
```

---

## File Structure

```
Mencari_Jurnal_Ilmiah/
├── scripts/                          # CLI wrapper scripts
│   ├── journal_search.py             # Multi-source paper search
│   ├── zotero_save.py                # Save to Zotero
│   └── citation_generator.py         # Generate APA/IEEE/MLA/Chicago citations
├── modules/                          # Python modules (journal finder system)
│   ├── search/                       # OpenAlex, Garuda, SearXNG sources
│   └── zotero/                       # Zotero client, formatter, analyzer
├── journal_analyzer/                 # Journal analyzer system
│   ├── analyze.py                    # CLI orchestrator
│   ├── workers/                      # Reader, Reviewer, Generator, etc.
│   ├── prompts/                      # System prompts + Jinja2 templates
│   └── tests/                        # Analyzer-specific tests
├── tests/                            # Journal finder tests
├── .opencode/skills/                 # opencode skills
│   ├── journal-finder/
│   ├── journal-finder-simple/
│   ├── journal-analyzer/             # ← NEW
│   ├── zotero/
│   ├── journal-workflow/
│   └── journal-help/
├── output/                           # Generated analysis files
└── cache/                            # Search result cache
```

---

## Testing

```bash
# Run all tests (213 total)
python -m pytest tests/ journal_analyzer/tests/ -v

# Run specific test file
python -m pytest tests/test_scoring.py -v
python -m pytest journal_analyzer/tests/test_reviewer_worker.py -v
```

---

## Architecture

### Journal Finder Pipeline
```
User → journal-workflow (orchestrator)
  ├── journal-finder → OpenAlex + Garuda + SearXNG → deduplicate → score → rank
  ├── User picks papers
  ├── zotero → save to library
  └── citation → APA/IEEE/MLA/Chicago
```

### Journal Analyzer Pipeline
```
User → analyze.py --mode <mode>
  ├── parse input (PDF/URL/text) → StructuredArticleData
  ├── select model (light/medium/heavy via 9Router)
  ├── run worker(s) (Reader, Reviewer, Generator, etc.)
  ├── aggregate output
  └── save to output/ + stdout
```

---

**Built with:** Python 3.10+, 9Router AI Gateway, pytest
**Tests:** 213 passed ✅
**Last updated:** 2026-05-30
