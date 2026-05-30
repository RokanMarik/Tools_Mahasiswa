# Journal Analysis System — Phase 1: Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the core pipeline — parsers, data model, model router, token budget, caching, error handling, prompt system, Reader Worker, Reviewer Worker, and CLI entry point — producing a working `analyze.py` that can parse a PDF/text/URL and produce a summary + review in Bahasa Indonesia.

**Architecture:** Modular pipeline with Parser Layer → StructuredArticleData → Model Router → Workers (Reader, Reviewer) → Output Aggregator. All orchestrated via CLI `analyze.py`. Uses 9Router for all LLM calls with auto model tier selection and token budget management.

**Tech Stack:** Python 3.10+, `pymupdf` (PDF parsing), `requests` (9Router HTTP), `jinja2` (prompt templates), `hashlib` (content hashing), `pytest` (testing).

**Related Spec:** `docs/superpowers/specs/2026-06-01-journal-analysis-system-design.md`

---

## File Structure (Phase 1)

```
Mencari_Jurnal_Ilmiah/
├── analyze.py                      # CREATE — CLI orchestrator
├── analyze.config.json             # CREATE — default config
├── parsers/
│   ├── __init__.py                 # CREATE
│   ├── pdf_parser.py               # CREATE — PDF extraction (OCR fallback deferred to Phase 2)
│   ├── text_parser.py              # CREATE — plain text/markdown parsing
│   └── url_fetcher.py              # CREATE — DOI/URL fetching via 9Router
├── workers/
│   ├── __init__.py                 # CREATE
│   ├── reader_worker.py            # CREATE — smart summarizer
│   └── reviewer_worker.py          # CREATE — peer reviewer
├── models/
│   ├── __init__.py                 # CREATE
│   ├── article_data.py             # CREATE — StructuredArticleData
│   └── model_router.py             # CREATE — auto model selection
├── core/
│   ├── __init__.py                 # CREATE
│   ├── cache.py                    # CREATE — content-hash based caching
│   ├── error_handler.py            # CREATE — 3-layer error handling
│   ├── token_budget.py             # CREATE — budget tracking
│   └── output_aggregator.py        # CREATE — combine outputs → Bahasa Indonesia
├── prompts/
│   ├── system/
│   │   ├── reader.md               # CREATE
│   │   └── reviewer.md             # CREATE
│   └── templates/
│       ├── reader_user.j2          # CREATE
│       └── reviewer_user.j2        # CREATE
└── tests/
    ├── test_article_data.py        # CREATE
    ├── test_parsers.py             # CREATE
    ├── test_model_router.py        # CREATE
    ├── test_token_budget.py        # CREATE
    ├── test_cache.py               # CREATE
    ├── test_error_handler.py       # CREATE
    ├── test_reader_worker.py       # CREATE
    ├── test_reviewer_worker.py     # CREATE
    └── test_output_aggregator.py   # CREATE
```

**Existing files NOT modified in Phase 1:**
- `9router_journal_finder.py` — keep as-is; new system is parallel, not a replacement
- `modules/search_cache.py` — superseded by `core/cache.py` but not deleted
- `modules/zotero/*` — used in Phase 4, untouched in Phase 1

---

### Task 1: StructuredArticleData Model

**Files:**
- Create: `models/__init__.py`
- Create: `models/article_data.py`
- Test: `tests/test_article_data.py`

- [ ] **Step 1: Write tests for StructuredArticleData**

```python
# tests/test_article_data.py
from models.article_data import StructuredArticleData, Chunk


def test_create_article_data():
    article = StructuredArticleData(
        metadata={"title": "Test Paper", "authors": ["John Doe"], "publication_year": 2024},
        sections={"abstract": "This is a test abstract.", "introduction": "Intro text."},
        methodology_type="kuantitatif",
        raw_text="Full text here."
    )
    assert article.metadata["title"] == "Test Paper"
    assert article.sections["abstract"] == "This is a test abstract."
    assert article.methodology_type == "kuantitatif"


def test_get_section():
    article = StructuredArticleData(
        metadata={"title": "Test"},
        sections={"abstract": "Abstract text", "methods": "Methods text"}
    )
    assert article.get_section("abstract") == "Abstract text"
    assert article.get_section("nonexistent") == ""


def test_get_full_text():
    article = StructuredArticleData(
        metadata={"title": "Test"},
        sections={"abstract": "A", "introduction": "B", "conclusion": "C"}
    )
    text = article.get_full_text()
    assert "A" in text
    assert "B" in text
    assert "C" in text


def test_word_count():
    article = StructuredArticleData(
        metadata={"title": "Test"},
        sections={"abstract": "one two three four five"}
    )
    assert article.word_count == 5


def test_add_chunks():
    article = StructuredArticleData(
        metadata={"title": "Test"},
        sections={"abstract": "text"},
        raw_text="long text"
    )
    article.add_chunks([
        Chunk(section="abstract", text="chunk 1", index=0),
        Chunk(section="intro", text="chunk 2", index=1),
    ])
    assert len(article.chunks) == 2
    assert article.chunks[0].text == "chunk 1"


def test_default_values():
    article = StructuredArticleData(metadata={"title": "Test"})
    assert article.methodology_type == "unknown"
    assert article.key_findings == []
    assert article.statistical_methods == []
    assert article.chunks == []
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_article_data.py -v
```
Expected: FAIL — module does not exist.

- [ ] **Step 3: Implement StructuredArticleData**

```python
# models/__init__.py
from models.article_data import StructuredArticleData, Chunk

__all__ = ["StructuredArticleData", "Chunk"]
```

```python
# models/article_data.py
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Chunk:
    """A chunk of a long document for section-by-section analysis."""
    section: str
    text: str
    index: int
    analysis_result: Optional[str] = None


@dataclass
class StructuredArticleData:
    """Shared data model that all parsers produce and all workers consume."""
    metadata: dict = field(default_factory=dict)
    sections: dict = field(default_factory=dict)
    methodology_type: str = "unknown"
    research_gap: str = ""
    key_findings: list = field(default_factory=list)
    statistical_methods: list = field(default_factory=list)
    chunks: list = field(default_factory=list)
    raw_text: str = ""

    def get_section(self, name: str) -> str:
        """Get a section by name. Returns empty string if not found."""
        return self.sections.get(name, "")

    def get_full_text(self) -> str:
        """Concatenate all sections with headers."""
        parts = []
        for section_name, content in self.sections.items():
            parts.append(f"## {section_name.upper()}\n\n{content}")
        return "\n\n".join(parts)

    @property
    def word_count(self) -> int:
        """Count total words across all sections."""
        return sum(len(text.split()) for text in self.sections.values())

    def add_chunks(self, chunks: list[Chunk]) -> None:
        """Add chunks for long document processing."""
        self.chunks = chunks
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/test_article_data.py -v
```
Expected: All 6 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add models/__init__.py models/article_data.py tests/test_article_data.py
git commit -m "feat: add StructuredArticleData model with chunks support"
```

---

### Task 2: Token Budget Manager

**Files:**
- Create: `core/__init__.py`
- Create: `core/token_budget.py`
- Test: `tests/test_token_budget.py`

- [ ] **Step 1: Write tests for TokenBudget**

```python
# tests/test_token_budget.py
from core.token_budget import TokenBudget, BudgetExceededError


def test_default_budget():
    budget = TokenBudget()
    assert budget.daily_limit == 50000
    assert budget.used_today == 0


