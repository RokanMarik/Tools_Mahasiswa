# Journal Analysis System — Phase 4: Polish & Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add comparison mode for multi-paper analysis, visualization support for data analysis, Zotero integration for saving analyzed papers, and comprehensive test coverage.

**Architecture:** Comparison mode uses a new `ComparisonWorker` that analyzes multiple papers side-by-side. Visualization uses matplotlib to generate charts from data analysis results. Zotero integration uses the existing `modules/zotero/` client to save papers with analysis metadata.

**Tech Stack:** Python 3.10+, `matplotlib` (visualization), `requests` (9Router + Zotero API), `jinja2` (prompts), `pytest` (testing).

**Related Spec:** `docs/superpowers/specs/2026-06-01-journal-analysis-system-design.md` (§13 Phase 4)

**Existing Context (Phase 1-3):**
- All workers in `journal_analyzer/workers/` follow same pattern
- CLI modes: read, review, full, gap, data-analysis, generate
- `journal_analyzer/core/output_aggregator.py` handles all worker outputs
- Existing Zotero modules at `modules/zotero/` — `ZoteroClient`, `CitationFormatter`, etc.
- 87 tests passing across Phase 1-3

---

## File Structure (Phase 4)

```
journal_analyzer/
├── analyze.py                      # MODIFY — add compare mode
├── workers/
│   └── comparison_worker.py        # CREATE — multi-paper comparison
├── core/
│   ├── output_aggregator.py        # MODIFY — add comparison section
│   └── visualizer.py               # CREATE — matplotlib charts
├── prompts/
│   ├── system/
│   │   └── comparison.md           # CREATE
│   └── templates/
│       └── comparison_user.j2      # CREATE
└── tests/
    ├── test_comparison.py          # CREATE
    ├── test_visualizer.py          # CREATE
    └── test_integration.py         # MODIFY — add compare pipeline test
```

---

### Task 1: Comparison Prompt System

**Files:**
- Create: `journal_analyzer/prompts/system/comparison.md`
- Create: `journal_analyzer/prompts/templates/comparison_user.j2`

- [ ] **Step 1: Create prompt files**

```markdown
# journal_analyzer/prompts/system/comparison.md
Anda adalah peneliti senior yang menganalisis perbandingan beberapa paper ilmiah.
Tugas Anda: membandingkan beberapa jurnal dan memberikan analisis komparatif.

Bahasa output: Bahasa Indonesia.
Tone: Analitis, objektif.

Format output:
1. TABEL PERBANDINGAN — ringkasan perbedaan utama per paper
2. KELEBIHAN & KEKURANGAN — per paper
3. KEKOHERENSAN — apakah temuan antar paper konsisten?
4. SYNTHESIS — insight gabungan dari semua paper
5. REKOMENDASI — paper mana yang paling relevan dan mengapa

Fokus pada:
- Metodologi yang berbeda dan implikasinya
- Hasil yang konsisten vs bertentangan
- Gap yang terungkap dari perbandingan
- Tren atau pola yang muncul dari multiple studies
```

```jinja2
{# journal_analyzer/prompts/templates/comparison_user.j2 #}
Bandingkan paper-paper berikut:

{% for paper in papers %}
--- Paper {{ loop.index }}: {{ paper.title }} ---
{% if paper.summary %}Ringkasan: {{ paper.summary }}{% endif %}
{% if paper.methodology %}Metodologi: {{ paper.methodology }}{% endif %}
{% if paper.key_findings %}Temuan: {{ paper.key_findings | join(', ') }}{% endif %}

{% endfor %}

Berikan analisis perbandingan sesuai format yang ditentukan.
```

- [ ] **Step 2: Commit**

```bash
git add journal_analyzer/prompts/system/comparison.md journal_analyzer/prompts/templates/comparison_user.j2
git commit -m "feat: add prompt templates for comparison worker"
```

---

### Task 2: Comparison Worker

**Files:**
- Create: `journal_analyzer/workers/comparison_worker.py`
- Test: `journal_analyzer/tests/test_comparison.py`

- [ ] **Step 1: Write tests**

