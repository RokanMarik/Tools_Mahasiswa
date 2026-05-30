# Journal Analysis System — Design Spec

**Date:** 2026-06-01
**Status:** Approved
**Author:** AI Agent + User Collaboration

---

## 1. Overview

A personal-use modular pipeline system that reads, analyzes, reviews, and generates academic journal articles. Supports PDF, plain text, and DOI/URL input. All output in Bahasa Indonesia. Auto-selects LLM models via 9Router based on task complexity.

### Core Capabilities

| Capability | Description |
|---|---|
| **Smart Reader** | Read and summarize journals without losing essence or scientific value |
| **Article Reviewer** | International journal-level peer review (methodology, statistics, structure, logic, ethics) |
| **Gap Analyzer** | Identify research gaps and suggest follow-up research |
| **Article Generator** | Create new scientific articles from submitted reference journals |
| **Data Analysis (In-Journal)** | Analyze and validate statistical methods within reviewed papers |
| **Data Analysis (Own Data)** | Analyze user's own research datasets with method recommendations |

---

## 2. Architecture

### 2.1 Pipeline

```
┌─────────────────────────────────────────────────────────┐
│                    analyze.py                           │
│              (Orchestrator / CLI Entry Point)            │
│                                                         │
│  Input: PDF / Teks / DOI / URL                         │
│  Output: Analisis lengkap dalam Bahasa Indonesia        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│           Parser Layer                  │
│  ┌───────────┐ ┌──────────┐ ┌────────┐ │
│  │ PDFParser │ │TextParser│ │URLFetch│ │
│  └─────┬─────┘ └────┬─────┘ └───┬────┘ │
└────────┼────────────┼───────────┼───────┘
         │            │           │
         ▼            ▼           ▼
┌─────────────────────────────────────────┐
│         StructuredArticleData           │
│  (judul, abstrak, metodologi, hasil,    │
│   referensi, tabel, dll)                │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│         Model Router                    │
│  Auto-pilih model via 9Router:          │
│  • Ringan → parsing, ekstrak            │
│  • Menengah → struktur, format          │
│  • Berat → critical appraisal, gap      │
└────────────────────┬────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Reader   │  │ Reviewer │  │  Gap     │
│ Worker   │  │ Worker   │  │ Analyzer │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     ▼             ▼             ▼
┌─────────────────────────────────────────┐
│         Output Aggregator               │
│  Gabungkan semua hasil → Bahasa Indo    │
│  Format: Markdown / Terminal / JSON     │
└─────────────────────────────────────────┘
```

### 2.2 Execution Flow

Workers execute with dependency awareness:

1. **Parser** → StructuredArticleData
2. **Reader Worker** → Summary (must run first, provides context)
3. **Reviewer Worker** → Detailed review (depends on Reader output)
4. **Gap Analyzer** → Research gaps (parallel-capable with Reviewer)
5. **Article Generator** → New article draft (separate trigger, not automatic)
6. **Data Analysis Worker** → User's own data analysis (separate trigger)

---

## 3. Components

### 3.1 Parser Layer

| Component | Responsibility | Details |
|---|---|---|
| **PDFParser** | Extract text from PDF files | Handle multi-column layouts, tables, figure captions, references. Uses `pymupdf` or `pdfplumber`. OCR fallback via `pypdfium2`/`tesseract` for scanned PDFs. |
| **TextParser** | Parse plain text/markdown input | Detect sections from headings (Abstract, Introduction, Methods, etc.) |
| **URLFetcher** | Fetch content from DOI or URL | Uses 9router-web-fetch → markdown → parse into StructuredArticleData |

All parsers produce the same output format: `StructuredArticleData`.

### 3.2 StructuredArticleData Model

Shared data model that all workers read and work from:

```
StructuredArticleData:
├── metadata
│   ├── title: str
│   ├── authors: list[str]
│   ├── journal_name: str
│   ├── publication_year: int
│   ├── doi: str
│   └── keywords: list[str]
├── sections: dict[str, str]
│   ├── abstract
│   ├── introduction
│   ├── literature_review
│   ├── methodology
│   ├── results
│   ├── discussion
│   ├── conclusion
│   └── references
├── methodology_type: str        → kualitatif | kuantitatif | mixed
├── research_gap: str            → AI-identified gap
├── key_findings: list[str]      → main findings
├── statistical_methods: list[str] → statistical methods used
├── chunks: list[Chunk]          → for long documents (see §7)
└── raw_text: str                → full text fallback
```

