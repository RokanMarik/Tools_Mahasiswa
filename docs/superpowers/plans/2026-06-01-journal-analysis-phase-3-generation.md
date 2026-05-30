# Journal Analysis System — Phase 3: Article Generation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Article Generator Worker that creates new scientific article drafts from reference journals, with self-review pipeline and journal style template support (APA, IEEE, Vancouver).

**Architecture:** GeneratorWorker follows the same pattern as existing workers — loads system prompt, renders Jinja2 template, calls 9Router. Self-review uses a separate ReviewerWorker-like pass on the generated draft. Citation formatting uses Python-based formatters (not LLM) for APA/IEEE/Vancouver.

**Tech Stack:** Python 3.10+, `requests` (9Router), `jinja2` (prompts + article templates), `pytest` (testing).

**Related Spec:** `docs/superpowers/specs/2026-06-01-journal-analysis-system-design.md` (§3.3 Article Generator Worker)

**Existing Context (Phase 1+2):**
- All workers in `journal_analyzer/workers/` follow same pattern: `__init__(ninerouter_url, ninerouter_key, prompts_dir="journal_analyzer/prompts")`, `run()` returns dict or None, `_chat()` for 9Router, `_load_system_prompt()`, `_build_user_prompt()` with Jinja2
- Imports use bare module names (`from models.article_data import ...`)
- CLI in `journal_analyzer/analyze.py` has modes: read, review, full, gap, data-analysis
- `journal_analyzer/core/output_aggregator.py` handles reader, reviewer, gap_analyzer, data_analysis

---

## File Structure (Phase 3)

```
journal_analyzer/
├── analyze.py                      # MODIFY — add generate mode
├── analyze.config.json             # MODIFY — add generate budget (already exists)
├── workers/
│   ├── generator_worker.py         # CREATE — article generation
│   └── self_review_worker.py       # CREATE — self-review of generated articles
├── prompts/
│   ├── system/
│   │   ├── generator.md            # CREATE
│   │   └── self_review.md          # CREATE
│   └── templates/
│       ├── generator_user.j2       # CREATE
│       └── self_review_user.j2     # CREATE
└── tests/
    ├── test_generator.py           # CREATE
    ├── test_self_review.py         # CREATE
    └── test_integration.py         # MODIFY — add generate pipeline test
```

---

### Task 1: Generator Prompt System

**Files:**
- Create: `journal_analyzer/prompts/system/generator.md`
- Create: `journal_analyzer/prompts/templates/generator_user.j2`

- [ ] **Step 1: Create prompt files**

```markdown
# journal_analyzer/prompts/system/generator.md
Anda adalah penulis artikel ilmiah berpengalaman yang telah mempublikasikan puluhan paper di jurnal internasional bereputasi.
Tugas Anda: membuat draft artikel ilmiah baru berdasarkan jurnal-jurnal referensi yang diberikan.

Bahasa output: Bahasa Indonesia.
Tone: Akademis, formal, dan sesuai standar penulisan ilmiah.

Format output (struktur IMRAD lengkap):
# [JUDUL ARTIKEL]

## ABSTRAK
[Latar belakang, tujuan, metode, hasil, implikasi — dalam 1 paragraf]

## PENDAHULUAN
[Konteks, masalah penelitian, tujuan, novelty]

## TINJAUAN PUSTAKA
[Landasan teori, studi terdahulu, kerangka konseptual]

## METODE
[Desain penelitian, populasi/sampel, instrumen, prosedur, analisis data]

## HASIL
[Temuan utama — gunakan placeholder [DATA] untuk data empiris yang perlu diisi peneliti]

## PEMBAHASAN
[Interpretasi hasil, perbandingan dengan studi terdahulu, implikasi]

## KESIMPULAN
[Kesimpulan utama, keterbatasan, saran riset lanjutan]

## DAFTAR PUSTAKA
[Referensi terformat sesuai {{ citation_style }}]

ATURAN PENTING:
- JANGAN fabrikasi data empiris — gunakan placeholder [DATA DIBUTUHKAN: deskripsi data yang diperlukan]
- JANGAN copy-paste kalimat dari jurnal referensi — sintesis ide, bukan plagiarisme
- Buat argumen yang koheren dan logical flow yang jelas
- Setiap klaim harus didukung referensi atau placeholder data
```

