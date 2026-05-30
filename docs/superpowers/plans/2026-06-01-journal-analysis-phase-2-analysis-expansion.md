# Journal Analysis System — Phase 2: Analysis Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Gap Analyzer Worker, Data Analysis Worker (own data), chunking strategy for long documents with cross-section consistency check, and extend the Output Aggregator and CLI to support the new capabilities.

**Architecture:** New workers (GapAnalyzer, DataAnalysisWorker) follow the same pattern as ReaderWorker/ReviewerWorker — load system prompt from `journal_analyzer/prompts/`, call 9Router via `_chat()`, return structured dict. Chunking is handled by a new `Chunker` class in `core/` that splits long documents by section. The CLI adds `--mode gap` and `--mode data-analysis` options.

**Tech Stack:** Python 3.10+, `requests` (9Router), `jinja2` (prompts), `scipy` + `statsmodels` + `pandas` (data analysis), `pytest` (testing).

**Related Spec:** `docs/superpowers/specs/2026-06-01-journal-analysis-system-design.md` (§3.3 Gap Analyzer, §3.3 Data Analysis Worker, §7 Chunking, §9 Output Aggregator improvements)

**Phase 1 Context (existing files):**
- `journal_analyzer/models/article_data.py` — `StructuredArticleData` (with `chunks: list[Chunk]` field already defined), `Chunk` dataclass
- `journal_analyzer/models/model_router.py` — `ModelRouter`, `ModelTier` (LIGHT/MEDIUM/HEAVY)
- `journal_analyzer/workers/reader_worker.py` — pattern: `__init__` with prompts_dir, `run()` returns dict, `_chat()` for 9Router
- `journal_analyzer/workers/reviewer_worker.py` — same pattern, plus `_extract_assessment()` regex
- `journal_analyzer/core/output_aggregator.py` — `aggregate()` method, handles reader + reviewer
- `journal_analyzer/analyze.py` — CLI orchestrator with read/review/full modes
- `journal_analyzer/core/cache.py` — `AnalysisCache` with `get_analysis(content_hash, worker)`
- `journal_analyzer/core/token_budget.py` — `TokenBudget` with `per_task` dict
- All imports use bare module names (e.g., `from models.article_data import ...`) because `conftest.py` adds `journal_analyzer/` to sys.path for tests. The CLI wrapper at root imports `from journal_analyzer.analyze import main`.

---

## File Structure (Phase 2)

```
journal_analyzer/
├── analyze.py                      # MODIFY — add gap, data-analysis modes + chunking
├── analyze.config.json             # MODIFY — add gap + data_analysis budget
├── core/
│   ├── chunker.py                  # CREATE — document chunking strategy
│   └── output_aggregator.py        # MODIFY — add gap + data analysis sections
├── workers/
│   ├── gap_analyzer_worker.py      # CREATE — research gap identification
│   └── data_analysis_worker.py     # CREATE — analyze user's own data
├── prompts/
│   ├── system/
│   │   ├── gap_analyzer.md         # CREATE
│   │   └── data_analysis.md        # CREATE
│   └── templates/
│       ├── gap_analyzer_user.j2    # CREATE
│       └── data_analysis_user.j2   # CREATE
└── tests/
    ├── test_chunker.py             # CREATE
    ├── test_gap_analyzer.py        # CREATE
    ├── test_data_analysis.py       # CREATE
    └── test_integration.py         # MODIFY — add Phase 2 integration tests
```

---

### Task 1: Chunker (Document Chunking Strategy)

**Files:**
- Create: `journal_analyzer/core/chunker.py`
- Test: `journal_analyzer/tests/test_chunker.py`

- [ ] **Step 1: Write tests**