def test_custom_budget():
    budget = TokenBudget(daily_limit=10000)
    assert budget.daily_limit == 10000


def test_add_usage():
    budget = TokenBudget(daily_limit=1000)
    budget.add_usage(500)
    assert budget.used_today == 500
    assert budget.remaining == 500


def test_check_within_budget():
    budget = TokenBudget(daily_limit=1000, used_today=400)
    assert budget.check_available(500) == True


def test_check_exceeds_budget():
    budget = TokenBudget(daily_limit=1000, used_today=800)
    assert budget.check_available(300) == False


def test_exceed_raises_error():
    budget = TokenBudget(daily_limit=1000, used_today=800)
    try:
        budget.reserve(300)
        assert False, "Should have raised BudgetExceededError"
    except BudgetExceededError:
        pass


def test_reserve_within_budget():
    budget = TokenBudget(daily_limit=1000, used_today=400)
    budget.reserve(500)
    assert budget.used_today == 900


def test_remaining():
    budget = TokenBudget(daily_limit=10000, used_today=3000)
    assert budget.remaining == 7000


def test_reset():
    budget = TokenBudget(daily_limit=1000, used_today=500)
    budget.reset()
    assert budget.used_today == 0
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_token_budget.py -v
```
Expected: FAIL.

- [ ] **Step 3: Implement TokenBudget**

```python
# core/__init__.py
from core.token_budget import TokenBudget, BudgetExceededError
from core.cache import AnalysisCache
from core.error_handler import ErrorHandler
from core.output_aggregator import OutputAggregator

__all__ = [
    "TokenBudget", "BudgetExceededError",
    "AnalysisCache", "ErrorHandler", "OutputAggregator",
]
```

```python
# core/token_budget.py
class BudgetExceededError(Exception):
    """Raised when token budget is exceeded."""
    pass


class TokenBudget:
    """Tracks and manages daily token usage with per-task limits."""

    DEFAULT_DAILY_LIMIT = 50000
    DEFAULT_PER_TASK = {
        "read": 5000,
        "review": 15000,
        "full": 30000,
        "generate": 40000,
        "data_analysis": 10000,
    }

    def __init__(
        self,
        daily_limit: int = DEFAULT_DAILY_LIMIT,
        per_task: dict | None = None,
        used_today: int = 0,
    ):
        self.daily_limit = daily_limit
        self.per_task = per_task or dict(self.DEFAULT_PER_TASK)
        self._used_today = used_today

    @property
    def used_today(self) -> int:
        return self._used_today

    @used_today.setter
    def used_today(self, value: int):
        self._used_today = value

    @property
    def remaining(self) -> int:
        return max(0, self.daily_limit - self._used_today)

    def check_available(self, tokens: int) -> bool:
        """Check if adding `tokens` would stay within budget."""
        return self._used_today + tokens <= self.daily_limit

    def reserve(self, tokens: int) -> None:
        """Reserve tokens. Raises BudgetExceededError if over limit."""
        if not self.check_available(tokens):
            raise BudgetExceededError(
                f"Token budget exceeded: need {tokens}, "
                f"have {self.remaining} of {self.daily_limit}"
            )
        self._used_today += tokens

    def add_usage(self, tokens: int) -> None:
        """Add token usage. Does NOT raise — just tracks."""
        self._used_today += tokens

    def get_task_budget(self, mode: str) -> int:
        """Get per-task budget for a mode."""
        return self.per_task.get(mode, 10000)

    def reset(self) -> None:
        """Reset daily counter."""
        self._used_today = 0
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/test_token_budget.py -v
```
Expected: All 9 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add core/__init__.py core/token_budget.py tests/test_token_budget.py
git commit -m "feat: add TokenBudget manager with daily limit and per-task budgets"
```

---

### Task 3: Content-Hash Cache

**Files:**
- Create: `core/cache.py`
- Test: `tests/test_cache.py`

- [ ] **Step 1: Write tests for AnalysisCache**

```python
# tests/test_cache.py
import os
import json
import tempfile
from core.cache import AnalysisCache


def test_set_and_get_parsed():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = AnalysisCache(cache_dir=tmpdir)
        cache.set_parsed("abc123", {"title": "Test Paper"})
        result = cache.get_parsed("abc123")
        assert result == {"title": "Test Paper"}


def test_get_parsed_missing():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = AnalysisCache(cache_dir=tmpdir)
        result = cache.get_parsed("nonexistent")
        assert result is None


def test_set_and_get_analysis():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = AnalysisCache(cache_dir=tmpdir)
        cache.set_analysis("abc123", "reader", {"summary": "Test"})
        result = cache.get_analysis("abc123", "reader")
        assert result == {"summary": "Test"}


def test_analysis_cache_miss():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = AnalysisCache(cache_dir=tmpdir)
        result = cache.get_analysis("abc123", "reviewer")
        assert result is None


def test_clear_analysis():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = AnalysisCache(cache_dir=tmpdir)
        cache.set_analysis("abc123", "reader", {"summary": "Test"})
        cache.clear_analysis("abc123")
        result = cache.get_analysis("abc123", "reader")
        assert result is None
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_cache.py -v
```
Expected: FAIL.

- [ ] **Step 3: Implement AnalysisCache**

```python
# core/cache.py
import os
import json
from typing import Optional


class AnalysisCache:
    """Content-hash based cache for parsed articles and analysis results.

    Parse cache is permanent. Analysis cache has configurable TTL.
    """

    def __init__(self, cache_dir: str = "cache", ttl_days: int = 7):
        self.cache_dir = cache_dir
        self.ttl_days = ttl_days
        self._parsed_dir = os.path.join(cache_dir, "parsed")
        self._analysis_dir = os.path.join(cache_dir, "analysis")
        os.makedirs(self._parsed_dir, exist_ok=True)
        os.makedirs(self._analysis_dir, exist_ok=True)

    def _parsed_path(self, content_hash: str) -> str:
        return os.path.join(self._parsed_dir, f"{content_hash}.json")

    def _analysis_path(self, content_hash: str, worker: str) -> str:
        return os.path.join(self._analysis_dir, f"{content_hash}_{worker}.json")

    # --- Parsed article cache (permanent) ---

    def set_parsed(self, content_hash: str, data: dict) -> None:
        path = self._parsed_path(content_hash)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def get_parsed(self, content_hash: str) -> Optional[dict]:
        path = self._parsed_path(content_hash)
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            return json.load(f)

    # --- Analysis result cache (TTL-based) ---

    def set_analysis(self, content_hash: str, worker: str, data: dict) -> None:
        import time
        path = self._analysis_path(content_hash, worker)
        with open(path, "w") as f:
            json.dump({"data": data, "timestamp": time.time()}, f, indent=2)

    def get_analysis(self, content_hash: str, worker: str) -> Optional[dict]:
        import time
        path = self._analysis_path(content_hash, worker)
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            entry = json.load(f)
        age_seconds = time.time() - entry["timestamp"]
        if age_seconds > self.ttl_days * 86400:
            os.remove(path)
            return None
        return entry["data"]

    def clear_analysis(self, content_hash: str) -> None:
        """Clear all analysis cache for a content hash."""
        import glob
        pattern = os.path.join(self._analysis_dir, f"{content_hash}_*.json")
        for path in glob.glob(pattern):
            os.remove(path)
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/test_cache.py -v
```
Expected: All 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add core/cache.py tests/test_cache.py
git commit -m "feat: add content-hash based AnalysisCache with TTL"
```

---

### Task 4: Error Handler

**Files:**
- Create: `core/error_handler.py`
- Test: `tests/test_error_handler.py`

- [ ] **Step 1: Write tests for ErrorHandler**

```python
# tests/test_error_handler.py
from core.error_handler import ErrorHandler, WorkerError