```jinja2
{# journal_analyzer/prompts/templates/generator_user.j2 #}
Buat draft artikel ilmiah berdasarkan referensi berikut:

Pertanyaan/Topik: {{ research_topic }}
{% if methodology %}Metodologi yang diminta: {{ methodology }}{% endif %}
{% if citation_style %}Format sitasi: {{ citation_style }}{% endif %}

{% if reader_summaries %}
Ringkasan Jurnal Referensi:
{% for summary in reader_summaries %}
--- Jurnal {{ loop.index }} ---
{{ summary }}

{% endfor %}
{% endif %}

{% if gap_analysis %}
Research Gap yang Teridentifikasi:
{{ gap_analysis }}
{% endif %}

Buat draft artikel lengkap sesuai format yang ditentukan. Gunakan placeholder [DATA DIBUTUHKAN: ...] untuk data empiris yang perlu diisi.
```

- [ ] **Step 2: Commit**

```bash
git add journal_analyzer/prompts/system/generator.md journal_analyzer/prompts/templates/generator_user.j2
git commit -m "feat: add prompt templates for article generator worker"
```

---

### Task 2: Self-Review Prompt System

**Files:**
- Create: `journal_analyzer/prompts/system/self_review.md`
- Create: `journal_analyzer/prompts/templates/self_review_user.j2`

- [ ] **Step 1: Create prompt files**

```markdown
# journal_analyzer/prompts/system/self_review.md
Anda adalah reviewer internal yang mengecek kualitas draft artikel ilmiah sebelum disubmit.
Tugas Anda: mereview draft yang dihasilkan oleh generator dan memberikan catatan perbaikan.

Bahasa output: Bahasa Indonesia.
Tone: Konstruktif dan spesifik.

Format output:
1. QUALITY SCORE (1-10)
2. STRENGTHS — apa yang sudah bagus
3. ISSUES — masalah yang ditemukan (plagiarisme, inkonsistensi, data fabricasi, logical flow)
4. RECOMMENDATIONS — saran perbaikan spesifik per section
5. DATA PLACEHOLDERS — daftar placeholder [DATA DIBUTUHKAN] yang perlu diisi peneliti

Periksa:
- Apakah ada kalimat yang terdengar seperti copy-paste (potensi plagiarisme)?
- Apakah ada data yang terdengar fabrikasi (bukan placeholder)?
- Apakah logical flow konsisten dari pendahuluan ke conclusion?
- Apakah semua klaim didukung referensi atau placeholder data?
- Apakah struktur IMRAD lengkap dan benar?
```

```jinja2
{# journal_analyzer/prompts/templates/self_review_user.j2 #}
Review draft artikel ilmiah berikut:

{% if research_topic %}Topik: {{ research_topic }}{% endif %}

--- DRAFT ARTIKEL ---
{{ draft_article }}

Berikan review sesuai format yang ditentukan.
```

- [ ] **Step 2: Commit**

```bash
git add journal_analyzer/prompts/system/self_review.md journal_analyzer/prompts/templates/self_review_user.j2
git commit -m "feat: add prompt templates for self-review worker"
```

---

### Task 3: Generator Worker

**Files:**
- Create: `journal_analyzer/workers/generator_worker.py`
- Test: `journal_analyzer/tests/test_generator.py`

- [ ] **Step 1: Write tests**

```python
# journal_analyzer/tests/test_generator.py
from unittest.mock import patch
from workers.generator_worker import GeneratorWorker


def test_generator_calls_chat():
    mock_result = "# DRAFT ARTIKEL\n\n## ABSTRAK\nTest abstract."

    with patch.object(GeneratorWorker, "_chat", return_value=mock_result) as mock_chat:
        worker = GeneratorWorker()
        result = worker.run(
            research_topic="AI in Education",
            reader_summaries=["Summary 1", "Summary 2"],
        )
        mock_chat.assert_called_once()
        assert "draft" in result


def test_generator_returns_structured_output():
    mock_result = "# DRAFT ARTIKEL\n\n## ABSTRAK\nTest."

    with patch.object(GeneratorWorker, "_chat", return_value=mock_result):
        worker = GeneratorWorker()
        result = worker.run(research_topic="Test topic")
        assert isinstance(result, dict)
        assert "draft" in result


def test_generator_with_gap_analysis():
    mock_result = "# DRAFT\n\nAddressing the gap in longitudinal studies."

    with patch.object(GeneratorWorker, "_chat", return_value=mock_result) as mock_chat:
        worker = GeneratorWorker()
        result = worker.run(
            research_topic="Test",
            gap_analysis="Gap: longitudinal studies needed",
        )
        call_args = mock_chat.call_args
        assert "longitudinal studies needed" in call_args[0][1]


def test_generator_handles_error():
    with patch.object(GeneratorWorker, "_chat", side_effect=Exception("API down")):
        worker = GeneratorWorker()
        result = worker.run(research_topic="Test")
        assert result is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest journal_analyzer/tests/test_generator.py -v`
