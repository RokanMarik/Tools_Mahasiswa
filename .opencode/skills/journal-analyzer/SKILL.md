---
name: journal-analyzer
description: Analyze, review, and generate academic journal articles. Use when user wants to review a paper, read/summarize a journal, find research gaps, generate article drafts, compare papers, or analyze research data.
---

# Journal Analyzer Skill

CLI-based academic journal analysis system with 7 modes: read, review, full, gap, generate, compare, data-analysis.

## Trigger

Natural language detection:
- "review jurnal [file/url]" → `--mode review`
- "baca paper ini" / "ringkas jurnal" → `--mode read`
- "analisis lengkap" / "review lengkap" → `--mode full`
- "cari research gap" / "gap analysis" → `--mode gap`
- "bandingkan paper" / "compare paper" → `--mode compare`
- "generate draft artikel" / "buat draft paper" → `--mode generate`
- "analisis data riset" / "data analysis" → `--mode data-analysis`

## Prerequisites

- `NINEROUTER_URL` and `NINEROUTER_KEY` environment variables set
- Python 3.10+ with dependencies installed
- For PDF input: `pypdf` or equivalent parser

## Workflow

### Step 1: Parse User Intent → Mode Mapping

| User says | Mode | Input needed |
|---|---|---|
| "review jurnal.pdf" | review | PDF file, URL, or text |
| "baca paper ini" | read | PDF file, URL, or text |
| "analisis lengkap" | full | PDF file, URL, or text |
| "cari research gap" | gap | PDF file, URL, or text |
| "bandingkan paper" | compare | Multiple PDF files |
| "generate draft" | generate | Research topic (text prompt) |
| "analisis data" | data-analysis | Research question + dataset |

### Step 2: Execute CLI

```bash
# Basic: single file review
python journal_analyzer/analyze.py <input> --mode <mode>

# With text input
python journal_analyzer/analyze.py --input-text "teks jurnal..." --mode review

# Generate mode (no input file needed)
python journal_analyzer/analyze.py --mode generate --prompt "Topik riset"

# Compare mode (multiple files)
python journal_analyzer/analyze.py paper1.pdf --mode compare --compare paper2.pdf paper3.pdf

# Data analysis mode
python journal_analyzer/analyze.py --mode data-analysis --research-question "Pertanyaan" --dataset data.csv

# Bypass token budget
python journal_analyzer/analyze.py jurnal.pdf --mode review --no-limit
```

### Step 3: Parse Output

Output goes to two places:
1. **stdout** — formatted markdown review/analysis
2. **File** — `output/analysis_<hash>.md`

Read the output file for the full result. The stdout output is also available in the terminal.

### Step 4: Present to User

Display the output in a readable format. Key sections depend on mode:

**review/full modes:**
- OVERALL ASSESSMENT (Accept / Minor Revision / Major Revision / Reject)
- DOMAIN & SCOPE FIT
- KEKUATAN
- METHODOLOGY & STATISTICAL VALIDITY
- MASALAH UTAMA
- MASALAH MINOR
- ETHICS & INTEGRITY CHECK
- PLAGIARISM & ORIGINALITY
- RESEARCH CONTEXT & TRENDS
- PUBLICATION READINESS
- REKOMENDASI

**read mode:** Summary of the paper (abstract, key findings, methodology)
**gap mode:** Research gaps identified
**generate mode:** Draft article + self-review
**compare mode:** Comparison table of multiple papers
**data-analysis mode:** Statistical analysis results

## Error Handling

| Scenario | Response |
|---|---|
| File not found | "File tidak ditemukan. Cek path-nya." |
| PDF parse fails | "Gagal parse PDF. Mungkin encrypted atau scan. Coba pakai `--input-text` dan paste teksnya." |
| Model unavailable | Retry with fallback model. Report if all tiers fail. |
| Token budget exceeded | "Token budget habis. Reset besok 00:00. Atau pakai `--no-limit`." |
| Cache hit | Use cached result. Print "[CACHED]" indicator. |
| No input for review/gap | "Butuh input: file PDF, URL, atau teks. Contoh: `jurnal.pdf` atau `--input-text '...'`" |

## Model Selection (Automatic via 9Router)

| Mode | Model tier | Reason |
|---|---|---|
| read | light | Summarization |
| review | heavy | Critical appraisal (needs deep reasoning) |
| full | heavy | Read + review combined |
| gap | medium | Pattern matching + analysis |
| generate | heavy | Article generation (complex) |
| compare | heavy | Multi-paper comparison |
| data-analysis | medium | Statistical reasoning |

## State

After analysis, the result is cached. If the same input is analyzed again, the cached result is returned.

Cache location: `journal_analyzer/.cache/`
Output files: `output/analysis_<hash>.md`

## Example Conversations

### Example 1: Review a PDF
```
User: review jurnal.pdf
AI:   [executes: python journal_analyzer/analyze.py jurnal.pdf --mode review]

      ## OVERALL ASSESSMENT
      Minor Revision

      ## DOMAIN & SCOPE FIT
      [analysis...]

      [full 11-section review output]
```

### Example 2: Quick Summary
```
User: baca paper ini
AI:   Butuh file-nya. Kirim PDF atau paste teksnya.

User: jurnal.pdf
AI:   [executes: python journal_analyzer/analyze.py jurnal.pdf --mode read]

      [summary output]
```

### Example 3: Full Analysis
```
User: analisis lengkap paper ini
AI:   [executes: python journal_analyzer/analyze.py paper.pdf --mode full]

      [reader summary + full reviewer output]
```

### Example 4: Generate Draft
```
User: generate draft artikel tentang federated learning di healthcare
AI:   [executes: python journal_analyzer/analyze.py --mode generate --prompt "federated learning di healthcare"]

      [draft article + self-review output]
```

### Example 5: Compare Papers
```
User: bandingkan paper1.pdf dan paper2.pdf
AI:   [executes: python journal_analyzer/analyze.py paper1.pdf --mode compare --compare paper2.pdf]

      [comparison output]
```