def test_record_success():
    handler = ErrorHandler()
    handler.record_success("reader", {"summary": "done"})
    assert handler.get_results("reader") == {"summary": "done"}
    assert handler.get_status("reader") == "success"


def test_record_failure():
    handler = ErrorHandler()
    handler.record_failure("reviewer", "Model unavailable")
    assert handler.get_status("reviewer") == "failed"
    assert "Model unavailable" in handler.get_error("reviewer")


def test_all_success():
    handler = ErrorHandler()
    handler.record_success("reader", {})
    assert handler.all_workers_succeeded(["reader", "reviewer"]) == False


def test_partial_failure():
    handler = ErrorHandler()
    handler.record_success("reader", {"summary": "ok"})
    handler.record_failure("reviewer", "timeout")
    assert handler.has_partial_failure(["reader", "reviewer"]) == True


def test_get_summary():
    handler = ErrorHandler()
    handler.record_success("reader", {"summary": "ok"})
    handler.record_failure("reviewer", "model down")
    summary = handler.get_summary(["reader", "reviewer"])
    assert summary["reader"] == {"status": "success"}
    assert summary["reviewer"]["status"] == "failed"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_error_handler.py -v
```
Expected: FAIL.

- [ ] **Step 3: Implement ErrorHandler**

```python
# core/error_handler.py
class WorkerError(Exception):
    """Raised when a worker fails."""
    def __init__(self, worker_name: str, message: str):
        self.worker_name = worker_name
        self.message = message
        super().__init__(f"[{worker_name}] Failed: {message}")


class ErrorHandler:
    """Tracks per-worker success/failure across the pipeline."""

    def __init__(self):
        self._results: dict[str, dict] = {}
        self._errors: dict[str, str] = {}

    def record_success(self, worker_name: str, result: dict) -> None:
        self._results[worker_name] = result
        self._errors.pop(worker_name, None)

    def record_failure(self, worker_name: str, error: str) -> None:
        self._errors[worker_name] = error
        self._results.pop(worker_name, None)

    def get_results(self, worker_name: str) -> dict | None:
        return self._results.get(worker_name)

    def get_error(self, worker_name: str) -> str | None:
        return self._errors.get(worker_name)

    def get_status(self, worker_name: str) -> str:
        if worker_name in self._results:
            return "success"
        if worker_name in self._errors:
            return "failed"
        return "not_run"

    def all_workers_succeeded(self, worker_names: list[str]) -> bool:
        return all(self.get_status(name) == "success" for name in worker_names)

    def has_partial_failure(self, worker_names: list[str]) -> bool:
        statuses = [self.get_status(name) for name in worker_names]
        return "failed" in statuses and "success" in statuses

    def get_summary(self, worker_names: list[str]) -> dict:
        summary = {}
        for name in worker_names:
            status = self.get_status(name)
            entry = {"status": status}
            if status == "success":
                entry["data"] = self._results.get(name)
            elif status == "failed":
                entry["error"] = self._errors.get(name)
            summary[name] = entry
        return summary
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/test_error_handler.py -v
```
Expected: All 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add core/error_handler.py tests/test_error_handler.py
git commit -m "feat: add ErrorHandler for tracking worker success/failure"
```

---

### Task 5: Model Router

**Files:**
- Create: `models/model_router.py`
- Test: `tests/test_model_router.py`

- [ ] **Step 1: Write tests for ModelRouter**

```python
# tests/test_model_router.py
from models.model_router import ModelRouter, ModelTier


def test_light_tier_for_parse():
    router = ModelRouter()
    tier = router.select_model("parse", input_size=1000)
    assert tier == ModelTier.LIGHT


def test_light_tier_for_metadata():
    router = ModelRouter()
    tier = router.select_model("extract_metadata", input_size=500)
    assert tier == ModelTier.LIGHT


def test_medium_tier_for_small_summary():
    router = ModelRouter()
    tier = router.select_model("summarize", input_size=3000)
    assert tier == ModelTier.MEDIUM


def test_heavy_tier_for_large_summary():
    router = ModelRouter()
    tier = router.select_model("summarize", input_size=10000)
    assert tier == ModelTier.HEAVY


def test_heavy_tier_for_critical_appraisal():
    router = ModelRouter()
    tier = router.select_model("critical_appraisal", input_size=5000)
    assert tier == ModelTier.HEAVY


def test_heavy_tier_for_generate():
    router = ModelRouter()
    tier = router.select_model("generate_article", input_size=8000)
    assert tier == ModelTier.HEAVY


def test_medium_for_gap_simple():
    router = ModelRouter()
    tier = router.select_model("gap_analysis", input_size=2000, complexity_hint="simple")
    assert tier == ModelTier.MEDIUM


def test_heavy_for_gap_complex():
    router = ModelRouter()
    tier = router.select_model("gap_analysis", input_size=2000, complexity_hint="complex")
    assert tier == ModelTier.HEAVY


def test_medium_for_data_analysis():
    router = ModelRouter()
    tier = router.select_model("data_analysis_own", input_size=1000)
    assert tier == ModelTier.MEDIUM


def test_get_model_name():
    router = ModelRouter(
        models={
            "light": "google/gemini-flash",
            "medium": "anthropic/claude-sonnet",
            "heavy": "anthropic/claude-opus",
        }
    )
    assert router.get_model_name(ModelTier.LIGHT) == "google/gemini-flash"
    assert router.get_model_name(ModelTier.HEAVY) == "anthropic/claude-opus"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_model_router.py -v
```
Expected: FAIL.

- [ ] **Step 3: Implement ModelRouter**