Expected: FAIL.

- [ ] **Step 3: Implement GeneratorWorker**

```python
# journal_analyzer/workers/generator_worker.py
import os
import requests
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class GeneratorWorker:
    """Article generation worker. Creates new article drafts from reference journals."""

    def __init__(
        self,
        ninerouter_url: str | None = None,
        ninerouter_key: str | None = None,
        prompts_dir: str = "journal_analyzer/prompts",
    ):
        self.ninerouter_url = ninerouter_url or os.getenv("NINEROUTER_URL", "http://localhost:20128")
        self.ninerouter_key = ninerouter_key or os.getenv("NINEROUTER_KEY", "")
        self._headers = {"Content-Type": "application/json"}
        if self.ninerouter_key:
            self._headers["Authorization"] = f"Bearer {self.ninerouter_key}"

        self._prompts_dir = Path(prompts_dir)
        self._env = Environment(loader=FileSystemLoader(str(self._prompts_dir / "templates")))

    def run(
        self,
        research_topic: str,
        reader_summaries: list[str] | None = None,
        gap_analysis: str = "",
        methodology: str = "",
        citation_style: str = "APA7",
        model: str = "anthropic/claude-opus-4-20250514",
    ) -> dict | None:
        """Generate an article draft.

        Returns:
            {"draft": str} or None on failure.
        """
        system_prompt = self._load_system_prompt("generator.md")
        user_prompt = self._build_user_prompt(research_topic, reader_summaries, gap_analysis, methodology, citation_style)

        try:
            response = self._chat(system_prompt, user_prompt, model)
            if response is None:
                return None
            return {"draft": response}
        except Exception:
            return None

    def _chat(self, system_prompt: str, user_prompt: str, model: str) -> str | None:
        endpoint = f"{self.ninerouter_url}/v1/chat/completions"
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "max_tokens": 16000,
            "temperature": 0.4,
            "stream": False,
        }
        try:
            response = requests.post(endpoint, headers=self._headers, json=payload, timeout=300)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception:
            return None

    def _load_system_prompt(self, filename: str) -> str:
        path = self._prompts_dir / "system" / filename
        if path.exists():
            return path.read_text(encoding="utf-8")
        return ""

    def _build_user_prompt(
        self,
        research_topic: str,
        reader_summaries: list[str] | None,
        gap_analysis: str,
        methodology: str,
        citation_style: str,
    ) -> str:
        template = self._env.get_template("generator_user.j2")
        return template.render(
            research_topic=research_topic,
            reader_summaries=reader_summaries or [],
            gap_analysis=gap_analysis,
            methodology=methodology,
            citation_style=citation_style,
        )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest journal_analyzer/tests/test_generator.py -v`
Expected: All 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add journal_analyzer/workers/generator_worker.py journal_analyzer/tests/test_generator.py
git commit -m "feat: add GeneratorWorker for article draft generation"
```

---

### Task 4: Self-Review Worker

**Files:**
- Create: `journal_analyzer/workers/self_review_worker.py`
- Test: `journal_analyzer/tests/test_self_review.py`

- [ ] **Step 1: Write tests**

```python
# journal_analyzer/tests/test_self_review.py
from unittest.mock import patch
from workers.self_review_worker import SelfReviewWorker


def test_self_review_calls_chat():
    mock_result = "QUALITY SCORE: 8/10\n\nSTRENGTHS: Good structure."

    with patch.object(SelfReviewWorker, "_chat", return_value=mock_result) as mock_chat:
        worker = SelfReviewWorker()
        result = worker.run(
            draft_article="# DRAFT\n\n## ABSTRAK\nTest abstract.",
            research_topic="AI in Education",
        )
        mock_chat.assert_called_once()
        assert "review" in result


def test_self_review_returns_structured_output():
    mock_result = "QUALITY SCORE: 7\n\nISSUES: Need more references."

    with patch.object(SelfReviewWorker, "_chat", return_value=mock_result):
        worker = SelfReviewWorker()
        result = worker.run(draft_article="# DRAFT\nTest")
        assert isinstance(result, dict)
        assert "review" in result


