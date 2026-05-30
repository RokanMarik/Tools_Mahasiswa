# Journal Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate Journal Finder + 9Router + Zotero into OpenCode as native skills so users can search papers, review results, and save to Zotero via natural language chat — no terminal needed.

**Architecture:** OpenCode Custom Skills approach. SKILL.md files in `.opencode/skills/` guide AI behavior. Python wrapper scripts in `scripts/` provide structured JSON I/O. Existing modules (`9router_journal_finder.py`, `modules/zotero/`) are reused, not rewritten.

**Tech Stack:** Python 3.14, requests, OpenCode SKILL.md convention, agentmemory slots for state, existing JournalFinder + ZoteroClient classes.

---

## File Map

| File | Action | Responsibility |
|------|--------|----------------|
| `scripts/journal_search.py` | Create | CLI wrapper: calls 9Router via JournalFinder, outputs JSON |
| `scripts/zotero_save.py` | Create | CLI wrapper: saves paper metadata to Zotero, outputs JSON |
| `scripts/citation_generator.py` | Create | CLI wrapper: generates APA citation from metadata, outputs JSON |
| `tests/test_journal_search.py` | Create | Tests for journal_search script |
| `tests/test_zotero_save.py` | Create | Tests for zotero_save script |
| `tests/test_citation_generator.py` | Create | Tests for citation_generator script |
| `.opencode/skills/journal-finder/SKILL.md` | Create | Skill: how AI searches journals |
| `.opencode/skills/zotero/SKILL.md` | Create | Skill: how AI saves to Zotero |
| `.opencode/skills/journal-help/SKILL.md` | Create | Skill: cheat sheet for users |
| `.opencode/skills/journal-workflow/SKILL.md` | Create (Phase 2) | Meta skill: orchestrates full workflow |

**Existing files reused (not modified):**
- `9router_journal_finder.py` — `JournalFinder` class (search, model routing)
- `modules/zotero/client.py` — `ZoteroClient` class (API calls)
- `modules/zotero/citation_formatter.py` — `CitationFormatter` class
- `modules/zotero/collection_picker.py` — `CollectionPicker` class

---

### Task 1: journal_search.py Script

**Files:**
- Create: `scripts/journal_search.py`
- Test: `tests/test_journal_search.py`
- Reuse: `9router_journal_finder.py` (JournalFinder)

- [ ] **Step 1: Write tests for journal_search.py**

Create `tests/test_journal_search.py`:

```python
"""Tests for scripts/journal_search.py"""

import json
import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestJournalSearch(unittest.TestCase):
    """Test journal_search script functions."""

    @patch("scripts.journal_search.JournalFinder")
    def test_search_returns_json_with_papers(self, MockFinder):
        """Search should return JSON with paper list."""
        mock_finder = MagicMock()
        mock_finder.find_journals.return_value = json.dumps({
            "status": "success",
            "query": "machine learning",
            "papers": [
                {
                    "index": 1,
                    "title": "Test Paper 1",
                    "authors": ["Smith, J."],
                    "year": 2024,
                    "journal": "Test Journal",
                    "doi": "10.1234/test1",
                    "url": "https://example.com/paper1",
                    "abstract": "Test abstract",
                    "metadata_source": "crossref",
                }
            ],
            "error": None,
        })
        MockFinder.return_value = mock_finder

        from scripts.journal_search import search_journals

        result = search_journals("machine learning", limit=1)
        data = json.loads(result)
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["papers"]), 1)
        self.assertEqual(data["papers"][0]["title"], "Test Paper 1")

    @patch("scripts.journal_search.JournalFinder")
    def test_search_handles_error(self, MockFinder):
        """Search should return JSON error on failure."""
        mock_finder = MagicMock()
        mock_finder.find_journals.side_effect = Exception("Connection refused")
        MockFinder.return_value = mock_finder

        from scripts.journal_search import search_journals

        result = search_journals("topic", limit=1)
        data = json.loads(result)
        self.assertEqual(data["status"], "error")
        self.assertIsNotNone(data["error"])

    @patch("scripts.journal_search.JournalFinder")
    def test_search_default_limit_is_3(self, MockFinder):
        """Default limit should be 3 papers."""
        mock_finder = MagicMock()
        mock_finder.find_journals.return_value = json.dumps({
            "status": "success",
            "query": "topic",
            "papers": [],
            "error": None,
        })
        MockFinder.return_value = mock_finder

        from scripts.journal_search import search_journals

        search_journals("topic")
        # Verify default limit was used (check call args)
        call_args = mock_finder.find_journals.call_args
        self.assertIn("limit", call_args.kwargs or {})


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_journal_search.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'scripts.journal_search'"

- [ ] **Step 3: Create scripts/__init__.py**

Create `scripts/__init__.py` (empty file) to make scripts a Python package:

```python
# scripts package
```

- [ ] **Step 4: Write journal_search.py**

Create `scripts/journal_search.py`:

```python
#!/usr/bin/env python3
"""Journal search wrapper script.

Usage:
    python scripts/journal_search.py --topic "machine learning" [--limit 3]

Output: JSON to stdout with paper list.
"""