### 3.3 Workers

#### Reader Worker (Smart Summarizer)
- **Input:** StructuredArticleData
- **Task:** Summarize without losing essence — richer than the original abstract
- **Output:** Structured summary (background, objectives, methods, results, implications)
- **Model Tier:** Medium
- **Token Budget:** 2K-8K

#### Reviewer Worker (Peer Reviewer)
- **Input:** StructuredArticleData (+ Reader summary as context)
- **Task:** Full international journal-level peer review:
  - IMRAD structure completeness check
  - Methodology appropriateness for research objectives
  - Statistical validity (methods, sample size, assumptions, effect size)
  - Logical flow and argument consistency
  - Real contribution vs. excessive claims
  - Reference adequacy (sufficient, relevant, current)
  - Potential plagiarism/self-plagiarism detection
  - Format and citation style check (APA, Vancouver, IEEE, etc.)
- **Output:** Structured review (Accept / Minor Revision / Major Revision / Reject) + detailed comments per section
- **Model Tier:** Heavy
- **Token Budget:** 8K-32K

#### Gap Analyzer Worker
- **Input:** StructuredArticleData (optionally + multiple papers for comparison)
- **Task:** Identify research gaps — unanswered questions, follow-up opportunities
- **Output:** List of gaps + suggested future research directions
- **Model Tier:** Medium (simple) or Heavy (complex comparison)
- **Token Budget:** 2K-16K

#### Article Generator Worker
- **Input:** 1+ reference journals + user prompt ("Buat artikel tentang X dengan metode Y")
- **Task:** Synthesize a new article draft:
  - Full IMRAD structure
  - Synthesis from reference journals (not copy-paste)
  - Methodology per user request
  - Formatted references (APA/Vancouver/IEEE)
  - Self-review: plagiarism check, consistency, logical flow
- **Output:** Draft article (Markdown/LaTeX) + notes on sources, sections needing user's own data, improvement suggestions
- **Constraints:**
  - Does NOT fabricate data — marks placeholders: `[DATA DIBUTUHKAN: isi dengan hasil riset kamu]`
  - Does NOT plagiarize — synthesizes ideas, does not copy sentences
  - Can follow target journal style
- **Model Tier:** Heavy
- **Token Budget:** 8K-40K

#### Data Analysis Worker (Own Data)
- **Input:** Dataset (CSV/Excel) + research question description
- **Task:**
  - Auto-detect data types (nominal, ordinal, interval, ratio)
  - Descriptive statistics (mean, SD, distribution, outliers)
  - Recommend analysis methods based on data type, variable count, hypothesis
  - Run statistical analysis via Python (scipy, statsmodels, pandas)
  - Interpret results in Bahasa Indonesia
- **Output:** Descriptive summary, method recommendations with justification, test results (values, p-values, effect sizes), interpretation, visualization suggestions, article writing recommendations
- **Model Tier:** Medium (LLM only interprets results; computation is Python)
- **Token Budget:** 2K-10K

#### Data Analysis (In-Journal) — Part of Reviewer Worker
Embedded in Reviewer Worker's evaluation checklist:
- Statistical method appropriateness
- Sample size adequacy
- Interpretation validity (e.g., correlation vs. causation claims)
- Statistical assumptions reported and met
- Effect size vs. statistical significance
- Data visualization quality

---

## 4. CLI Interface