```python
# models/model_router.py
from enum import Enum
from typing import Optional


class ModelTier(Enum):
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"


class ModelRouter:
    """Auto-selects 9Router models based on task type and input size.

    Routing rules (from spec §5):
    - parse, extract_metadata, format_check → Light
    - summarize, translate, structure_review (<5000 words) → Medium
    - summarize, translate, structure_review (>=5000 words) → Heavy
    - critical_appraisal, methodology_review, statistical_validation, generate_article → Heavy
    - gap_analysis (simple) → Medium, (complex) → Heavy
    - data_analysis_own → Medium
    """

    LIGHT_TASKS = {"parse", "extract_metadata", "format_check"}
    MEDIUM_SUMMARY_THRESHOLD = 5000  # words
    HEAVY_TASKS = {
        "critical_appraisal", "methodology_review",
        "statistical_validation", "generate_article",
    }

    DEFAULT_MODELS = {
        "light": "google/gemini-2.0-flash",
        "medium": "anthropic/claude-sonnet-4-20250514",
        "heavy": "anthropic/claude-opus-4-20250514",
    }

    def __init__(self, models: dict | None = None):
        self.models = models or dict(self.DEFAULT_MODELS)

    def select_model(
        self,
        task_type: str,
        input_size: int,
        complexity_hint: Optional[str] = None,
    ) -> ModelTier:
        """Select the appropriate model tier for a task."""
        if task_type in self.LIGHT_TASKS:
            return ModelTier.LIGHT

        if task_type in ("summarize", "translate", "structure_review"):
            if input_size < self.MEDIUM_SUMMARY_THRESHOLD:
                return ModelTier.MEDIUM
            return ModelTier.HEAVY

        if task_type in self.HEAVY_TASKS:
            return ModelTier.HEAVY

        if task_type == "gap_analysis":
            if complexity_hint == "simple":
                return ModelTier.MEDIUM
            return ModelTier.HEAVY

        if task_type == "data_analysis_own":
            return ModelTier.MEDIUM

        # Default to medium for unknown tasks
        return ModelTier.MEDIUM

    def get_model_name(self, tier: ModelTier) -> str:
        """Get the 9Router model name for a tier."""
        return self.models[tier.value]

    def get_fallback_chain(self, tier: ModelTier) -> list[ModelTier]:
        """Get the fallback chain for a tier."""
        all_tiers = [ModelTier.LIGHT, ModelTier.MEDIUM, ModelTier.HEAVY]
        idx = all_tiers.index(tier)
        # Same tier alternatives handled by caller; here we return tier-down chain
        return all_tiers[max(0, idx - 1):idx] + all_tiers[idx + 1:]
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/test_model_router.py -v
```
Expected: All 10 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add models/model_router.py tests/test_model_router.py
git commit -m "feat: add ModelRouter with heuristic tier selection and fallback chain"
```

---

### Task 6: PDF Parser

**Files:**
- Create: `parsers/__init__.py`
- Create: `parsers/pdf_parser.py`
- Test: `tests/test_parsers.py`

- [ ] **Step 1: Write tests for PDFParser**

```python
# tests/test_parsers.py (partial — parser tests)
import os
import tempfile
from parsers.pdf_parser import PDFParser


def _create_test_pdf(text: str, path: str) -> str:
    """Create a minimal PDF with the given text using pymupdf."""
    import fitz
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    doc.save(path)
    doc.close()
    return path


def test_parse_simple_pdf(tmp_path):
    pdf_path = str(tmp_path / "test.pdf")
    _create_test_pdf("Abstract: This is a test.\n\nIntroduction: Hello world.", pdf_path)
    parser = PDFParser()
    article = parser.parse(pdf_path)
    assert "test" in article.raw_text.lower()
    assert article.metadata.get("source_file") == pdf_path


def test_parse_nonexistent_file():
    parser = PDFParser()
    try:
        parser.parse("/nonexistent/file.pdf")
        assert False, "Should raise FileNotFoundError"
    except FileNotFoundError:
        pass
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_parsers.py::test_parse_simple_pdf tests/test_parsers.py::test_parse_nonexistent_file -v
```
Expected: FAIL.

- [ ] **Step 3: Implement PDFParser**

```python
# parsers/__init__.py
from parsers.pdf_parser import PDFParser
from parsers.text_parser import TextParser
from parsers.url_fetcher import URLFetcher

__all__ = ["PDFParser", "TextParser", "URLFetcher"]
```

```python
# parsers/pdf_parser.py
import os
from models.article_data import StructuredArticleData


class PDFParser:
    """Extract text and structure from PDF files.

    Uses pymupdf (fitz) for text extraction.
    """

    def __init__(self):
        self._fitz = None

    def _get_fitz(self):
        """Lazy import fitz to avoid import error if pymupdf not installed."""
        if self._fitz is None:
            try:
                import fitz
                self._fitz = fitz
            except ImportError:
                raise ImportError(
                    "pymupdf is required for PDF parsing. Install: pip install pymupdf"
                )
        return self._fitz

    def parse(self, file_path: str) -> StructuredArticleData:
        """Parse a PDF file into StructuredArticleData."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        fitz = self._get_fitz()
        doc = fitz.open(file_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()

        article = StructuredArticleData(
            metadata={"source_file": file_path, "source_type": "pdf"},
            raw_text=full_text,
        )

        # Basic section detection from headings
        article.sections = self._detect_sections(full_text)
        return article

    def _detect_sections(self, text: str) -> dict[str, str]:
        """Detect sections from common academic paper headings."""
        import re
        section_patterns = [
            r"(?i)^abstract\s*$",
            r"(?i)^introduction\s*$",
            r"(?i)^(literature\s*review|related\s*work)\s*$",
            r"(?i)^(methodology|methods|materials?\s*and\s*methods)\s*$",
            r"(?i)^(results?|findings)\s*$",
            r"(?i)^discussion\s*$",
            r"(?i)^conclusion\s*$",
            r"(?i)^(references|bibliography)\s*$",
        ]
        section_names = [
            "abstract", "introduction", "literature_review",
            "methodology", "results", "discussion", "conclusion", "references",
        ]

        sections = {}
        lines = text.split("\n")
        current_section = None
        current_text = []

        for line in lines:
            matched = False
            for i, pattern in enumerate(section_patterns):
                if re.match(pattern, line.strip()):
                    if current_section is not None:
                        sections[current_section] = "\n".join(current_text).strip()
                    current_section = section_names[i]
                    current_text = []
                    matched = True
                    break
            if not matched:
                current_text.append(line)

        if current_section is not None:
            sections[current_section] = "\n".join(current_text).strip()

        # If no sections detected, put everything in raw_text fallback
        if not sections:
            sections["full_text"] = text.strip()

        return sections
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pip install pymupdf  # if not already installed
pytest tests/test_parsers.py::test_parse_simple_pdf tests/test_parsers.py::test_parse_nonexistent_file -v
```
Expected: All 2 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add parsers/__init__.py parsers/pdf_parser.py tests/test_parsers.py
git commit -m "feat: add PDFParser with section detection from headings"
```

---

### Task 7: Text Parser

**Files:**
- Create: `parsers/text_parser.py`
- Test: `tests/test_parsers.py` (add tests)

- [ ] **Step 1: Write tests for TextParser**

Add to `tests/test_parsers.py`:

```python
from parsers.text_parser import TextParser


def test_parse_text_with_sections():
    text = """## ABSTRACT
This is the abstract.

## INTRODUCTION
This is the introduction.