def test_self_review_handles_error():
    with patch.object(SelfReviewWorker, "_chat", side_effect=Exception("API down")):
        worker = SelfReviewWorker()
        result = worker.run(draft_article="# DRAFT\nTest")
        assert result is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest journal_analyzer/tests/test_self_review.py -v`
Expected: FAIL.

- [ ] **Step 3: Implement SelfReviewWorker**

```python
# journal_analyzer/workers/self_review_worker.py
import os
import requests
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class SelfReviewWorker:
    """Self-review worker. Reviews generated article drafts for quality issues."""

    def __init__(
        self,
        ninerouter_url: str | None = None,
        ninerouter_key: str | None = None,
        prompts_dir: str = "journal_analyzer/prompts",
    ):
        self.ninerouter_url = ninerouter_url or os.getenv("NINEROUTER_URL", "http://localhost:20128")
        self.ninerouter_key = ninerouter_key or os.getenv("NINEROUTER_KEY", "")
        self._headers = {"Content-Type": "application/json"}
        if self.ninerouter_key:
            self._headers["Authorization"] = f"Bearer {self.ninerouter_key}"

        self._prompts_dir = Path(prompts_dir)
        self._env = Environment(loader=FileSystemLoader(str(self._prompts_dir / "templates")))

    def run(
        self,
        draft_article: str,
        research_topic: str = "",
        model: str = "anthropic/claude-sonnet-4-20250514",
    ) -> dict | None:
        """Review a generated article draft.

        Returns:
            {"review": str} or None on failure.
        """
        system_prompt = self._load_system_prompt("self_review.md")
        user_prompt = self._build_user_prompt(draft_article, research_topic)

        try:
            response = self._chat(system_prompt, user_prompt, model)
            if response is None:
                return None
            return {"review": response}
        except Exception:
            return None

    def _chat(self, system_prompt: str, user_prompt: str, model: str) -> str | None:
        endpoint = f"{self.ninerouter_url}/v1/chat/completions"
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "max_tokens": 8000,
            "temperature": 0.2,
            "stream": False,
        }
        try:
            response = requests.post(endpoint, headers=self._headers, json=payload, timeout=180)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception:
            return None

    def _load_system_prompt(self, filename: str) -> str:
        path = self._prompts_dir / "system" / filename
        if path.exists():
            return path.read_text(encoding="utf-8")
        return ""

    def _build_user_prompt(self, draft_article: str, research_topic: str) -> str:
        template = self._env.get_template("self_review_user.j2")
        return template.render(
            draft_article=draft_article,
            research_topic=research_topic,
        )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest journal_analyzer/tests/test_self_review.py -v`
Expected: All 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add journal_analyzer/workers/self_review_worker.py journal_analyzer/tests/test_self_review.py
git commit -m "feat: add SelfReviewWorker for quality checking generated articles"
```

---

### Task 5: Extend Output Aggregator for Generate Mode

**Files:**
- Modify: `journal_analyzer/core/output_aggregator.py`
- Test: `journal_analyzer/tests/test_output_aggregator.py` (append tests)

- [ ] **Step 1: Append tests**

Append to `journal_analyzer/tests/test_output_aggregator.py`:

```python
def test_aggregate_with_generation():
    agg = OutputAggregator()
    result = agg.aggregate({
        "generator": {"status": "success", "data": {"draft": "# DRAFT ARTIKEL\n\nTest content."}},
    })
    assert "Draft Artikel" in result
    assert "Test content" in result


def test_aggregate_with_generation_and_self_review():
    agg = OutputAggregator()
    result = agg.aggregate({
        "generator": {"status": "success", "data": {"draft": "# DRAFT\nContent."}},
        "self_review": {"status": "success", "data": {"review": "QUALITY SCORE: 8/10"}},
    })
    assert "Draft Artikel" in result
    assert "Self-Review" in result
    assert "8/10" in result
```

- [ ] **Step 2: Run test to verify new tests fail**

Run: `python -m pytest journal_analyzer/tests/test_output_aggregator.py -v`
Expected: 2 new tests FAIL.

- [ ] **Step 3: Update OutputAggregator**

Append to the `aggregate` method (before `return "\n".join(parts)`):