```bash
# Mode 1: Read & summarize (fast)
python analyze.py jurnal.pdf --mode read

# Mode 2: Full review (Reader + Reviewer)
python analyze.py jurnal.pdf --mode review

# Mode 3: Full analysis (Reader + Reviewer + Gap Analyzer)
python analyze.py jurnal.pdf --mode full

# Mode 4: Generate new article from reference journals
python analyze.py jurnal.pdf --mode generate --prompt "Buat artikel tentang X"

# Mode 5: Compare multiple papers
python analyze.py paper1.pdf paper2.pdf paper3.pdf --mode compare

# Input from URL/DOI
python analyze.py "https://doi.org/10.xxxx/xxxxx" --mode full

# Input from text
python analyze.py --input-text "paste teks di sini..." --mode review

# Analyze own dataset
python analyze.py --data dataset.csv --research-question "Pengaruh X terhadap Y" --mode data-analysis

# Analyze data + compare with reference journals
python analyze.py --data dataset.csv --compare jurnal.pdf --mode data-analysis

# Bypass token budget limit
python analyze.py jurnal.pdf --mode full --no-limit
```

---

## 5. Model Router Heuristics

### Tier Definitions

| Tier | Example Models | When Used | Est. Tokens |
|---|---|---|---|
| **Light** | google/gemini-2.0-flash, anthropic/claude-haiku | Parsing, metadata extraction, format check, short summaries | 500-2K |
| **Medium** | anthropic/claude-sonnet-4-20250514, openai/gpt-4o | Full summaries, structure review, initial gap identification, translation | 2K-8K |
| **Heavy** | anthropic/claude-opus-4-20250514, openai/o1, openai/o3-mini | Critical appraisal, methodology deep-review, statistical validity, article generation | 8K-32K |

### Routing Rules

```
IF task IN [parse, extract_metadata, format_check]:
    → Light

IF task IN [summarize, translate, structure_review]:
    IF input_size < 5000 words: → Medium
    ELSE: → Heavy

IF task IN [critical_appraisal, methodology_review,
            statistical_validation, generate_article]:
    → Heavy

IF task == gap_analysis:
    IF complexity_hint == simple: → Medium
    ELSE: → Heavy

IF task == data_analysis_own:
    → Medium (LLM interprets; Python computes)
```

### Fallback Chain

```
Primary model fails → Same tier (alternative model)
                    → 1 tier lower
                    → 2 tiers lower
                    → Skip worker, display error
```

---

## 6. Token Budget Management

### Budget Structure

```
TokenBudget:
├── daily_limit: int           → default 50,000 tokens/day (user configurable)
├── used_today: int            → counter, resets at 00:00
├── per_task_budget: dict      → allocation per mode:
│   ├── read: 5,000
│   ├── review: 15,000
│   ├── full: 30,000
│   ├── generate: 40,000
│   └── data_analysis: 10,000
└── cost_estimate: float       → estimated cost (if 9Router provides pricing)
```

### Behavior

| Condition | Action |
|---|---|
| 80% budget used | Terminal warning: "⚠️ 80% token budget terpakai hari ini" |
| 100% budget used | Stop new analysis. Cache still readable. Error: "Token budget habis, reset besok 00:00" |
| Task exceeds per_task_budget | Chunk input, analyze per section, continue with remaining budget |
| User overrides | `--no-limit` flag bypasses limit (still warns) |

### Configuration File

```json
// analyze.config.json
{
  "token_budget": {
    "daily_limit": 50000,
    "per_task": {
      "read": 5000,
      "review": 15000,
      "full": 30000,
      "generate": 40000,
      "data_analysis": 10000
    }
  },
  "default_models": {
    "light": "google/gemini-2.0-flash",
    "medium": "anthropic/claude-sonnet-4-20250514",
    "heavy": "anthropic/claude-opus-4-20250514"
  },
  "cache_ttl_days": 7,
  "output_language": "id",
  "citation_style": "APA7"
}
```

---

## 7. Chunking Strategy for Long Documents

### Thresholds

| Document Size | Strategy |
|---|---|
| < 5,000 words | Process directly, no chunking |
| 5,000 - 20,000 words | Chunk by section (Abstract, Intro, Methods, Results, Discussion, Conclusion) |
| > 20,000 words | Sub-chunk per section (each section max 5,000 words) |

### Flow