```python
# journal_analyzer/tests/test_chunker.py
from journal_analyzer.core.chunker import Chunker
from journal_analyzer.models.article_data import StructuredArticleData


def _make_article(sections: dict) -> StructuredArticleData:
    return StructuredArticleData(
        metadata={"title": "Test"},
        sections=sections,
    )


def test_no_chunking_small_article():
    article = _make_article({"abstract": "one two three"})
    chunker = Chunker(threshold_small=5000, threshold_large=20000, max_chunk_size=5000)
    result = chunker.chunk(article)
    assert result.chunks == []
    assert result == article


def test_chunk_by_section_medium_article():
    sections = {
        "abstract": "word " * 1000,
        "introduction": "word " * 3000,
        "methodology": "word " * 3000,
        "results": "word " * 3000,
    }
    article = _make_article(sections)
    chunker = Chunker()
    result = chunker.chunk(article)
    assert len(result.chunks) == 4
    assert result.chunks[0].section == "abstract"
    assert result.chunks[0].index == 0


def test_sub_chunk_large_section():
    sections = {
        "abstract": "word " * 1000,
        "introduction": "word " * 8000,
    }
    article = _make_article(sections)
    chunker = Chunker(max_chunk_size=5000)
    result = chunker.chunk(article)
    # introduction > 5000 words, should be split
    intro_chunks = [c for c in result.chunks if c.section == "introduction"]
    assert len(intro_chunks) >= 2


def test_chunk_preserves_raw_text():
    article = _make_article({"abstract": "test content"})
    article.raw_text = "full raw text"
    chunker = Chunker()
    result = chunker.chunk(article)
    assert result.raw_text == "full raw text"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest journal_analyzer/tests/test_chunker.py -v`
Expected: FAIL — module does not exist.

- [ ] **Step 3: Implement Chunker**

```python
# journal_analyzer/core/chunker.py
from models.article_data import StructuredArticleData, Chunk


class Chunker:
    """Splits long documents into chunks for section-by-section analysis.

    Thresholds (from spec §7):
    - < 5,000 words: no chunking
    - 5,000 - 20,000 words: chunk by section
    - > 20,000 words: sub-chunk per section (max_chunk_size per chunk)
    """

    def __init__(
        self,
        threshold_small: int = 5000,
        threshold_large: int = 20000,
        max_chunk_size: int = 5000,
    ):
        self.threshold_small = threshold_small
        self.threshold_large = threshold_large
        self.max_chunk_size = max_chunk_size

    def chunk(self, article: StructuredArticleData) -> StructuredArticleData:
        """Apply chunking strategy based on article word count.

        Returns the same article with chunks populated if needed.
        """
        word_count = article.word_count

        if word_count < self.threshold_small:
            return article

        chunks = []
        index = 0

        for section_name, content in article.sections.items():
            section_words = len(content.split())

            if word_count > self.threshold_large and section_words > self.max_chunk_size:
                # Sub-chunk large sections
                sub_chunks = self._split_text(content, section_name, index)
                chunks.extend(sub_chunks)
                index += len(sub_chunks)
            else:
                chunks.append(Chunk(section=section_name, text=content, index=index))
                index += 1

        article.add_chunks(chunks)
        return article

    def _split_text(self, text: str, section_name: str, start_index: int) -> list[Chunk]:
        """Split a large section into sub-chunks of max_chunk_size words."""
        words = text.split()
        chunks = []
        idx = start_index

        for i in range(0, len(words), self.max_chunk_size):
            sub_words = words[i : i + self.max_chunk_size]
            sub_text = " ".join(sub_words)
            chunks.append(Chunk(section=section_name, text=sub_text, index=idx))
            idx += 1

        return chunks
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest journal_analyzer/tests/test_chunker.py -v`
Expected: All 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add journal_analyzer/core/chunker.py journal_analyzer/tests/test_chunker.py
git commit -m "feat: add Chunker for section-based document chunking"
```

---

### Task 2: Gap Analyzer Prompt System

**Files:**
- Create: `journal_analyzer/prompts/system/gap_analyzer.md`
- Create: `journal_analyzer/prompts/templates/gap_analyzer_user.j2`

- [ ] **Step 1: Create prompt files**

```markdown
# journal_analyzer/prompts/system/gap_analyzer.md
Anda adalah peneliti senior yang berpengalaman mengidentifikasi research gap.
Tugas Anda: menganalisis jurnal ilmiah dan mengidentifikasi celah penelitian yang belum dijawab.