```python
        if "generator" in worker_results:
            gen = worker_results["generator"]
            if gen["status"] == "success":
                parts.append("## Draft Artikel\n")
                parts.append(gen["data"].get("draft", "Tidak ada draft."))
            else:
                parts.append("## Draft Artikel\n")
                parts.append(f"[generator] Gagal: {gen.get('error', 'Unknown error')}. Coba lagi nanti.\n")
            parts.append("")

        if "self_review" in worker_results:
            sr = worker_results["self_review"]
            if sr["status"] == "success":
                parts.append("## Self-Review\n")
                parts.append(sr["data"].get("review", "Tidak ada review."))
            else:
                parts.append("## Self-Review\n")
                parts.append(f"[self_review] Gagal: {sr.get('error', 'Unknown error')}. Coba lagi nanti.\n")
            parts.append("")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest journal_analyzer/tests/test_output_aggregator.py -v`
Expected: All 9 tests PASS (7 existing + 2 new).

- [ ] **Step 5: Commit**

```bash
git add journal_analyzer/core/output_aggregator.py journal_analyzer/tests/test_output_aggregator.py
git commit -m "feat: extend OutputAggregator to support generator and self-review"
```

---

### Task 6: Update CLI for Generate Mode

**Files:**
- Modify: `journal_analyzer/analyze.py`
- Modify: `analyze.py` (wrapper at root)

- [ ] **Step 1: Read existing files**

Read `journal_analyzer/analyze.py` and `analyze.py` (root wrapper).

- [ ] **Step 2: Update CLI in analyze.py**

1. Change the argparse choices line to include "generate":
```python
    parser.add_argument("--mode", required=True, choices=["read", "review", "full", "gap", "data-analysis", "generate"], help="Analysis mode")
```

2. Add `--prompt` argument after `--dataset`:
```python
    parser.add_argument("--prompt", help="Research topic/prompt for generate mode")
    parser.add_argument("--methodology", help="Requested methodology for generate mode")
    parser.add_argument("--citation-style", help="Citation style for generate mode (default: APA7)")
```

3. Add runner function before `if __name__`:

```python
def _run_generate(args, article, reader_result, gap_result, cache, content_hash, config, router):
    from workers.generator_worker import GeneratorWorker
    from workers.self_review_worker import SelfReviewWorker

    results = {}

    # Check cache for draft
    cached_draft = cache.get_analysis(content_hash, "generator")
    if cached_draft:
        results["generator"] = {"status": "success", "data": cached_draft}
    else:
        model = router.get_model_name(router.select_model("generate_article", article.word_count))
        reader_summaries = [reader_result["data"]["summary"]] if reader_result and reader_result["status"] == "success" else []
        gap_text = gap_result["data"].get("gap_text", "") if gap_result and gap_result["status"] == "success" else ""

        worker = GeneratorWorker()
        draft_result = worker.run(
            research_topic=args.prompt or "",
            reader_summaries=reader_summaries,
            gap_analysis=gap_text,
            methodology=args.methodology or "",
            citation_style=args.citation_style or "APA7",
            model=model,
        )

        if draft_result is None:
            results["generator"] = {"status": "failed", "error": "Generator gagal"}
        else:
            cache.set_analysis(content_hash, "generator", draft_result)
            results["generator"] = {"status": "success", "data": draft_result}

            # Self-review the draft
            cached_review = cache.get_analysis(content_hash, "self_review")
            if cached_review:
                results["self_review"] = {"status": "success", "data": cached_review}
            else:
                review_worker = SelfReviewWorker()
                review_result = review_worker.run(
                    draft_article=draft_result["draft"],
                    research_topic=args.prompt or "",
                )

                if review_result is None:
                    results["self_review"] = {"status": "failed", "error": "Self-review gagal"}
                else:
                    cache.set_analysis(content_hash, "self_review", review_result)
                    results["self_review"] = {"status": "success", "data": review_result}

    return results
```

4. In the "Execute workers based on mode" section, after the existing mode blocks, add:

```python
    if args.mode == "generate":
        reader_result = _run_reader(article, cache, content_hash, config, router)
        results["reader"] = reader_result
        gap_result = _run_gap_analyzer(article, reader_result, cache, content_hash, config, router)
        results["gap_analyzer"] = gap_result
        gen_results = _run_generate(args, article, reader_result, gap_result, cache, content_hash, config, router)
        results.update(gen_results)
```

- [ ] **Step 3: Update wrapper analyze.py**

Update docstring:

```python
"""Journal Analysis System — Entry point wrapper.

Usage:
    python analyze.py jurnal.pdf --mode read
    python analyze.py jurnal.pdf --mode review
    python analyze.py jurnal.pdf --mode full
    python analyze.py jurnal.pdf --mode gap
    python analyze.py jurnal.pdf --mode generate --prompt "Topik riset"
    python analyze.py --input-text "teks..." --mode review
    python analyze.py --research-question "Pertanyaan riset" --dataset data.csv --mode data-analysis
"""
```