## METHODOLOGY
We used a survey method.
"""
    parser = TextParser()
    article = parser.parse(text)
    assert article.sections["abstract"] == "This is the abstract."
    assert article.sections["introduction"] == "This is the introduction."
    assert article.sections["methodology"] == "We used a survey method."


def test_parse_text_without_sections():
    text = "This is just plain text with no headings."
    parser = TextParser()
    article = parser.parse(text)
    assert article.sections["full_text"] == text
    assert article.raw_text == text


def test_parse_short_text_warning():
    text = "Short text."
    parser = TextParser()
    article = parser.parse(text)
    assert article.metadata.get("warning") is not None
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_parsers.py -k "text" -v
```
Expected: FAIL.

- [ ] **Step 3: Implement TextParser**

```python
# parsers/text_parser.py
import re
from models.article_data import StructuredArticleData


class TextParser:
    """Parse plain text or markdown input into StructuredArticleData.

    Detects sections from markdown-style headings (## HEADING).
    """

    SECTION_PATTERNS = {
        r"(?i)##\s*abstract\s*$": "abstract",
        r"(?i)##\s*introduction\s*$": "introduction",
        r"(?i)##\s*(literature\s*review|related\s*work)\s*$": "literature_review",
        r"(?i)##\s*(methodology|methods)\s*$": "methodology",
        r"(?i)##\s*(results?|findings)\s*$": "results",
        r"(?i)##\s*discussion\s*$": "discussion",
        r"(?i)##\s*conclusion\s*$": "conclusion",
        r"(?i)##\s*(references|bibliography)\s*$": "references",
    }

    def parse(self, text: str) -> StructuredArticleData:
        """Parse text into StructuredArticleData."""
        article = StructuredArticleData(
            metadata={"source_type": "text"},
            raw_text=text,
        )

        article.sections = self._detect_sections(text)

        if len(text.split()) < 500:
            article.metadata["warning"] = "Teks terlalu pendek untuk analisis meaningful"

        return article

    def _detect_sections(self, text: str) -> dict[str, str]:
        """Detect sections from markdown headings."""
        lines = text.split("\n")
        sections = {}
        current_section = None
        current_text = []

        for line in lines:
            matched = False
            for pattern, name in self.SECTION_PATTERNS.items():
                if re.match(pattern, line.strip()):
                    if current_section is not None:
                        sections[current_section] = "\n".join(current_text).strip()
                    current_section = name
                    current_text = []
                    matched = True
                    break
            if not matched:
                current_text.append(line)

        if current_section is not None:
            sections[current_section] = "\n".join(current_text).strip()

        if not sections:
            sections["full_text"] = text.strip()

        return sections
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/test_parsers.py -k "text" -v
```
Expected: All 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add parsers/text_parser.py tests/test_parsers.py
git commit -m "feat: add TextParser with markdown heading detection"
```

---

### Task 8: URL Fetcher

**Files:**
- Create: `parsers/url_fetcher.py`
- Test: `tests/test_parsers.py` (add tests)

- [ ] **Step 1: Write tests for URLFetcher**

Add to `tests/test_parsers.py`:

```python
from unittest.mock import patch, MagicMock
from parsers.url_fetcher import URLFetcher


def test_fetch_url_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "## ABSTRACT\nTest abstract.\n\n## INTRODUCTION\nTest intro."}}]
    }
    with patch("parsers.url_fetcher.requests.post", return_value=mock_response):
        fetcher = URLFetcher(ninerouter_url="http://localhost:20128", ninerouter_key="test-key")
        article = fetcher.fetch("https://doi.org/10.1234/test")
        assert article.metadata["source_type"] == "url"
        assert article.sections["abstract"] == "Test abstract."


def test_fetch_invalid_url():
    with patch("parsers.url_fetcher.requests.post") as mock_post:
        mock_post.side_effect = Exception("Connection refused")
        fetcher = URLFetcher(ninerouter_url="http://localhost:20128", ninerouter_key="test-key")
        try:
            fetcher.fetch("https://invalid-url-xyz.com")
            assert False, "Should raise"
        except Exception as e:
            assert "Connection refused" in str(e)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_parsers.py -k "url" -v
```
Expected: FAIL.

- [ ] **Step 3: Implement URLFetcher**

```python
# parsers/url_fetcher.py
import os
import requests
from models.article_data import StructuredArticleData
from parsers.text_parser import TextParser


class URLFetcher:
    """Fetch content from DOI or URL via 9router-web-fetch, then parse."""

    def __init__(self, ninerouter_url: str | None = None, ninerouter_key: str | None = None):
        self.ninerouter_url = ninerouter_url or os.getenv("NINEROUTER_URL", "http://localhost:20128")
        self.ninerouter_key = ninerouter_key or os.getenv("NINEROUTER_KEY", "")
        self._headers = {"Content-Type": "application/json"}
        if self.ninerouter_key:
            self._headers["Authorization"] = f"Bearer {self.ninerouter_key}"

    def fetch(self, url: str) -> StructuredArticleData:
        """Fetch URL content and parse into StructuredArticleData."""
        text = self._fetch_via_9router(url)
        parser = TextParser()
        article = parser.parse(text)
        article.metadata["source_type"] = "url"
        article.metadata["source_url"] = url
        return article

    def _fetch_via_9router(self, url: str) -> str:
        """Fetch URL content using 9router-web-fetch."""
        endpoint = f"{self.ninerouter_url}/v1/chat/completions"
        payload = {
            "model": "jina/reader",
            "messages": [
                {
                    "role": "user",
                    "content": f"Fetch and extract the full text content from this URL: {url}. Return only the article text in markdown format."
                }
            ],
            "max_tokens": 16000,
            "temperature": 0,
            "stream": False,
        }
        response = requests.post(endpoint, headers=self._headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/test_parsers.py -k "url" -v
```
Expected: All 2 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add parsers/url_fetcher.py tests/test_parsers.py
git commit -m "feat: add URLFetcher via 9router-web-fetch"
```

---

### Task 9: Output Aggregator

**Files:**
- Create: `core/output_aggregator.py`
- Test: `tests/test_output_aggregator.py`

- [ ] **Step 1: Write tests for OutputAggregator**

```python
# tests/test_output_aggregator.py
from core.output_aggregator import OutputAggregator


def test_aggregate_single_worker():
    agg = OutputAggregator()
    result = agg.aggregate({
        "reader": {"status": "success", "data": {"summary": "Paper about X."}},
    })
    assert "Paper about X." in result


def test_aggregate_multiple_workers():
    agg = OutputAggregator()
    result = agg.aggregate({
        "reader": {"status": "success", "data": {"summary": "Summary here."}},
        "reviewer": {"status": "success", "data": {"assessment": "Major Revision", "comments": "Fix methods."}},
    })
    assert "Summary here." in result
    assert "Major Revision" in result


def test_aggregate_partial_failure():
    agg = OutputAggregator()
    result = agg.aggregate({
        "reader": {"status": "success", "data": {"summary": "Summary."}},
        "reviewer": {"status": "failed", "error": "Model unavailable"},
    })
    assert "Summary." in result
    assert "[reviewer] Gagal: Model unavailable" in result


def test_format_markdown():
    agg = OutputAggregator()
    result = agg.aggregate({
        "reader": {"status": "success", "data": {"summary": "Test summary"}},
    })
    assert "# Ringkasan Jurnal" in result
    assert "Test summary" in result
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_output_aggregator.py -v
```
Expected: FAIL.

- [ ] **Step 3: Implement OutputAggregator**

```python
# core/output_aggregator.py
class OutputAggregator:
    """Combines worker outputs into a single Bahasa Indonesia markdown report."""

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
                parts.append(f"## Review Peer\n")
                parts.append(f"[reviewer] Gagal: {wr.get('error', 'Unknown error')}. Coba lagi nanti.\n")
            parts.append("")

        return "\n".join(parts)
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/test_output_aggregator.py -v
```
Expected: All 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add core/output_aggregator.py tests/test_output_aggregator.py
git commit -m "feat: add OutputAggregator for combining worker outputs into markdown"
```

---

### Task 10: Prompt System

**Files:**
- Create: `prompts/system/reader.md`
- Create: `prompts/system/reviewer.md`
- Create: `prompts/templates/reader_user.j2`
- Create: `prompts/templates/reviewer_user.j2`

- [ ] **Step 1: Create prompt files**

```markdown
# prompts/system/reader.md
Anda adalah pembaca jurnal ilmiah profesional yang berpengalaman.
Tugas Anda: meringkas jurnal ilmiah tanpa menghilangkan esensi dan nilai ilmiahnya.

Bahasa output: Bahasa Indonesia.
Tone: Akademis, jelas, dan ringkas.

Format ringkasan:
1. LATAR BELAKANG — konteks dan motivasi penelitian
2. TUJUAN — apa yang ingin dicapai peneliti
3. METODE — pendekatan dan teknik yang digunakan
4. HASIL — temuan utama (angka/persentase jika ada)
5. IMPLIKASI — dampak dan aplikasi praktis dari temuan

Jangan menghilangkan metodologi, hasil kuantitatif, atau implikasi penting.
```

```markdown
# prompts/system/reviewer.md
Anda adalah peer reviewer jurnal internasional bereputasi (Q1/Q2).
Tugas Anda: mengevaluasi naskah ilmiah secara objektif, konstruktif, dan mendalam.

Bahasa output: Bahasa Indonesia.
Tone: Profesional, kritis namun menghargai karya penulis.

Format review:
1. OVERALL ASSESSMENT (Accept / Minor Revision / Major Revision / Reject)
2. KEKUATAN (3-5 poin)
3. MASALAH UTAMA (jika ada — dengan justifikasi)
4. MASALAH MINOR (jika ada — spesifik per section)
5. REKOMENDASI (saran konkret untuk perbaikan)

Kriteria evaluasi:
- Originalitas dan kontribusi
- Kesesuaian metode dengan tujuan riset
- Validitas analisis data dan statistik
- Koherensi argumen (logical flow)
- Kelengkapan dan relevansi referensi
- Kejelasan penulisan dan struktur IMRAD
```

```jinja2
{# prompts/templates/reader_user.j2 #}
Ringkas jurnal berikut:

Judul: {{ metadata.title }}
{% if metadata.authors %}Penulis: {{ metadata.authors | join(', ') }}{% endif %}
{% if metadata.publication_year %}Tahun: {{ metadata.publication_year }}{% endif %}

{% for section_name, content in sections.items() %}
## {{ section_name | upper }}
{{ content }}
{% endfor %}

Berikan ringkasan sesuai format yang ditentukan.
```

```jinja2
{# prompts/templates/reviewer_user.j2 #}
Review jurnal berikut sebagai peer reviewer jurnal internasional:

Judul: {{ metadata.title }}
{% if metadata.authors %}Penulis: {{ metadata.authors | join(', ') }}{% endif %}
{% if metadata.publication_year %}Tahun: {{ metadata.publication_year }}{% endif %}
{% if methodology_type %}Metodologi: {{ methodology_type }}{% endif %}

{% if reader_summary %}
Ringkasan dari pembaca sebelumnya:
{{ reader_summary }}
{% endif %}

--- TEKS LENGKAP ---
{% for section_name, content in sections.items() %}
## {{ section_name | upper }}
{{ content }}
{% endfor %}

Berikan review sesuai format yang ditentukan.
```

- [ ] **Step 2: Commit**

```bash
git add prompts/
git commit -m "feat: add prompt templates for reader and reviewer workers"
```

---

### Task 11: Reader Worker

**Files:**
- Create: `workers/__init__.py`
- Create: `workers/reader_worker.py`
- Test: `tests/test_reader_worker.py`

- [ ] **Step 1: Write tests for ReaderWorker**

```python
# tests/test_reader_worker.py
from unittest.mock import patch, MagicMock
from models.article_data import StructuredArticleData
from workers.reader_worker import ReaderWorker


def _make_article() -> StructuredArticleData:
    return StructuredArticleData(
        metadata={"title": "Test Paper", "authors": ["Test Author"]},
        sections={"abstract": "Test abstract", "introduction": "Test intro"},
        raw_text="Test full text",
    )


def test_reader_calls_chat():
    article = _make_article()
    mock_result = "LATAR BELAKANG: Test.\nTUJUAN: Test.\nMETODE: Test."

    with patch.object(ReaderWorker, "_chat", return_value=mock_result) as mock_chat:
        worker = ReaderWorker(ninerouter_url="http://test", ninerouter_key="key")
        result = worker.run(article)
        mock_chat.assert_called_once()
        assert "summary" in result
        assert "LATAR BELAKANG" in result["summary"]


def test_reader_returns_structured_output():
    article = _make_article()
    mock_result = "LATAR BELAKANG: Test context.\nTUJUAN: Test goal."

    with patch.object(ReaderWorker, "_chat", return_value=mock_result):
        worker = ReaderWorker(ninerouter_url="http://test", ninerouter_key="key")
        result = worker.run(article)
        assert isinstance(result, dict)
        assert "summary" in result


def test_reader_handles_error():
    article = _make_article()

    with patch.object(ReaderWorker, "_chat", side_effect=Exception("API down")):
        worker = ReaderWorker(ninerouter_url="http://test", ninerouter_key="key")
        result = worker.run(article)
        assert result is None
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_reader_worker.py -v
```
Expected: FAIL.

- [ ] **Step 3: Implement ReaderWorker**

```python
# workers/__init__.py
from workers.reader_worker import ReaderWorker
from workers.reviewer_worker import ReviewerWorker

__all__ = ["ReaderWorker", "ReviewerWorker"]
```

```python
# workers/reader_worker.py
import os
import requests
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from models.article_data import StructuredArticleData


class ReaderWorker:
    """Smart summarizer worker. Produces richer summaries than original abstracts."""

    def __init__(
        self,
        ninerouter_url: str | None = None,
        ninerouter_key: str | None = None,
        prompts_dir: str = "prompts",
    ):
        self.ninerouter_url = ninerouter_url or os.getenv("NINEROUTER_URL", "http://localhost:20128")
        self.ninerouter_key = ninerouter_key or os.getenv("NINEROUTER_KEY", "")
        self._headers = {"Content-Type": "application/json"}
        if self.ninerouter_key:
            self._headers["Authorization"] = f"Bearer {self.ninerouter_key}"

        self._prompts_dir = Path(prompts_dir)
        self._env = Environment(loader=FileSystemLoader(str(self._prompts_dir / "templates")))

    def run(self, article: StructuredArticleData, model: str = "anthropic/claude-sonnet-4-20250514") -> dict | None:
        """Run the reader worker on an article.

        Returns:
            {"summary": str} or None on failure.
        """
        system_prompt = self._load_system_prompt("reader.md")
        user_prompt = self._build_user_prompt(article)

        response = self._chat(system_prompt, user_prompt, model)
        if response is None:
            return None

        return {"summary": response}

    def _chat(self, system_prompt: str, user_prompt: str, model: str) -> str | None:
        """Call 9Router chat completion."""
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

    def _build_user_prompt(self, article: StructuredArticleData) -> str:
        template = self._env.get_template("reader_user.j2")
        return template.render(
            metadata=article.metadata,
            sections=article.sections,
        )
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/test_reader_worker.py -v
```
Expected: All 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add workers/__init__.py workers/reader_worker.py tests/test_reader_worker.py
git commit -m "feat: add ReaderWorker with 9Router chat and Jinja2 prompt templates"
```

---

### Task 12: Reviewer Worker

**Files:**
- Create: `workers/reviewer_worker.py`
- Test: `tests/test_reviewer_worker.py`

- [ ] **Step 1: Write tests for ReviewerWorker**

```python
# tests/test_reviewer_worker.py
from unittest.mock import patch
from models.article_data import StructuredArticleData
from workers.reviewer_worker import ReviewerWorker


def _make_article() -> StructuredArticleData:
    return StructuredArticleData(
        metadata={"title": "Test Paper", "authors": ["Test Author"], "publication_year": 2024},
        sections={
            "abstract": "Test abstract about methodology.",
            "introduction": "Background and research question.",
            "methodology": "We used quantitative survey method with n=200.",
            "results": "Significant correlation found (p<0.05).",
            "discussion": "Results support the hypothesis.",
            "conclusion": "Further research needed.",
        },
        methodology_type="kuantitatif",
        raw_text="Full text.",
    )


def test_reviewer_calls_chat_with_context():
    article = _make_article()
    mock_result = "OVERALL ASSESSMENT: Major Revision\n\nKEKUATAN: 1. Good methodology"

    with patch.object(ReviewerWorker, "_chat", return_value=mock_result) as mock_chat:
        worker = ReviewerWorker(ninerouter_url="http://test", ninerouter_key="key")
        result = worker.run(article, reader_summary="Summary context")
        mock_chat.assert_called_once()
        assert "assessment" in result
        assert "review_text" in result


def test_reviewer_extracts_assessment():
    article = _make_article()
    mock_result = "OVERALL ASSESSMENT: Minor Revision\n\nSome review text here."

    with patch.object(ReviewerWorker, "_chat", return_value=mock_result):
        worker = ReviewerWorker(ninerouter_url="http://test", ninerouter_key="key")
        result = worker.run(article)
        assert result["assessment"] == "Minor Revision"


def test_reviewer_handles_no_assessment():
    article = _make_article()
    mock_result = "This paper is good."

    with patch.object(ReviewerWorker, "_chat", return_value=mock_result):
        worker = ReviewerWorker(ninerouter_url="http://test", ninerouter_key="key")
        result = worker.run(article)
        assert result["assessment"] == "N/A"
        assert result["review_text"] == "This paper is good."


def test_reviewer_handles_error():
    article = _make_article()

    with patch.object(ReviewerWorker, "_chat", side_effect=Exception("API down")):
        worker = ReviewerWorker(ninerouter_url="http://test", ninerouter_key="key")
        result = worker.run(article)
        assert result is None
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_reviewer_worker.py -v
```
Expected: FAIL.

- [ ] **Step 3: Implement ReviewerWorker**

```python
# workers/reviewer_worker.py
import os
import re
import requests
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from models.article_data import StructuredArticleData


class ReviewerWorker:
    """Peer reviewer worker. Produces international journal-level reviews."""

    def __init__(
        self,
        ninerouter_url: str | None = None,
        ninerouter_key: str | None = None,
        prompts_dir: str = "prompts",
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
        model: str = "anthropic/claude-opus-4-20250514",
    ) -> dict | None:
        """Run the reviewer worker on an article.

        Args:
            article: The article to review.
            reader_summary: Optional summary from Reader Worker for context.
            model: 9Router model name.

        Returns:
            {"assessment": str, "review_text": str} or None on failure.
        """
        system_prompt = self._load_system_prompt("reviewer.md")
        user_prompt = self._build_user_prompt(article, reader_summary)

        response = self._chat(system_prompt, user_prompt, model)
        if response is None:
            return None

        assessment = self._extract_assessment(response)
        return {"assessment": assessment, "review_text": response}

    def _chat(self, system_prompt: str, user_prompt: str, model: str) -> str | None:
        """Call 9Router chat completion."""
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

    def _build_user_prompt(
        self, article: StructuredArticleData, reader_summary: str | None = None
    ) -> str:
        template = self._env.get_template("reviewer_user.j2")
        return template.render(
            metadata=article.metadata,
            sections=article.sections,
            methodology_type=article.methodology_type,
            reader_summary=reader_summary or "",
        )

    def _extract_assessment(self, review_text: str) -> str:
        """Extract overall assessment from review text."""
        patterns = [
            r"(?i)OVERALL ASSESSMENT[:\s]*(Accept|Minor Revision|Major Revision|Reject)",
            r"(?i)overall[:\s]*(Accept|Minor Revision|Major Revision|Reject)",
            r"(?i)penilaian[:\s]*(Accept|Minor Revision|Major Revision|Reject)",
        ]
        for pattern in patterns:
            match = re.search(pattern, review_text)
            if match:
                return match.group(1).strip()
        return "N/A"
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/test_reviewer_worker.py -v
```
Expected: All 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add workers/reviewer_worker.py tests/test_reviewer_worker.py
git commit -m "feat: add ReviewerWorker with assessment extraction and 9Router chat"
```

---

### Task 13: Config File

**Files:**
- Create: `analyze.config.json`

- [ ] **Step 1: Create config file**

```json
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

- [ ] **Step 2: Commit**

```bash
git add analyze.config.json
git commit -m "feat: add default config file for analyze.py"
```

---

### Task 14: CLI Orchestrator (analyze.py)

**Files:**
- Create: `analyze.py`

- [ ] **Step 1: Implement analyze.py**

```python
#!/usr/bin/env python3
"""Journal Analysis System — CLI Orchestrator.

Usage:
    python analyze.py jurnal.pdf --mode read
    python analyze.py jurnal.pdf --mode review
    python analyze.py jurnal.pdf --mode full
    python analyze.py --input-text "teks..." --mode review

Note: generate, data-analysis, and compare modes deferred to Phase 2-4.
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Journal Analysis System")
    parser.add_argument("input", nargs="?", help="PDF file or URL/DOI")
    parser.add_argument("--mode", required=True, choices=["read", "review", "full"], help="Analysis mode")
    parser.add_argument("--input-text", help="Input text directly")
    parser.add_argument("--no-limit", action="store_true", help="Bypass token budget limit")
    args = parser.parse_args()

    # Load config
    config = _load_config()

    # Initialize core components
    from core.token_budget import TokenBudget
    from core.cache import AnalysisCache
    from core.error_handler import ErrorHandler
    from core.output_aggregator import OutputAggregator
    from models.model_router import ModelRouter, ModelTier

    budget = TokenBudget(
        daily_limit=config["token_budget"]["daily_limit"],
        per_task=config["token_budget"]["per_task"],
    )
    cache = AnalysisCache(ttl_days=config["cache_ttl_days"])
    error_handler = ErrorHandler()
    aggregator = OutputAggregator()
    router = ModelRouter(models=config["default_models"])

    # Check budget
    task_budget = budget.get_task_budget(args.mode)
    if not args.no_limit and not budget.check_available(task_budget):
        print(f"Token budget habis (sisa {budget.remaining}). Reset besok 00:00.")
        sys.exit(1)

    if not args.no_limit and budget.used_today / budget.daily_limit >= 0.8:
        print(f"Warning: 80% token budget terpakai hari ini.")

    # Parse input
    article = _parse_input(args, cache)
    if article is None:
        print("Error: Tidak bisa parse input.")
        sys.exit(1)

    # Content hash for caching
    content_hash = hashlib.sha256(article.raw_text.encode()).hexdigest()

    # Check parse cache
    cached = cache.get_parsed(content_hash)
    if cached:
        from models.article_data import StructuredArticleData
        article = StructuredArticleData(**cached)
    else:
        cache.set_parsed(content_hash, {
            "metadata": article.metadata,
            "sections": article.sections,
            "methodology_type": article.methodology_type,
            "raw_text": article.raw_text,
        })

    # Execute workers based on mode
    results = {}

    if args.mode in ("read", "review", "full"):
        # Reader always runs first
        reader_result = _run_reader(article, cache, content_hash, config, router, budget, args.no_limit)
        results["reader"] = reader_result

    if args.mode in ("review", "full"):
        reviewer_result = _run_reviewer(article, results.get("reader"), cache, content_hash, config, router, budget, args.no_limit)
        results["reviewer"] = reviewer_result

    # Output
    output = aggregator.aggregate(results)
    print(output)

    # Save to file
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"analysis_{content_hash[:8]}.md"
    output_file.write_text(output, encoding="utf-8")
    print(f"\nOutput saved to: {output_file}")

    budget.add_usage(_estimate_tokens(article.word_count, args.mode))


def _load_config() -> dict:
    config_path = Path("analyze.config.json")
    if config_path.exists():
        with open(config_path, "r") as f:
            return json.load(f)
    return {
        "token_budget": {"daily_limit": 50000, "per_task": {"read": 5000, "review": 15000, "full": 30000}},
        "default_models": {"light": "google/gemini-2.0-flash", "medium": "anthropic/claude-sonnet-4-20250514", "heavy": "anthropic/claude-opus-4-20250514"},
        "cache_ttl_days": 7,
    }


def _parse_input(args, cache) -> "StructuredArticleData":
    from parsers.pdf_parser import PDFParser
    from parsers.text_parser import TextParser
    from parsers.url_fetcher import URLFetcher

    if args.input_text:
        parser = TextParser()
        return parser.parse(args.input_text)

    if args.input is None:
        return None

    input_path = Path(args.input)

    # Check if URL/DOI
    if args.input.startswith(("http://", "https://", "doi:")):
        fetcher = URLFetcher()
        return fetcher.fetch(args.input)

    # Check if PDF
    if input_path.suffix.lower() == ".pdf":
        pdf_parser = PDFParser()
        return pdf_parser.parse(str(input_path))

    # Default: treat as text file
    text_parser = TextParser()
    return text_parser.parse(input_path.read_text(encoding="utf-8"))


def _run_reader(article, cache, content_hash, config, router, budget, no_limit):
    from core.cache import AnalysisCache
    from workers.reader_worker import ReaderWorker

    # Check analysis cache
    cached = cache.get_analysis(content_hash, "reader")
    if cached:
        return {"status": "success", "data": cached}

    model = router.get_model_name(router.select_model("summarize", article.word_count))
    worker = ReaderWorker()
    result = worker.run(article, model=model)

    if result is None:
        return {"status": "failed", "error": "Reader Worker gagal"}

    cache.set_analysis(content_hash, "reader", result)
    return {"status": "success", "data": result}


def _run_reviewer(article, reader_result, cache, content_hash, config, router, budget, no_limit):
    from workers.reviewer_worker import ReviewerWorker

    # Check analysis cache
    cached = cache.get_analysis(content_hash, "reviewer")
    if cached:
        return {"status": "success", "data": cached}

    model = router.get_model_name(router.select_model("critical_appraisal", article.word_count))
    reader_summary = reader_result["data"]["summary"] if reader_result and reader_result["status"] == "success" else None

    worker = ReviewerWorker()
    result = worker.run(article, reader_summary=reader_summary, model=model)

    if result is None:
        return {"status": "failed", "error": "Reviewer Worker gagal"}

    cache.set_analysis(content_hash, "reviewer", result)
    return {"status": "success", "data": result}


def _estimate_tokens(word_count: int, mode: str) -> int:
    """Rough estimate: 1 word ≈ 1.3 tokens for input, plus output tokens."""
    input_tokens = int(word_count * 1.3)
    output_multiplier = {"read": 2, "review": 5, "full": 7}.get(mode, 3)
    return input_tokens + (input_tokens * output_multiplier // 10)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Commit**

```bash
git add analyze.py
git commit -m "feat: add analyze.py CLI orchestrator with mode routing and caching"
```

---

### Task 15: Integration Test

**Files:**
- Create: `tests/test_integration.py`

- [ ] **Step 1: Write integration test**

```python
# tests/test_integration.py
"""Integration test: full pipeline with mocked 9Router."""
import json
import tempfile
from unittest.mock import patch
from models.article_data import StructuredArticleData
from parsers.text_parser import TextParser
from workers.reader_worker import ReaderWorker
from workers.reviewer_worker import ReviewerWorker
from core.output_aggregator import OutputAggregator


def _mock_chat_response(content: str):
    """Create a mock 9Router response."""
    from unittest.mock import MagicMock
    mock = MagicMock()
    mock.json.return_value = {"choices": [{"message": {"content": content}}]}
    mock.raise_for_status = MagicMock()
    return mock


def test_full_pipeline_text_input():
    """Test: text input → parse → reader → reviewer → aggregate."""
    text = """## ABSTRACT
This paper investigates the impact of AI on education.

## INTRODUCTION
AI is transforming education. This study explores how.

## METHODOLOGY
We conducted a survey of 500 teachers using quantitative methods.

## RESULTS
80% of teachers reported improved student engagement.

## DISCUSSION
Results suggest AI has significant positive impact.

## CONCLUSION
More research is needed on long-term effects.
"""
    # Parse
    parser = TextParser()
    article = parser.parse(text)
    assert article.sections["abstract"] == "This paper investigates the impact of AI on education."
    assert article.word_count > 0

    # Reader (mocked)
    reader_summary = "LATAR BELAKANG: AI di pendidikan sedang berkembang.\nTUJUAN: Meneliti dampak AI.\nMETODE: Survei 500 guru.\nHASIL: 80% engagement meningkat.\nIMPLIKASI: AI berdampak positif."

    with patch.object(ReaderWorker, "_chat", return_value=reader_summary):
        reader = ReaderWorker(prompts_dir="prompts")
        reader_result = reader.run(article)
        assert reader_result is not None
        assert "summary" in reader_result

    # Reviewer (mocked)
    review_text = "OVERALL ASSESSMENT: Minor Revision\n\nKEKUATAN:\n1. Metodologi jelas\n2. Sample size cukup\n\nMASALAH MINOR:\n1. Tambahkan effect size"

    with patch.object(ReviewerWorker, "_chat", return_value=review_text):
        reviewer = ReviewerWorker(prompts_dir="prompts")
        reviewer_result = reviewer.run(article, reader_summary=reader_summary)
        assert reviewer_result is not None
        assert reviewer_result["assessment"] == "Minor Revision"

    # Aggregate
    agg = OutputAggregator()
    output = agg.aggregate({
        "reader": {"status": "success", "data": reader_result},
        "reviewer": {"status": "success", "data": reviewer_result},
    })
    assert "# Ringkasan Jurnal" in output
    assert "## Review Peer" in output
    assert "Minor Revision" in output
```

- [ ] **Step 2: Run test to verify it passes**

```bash
pytest tests/test_integration.py -v
```
Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add tests/test_integration.py
git commit -m "test: add integration test for full pipeline"
```

---

### Task 16: Run All Tests + Final Commit

- [ ] **Step 1: Run all tests**

```bash
pytest tests/ -v --ignore=tests/test_9router.py --ignore=tests/test_journal_search.py --ignore=tests/test_integration.py
```
Expected: All Phase 1 tests PASS (40+ tests).

- [ ] **Step 2: Run integration test**

```bash
pytest tests/test_integration.py -v
```
Expected: PASS.

- [ ] **Step 3: Final commit**

```bash
git add -A
git commit -m "feat: journal analysis system phase 1 complete — foundation pipeline working"
```