```
Paper 50 pages (~25,000 words)
│
├── Chunk 1: Abstract + Introduction    → 3,000 words
├── Chunk 2: Literature Review          → 5,000 words (sub-chunk A: 2,500, B: 2,500)
├── Chunk 3: Methodology                → 4,000 words
├── Chunk 4: Results                    → 5,000 words (sub-chunk A: 2,500, B: 2,500)
├── Chunk 5: Discussion                 → 5,000 words (sub-chunk A: 2,500, B: 2,500)
├── Chunk 6: Conclusion + References    → 3,000 words
│
└── Each chunk analyzed separately
    │
    └── Aggregator combines results:
        • Per-section summary → global summary
        • Per-section review → global review
        • Cross-section consistency check (requires all chunks complete)
```

### Cross-Section Consistency Check

After all chunks are processed, a validation pass runs — medium model reads all chunk summaries and checks:
- Are results in Results section consistent with claims in Discussion?
- Does methodology in Methods section match analysis in Results?
- Does conclusion answer the research question from Introduction?

---

## 8. Error Handling

### Layer 1 — Parser

| Error | Handling |
|---|---|
| PDF corrupt / scanned (not text) | OCR fallback (`pypdfium2` or `tesseract`). If fails → clear message: "PDF ini gambar/scan, tidak bisa diekstrak" |
| Invalid URL/DOI | Retry once with alternative URL format. Fail → clear error: "DOI tidak ditemukan" |
| Text too short (< 500 words) | Warning: "Teks terlalu pendek untuk analisis meaningful" but still process |

### Layer 2 — Worker

| Error | Handling |
|---|---|
| 9Router down / model unavailable | Retry with fallback model (heavy → medium → light). All fail → save partial results |
| Token limit exceeded | Chunk input by section, analyze per part, then combine |
| Timeout | Retry once with longer timeout. Fail → skip that worker, other workers continue |

### Layer 3 — System

| Error | Handling |
|---|---|
| Partial failure (e.g., Reviewer fails, Reader succeeds) | Display successful results, mark failed: "[Reviewer] Gagal: [reason]. Coba lagi nanti." |
| All workers fail | Error summary + troubleshooting suggestions |

---

## 9. Caching

### Structure

```
cache/
├── parsed/          → Parse results (StructuredArticleData as JSON)
├── analysis/        → Analysis results per worker
└── models/          → Model selection cache (optional)
```

### Cache Key

Content hash (not filename) — same paper from different sources still hits cache.

### Policy

- **Parse cache:** Permanent (PDF does not change)
- **Analysis cache:** 7 days (analysis may become outdated if newer models are better)
- **Auto-invalidate:** If the model used changes, analysis cache is cleared

### Benefit

Same paper analyzed twice → instant, zero token usage.

---

## 10. Prompt Design System

Each worker has structured prompt templates, not hardcoded strings:

### Structure

```
prompts/
├── system/
│   ├── reviewer.md          # Reviewer system prompt
│   ├── reader.md            # Reader system prompt
│   ├── gap_analyzer.md      # Gap analyzer system prompt
│   ├── generator.md         # Article generator system prompt
│   └── data_analysis.md     # Data analysis interpreter system prompt
└── templates/
    ├── reviewer_user.j2     # Jinja2 template for user prompt
    ├── reader_user.j2
    └── ...
```

### Example: Reviewer System Prompt

```
Anda adalah peer reviewer jurnal internasional bereputasi (Q1/Q2).
Tugas Anda: mengevaluasi naskah ilmiah secara objektif, konstruktif, dan mendalam.

Bahasa output: Bahasa Indonesia.
Tone: Profesional, kritis namun menghargai karya penulis.

Format review:
1. OVERALL ASSESSMENT (Accept / Minor Revision / Major Revision / Reject)
2. STRENGTHS (3-5 poin)
3. MAJOR ISSUES (jika ada — dengan justifikasi)
4. MINOR ISSUES (jika ada — spesifik per section)
5. RECOMMENDATIONS (saran konkret untuk perbaikan)

Kriteria evaluasi:
- Originalitas dan kontribusi
- Kesesuaian metode dengan tujuan riset
- Validitas analisis data dan statistik
- Koherensi argumen (logical flow)
- Kelengkapan dan relevansi referensi
- Kejelasan penulisan dan struktur IMRAD
```

User prompts are dynamically built using Jinja2 templates, injecting data from StructuredArticleData.