Bahasa output: Bahasa Indonesia.
Tone: Analitis, objektif, dan konstruktif.

Format output:
1. GAP YANG DIIDENTIFIKASI — daftar gap utama (3-5 poin)
2. ALASAN — mengapa setiap gap penting untuk diteliti
3. SARAN RISET LANJUTAN — pertanyaan penelitian yang bisa mengisi gap
4. POTENSI KONTRIBUSI — dampak jika gap tersebut diisi

Fokus pada:
- Metodologi yang belum dieksplorasi
- Populasi/konteks yang belum diteliti
- Variabel yang belum dianalisis
- Periode waktu atau tren yang terlewat
- Inkonsistensi antar studi yang perlu didamaikan
```

```jinja2
{# journal_analyzer/prompts/templates/gap_analyzer_user.j2 #}
Analisis research gap dari jurnal berikut:

Judul: {{ metadata.title }}
{% if metadata.authors %}Penulis: {{ metadata.authors | join(', ') }}{% endif %}
{% if methodology_type %}Metodologi: {{ methodology_type }}{% endif %}

{% if reader_summary %}
Ringkasan:
{{ reader_summary }}
{% endif %}

{% for section_name, content in sections.items() %}
## {{ section_name | upper }}
{{ content }}
{% endfor %}

{% if key_findings %}
Temuan utama:
{% for finding in key_findings %}
- {{ finding }}
{% endfor %}
{% endif %}

Identifikasi research gap sesuai format yang ditentukan.
```

- [ ] **Step 2: Commit**

```bash
git add journal_analyzer/prompts/system/gap_analyzer.md journal_analyzer/prompts/templates/gap_analyzer_user.j2
git commit -m "feat: add prompt templates for gap analyzer worker"
```

---

### Task 3: Gap Analyzer Worker

**Files:**
- Create: `journal_analyzer/workers/gap_analyzer_worker.py`
- Test: `journal_analyzer/tests/test_gap_analyzer.py`

- [ ] **Step 1: Write tests**

```python
# journal_analyzer/tests/test_gap_analyzer.py
from unittest.mock import patch
from models.article_data import StructuredArticleData
from workers.gap_analyzer_worker import GapAnalyzerWorker


def _make_article() -> StructuredArticleData:
    return StructuredArticleData(
        metadata={"title": "AI in Education", "authors": ["Dr. Smith"], "publication_year": 2024},
        sections={
            "abstract": "This study explores AI use in classrooms.",
            "introduction": "AI is transforming education globally.",
            "methodology": "Survey of 500 teachers across 3 countries.",
            "results": "75% reported improved engagement.",
            "discussion": "Results suggest positive impact.",
            "conclusion": "More research needed on long-term effects.",
        },
        methodology_type="kuantitatif",
        key_findings=["75% improved engagement", "AI tools effective"],
        raw_text="Full text.",
    )


def test_gap_analyzer_calls_chat():
    article = _make_article()
    mock_result = "GAP YANG DIIDENTIFIKASI:\n1. Belum ada studi longitudinal."

    with patch.object(GapAnalyzerWorker, "_chat", return_value=mock_result) as mock_chat:
        worker = GapAnalyzerWorker()
        result = worker.run(article)
        mock_chat.assert_called_once()
        assert "gap_text" in result


def test_gap_analyzer_returns_structured_output():
    article = _make_article()
    mock_result = "GAP YANG DIIDENTIFIKASI:\n1. Longitudinal study belum ada."

    with patch.object(GapAnalyzerWorker, "_chat", return_value=mock_result):
        worker = GapAnalyzerWorker()
        result = worker.run(article)
        assert isinstance(result, dict)
        assert "gap_text" in result


def test_gap_analyzer_with_reader_summary():
    article = _make_article()
    mock_result = "GAP: 1. Context Indonesia belum diteliti."

    with patch.object(GapAnalyzerWorker, "_chat", return_value=mock_result) as mock_chat:
        worker = GapAnalyzerWorker()
        result = worker.run(article, reader_summary="AI improves engagement in Western context")
        call_args = mock_chat.call_args
        assert "AI improves engagement in Western context" in call_args[0][1]


def test_gap_analyzer_handles_error():
    article = _make_article()

    with patch.object(GapAnalyzerWorker, "_chat", side_effect=Exception("API down")):
        worker = GapAnalyzerWorker()
        result = worker.run(article)
        assert result is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest journal_analyzer/tests/test_gap_analyzer.py -v`
Expected: FAIL.

- [ ] **Step 3: Implement GapAnalyzerWorker**

```python
# journal_analyzer/workers/gap_analyzer_worker.py
import os
import requests
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from models.article_data import StructuredArticleData


class GapAnalyzerWorker:
    """Research gap identification worker."""

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
        article: StructuredArticleData,
        reader_summary: str | None = None,
        model: str = "anthropic/claude-sonnet-4-20250514",
    ) -> dict | None:
        """Run gap analysis on an article.

        Returns:
            {"gap_text": str} or None on failure.
        """
        system_prompt = self._load_system_prompt("gap_analyzer.md")
        user_prompt = self._build_user_prompt(article, reader_summary)

        response = self._chat(system_prompt, user_prompt, model)
        if response is None:
            return None

        return {"gap_text": response}

    def _chat(self, system_prompt: str, user_prompt: str, model: str) -> str | None:
        endpoint = f"{self.ninerouter_url}/v1/chat/completions"
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "max_tokens": 4000,
            "temperature": 0.3,
            "stream": False,
        }
        try:
            response = requests.post(endpoint, headers=self._headers, json=payload, timeout=120)
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
        self, article: StructuredArticleData, reader_summary: str | None = None
    ) -> str:
        template = self._env.get_template("gap_analyzer_user.j2")
        return template.render(
            metadata=article.metadata,
            sections=article.sections,
            methodology_type=article.methodology_type,
            reader_summary=reader_summary or "",
            key_findings=article.key_findings,
        )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest journal_analyzer/tests/test_gap_analyzer.py -v`
Expected: All 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add journal_analyzer/workers/gap_analyzer_worker.py journal_analyzer/tests/test_gap_analyzer.py
git commit -m "feat: add GapAnalyzerWorker for research gap identification"
```