import argparse
import json
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from importlib import import_module


def search_journals(topic: str, limit: int = 3) -> str:
    """Search for journals on a topic. Returns JSON string.

    Args:
        topic: Search topic.
        limit: Max papers to return (default 3).

    Returns:
        JSON string matching the spec schema:
        {
            "status": "success" | "error",
            "query": "...",
            "papers": [{index, title, authors, year, journal, doi, url, abstract, metadata_source}],
            "error": null | "error message"
        }
    """
    try:
        JournalFinder = import_module("9router_journal_finder").JournalFinder
        finder = JournalFinder()

        # Call 9Router to search — it returns text, we parse into structured format
        raw_response = finder.find_journals(topic)

        # Parse the raw response into structured papers
        # The 9Router model returns formatted text; we extract paper info
        papers = _parse_journal_response(raw_response, topic, limit)

        return json.dumps({
            "status": "success",
            "query": topic,
            "papers": papers,
            "error": None,
        }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "query": topic,
            "papers": [],
            "error": str(e),
        }, ensure_ascii=False)


def _parse_journal_response(raw: str, query: str, limit: int) -> list:
    """Parse raw 9Router response into structured paper list.

    The 9Router model returns text like:
        1. Title
           Authors: ...
           Year: 2024
           DOI: ...
           URL: ...

    We extract these into structured dicts.
    """
    papers = []
    lines = raw.split("\n")
    current_paper = {}

    for line in lines:
        line = line.strip()
        if not line:
            if current_paper.get("title"):
                papers.append(current_paper)
                current_paper = {}
            continue

        # Detect paper number (e.g., "1. Title" or "1) Title")
        if line[0].isdigit() and (line[1] == "." or line[1] == ")"):
            if current_paper.get("title"):
                papers.append(current_paper)
            title = line[2:].strip()
            current_paper = {"title": title, "authors": [], "year": None, "journal": "", "doi": "", "url": "", "abstract": "", "metadata_source": "9router"}
            continue

        # Parse fields
        lower = line.lower()
        if lower.startswith("author"):
            authors_raw = line.split(":", 1)[-1].strip()
            current_paper["authors"] = [a.strip() for a in authors_raw.split(",") if a.strip()]
        elif lower.startswith("year"):
            try:
                current_paper["year"] = int(line.split(":", 1)[-1].strip()[:4])
            except (ValueError, IndexError):
                current_paper["year"] = None
        elif lower.startswith("journal"):
            current_paper["journal"] = line.split(":", 1)[-1].strip()
        elif lower.startswith("doi"):
            current_paper["doi"] = line.split(":", 1)[-1].strip()
        elif lower.startswith("url") or lower.startswith("link") or lower.startswith("http"):
            url_part = line.split(":", 1)[-1].strip() if ":" in line else line
            current_paper["url"] = url_part

    # Don't forget the last paper
    if current_paper.get("title"):
        papers.append(current_paper)

    # Add index and truncate to limit
    for i, paper in enumerate(papers[:limit]):
        paper["index"] = i + 1

    return papers[:limit]