```python
# journal_analyzer/tests/test_comparison.py
from unittest.mock import patch
from workers.comparison_worker import ComparisonWorker


def test_comparison_calls_chat():
    papers = [
        {"title": "Paper 1", "summary": "Summary 1", "methodology": "Quantitative", "key_findings": ["Finding A"]},
        {"title": "Paper 2", "summary": "Summary 2", "methodology": "Qualitative", "key_findings": ["Finding B"]},
    ]
    mock_result = "TABEL PERBANDINGAN:\nPaper 1 vs Paper 2: ..."

    with patch.object(ComparisonWorker, "_chat", return_value=mock_result) as mock_chat:
        worker = ComparisonWorker()
        result = worker.run(papers)
        mock_chat.assert_called_once()
        assert "comparison" in result


def test_comparison_returns_structured_output():
    papers = [{"title": "Test Paper", "summary": "Test"}]
    mock_result = "SYNTHESIS: All papers agree on X."

    with patch.object(ComparisonWorker, "_chat", return_value=mock_result):
        worker = ComparisonWorker()
        result = worker.run(papers)
        assert isinstance(result, dict)
        assert "comparison" in result


def test_comparison_handles_error():
    papers = [{"title": "Test"}]

    with patch.object(ComparisonWorker, "_chat", side_effect=Exception("API down")):
        worker = ComparisonWorker()
        result = worker.run(papers)
        assert result is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest journal_analyzer/tests/test_comparison.py -v`
Expected: FAIL.

- [ ] **Step 3: Implement ComparisonWorker**

```python
# journal_analyzer/workers/comparison_worker.py
import os
import requests
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class ComparisonWorker:
    """Multi-paper comparison worker. Analyzes multiple papers side-by-side."""

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
        papers: list[dict],
        model: str = "anthropic/claude-opus-4-20250514",
    ) -> dict | None:
        """Run comparison analysis on multiple papers.

        Args:
            papers: List of dicts with keys: title, summary, methodology, key_findings.

        Returns:
            {"comparison": str} or None on failure.
        """
        if len(papers) < 2:
            return {"comparison": "Perbandingan membutuhkan minimal 2 paper."}

        system_prompt = self._load_system_prompt("comparison.md")
        user_prompt = self._build_user_prompt(papers)

        try:
            response = self._chat(system_prompt, user_prompt, model)
            if response is None:
                return None
            return {"comparison": response}
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
            "temperature": 0.3,
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

    def _build_user_prompt(self, papers: list[dict]) -> str:
        template = self._env.get_template("comparison_user.j2")
        return template.render(papers=papers)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest journal_analyzer/tests/test_comparison.py -v`
Expected: All 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add journal_analyzer/workers/comparison_worker.py journal_analyzer/tests/test_comparison.py
git commit -m "feat: add ComparisonWorker for multi-paper analysis"
```

---

### Task 3: Visualizer (Data Analysis Charts)

**Files:**
- Create: `journal_analyzer/core/visualizer.py`
- Test: `journal_analyzer/tests/test_visualizer.py`

- [ ] **Step 1: Write tests**

```python
# journal_analyzer/tests/test_visualizer.py
import os
import tempfile
from journal_analyzer.core.visualizer import Visualizer


def test_create_bar_chart():
    with tempfile.TemporaryDirectory() as tmpdir:
        viz = Visualizer(output_dir=tmpdir)
        path = viz.create_bar_chart(
            title="Test Chart",
            labels=["A", "B", "C"],
            values=[10, 20, 15],
            filename="test_bar",
        )
        assert os.path.exists(path)
        assert path.endswith("test_bar.png")


def test_create_line_chart():
    with tempfile.TemporaryDirectory() as tmpdir:
        viz = Visualizer(output_dir=tmpdir)
        path = viz.create_line_chart(
            title="Trend",
            x_labels=["2020", "2021", "2022"],
            y_values=[5, 10, 15],
            filename="test_line",
        )
        assert os.path.exists(path)


def test_create_summary_visualization():
    with tempfile.TemporaryDirectory() as tmpdir:
        viz = Visualizer(output_dir=tmpdir)
        stats = {"mean": 75.3, "median": 78.0, "std": 12.1, "min": 45, "max": 98, "n": 200}
        path = viz.create_summary_visualization(stats, filename="test_summary")
        assert os.path.exists(path)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest journal_analyzer/tests/test_visualizer.py -v`
Expected: FAIL.

- [ ] **Step 3: Implement Visualizer**

```python
# journal_analyzer/core/visualizer.py
import os
from typing import Optional