- [ ] **Step 4: Test CLI help**

Run: `python analyze.py --help`
Expected: Shows `--mode {read,review,full,gap,data-analysis,generate}`, `--prompt`, `--methodology`, `--citation-style`.

- [ ] **Step 5: Commit**

```bash
git add journal_analyzer/analyze.py analyze.py
git commit -m "feat: add generate CLI mode with generator + self-review pipeline"
```

---

### Task 7: Integration Test for Generate Mode

**Files:**
- Modify: `journal_analyzer/tests/test_integration.py` (append test)

- [ ] **Step 1: Append integration test**

Append to `journal_analyzer/tests/test_integration.py`:

```python
def test_generate_pipeline():
    """Test: parse → reader → gap analyzer → generator → self-review → aggregate."""
    from unittest.mock import patch
    text = """## ABSTRACT
This study examines AI use in education.

## INTRODUCTION
AI is transforming education.

## METHODOLOGY
Survey of 500 teachers.

## RESULTS
75% reported improved engagement.

## CONCLUSION
More research needed.
"""
    from parsers.text_parser import TextParser
    parser = TextParser()
    article = parser.parse(text)

    from workers.reader_worker import ReaderWorker
    from workers.gap_analyzer_worker import GapAnalyzerWorker
    from workers.generator_worker import GeneratorWorker
    from workers.self_review_worker import SelfReviewWorker
    from core.output_aggregator import OutputAggregator

    # Mock reader
    with patch.object(ReaderWorker, "_chat", return_value="AI improves engagement."):
        reader = ReaderWorker(prompts_dir="journal_analyzer/prompts")
        reader_result = reader.run(article)

    # Mock gap analyzer
    with patch.object(GapAnalyzerWorker, "_chat", return_value="GAP: Longitudinal studies needed."):
        gap_worker = GapAnalyzerWorker(prompts_dir="journal_analyzer/prompts")
        gap_result = gap_worker.run(article, reader_summary="AI improves engagement.")

    # Mock generator
    draft = "# DRAFT ARTIKEL\n\n## ABSTRAK\nAI in education improves engagement.\n\n## DATA DIBUTUHKAN: Empirical results."
    with patch.object(GeneratorWorker, "_chat", return_value=draft):
        gen_worker = GeneratorWorker(prompts_dir="journal_analyzer/prompts")
        gen_result = gen_worker.run(
            research_topic="AI in Education",
            reader_summaries=["AI improves engagement."],
            gap_analysis="GAP: Longitudinal studies needed.",
        )
        assert gen_result is not None
        assert "draft" in gen_result

    # Mock self-review
    review = "QUALITY SCORE: 8/10\n\nSTRENGTHS: Good structure.\nISSUES: Need to fill data placeholders."
    with patch.object(SelfReviewWorker, "_chat", return_value=review):
        review_worker = SelfReviewWorker(prompts_dir="journal_analyzer/prompts")
        review_result = review_worker.run(draft_article=draft, research_topic="AI in Education")
        assert review_result is not None
        assert "review" in review_result

    # Aggregate
    agg = OutputAggregator()
    output = agg.aggregate({
        "reader": {"status": "success", "data": reader_result},
        "gap_analyzer": {"status": "success", "data": gap_result},
        "generator": {"status": "success", "data": gen_result},
        "self_review": {"status": "success", "data": review_result},
    })
    assert "# Ringkasan Jurnal" in output
    assert "## Research Gap" in output
    assert "## Draft Artikel" in output
    assert "## Self-Review" in output
    assert "8/10" in output
```

- [ ] **Step 2: Run all tests**

Run: `python -m pytest journal_analyzer/tests/ -v`
Expected: All tests PASS (77 existing + 1 new = 78 tests).

- [ ] **Step 3: Commit**

```bash
git add journal_analyzer/tests/test_integration.py
git commit -m "test: add Phase 3 integration test for generate pipeline"
```

---

### Task 8: Run All Tests + Final Commit

- [ ] **Step 1: Run all Phase 1+2+3 tests**

Run: `python -m pytest journal_analyzer/tests/ -v --tb=short`
Expected: All 78+ tests PASS.

- [ ] **Step 2: Final commit**

```bash
git add -A
git commit -m "feat: journal analysis system phase 3 complete — article generator with self-review"
```