### Benefits

- Prompts are editable without touching code
- Version-controllable
- Easy to A/B test prompt variants
- Clear separation of logic and prompt content

---

## 11. Testing Strategy

| Level | Scope | Tools | Mock? |
|---|---|---|---|
| **Unit** | Parsers, models, cache, individual worker logic | pytest | ✅ Mock 9Router responses |
| **Integration** | End-to-end pipeline (Parser → Worker → Aggregator) | pytest + fixtures | ✅ Sample paper fixtures (PDF + expected output) |
| **Model Router** | Routing heuristics, fallback chain | pytest | ✅ Mock model availability |
| **Token Budget** | Tracking, limits, warnings, overrides | pytest | ✅ Mock counter |
| **Chunking** | Long papers, sub-chunks, cross-section check | pytest + 50-page paper fixture | ✅ |
| **E2E (optional)** | Real 9Router call with real paper | pytest (mark=slow) | ❌ Real call, skipped in CI |

```bash
# Quick tests (mock, < 10 seconds)
pytest tests/ -v

# Full tests (including slow tests, requires 9Router active)
pytest tests/ -v --run-slow
```

---

## 12. File Structure

```
Mencari_Jurnal_Ilmiah/
├── analyze.py                    # Orchestrator / CLI entry point
├── analyze.config.json           # User configuration
├── parsers/
│   ├── __init__.py
│   ├── pdf_parser.py             # PDF extraction
│   ├── text_parser.py            # Plain text parsing
│   └── url_fetcher.py            # DOI/URL fetching via 9Router
├── workers/
│   ├── __init__.py
│   ├── reader_worker.py          # Smart summarizer
│   ├── reviewer_worker.py        # Peer reviewer (incl. in-journal data analysis)
│   ├── gap_analyzer_worker.py    # Research gap identification
│   ├── generator_worker.py       # Article generation
│   └── data_analysis_worker.py   # Analyze user's own data
├── models/
│   ├── __init__.py
│   ├── article_data.py           # StructuredArticleData model
│   └── model_router.py           # Auto-select model via 9Router
├── core/
│   ├── __init__.py
│   ├── cache.py                  # Caching layer
│   ├── error_handler.py          # Error handling across layers
│   ├── token_budget.py           # Token budget tracking and management
│   └── output_aggregator.py      # Combine worker outputs → Bahasa Indonesia
├── prompts/
│   ├── system/                   # System prompts per worker
│   └── templates/                # Jinja2 user prompt templates
├── cache/                        # Auto-created cache directory
│   ├── parsed/
│   └── analysis/
├── output/                       # Generated articles, reports
└── tests/
    ├── __init__.py
    ├── test_parsers.py
    ├── test_workers.py
    ├── test_model_router.py
    ├── test_token_budget.py
    ├── test_chunking.py
    └── test_integration.py
```

---

## 13. Implementation Phases

### Phase 1: Foundation (Reader + Reviewer)
- Parser layer (PDF, Text, URL)
- StructuredArticleData model
- Model Router with heuristics
- Token Budget management
- Reader Worker
- Reviewer Worker (including in-journal data analysis)
- Caching layer
- Error handling
- Prompt system
- CLI entry point

### Phase 2: Analysis Expansion
- Gap Analyzer Worker
- Data Analysis Worker (own data)
- Chunking strategy for long documents
- Cross-section consistency check
- Output Aggregator improvements

### Phase 3: Generation
- Article Generator Worker
- Self-review pipeline for generated articles
- Template support for journal styles (APA, IEEE, Vancouver)

### Phase 4: Polish
- Comparison mode (multi-paper)
- Visualization output for data analysis
- Integration with existing Zotero modules
- Full test suite

---

## 14. Constraints & Guardrails

1. **No data fabrication** — Generator marks placeholders where real data is needed
2. **No plagiarism** — Synthesis of ideas, not sentence copying
3. **Confidentiality** — All processing local; no data sent outside 9Router
4. **Objectivity** — Review based on scientific merit, not author/institution name
5. **Token efficiency** — Budget management, caching, model tiering
6. **Graceful degradation** — Partial results better than no results