class Visualizer:
    """Generates matplotlib charts for data analysis results."""

    def __init__(self, output_dir: str = "output/visualizations"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def create_bar_chart(
        self,
        title: str,
        labels: list[str],
        values: list[float],
        filename: str = "bar_chart",
        xlabel: str = "",
        ylabel: str = "Nilai",
    ) -> str:
        """Create a bar chart and save to file."""
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(labels, values, color="steelblue")
        ax.set_title(title)
        if xlabel:
            ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.tight_layout()

        path = os.path.join(self.output_dir, f"{filename}.png")
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path

    def create_line_chart(
        self,
        title: str,
        x_labels: list[str],
        y_values: list[float],
        filename: str = "line_chart",
        xlabel: str = "",
        ylabel: str = "Nilai",
    ) -> str:
        """Create a line chart and save to file."""
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x_labels, y_values, marker="o", linewidth=2, markersize=8)
        ax.set_title(title)
        if xlabel:
            ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()

        path = os.path.join(self.output_dir, f"{filename}.png")
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path

    def create_summary_visualization(
        self,
        stats: dict,
        filename: str = "summary",
    ) -> str:
        """Create a summary visualization showing key statistics."""
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.axis("off")

        lines = [f"Statistik Deskriptif"]
        lines.append(f"")
        lines.append(f"N = {stats.get('n', 'N/A')}")
        lines.append(f"Mean = {stats.get('mean', 'N/A')}")
        lines.append(f"Median = {stats.get('median', 'N/A')}")
        lines.append(f"Std Dev = {stats.get('std', 'N/A')}")
        lines.append(f"Min = {stats.get('min', 'N/A')}")
        lines.append(f"Max = {stats.get('max', 'N/A')}")

        ax.text(0.5, 0.5, "\n".join(lines), ha="center", va="center",
                fontsize=14, family="monospace",
                bbox=dict(boxstyle="round,pad=1", facecolor="lightblue", alpha=0.5))

        path = os.path.join(self.output_dir, f"{filename}.png")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return path
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest journal_analyzer/tests/test_visualizer.py -v`
Expected: All 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add journal_analyzer/core/visualizer.py journal_analyzer/tests/test_visualizer.py
git commit -m "feat: add Visualizer for matplotlib chart generation"
```

---

### Task 4: Extend Output Aggregator for Comparison

**Files:**
- Modify: `journal_analyzer/core/output_aggregator.py`
- Test: `journal_analyzer/tests/test_output_aggregator.py` (append test)

- [ ] **Step 1: Append test**

Append to `journal_analyzer/tests/test_output_aggregator.py`:

```python
def test_aggregate_with_comparison():
    agg = OutputAggregator()
    result = agg.aggregate({
        "comparison": {"status": "success", "data": {"comparison": "Paper 1 vs Paper 2: ..."}},
    })
    assert "Perbandingan" in result
    assert "Paper 1 vs Paper 2" in result
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest journal_analyzer/tests/test_output_aggregator.py::test_aggregate_with_comparison -v`
Expected: FAIL.

- [ ] **Step 3: Update OutputAggregator**

Append before `return "\n".join(parts)`:

```python
        if "comparison" in worker_results:
            comp = worker_results["comparison"]
            if comp["status"] == "success":
                parts.append("## Perbandingan Paper\n")
                parts.append(comp["data"].get("comparison", "Tidak ada perbandingan."))
            else:
                parts.append("## Perbandingan Paper\n")
                parts.append(f"[comparison] Gagal: {comp.get('error', 'Unknown error')}. Coba lagi nanti.\n")
            parts.append("")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest journal_analyzer/tests/test_output_aggregator.py -v`
Expected: All tests PASS.

- [ ] **Step 5: Commit**

```bash
git add journal_analyzer/core/output_aggregator.py journal_analyzer/tests/test_output_aggregator.py
git commit -m "feat: extend OutputAggregator to support comparison mode"
```

---

### Task 5: Update CLI for Compare Mode + Zotero Save

**Files:**
- Modify: `journal_analyzer/analyze.py`
- Modify: `analyze.py` (wrapper)

- [ ] **Step 1: Read existing files**

Read both `journal_analyzer/analyze.py` and `analyze.py`.

- [ ] **Step 2: Update CLI in journal_analyzer/analyze.py**

1. Change argparse choices to include "compare":
```python
    parser.add_argument("--mode", required=True, choices=["read", "review", "full", "gap", "data-analysis", "generate", "compare"], help="Analysis mode")
```

2. Add `--compare` argument (accepts multiple files):
```python
    parser.add_argument("--compare", nargs="*", help="Additional paper files to compare with")
```

3. Add runner function before `if __name__`:

```python
def _run_compare(args, articles, cache, content_hash, config, router):
    from workers.comparison_worker import ComparisonWorker

    cached = cache.get_analysis(content_hash, "comparison")
    if cached:
        return {"status": "success", "data": cached}

    papers = []
    for art in articles:
        paper = {"title": art.metadata.get("title", "Unknown")}
        if art.sections.get("abstract"):
            paper["summary"] = art.sections["abstract"][:500]
        if art.methodology_type:
            paper["methodology"] = art.methodology_type
        if art.key_findings:
            paper["key_findings"] = art.key_findings
        papers.append(paper)

    model = router.get_model_name(ModelTier.HEAVY)
    worker = ComparisonWorker()
    result = worker.run(papers, model=model)

    if result is None:
        return {"status": "failed", "error": "Comparison gagal"}

    cache.set_analysis(content_hash, "comparison", result)
    return {"status": "success", "data": result}
```

4. Add import for ModelTier at top of file:
```python
    from models.model_router import ModelRouter, ModelTier
```
Change to include ModelTier (already imported, just ensure it's used).

5. In the "Execute workers based on mode" section, add:

```python
    if args.mode == "compare":
        # Parse main input + additional compare files
        all_articles = [article]
        if args.compare:
            for compare_file in args.compare:
                compare_article = _parse_input(argparse.Namespace(input=compare_file, input_text=None))
                if compare_article:
                    all_articles.append(compare_article)
        comparison_result = _run_compare(args, all_articles, cache, content_hash, config, router)
        results["comparison"] = comparison_result
```

- [ ] **Step 3: Update wrapper analyze.py**

Update docstring to include compare mode.

- [ ] **Step 4: Test CLI help**

Run: `python analyze.py --help`
Expected: Shows `--mode {...,compare}`, `--compare [COMPARE ...]`.

- [ ] **Step 5: Commit**

```bash
git add journal_analyzer/analyze.py analyze.py
git commit -m "feat: add compare CLI mode for multi-paper comparison"
```

---

### Task 6: Integration Test for Compare Mode

**Files:**
- Modify: `journal_analyzer/tests/test_integration.py` (append test)

- [ ] **Step 1: Append test**

Append to `journal_analyzer/tests/test_integration.py`:

```python
def test_compare_pipeline():
    """Test: parse multiple papers → comparison → aggregate."""
    from unittest.mock import patch
    text1 = """## ABSTRACT\nPaper 1 about AI in education using quantitative method."""
    text2 = """## ABSTRACT\nPaper 2 about AI in education using qualitative method."""

    from parsers.text_parser import TextParser
    article1 = TextParser().parse(text1)
    article2 = TextParser().parse(text2)

    from workers.comparison_worker import ComparisonWorker
    from core.output_aggregator import OutputAggregator

    comp_text = "TABEL PERBANDINGAN:\nPaper 1: Kuantitatif\nPaper 2: Kualitatif\n\nSYNTHESIS: Both show positive impact."

    with patch.object(ComparisonWorker, "_chat", return_value=comp_text):
        worker = ComparisonWorker(prompts_dir="journal_analyzer/prompts")
        papers = [
            {"title": article1.metadata.get("title", "Paper 1"), "summary": article1.sections.get("abstract", "")},
            {"title": article2.metadata.get("title", "Paper 2"), "summary": article2.sections.get("abstract", "")},
        ]
        result = worker.run(papers)
        assert result is not None
        assert "comparison" in result

    agg = OutputAggregator()
    output = agg.aggregate({
        "comparison": {"status": "success", "data": result},
    })
    assert "## Perbandingan Paper" in output
    assert "Kuantitatif" in output
    assert "Kualitatif" in output
```

- [ ] **Step 2: Run all tests**

Run: `python -m pytest journal_analyzer/tests/ -v`
Expected: All tests PASS (87 existing + 2 new = 89+ tests).

- [ ] **Step 3: Commit**

```bash
git add journal_analyzer/tests/test_integration.py
git commit -m "test: add Phase 4 integration tests for comparison and visualization"
```

---

### Task 7: Run All Tests + Final Commit

- [ ] **Step 1: Run all Phase 1-4 tests**

Run: `python -m pytest journal_analyzer/tests/ -v --tb=short`
Expected: All tests PASS.

- [ ] **Step 2: Final commit**

```bash
git add -A
git commit -m "feat: journal analysis system phase 4 complete — comparison, visualization, polish"
```