---

### Task 4: Data Analysis Prompt System

**Files:**
- Create: `journal_analyzer/prompts/system/data_analysis.md`
- Create: `journal_analyzer/prompts/templates/data_analysis_user.j2`

- [ ] **Step 1: Create prompt files**

```markdown
# journal_analyzer/prompts/system/data_analysis.md
Anda adalah ahli statistik dan metodologi penelitian.
Tugas Anda: menginterpretasikan hasil analisis statistik data riset dan memberikan rekomendasi dalam Bahasa Indonesia.

Bahasa output: Bahasa Indonesia.
Tone: Profesional, jelas, dan edukatif.

Format output:
1. RINGKASAN DESKRIPTIF — statistik dasar (mean, SD, distribusi)
2. SARAN METODE ANALISIS — rekomendasi uji statistik dengan justifikasi
3. HASIL UJI — interpretasi nilai statistik, p-value, effect size
4. INTERPRETASI — apa artinya dalam konteks riset
5. REKOMENDASI PENULISAN — cara menulis hasil ini di artikel ilmiah

Jelaskan istilah statistik dengan bahasa yang mudah dipahami. Hindari jargon tanpa penjelasan.
```

```jinja2
{# journal_analyzer/prompts/templates/data_analysis_user.j2 #}
Interpretasikan hasil analisis data berikut:

Pertanyaan Penelitian: {{ research_question }}

{% if dataset_description %}
Deskripsi Dataset:
{{ dataset_description }}
{% endif %}

{% if statistical_results %}
Hasil Analisis Statistik:
{{ statistical_results }}
{% endif %}

{% if hypothesis %}
Hipotesis: {{ hypothesis }}
{% endif %}

Berikan interpretasi dan rekomendasi sesuai format yang ditentukan.
```