def main():
    parser = argparse.ArgumentParser(description="Search for academic journals")
    parser.add_argument("--topic", required=True, help="Search topic")
    parser.add_argument("--limit", type=int, default=3, help="Max papers to return")
    args = parser.parse_args()

    result = search_journals(args.topic, args.limit)
    print(result)


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/test_journal_search.py -v`
Expected: All tests PASS

- [ ] **Step 6: Manual smoke test**

Run: `python scripts/journal_search.py --topic "test topic" --limit 1`
Expected: JSON output (may be error if 9Router not running, but format should be valid JSON)

- [ ] **Step 7: Commit**

```bash
git add scripts/__init__.py scripts/journal_search.py tests/test_journal_search.py
git commit -m "feat: add journal_search script with tests"
```

---

### Task 2: zotero_save.py Script

**Files:**
- Create: `scripts/zotero_save.py`
- Test: `tests/test_zotero_save.py`
- Reuse: `modules/zotero/client.py` (ZoteroClient), `modules/zotero/citation_formatter.py`

- [ ] **Step 1: Write tests for zotero_save.py**

Create `tests/test_zotero_save.py`:

```python
"""Tests for scripts/zotero_save.py"""

import json
import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestZoteroSave(unittest.TestCase):
    """Test zotero_save script functions."""

    @patch("scripts.zotero_save.ZoteroClient")
    @patch("scripts.zotero_save.CitationFormatter")
    def test_save_returns_json_on_success(self, MockFormatter, MockClient):
        """Save should return JSON with saved papers and citations."""
        mock_client = MagicMock()
        mock_client.get_user_id.return_value = "12345"
        mock_client.add_item.return_value = {"key": "ABC123", "version": 1}
        MockClient.return_value = mock_client

        mock_formatter = MagicMock()
        mock_formatter.format.return_value = "Smith, J. (2024). Test Paper. Test Journal. https://doi.org/10.1234"
        MockFormatter.return_value = mock_formatter

        from scripts.zotero_save import save_to_zotero

        papers = [
            {
                "title": "Test Paper",
                "authors": ["John Smith"],
                "year": 2024,
                "journal": "Test Journal",
                "doi": "10.1234/test",
                "url": "https://example.com",
            }
        ]

        result = save_to_zotero(papers, api_key="test-key", collection_key="COL1")
        data = json.loads(result)
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["saved"]), 1)
        self.assertEqual(data["saved"][0]["title"], "Test Paper")

    @patch("scripts.zotero_save.ZoteroClient")
    def test_save_handles_connection_error(self, MockClient):
        """Save should return JSON error on connection failure."""
        mock_client = MagicMock()
        mock_client.get_user_id.side_effect = Exception("Connection refused")
        MockClient.return_value = mock_client

        from scripts.zotero_save import save_to_zotero

        papers = [{"title": "Test"}]
        result = save_to_zotero(papers, api_key="test-key")
        data = json.loads(result)
        self.assertEqual(data["status"], "error")
        self.assertIsNotNone(data["error"])

    def test_validate_paper_metadata_requires_title(self):
        """Validation should fail if title is missing."""
        from scripts.zotero_save import validate_paper_metadata

        result = validate_paper_metadata({"authors": ["Smith"]})
        self.assertFalse(result["valid"])
        self.assertIn("title", result["errors"])

    def test_validate_paper_metadata_passes_with_title(self):
        """Validation should pass with at least a title."""
        from scripts.zotero_save import validate_paper_metadata

        result = validate_paper_metadata({"title": "Test Paper"})
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_zotero_save.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'scripts.zotero_save'"

- [ ] **Step 3: Write zotero_save.py**

Create `scripts/zotero_save.py`:

```python
#!/usr/bin/env python3
"""Zotero save wrapper script.

Usage:
    python scripts/zotero_save.py --api-key "KEY" --collection "COL_KEY" --papers '{"title": "...", ...}'

Input: Paper metadata as JSON (one or more papers).
Output: JSON to stdout with save results.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.zotero.client import ZoteroClient
from modules.zotero.citation_formatter import CitationFormatter


def save_to_zotero(papers: list, api_key: str, collection_key: str = None) -> str:
    """Save papers to Zotero. Returns JSON string.

    Args:
        papers: List of paper dicts with title, authors, year, journal, doi, url.
        api_key: Zotero API key.
        collection_key: Target collection key (None for top-level).

    Returns:
        JSON string matching spec schema:
        {
            "status": "success" | "error" | "duplicate",
            "saved": [{"title": "...", "zotero_key": "...", "citation_apa": "..."}],
            "skipped": [{"title": "...", "reason": "duplicate"}],
            "error": null | "error message"
        }
    """
    saved = []
    skipped = []
    formatter = CitationFormatter()

    try:
        client = ZoteroClient(api_key=api_key)
        client.library_id = client.get_user_id()
    except Exception as e:
        return json.dumps({
            "status": "error",
            "saved": [],
            "skipped": [],
            "error": f"Zotero connection failed: {e}",
        }, ensure_ascii=False)

    for paper in papers:
        # Validate metadata
        validation = validate_paper_metadata(paper)
        if not validation["valid"]:
            skipped.append({
                "title": paper.get("title", "Unknown"),
                "reason": f"Invalid metadata: {', '.join(validation['errors'])}",
            })
            continue

        # Build Zotero item data
        item_data = {
            "title": paper["title"],
            "authors": paper.get("authors", []),
            "date": str(paper.get("year", "")),
            "doi": paper.get("doi", ""),
            "url": paper.get("url", ""),
            "journal": paper.get("journal", ""),
            "itemType": "journalArticle",
        }

        try:
            # If no collection specified, save to library root
            target_key = collection_key or ""
            result = client.add_item(target_key, item_data) if target_key else client.add_item("", item_data)

            # Generate APA citation
            citation = formatter.format(item_data, style="apa")

            saved.append({
                "title": paper["title"],
                "zotero_key": result.get("key", ""),
                "citation_apa": citation,
            })
        except Exception as e:
            error_msg = str(e).lower()
            if "duplicate" in error_msg or "already exists" in error_msg:
                skipped.append({
                    "title": paper["title"],
                    "reason": "duplicate",
                })
            else:
                skipped.append({
                    "title": paper["title"],
                    "reason": f"Save failed: {e}",
                })

    status = "success" if saved else ("duplicate" if skipped else "error")
    return json.dumps({
        "status": status,
        "saved": saved,
        "skipped": skipped,
        "error": None,
    }, ensure_ascii=False)


def validate_paper_metadata(paper: dict) -> dict:
    """Validate paper metadata before saving.

    Args:
        paper: Paper dict with title, authors, etc.

    Returns:
        {valid: bool, errors: list[str]}
    """
    errors = []
    if not paper.get("title"):
        errors.append("title")
    return {"valid": len(errors) == 0, "errors": errors}


def main():
    parser = argparse.ArgumentParser(description="Save papers to Zotero")
    parser.add_argument("--api-key", required=True, help="Zotero API key")
    parser.add_argument("--collection", default=None, help="Collection key (optional)")
    parser.add_argument("--papers", required=True, help="JSON array of paper metadata")
    args = parser.parse_args()

    papers = json.loads(args.papers)
    if not isinstance(papers, list):
        papers = [papers]

    result = save_to_zotero(papers, api_key=args.api_key, collection_key=args.collection)
    print(result)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_zotero_save.py -v`
Expected: All tests PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/zotero_save.py tests/test_zotero_save.py
git commit -m "feat: add zotero_save script with tests"
```

---

### Task 3: citation_generator.py Script

**Files:**
- Create: `scripts/citation_generator.py`
- Test: `tests/test_citation_generator.py`
- Reuse: `modules/zotero/citation_formatter.py`

- [ ] **Step 1: Write tests for citation_generator.py**

Create `tests/test_citation_generator.py`:

```python
"""Tests for scripts/citation_generator.py"""