- [ ] **Step 2: Commit**

```bash
git add journal_analyzer/prompts/system/data_analysis.md journal_analyzer/prompts/templates/data_analysis_user.j2
git commit -m "feat: add prompt templates for data analysis worker"
```

---

### Task 5: Data Analysis Worker

**Files:**
- Create: `journal_analyzer/workers/data_analysis_worker.py`
- Test: `journal_analyzer/tests/test_data_analysis.py`

- [ ] **Step 1: Write tests**

```python
# journal_analyzer/tests/test_data_analysis.py
from unittest.mock import patch
from workers.data_analysis_worker import DataAnalysisWorker


def test_data_analysis_basic():
    mock_result = "RINGKASAN DESKRIPTIF:\nMean = 75.3, SD = 12.1"

    with patch.object(DataAnalysisWorker, "_chat", return_value=mock_result) as mock_chat:
        worker = DataAnalysisWorker()
        result = worker.run(
            research_question="Pengaruh metode X terhadap hasil belajar",
            dataset_description="n=200, variabel: skor_pretest, skor_posttest",
            statistical_results="t(199) = 5.67, p < 0.001, Cohen's d = 0.85",
        )
        mock_chat.assert_called_once()
        assert "interpretation" in result


def test_data_analysis_with_hypothesis():
    mock_result = "INTERPRETASI: H0 ditolak."

    with patch.object(DataAnalysisWorker, "_chat", return_value=mock_result):
        worker = DataAnalysisWorker()
        result = worker.run(
            research_question="Perbedaan skor antara grup A dan B",
            hypothesis="Grup A > Grup B",
            statistical_results="t = 2.34, p = 0.02",
        )
        assert "interpretation" in result


def test_data_analysis_handles_error():
    with patch.object(DataAnalysisWorker, "_chat", side_effect=Exception("API down")):
        worker = DataAnalysisWorker()
        result = worker.run(
            research_question="Test question",
            dataset_description="Test data",
        )
        assert result is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest journal_analyzer/tests/test_data_analysis.py -v`
Expected: FAIL.

- [ ] **Step 3: Implement DataAnalysisWorker**

```python
# journal_analyzer/workers/data_analysis_worker.py
import os
import requests
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class DataAnalysisWorker:
    """Analyzes user's own research data and provides statistical interpretation."""

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
        research_question: str,
        dataset_description: str = "",
        statistical_results: str = "",
        hypothesis: str = "",
        model: str = "anthropic/claude-sonnet-4-20250514",
    ) -> dict | None:
        """Run data analysis interpretation.

        Returns:
            {"interpretation": str} or None on failure.
        """
        system_prompt = self._load_system_prompt("data_analysis.md")
        user_prompt = self._build_user_prompt(research_question, dataset_description, statistical_results, hypothesis)

        response = self._chat(system_prompt, user_prompt, model)
        if response is None:
            return None

        return {"interpretation": response}

    def _chat(self, system_prompt: str, user_prompt: str, model: str) -> str | None:
        endpoint = f"{self.ninerouter_url}/v1/chat/completions"
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "max_tokens": 4000,
            "temperature": 0.2,
            "stream": False,
        }
        try:
            response = requests.post(endpoint, headers=self._headers, json=payload, timeout=120)
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
        research_question: str,
        dataset_description: str,
        statistical_results: str,
        hypothesis: str,
    ) -> str:
        template = self._env.get_template("data_analysis_user.j2")
        return template.render(
            research_question=research_question,
            dataset_description=dataset_description,
            statistical_results=statistical_results,
            hypothesis=hypothesis,
        )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest journal_analyzer/tests/test_data_analysis.py -v`
Expected: All 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add journal_analyzer/workers/data_analysis_worker.py journal_analyzer/tests/test_data_analysis.py
git commit -m "feat: add DataAnalysisWorker for statistical interpretation"
```

---

### Task 6: Extend Output Aggregator

**Files:**
- Modify: `journal_analyzer/core/output_aggregator.py`
- Test: `journal_analyzer/tests/test_output_aggregator.py` (append tests)

- [ ] **Step 1: Append tests**

Append to `journal_analyzer/tests/test_output_aggregator.py`:

```python
def test_aggregate_with_gap_analysis():
    agg = OutputAggregator()
    result = agg.aggregate({
        "reader": {"status": "success", "data": {"summary": "Summary."}},
        "gap_analyzer": {"status": "success", "data": {"gap_text": "Gap: longitudinal study needed."}},
    })
    assert "Ringkasan Jurnal" in result
    assert "Research Gap" in result
    assert "longitudinal study" in result


def test_aggregate_with_data_analysis():
    agg = OutputAggregator()
    result = agg.aggregate({
        "data_analysis": {"status": "success", "data": {"interpretation": "H0 ditolak, p<0.05"}},
    })
    assert "Analisis Data" in result
    assert "H0 ditolak" in result


def test_aggregate_all_workers():
    agg = OutputAggregator()
    result = agg.aggregate({
        "reader": {"status": "success", "data": {"summary": "Summary."}},
        "reviewer": {"status": "success", "data": {"assessment": "Minor Revision", "review_text": "Good paper."}},
        "gap_analyzer": {"status": "success", "data": {"gap_text": "Gap identified."}},
    })
    assert "Ringkasan Jurnal" in result
    assert "Review Peer" in result
    assert "Research Gap" in result