import json
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestCitationGenerator(unittest.TestCase):
    """Test citation_generator script functions."""

    def test_generate_apa_citation(self):
        """Should generate APA citation from paper metadata."""
        from scripts.citation_generator import generate_citations

        papers = [
            {
                "title": "Deep Learning for Medical Imaging",
                "authors": ["John Smith", "Jane Doe"],
                "year": 2024,
                "journal": "Journal of Medical AI",
                "doi": "10.1234/test",
            }
        ]

        result = generate_citations(papers, style="apa")
        data = json.loads(result)
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["citations"]), 1)
        # APA format: Author. (Year). Title. Journal. DOI
        citation = data["citations"][0]["apa"]
        self.assertIn("Smith", citation)
        self.assertIn("2024", citation)
        self.assertIn("Deep Learning", citation)

    def test_generate_citation_missing_authors(self):
        """Should handle papers with no authors."""
        from scripts.citation_generator import generate_citations

        papers = [{"title": "Untitled Paper", "year": 2024}]
        result = generate_citations(papers, style="apa")
        data = json.loads(result)
        self.assertEqual(data["status"], "success")
        citation = data["citations"][0]["apa"]
        self.assertIn("Unknown Author", citation)

    def test_generate_citation_empty_list(self):
        """Should handle empty paper list."""
        from scripts.citation_generator import generate_citations

        result = generate_citations([], style="apa")
        data = json.loads(result)
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["citations"]), 0)

    def test_generate_citation_unsupported_style_defaults_to_apa(self):
        """Unsupported style should default to APA."""
        from scripts.citation_generator import generate_citations

        papers = [{"title": "Test", "authors": ["Smith"], "year": 2024}]
        result = generate_citations(papers, style="harvard")
        data = json.loads(result)
        self.assertEqual(data["status"], "success")
        self.assertIn("apa", data["citations"][0])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_citation_generator.py -v`
Expected: FAIL with "ModuleNotFoundError"

- [ ] **Step 3: Write citation_generator.py**

Create `scripts/citation_generator.py`:

```python
#!/usr/bin/env python3
"""Citation generator wrapper script.

Usage:
    python scripts/citation_generator.py --papers '{"title": "...", ...}' [--style apa]

Output: JSON to stdout with formatted citations.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.zotero.citation_formatter import CitationFormatter


def generate_citations(papers: list, style: str = "apa") -> str:
    """Generate citations for papers. Returns JSON string.

    Args:
        papers: List of paper dicts with title, authors, year, journal, doi.
        style: Citation style (apa, ieee, mla, chicago). Defaults to apa.

    Returns:
        JSON string matching spec schema:
        {
            "status": "success" | "error",
            "citations": [{"title": "...", "apa": "..."}],
            "error": null | "error message"
        }
    """
    try:
        formatter = CitationFormatter()
        # Normalize style
        if style not in formatter.STYLES:
            style = "apa"

        citations = []
        for paper in papers:
            item = {
                "title": paper.get("title", "Untitled"),
                "authors": paper.get("authors", []),
                "date": str(paper.get("year", "n.d.")),
                "journal": paper.get("journal", ""),
                "doi": paper.get("doi", ""),
            }
            citation_text = formatter.format(item, style=style)
            citations.append({
                "title": paper.get("title", "Untitled"),
                "apa": citation_text,
            })

        return json.dumps({
            "status": "success",
            "citations": citations,
            "error": None,
        }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "citations": [],
            "error": str(e),
        }, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Generate citations")
    parser.add_argument("--papers", required=True, help="JSON array of paper metadata")
    parser.add_argument("--style", default="apa", help="Citation style (apa, ieee, mla, chicago)")
    args = parser.parse_args()

    papers = json.loads(args.papers)
    if not isinstance(papers, list):
        papers = [papers]

    result = generate_citations(papers, style=args.style)
    print(result)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_citation_generator.py -v`
Expected: All tests PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/citation_generator.py tests/test_citation_generator.py
git commit -m "feat: add citation_generator script with tests"
```

---

### Task 4: journal-finder SKILL.md

**Files:**
- Create: `.opencode/skills/journal-finder/SKILL.md`

- [ ] **Step 1: Create journal-finder SKILL.md**

Create `.opencode/skills/journal-finder/SKILL.md`:

```markdown
---
name: journal-finder
description: Search for academic journals via 9Router. Use when user asks to find papers, search journals, or look up research.
---

# Journal Finder Skill

Search for academic journals and papers via 9Router. Returns structured paper metadata.

## Trigger

Natural language detection:
- "cari jurnal [topik]"
- "find papers about [topic]"
- "search for journals on [topic]"
- "cari paper tentang [topik]"

## Workflow

1. **Parse topic** from user request
2. **Clarify if needed** — if topic is too broad, ask one brief clarification question
3. **Select model** based on context:
   - `Mencari_Jurnal_Ilmiah` → journal search and recommendation
   - `Merangkum_Memperjelas_Catatan` → paper analysis/summarization
   - `kr/claude-sonnet-4.5` → general questions about research
4. **Execute search**: `python scripts/journal_search.py --topic "<topic>" --limit 3`
5. **Parse JSON output** and display papers to user in readable format
6. **Offer next steps**: "Mau simpan ke Zotero?", "Mau analisis paper tertentu?", atau "Cari lagi?"

## Script Interface

```bash
python scripts/journal_search.py --topic "machine learning" --limit 3
```

Output JSON:
```json
{
  "status": "success",
  "query": "machine learning",
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
      "metadata_source": "crossref"
    }
  ],
  "error": null
}
```

## Error Handling

- **9Router not running**: "9Router belum jalan. Nyalakan dulu (`npx -y @9router/server` atau sesuai setup kamu), lalu coba lagi."
- **No results**: "Nggak nemu paper untuk topik itu. Coba kata kunci lain atau topik yang lebih spesifik?"
- **JSON parse error**: Retry once, then report error to user

## Display Format

Show papers as:
```
Nemu {n} paper:

1. {title}
   Authors: {authors}
   Year: {year} | Journal: {journal}
   DOI: {doi}
   {url}
```

## State

After search, remember results for potential Zotero save. The AI should track which papers were found so user can reference them by number ("simpan 1 dan 3").
```

- [ ] **Step 2: Commit**

```bash
git add .opencode/skills/journal-finder/SKILL.md
git commit -m "feat: add journal-finder skill"
```

---

### Task 5: zotero SKILL.md

**Files:**
- Create: `.opencode/skills/zotero/SKILL.md`

- [ ] **Step 1: Create zotero SKILL.md**

Create `.opencode/skills/zotero/SKILL.md`:

```markdown
---
name: zotero
description: Save papers to Zotero library, generate citations. Use when user asks to save papers, add to library, or generate citations.
---

# Zotero Skill

Save academic papers to Zotero and generate formatted citations (APA style).

## Trigger

Natural language detection:
- "simpan ke zotero"
- "save to zotero"
- "add to library"
- "simpan paper [nomor/judul]"
- "buat citation"
- "generate citation"

## Prerequisites

Requires:
- `ZOTERO_API_KEY` environment variable (or user provides it)
- Zotero desktop running (for local sync)

## Workflow: Save Paper

1. **Get paper metadata** from context (previous search results or user input)
2. **Validate metadata** — title is required, DOI recommended
3. **Execute save**: `python scripts/zotero_save.py --api-key "$ZOTERO_API_KEY" --papers '<json>'`
4. **Parse JSON output** — check `status`, `saved`, `skipped`
5. **Confirm to user** with APA citation

## Workflow: Generate Citation Only

1. **Get paper metadata** from context
2. **Execute**: `python scripts/citation_generator.py --papers '<json>' --style apa`
3. **Display citation** to user

## Script Interfaces

### zotero_save.py
```bash
python scripts/zotero_save.py --api-key "KEY" --papers '[{"title":"...", "authors":["..."], "year":2024, "journal":"...", "doi":"..."}]'
```

Output:
```json
{
  "status": "success",
  "saved": [{"title": "...", "zotero_key": "ABC123", "citation_apa": "..."}],
  "skipped": [],
  "error": null
}
```

### citation_generator.py
```bash
python scripts/citation_generator.py --papers '[{"title":"...", "authors":["..."], "year":2024}]' --style apa
```

Output:
```json
{
  "status": "success",
  "citations": [{"title": "...", "apa": "Author. (Year). Title. Journal. DOI"}],
  "error": null
}
```

## Error Handling

- **No API key**: "API key Zotero belum diset. Set env var `ZOTERO_API_KEY` atau kasih key-nya langsung."
- **Zotero not running**: "Zotero desktop belum dibuka. Buka dulu, terus coba lagi."
- **Invalid metadata**: "Metadata paper ini tidak lengkap. Minimal butuh judul. Mau coba fetch dari DOI?"
- **Duplicate**: "Paper ini sudah ada di Zotero. Mau skip atau buat duplicate?"

## Citation Format

Always use APA style by default:
```
Author, A. A., & Author, B. B. (Year). Title of paper. Journal Name, volume(issue), pages. https://doi.org/xxx
```

Metadata MUST come from verified sources (DOI lookup, journal page, CrossRef API) — NEVER generate citation from AI memory.
```

- [ ] **Step 2: Commit**

```bash
git add .opencode/skills/zotero/SKILL.md
git commit -m "feat: add zotero skill"
```

---

### Task 6: journal-help SKILL.md (Cheat Sheet)

**Files:**
- Create: `.opencode/skills/journal-help/SKILL.md`

- [ ] **Step 1: Create journal-help SKILL.md**

Create `.opencode/skills/journal-help/SKILL.md`:

```markdown
---
name: journal-help
description: Show cheat sheet for journal finder commands. Use when user types ?, /help, or asks for help.
---

# Journal Help — Cheat Sheet

Show this when user types `?`, `/help`, "bantuan", or asks what commands are available.

## Cheat Sheet

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

## When to Show

- User explicitly types `?`, `/help`, "bantuan", "help"
- User seems confused or asks "bisa apa aja?"
- First time user interacts with journal-related commands (optional welcome hint)

## How to Show

Display the cheat sheet as a code block. Keep it concise — don't add extra explanation unless user asks.
```

- [ ] **Step 2: Commit**

```bash
git add .opencode/skills/journal-help/SKILL.md
git commit -m "feat: add journal-help cheat sheet skill"
```

---

### Task 7: journal-workflow SKILL.md (Phase 2 — Meta Skill)

**Files:**
- Create: `.opencode/skills/journal-workflow/SKILL.md`

- [ ] **Step 1: Create journal-workflow SKILL.md**

Create `.opencode/skills/journal-workflow/SKILL.md`:

```markdown
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
- `journal-finder` skill for search logic
- `zotero` skill for save/citation logic
- Do NOT duplicate code from those skills — reference them

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
```

- [ ] **Step 2: Commit**

```bash
git add .opencode/skills/journal-workflow/SKILL.md
git commit -m "feat: add journal-workflow meta skill"
```

---

### Task 8: Integration Test

**Files:**
- Create: `tests/test_integration.py`

- [ ] **Step 1: Write integration test**

Create `tests/test_integration.py`:

```python
"""Integration tests for the journal workflow scripts."""

import json
import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(__file__))


class TestIntegration(unittest.TestCase):
    """Test full workflow: search → save → citation."""

    @patch("scripts.journal_search.JournalFinder")
    @patch("scripts.zotero_save.ZoteroClient")
    @patch("scripts.zotero_save.CitationFormatter")
    def test_full_workflow_search_then_save(self, MockFormatter, MockClient, MockFinder):
        """Full workflow: search papers, then save selected ones."""
        # Mock search
        mock_finder = MagicMock()
        mock_finder.find_journals.return_value = json.dumps({
            "status": "success",
            "query": "test topic",
            "papers": [
                {"index": 1, "title": "Paper A", "authors": ["Smith"], "year": 2024, "journal": "J1", "doi": "10.1/a", "url": "https://a.com", "abstract": "", "metadata_source": "crossref"},
                {"index": 2, "title": "Paper B", "authors": ["Doe"], "year": 2023, "journal": "J2", "doi": "10.2/b", "url": "https://b.com", "abstract": "", "metadata_source": "crossref"},
            ],
            "error": None,
        })
        MockFinder.return_value = mock_finder

        # Mock Zotero
        mock_client = MagicMock()
        mock_client.get_user_id.return_value = "12345"
        mock_client.add_item.return_value = {"key": "KEY1", "version": 1}
        MockClient.return_value = mock_client

        mock_formatter = MagicMock()
        mock_formatter.format.return_value = "Smith. (2024). Paper A. J1. https://doi.org/10.1/a"
        MockFormatter.return_value = mock_formatter

        # Step 1: Search
        from scripts.journal_search import search_journals
        search_result = json.loads(search_journals("test topic"))
        self.assertEqual(search_result["status"], "success")
        self.assertEqual(len(search_result["papers"]), 2)

        # Step 2: Select paper 1
        selected = [search_result["papers"][0]]

        # Step 3: Save
        from scripts.zotero_save import save_to_zotero
        save_result = json.loads(save_to_zotero(selected, api_key="test-key"))
        self.assertEqual(save_result["status"], "success")
        self.assertEqual(len(save_result["saved"]), 1)
        self.assertEqual(save_result["saved"][0]["title"], "Paper A")

    def test_citation_from_search_result(self):
        """Citation should work with data from search results."""
        from scripts.citation_generator import generate_citations

        # Simulate a search result paper
        paper = {
            "title": "Test Paper",
            "authors": ["Jane Doe", "John Smith"],
            "year": 2024,
            "journal": "Test Journal",
            "doi": "10.9999/test",
        }

        result = json.loads(generate_citations([paper], style="apa"))
        self.assertEqual(result["status"], "success")
        citation = result["citations"][0]["apa"]
        self.assertIn("Doe", citation)
        self.assertIn("2024", citation)
        self.assertIn("Test Paper", citation)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run integration tests**

Run: `pytest tests/test_integration.py -v`
Expected: All tests PASS

- [ ] **Step 3: Run all tests together**

Run: `pytest tests/ -v`
Expected: All tests from all test files PASS

- [ ] **Step 4: Commit**

```bash
git add tests/test_integration.py
git commit -m "test: add integration tests for full workflow"
```

---

### Task 9: Update opencode.json (if needed)

**Files:**
- Modify: `opencode.json`

- [ ] **Step 1: Verify opencode.json includes skills path**

Read `opencode.json` and verify it doesn't need changes. OpenCode auto-discovers skills from `.opencode/skills/`. If the config already exists and is valid, no changes needed.

- [ ] **Step 2: Commit if changes made**

Only commit if changes were made.

---

## Self-Review Checklist

- [ ] **Spec coverage:** All spec requirements covered?
  - ✅ journal-finder skill → Task 4
  - ✅ zotero skill → Task 5
  - ✅ journal-help skill → Task 6
  - ✅ journal-workflow meta skill → Task 7
  - ✅ journal_search.py script → Task 1
  - ✅ zotero_save.py script → Task 2
  - ✅ citation_generator.py script → Task 3
  - ✅ APA citation from verified metadata → Tasks 2, 3, 5
  - ✅ JSON output schemas → All scripts
  - ✅ Error handling → All scripts + skills
  - ✅ State management → Task 7
  - ✅ Cheat sheet → Task 6

- [ ] **Placeholder scan:** No TBD, TODO, "implement later", "add validation" without code — all code is explicit

- [ ] **Type consistency:** All scripts use same paper dict format: `{title, authors, year, journal, doi, url}`. `CitationFormatter` from existing `modules/zotero/citation_formatter.py` is reused consistently.

- [ ] **DRY/YAGNI:** Reuse existing `JournalFinder`, `ZoteroClient`, `CitationFormatter`. No new classes for existing functionality. Wrapper scripts only handle JSON I/O and validation.