```

- [ ] **Step 2: Run test to verify new tests fail**

Run: `python -m pytest journal_analyzer/tests/test_output_aggregator.py -v`
Expected: 3 new tests FAIL.

- [ ] **Step 3: Update OutputAggregator**

Replace the entire `aggregate` method:

```python
# journal_analyzer/core/output_aggregator.py (replace aggregate method)
    def aggregate(self, worker_results: dict[str, dict]) -> str:
        """Aggregate worker results into markdown.

        Args:
            worker_results: {worker_name: {"status": "success"|"failed", "data": {...}|None, "error": str|None}}

        Returns:
            Markdown string in Bahasa Indonesia.
        """
        parts = []

        if "reader" in worker_results and worker_results["reader"]["status"] == "success":
            data = worker_results["reader"]["data"]
            parts.append("# Ringkasan Jurnal\n")
            parts.append(data.get("summary", "Tidak ada ringkasan."))
            parts.append("")

        if "reviewer" in worker_results:
            wr = worker_results["reviewer"]
            if wr["status"] == "success":
                data = wr["data"]
                parts.append("## Review Peer\n")
                parts.append(f"**Penilaian:** {data.get('assessment', 'N/A')}\n")
                parts.append(data.get("review_text", "Tidak ada review."))
            else:
                parts.append("## Review Peer\n")
                parts.append(f"[reviewer] Gagal: {wr.get('error', 'Unknown error')}. Coba lagi nanti.\n")
            parts.append("")

        if "gap_analyzer" in worker_results:
            ga = worker_results["gap_analyzer"]
            if ga["status"] == "success":
                parts.append("## Research Gap\n")
                parts.append(ga["data"].get("gap_text", "Tidak ada gap teridentifikasi."))
            else:
                parts.append("## Research Gap\n")
                parts.append(f"[gap_analyzer] Gagal: {ga.get('error', 'Unknown error')}. Coba lagi nanti.\n")
            parts.append("")

        if "data_analysis" in worker_results:
            da = worker_results["data_analysis"]
            if da["status"] == "success":
                parts.append("## Analisis Data\n")
                parts.append(da["data"].get("interpretation", "Tidak ada interpretasi."))
            else:
                parts.append("## Analisis Data\n")
                parts.append(f"[data_analysis] Gagal: {da.get('error', 'Unknown error')}. Coba lagi nanti.\n")
            parts.append("")

        return "\n".join(parts)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest journal_analyzer/tests/test_output_aggregator.py -v`
Expected: All 7 tests PASS (4 existing + 3 new).

- [ ] **Step 5: Commit**

```bash
git add journal_analyzer/core/output_aggregator.py journal_analyzer/tests/test_output_aggregator.py
git commit -m "feat: extend OutputAggregator to support gap analysis and data analysis"
```

---

### Task 7: Update Config and CLI for New Modes

**Files:**
- Modify: `journal_analyzer/analyze.config.json`
- Modify: `journal_analyzer/analyze.py`

- [ ] **Step 1: Update config**

Add `gap` and `data_analysis` per_task budgets:

```json
{
  "token_budget": {
    "daily_limit": 50000,
    "per_task": {
      "read": 5000,
      "review": 15000,
      "full": 30000,
      "gap": 10000,
      "data_analysis": 10000,
      "generate": 40000
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

- [ ] **Step 2: Update CLI in analyze.py**

Add `--mode gap` and `--mode data-analysis` options, plus `--research-question` and `--dataset` args.

Modify the `main()` function in `journal_analyzer/analyze.py`:

1. Change the argparse choices:
```python
    parser.add_argument("--mode", required=True, choices=["read", "review", "full", "gap", "data-analysis"], help="Analysis mode")
```

2. Add new arguments after `--no-limit`:
```python
    parser.add_argument("--research-question", help="Research question for data-analysis or gap mode")
    parser.add_argument("--dataset", help="CSV/Excel dataset file for data-analysis mode")
```

3. Add new runner functions at the end of the file (before `if __name__`):

```python
def _run_gap_analyzer(article, reader_result, cache, content_hash, config, router):
    from workers.gap_analyzer_worker import GapAnalyzerWorker

    cached = cache.get_analysis(content_hash, "gap_analyzer")
    if cached:
        return {"status": "success", "data": cached}

    model = router.get_model_name(router.select_model("gap_analysis", article.word_count))
    reader_summary = reader_result["data"]["summary"] if reader_result and reader_result["status"] == "success" else None

    worker = GapAnalyzerWorker()
    result = worker.run(article, reader_summary=reader_summary, model=model)

    if result is None:
        return {"status": "failed", "error": "Gap Analyzer gagal"}

    cache.set_analysis(content_hash, "gap_analyzer", result)
    return {"status": "success", "data": result}


def _run_data_analysis(args, cache, content_hash, config, router):
    from workers.data_analysis_worker import DataAnalysisWorker

    cached = cache.get_analysis(content_hash, "data_analysis")
    if cached:
        return {"status": "success", "data": cached}

    model = router.get_model_name(router.select_model("data_analysis_own", 1000))

    worker = DataAnalysisWorker()
    result = worker.run(
        research_question=args.research_question or "",
        dataset_description=args.dataset or "",
        statistical_results="",
    )

    if result is None:
        return {"status": "failed", "error": "Data Analysis gagal"}

    cache.set_analysis(content_hash, "data_analysis", result)
    return {"status": "success", "data": result}
```

4. In the "Execute workers based on mode" section, add handling for new modes:

After the existing `if args.mode in ("review", "full"):` block, add:

```python
    if args.mode == "gap":
        reader_result = _run_reader(article, cache, content_hash, config, router)
        results["reader"] = reader_result
        gap_result = _run_gap_analyzer(article, reader_result, cache, content_hash, config, router)
        results["gap_analyzer"] = gap_result

    if args.mode == "data-analysis":
        da_result = _run_data_analysis(args, cache, content_hash, config, router)
        results["data_analysis"] = da_result
```

- [ ] **Step 3: Update wrapper analyze.py**

Update the docstring in the root `analyze.py` wrapper:

```python
"""Journal Analysis System — Entry point wrapper.

Usage:
    python analyze.py jurnal.pdf --mode read
    python analyze.py jurnal.pdf --mode review
    python analyze.py jurnal.pdf --mode full
    python analyze.py jurnal.pdf --mode gap
    python analyze.py --input-text "teks..." --mode review
    python analyze.py --research-question "Pertanyaan riset" --dataset data.csv --mode data-analysis
"""
```

- [ ] **Step 4: Test CLI help**

Run: `python analyze.py --help`
Expected: Shows `--mode {read,review,full,gap,data-analysis}`, `--research-question`, `--dataset`.

- [ ] **Step 5: Commit**

```bash
git add journal_analyzer/analyze.config.json journal_analyzer/analyze.py analyze.py
git commit -m "feat: add gap and data-analysis CLI modes with new worker runners"
```

---

### Task 8: Integration Test for Phase 2

**Files:**
- Modify: `journal_analyzer/tests/test_integration.py` (append tests)

- [ ] **Step 1: Append integration tests**

Append to `journal_analyzer/tests/test_integration.py`:

```python
def test_gap_analysis_pipeline():
    """Test: parse → reader → gap analyzer → aggregate."""
    text = """## ABSTRACT
This study examines AI in education with a survey of 500 teachers.

## INTRODUCTION
AI is transforming education globally.

## METHODOLOGY
Quantitative survey method.

## RESULTS
75% reported improved engagement.

## CONCLUSION
More longitudinal research is needed.
"""
    from parsers.text_parser import TextParser
    parser = TextParser()
    article = parser.parse(text)

    reader_summary = "AI improves engagement in education."

    from workers.reader_worker import ReaderWorker
    from workers.gap_analyzer_worker import GapAnalyzerWorker
    from core.output_aggregator import OutputAggregator

    with patch.object(ReaderWorker, "_chat", return_value=reader_summary):
        reader = ReaderWorker(prompts_dir="journal_analyzer/prompts")
        reader_result = reader.run(article)

    gap_text = "GAP: 1. Studi longitudinal belum ada. 2. Konteks Asia Tenggara kurang diteliti."

    with patch.object(GapAnalyzerWorker, "_chat", return_value=gap_text):
        gap_worker = GapAnalyzerWorker(prompts_dir="journal_analyzer/prompts")
        gap_result = gap_worker.run(article, reader_summary=reader_summary)
        assert gap_result is not None
        assert "gap_text" in gap_result

    agg = OutputAggregator()
    output = agg.aggregate({
        "reader": {"status": "success", "data": reader_result},
        "gap_analyzer": {"status": "success", "data": gap_result},
    })
    assert "# Ringkasan Jurnal" in output
    assert "## Research Gap" in output
    assert "longitudinal" in output


def test_data_analysis_pipeline():
    """Test: data analysis worker → aggregate."""
    from workers.data_analysis_worker import DataAnalysisWorker
    from core.output_aggregator import OutputAggregator

    interp_text = "RINGKASAN DESKRIPTIF:\nMean = 75.3, SD = 12.1\n\nINTERPRETASI: H0 ditolak (p < 0.05)."

    with patch.object(DataAnalysisWorker, "_chat", return_value=interp_text):
        worker = DataAnalysisWorker(prompts_dir="journal_analyzer/prompts")
        result = worker.run(
            research_question="Pengaruh metode X terhadap hasil belajar",
            dataset_description="n=200, pretest-posttest design",
        )
        assert result is not None
        assert "interpretation" in result

    agg = OutputAggregator()
    output = agg.aggregate({
        "data_analysis": {"status": "success", "data": result},
    })
    assert "## Analisis Data" in output
    assert "H0 ditolak" in output
```

- [ ] **Step 2: Run all tests**

Run: `python -m pytest journal_analyzer/tests/ -v`
Expected: All tests PASS (61 existing + 2 new = 63 tests).

- [ ] **Step 3: Commit**

```bash
git add journal_analyzer/tests/test_integration.py
git commit -m "test: add Phase 2 integration tests for gap analysis and data analysis pipelines"
```

---

### Task 9: Run All Tests + Final Commit

- [ ] **Step 1: Run all Phase 1 + Phase 2 tests**

Run: `python -m pytest journal_analyzer/tests/ -v --tb=short`
Expected: All 63+ tests PASS.

- [ ] **Step 2: Final commit**

```bash
git add -A
git commit -m "feat: journal analysis system phase 2 complete — gap analyzer, data analysis, chunking"
```
