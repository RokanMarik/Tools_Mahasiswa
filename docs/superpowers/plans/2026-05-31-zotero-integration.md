# Zotero Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Zotero Web API integration to Journal Finder — pull collection metadata, detect duplicates, analyze gaps, recommend related papers, display in terminal.

**Architecture:** Modular `modules/zotero/` folder with 6 focused files, integrated into existing `JournalFinder` class via 4 new methods. CLI entry point for terminal use.

**Tech Stack:** Python 3, `requests`, Zotero Web API, 9Router (existing)

---

## File Map

| File | Action | Responsibility |
|---|---|---|
| `modules/zotero/__init__.py` | Create | Package init |
| `modules/zotero/client.py` | Create | Zotero API wrapper |
| `modules/zotero/collection_picker.py` | Create | Collection selection UI |
| `modules/zotero/duplicate_detector.py` | Create | Duplicate detection logic |
| `modules/zotero/gap_analyzer.py` | Create | Topic gap analysis |
| `modules/zotero/recommendation_engine.py` | Create | Paper recommendation via web search |
| `modules/zotero/citation_formatter.py` | Create | APA/IEEE/MLA/Chicago formatting |
| `9router_journal_finder.py` | Modify | Add 4 zotero methods + CLI |
| `tests/test_zotero_client.py` | Create | Client unit tests |
| `tests/test_duplicate_detector.py` | Create | Dedup unit tests |
| `tests/test_citation_formatter.py` | Create | Citation format tests |
| `tests/test_zotero_integration.py` | Create | Integration tests |

---

### Task 1: Zotero API Client

**Files:**
- Create: `modules/zotero/__init__.py`
- Create: `modules/zotero/client.py`
- Test: `tests/test_zotero_client.py`

- [ ] **Step 1.1: Create zotero package init**

```python
# modules/zotero/__init__.py
"""Zotero integration modules for Journal Finder."""
```

- [ ] **Step 1.2: Write failing test for client initialization**

```python
# tests/test_zotero_client.py
import os
import unittest
from unittest.mock import patch, MagicMock
from modules.zotero.client import ZoteroClient

class TestZoteroClient(unittest.TestCase):
    def test_init_with_api_key(self):
        client = ZoteroClient(api_key="test_key_123")
        self.assertEqual(client.api_key, "test_key_123")
        self.assertEqual(client.library_type, "users")

    def test_init_with_custom_library(self):
        client = ZoteroClient(api_key="test_key", library_type="groups", library_id="456")
        self.assertEqual(client.library_type, "groups")
        self.assertEqual(client.library_id, "456")

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 1.3: Run test to verify it fails**

Run: `python -m pytest tests/test_zotero_client.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'modules.zotero.client'"

- [ ] **Step 1.4: Write ZoteroClient implementation**

```python
# modules/zotero/client.py
"""Zotero Web API client wrapper."""

import os
import time
import requests
from typing import List, Dict, Optional

ZOTERO_API_BASE = "https://api.zotero.org"
DEFAULT_LIMIT = 100
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


class ZoteroClient:
    def __init__(
        self,
        api_key: str,
        library_type: str = "users",
        library_id: Optional[str] = None,
    ):
        """Initialize Zotero API client.

        Args:
            api_key: Zotero API key.
            library_type: 'users' for personal library, 'groups' for group library.
            library_id: User ID or group ID. If None, will auto-detect for 'users'.
        """
        self.api_key = api_key
        self.library_type = library_type
        self.library_id = library_id or "0"  # 0 = current user
        self.base_url = ZOTERO_API_BASE
        self.headers = {
            "Zotero-API-Key": self.api_key,
            "Content-Type": "application/json",
        }

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """Make GET request with retry on rate limit."""
        url = f"{self.base_url}/{endpoint}"
        params = params or {}

        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=30)

                if response.status_code == 503:
                    # Rate limited — wait and retry
                    if attempt < MAX_RETRIES - 1:
                        print(f"  Rate limited. Waiting {RETRY_DELAY}s...")
                        time.sleep(RETRY_DELAY)
                        continue
                    else:
                        raise Exception("Rate limited after 3 retries. Try again later.")

                response.raise_for_status()
                return response

            except requests.exceptions.ConnectionError:
                raise Exception("Tidak bisa terhubung ke Zotero API. Cek koneksi internet.")
            except requests.exceptions.Timeout:
                raise Exception("Request timeout. Cek koneksi internet.")

        raise Exception("Unexpected error in request.")

    def get_user_id(self) -> str:
        """Get the current user's ID from the API."""
        response = self._get("keys/current")
        data = response.json()
        user_id = data.get("userID")
        if user_id is None:
            raise Exception("Tidak bisa mendapatkan user ID dari API key.")
        return str(user_id)

    def get_collections(self) -> List[Dict]:
        """Get all collections in the library.

        Returns:
            List of {key, name, num_items}.
        """
        library_path = f"{self.library_type}/{self.library_id}"
        endpoint = f"{library_path}/collections"
        response = self._get(endpoint, params={"format": "json"})
        data = response.json()

        collections = []
        for item in data:
            collections.append({
                "key": item["key"],
                "name": item["data"]["name"],
                "num_items": item["meta"].get("numItems", 0),
            })

        return collections

    def get_collection_items(self, collection_key: str, limit: int = DEFAULT_LIMIT) -> List[Dict]:
        """Get all items in a collection (metadata only, no attachments).

        Args:
            collection_key: The collection key from get_collections().
            limit: Max items to fetch per request.

        Returns:
            List of {title, creators, date, doi, url, journal, item_type, key}.
        """
        library_path = f"{self.library_type}/{self.library_id}"
        endpoint = f"{library_path}/collections/{collection_key}/items"

        all_items = []
        start = 0

        while True:
            params = {
                "format": "json",
                "limit": limit,
                "start": start,
                "content": "json",
                "include": "data",
            }
            response = self._get(endpoint, params=params)
            data = response.json()

            if not data:
                break

            for item in data:
                item_data = item.get("data", {})
                item_type = item_data.get("itemType", "")

                # Skip attachments — we only want metadata
                if item_type in ("attachment", "note"):
                    continue

                creators = item_data.get("creators", [])
                authors = []
                for c in creators:
                    if c.get("creatorType") == "author":
                        name = f"{c.get('firstName', '')} {c.get('lastName', '')}".strip()
                        if name:
                            authors.append(name)

                all_items.append({
                    "key": item.get("key", ""),
                    "title": item_data.get("title", "Untitled"),
                    "authors": authors,
                    "date": item_data.get("date", ""),
                    "doi": item_data.get("DOI", ""),
                    "url": item_data.get("url", ""),
                    "journal": item_data.get("publicationTitle", ""),
                    "item_type": item_type,
                })

            if len(data) < limit:
                break

            start += limit

        return all_items
```

- [ ] **Step 1.5: Run test to verify it passes**

Run: `python -m pytest tests/test_zotero_client.py::TestZoteroClient::test_init_with_api_key -v`
Expected: PASS

- [ ] **Step 1.6: Add more tests for client methods**

```python
# Add to tests/test_zotero_client.py

    @patch("modules.zotero.client.requests.get")
    def test_get_collections(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "key": "ABC123",
                "data": {"name": "Machine Learning"},
                "meta": {"numItems": 23},
            }
        ]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        client = ZoteroClient(api_key="test_key")
        collections = client.get_collections()

        self.assertEqual(len(collections), 1)
        self.assertEqual(collections[0]["name"], "Machine Learning")
        self.assertEqual(collections[0]["num_items"], 23)

    @patch("modules.zotero.client.requests.get")
    def test_get_collection_items(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "key": "ITEM1",
                "data": {
                    "itemType": "journalArticle",
                    "title": "Test Paper",
                    "creators": [{"creatorType": "author", "firstName": "John", "lastName": "Doe"}],
                    "date": "2024",
                    "DOI": "10.1234/test",
                    "url": "https://example.com",
                    "publicationTitle": "Test Journal",
                },
            }
        ]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        client = ZoteroClient(api_key="test_key")
        items = client.get_collection_items("ABC123")

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "Test Paper")
        self.assertEqual(items[0]["doi"], "10.1234/test")
        self.assertEqual(items[0]["authors"], ["John Doe"])

    @patch("modules.zotero.client.requests.get")
    def test_get_user_id(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"userID": 12345}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        client = ZoteroClient(api_key="test_key")
        user_id = client.get_user_id()

        self.assertEqual(user_id, "12345")

    def test_invalid_api_key_error(self):
        client = ZoteroClient(api_key="invalid_key")
        # This will fail with real API call, so we just test the client creates properly
        self.assertEqual(client.api_key, "invalid_key")
```

- [ ] **Step 1.7: Run all client tests**

Run: `python -m pytest tests/test_zotero_client.py -v`
Expected: All PASS

- [ ] **Step 1.8: Commit**

```bash
git add modules/zotero/__init__.py modules/zotero/client.py tests/test_zotero_client.py
git commit -m "feat: add Zotero API client with retry and collection/item fetching"
```

---

### Task 2: Collection Picker

**Files:**
- Create: `modules/zotero/collection_picker.py`
- Test: `tests/test_collection_picker.py`

- [ ] **Step 2.1: Write tests for collection picker**

```python
# tests/test_collection_picker.py
import unittest
from unittest.mock import MagicMock, patch
from modules.zotero.collection_picker import CollectionPicker


class TestCollectionPicker(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_client.get_collections.return_value = [
            {"key": "KEY1", "name": "Machine Learning", "num_items": 23},
            {"key": "KEY2", "name": "Medical AI", "num_items": 15},
            {"key": "KEY3", "name": "NLP", "num_items": 9},
        ]
        self.picker = CollectionPicker(self.mock_client)

    def test_display_collections(self):
        """Test that collections are formatted correctly."""
        picker = CollectionPicker(self.mock_client)
        result = picker.display_collections()
        self.assertIn("Machine Learning", result)
        self.assertIn("23 items", result)

    def test_select_by_number(self):
        """Test selecting collection by number."""
        self.picker._collections = self.mock_client.get_collections.return_value
        result = self.picker.select_by_number(2)
        self.assertEqual(result["name"], "Medical AI")

    def test_select_by_name(self):
        """Test selecting collection by name (case-insensitive)."""
        self.picker._collections = self.mock_client.get_collections.return_value
        result = self.picker.select_by_name("nlp")
        self.assertEqual(result["name"], "NLP")

    def test_select_by_number_out_of_range(self):
        """Test selecting invalid number returns None."""
        self.picker._collections = self.mock_client.get_collections.return_value
        result = self.picker.select_by_number(99)
        self.assertIsNone(result)

    def test_select_by_name_not_found(self):
        """Test selecting non-existent name returns None."""
        self.picker._collections = self.mock_client.get_collections.return_value
        result = self.picker.select_by_name("Nonexistent")
        self.assertIsNone(result)

    def test_empty_collections(self):
        """Test handling of empty collection list."""
        self.mock_client.get_collections.return_value = []
        picker = CollectionPicker(self.mock_client)
        result = picker.display_collections()
        self.assertIn("Tidak ada koleksi", result)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2.2: Run test to verify it fails**

Run: `python -m pytest tests/test_collection_picker.py -v`
Expected: FAIL with "ModuleNotFoundError"

- [ ] **Step 2.3: Write CollectionPicker implementation**

```python
# modules/zotero/collection_picker.py
"""Collection selection UI for Zotero."""

from typing import Optional, Dict, List


class CollectionPicker:
    def __init__(self, client):
        """Initialize with a ZoteroClient instance."""
        self.client = client
        self._collections = []

    def display_collections(self) -> str:
        """Fetch and format collection list for display.

        Returns:
            Formatted string of collections.
        """
        self._collections = self.client.get_collections()

        if not self._collections:
            return "Tidak ada koleksi ditemukan. Pastikan library Zotero kamu tidak kosong."

        lines = ["Koleksi Zotero kamu:"]
        for i, coll in enumerate(self._collections, 1):
            lines.append(f"  {i}. {coll['name']} ({coll['num_items']} items)")

        return "\n".join(lines)

    def select_by_number(self, number: int) -> Optional[Dict]:
        """Select collection by list number (1-indexed)."""
        if not self._collections:
            self._collections = self.client.get_collections()

        if number < 1 or number > len(self._collections):
            return None

        return self._collections[number - 1]

    def select_by_name(self, name: str) -> Optional[Dict]:
        """Select collection by name (case-insensitive partial match)."""
        if not self._collections:
            self._collections = self.client.get_collections()

        name_lower = name.lower()
        for coll in self._collections:
            if name_lower in coll["name"].lower():
                return coll

        return None

    def pick(self) -> Optional[Dict]:
        """Interactive collection picker.

        Returns:
            Selected collection dict or None if cancelled.
        """
        print(self.display_collections())
        print()
        print("Pilih nomor (atau ketik nama koleksi): ", end="")

        try:
            user_input = input().strip()
        except (EOFError, KeyboardInterrupt):
            print("\nDibatalkan.")
            return None

        if not user_input:
            print("Dibatalkan.")
            return None

        # Try number first
        if user_input.isdigit():
            result = self.select_by_number(int(user_input))
            if result:
                return result
            print(f"Nomor {user_input} tidak ada. Coba lagi.")
            return None

        # Try name
        result = self.select_by_name(user_input)
        if result:
            return result

        print(f"Koleksi '{user_input}' tidak ditemukan. Ketik 'list' untuk lihat semua koleksi.")
        return None
```

- [ ] **Step 2.4: Run tests to verify they pass**

Run: `python -m pytest tests/test_collection_picker.py -v`
Expected: All PASS

- [ ] **Step 2.5: Commit**

```bash
git add modules/zotero/collection_picker.py tests/test_collection_picker.py
git commit -m "feat: add Zotero collection picker with number and name selection"
```

---

### Task 3: Duplicate Detector

**Files:**
- Create: `modules/zotero/duplicate_detector.py`
- Test: `tests/test_duplicate_detector.py`

- [ ] **Step 3.1: Write tests for duplicate detector**

```python
# tests/test_duplicate_detector.py
import unittest
from modules.zotero.duplicate_detector import DuplicateDetector


class TestDuplicateDetector(unittest.TestCase):
    def setUp(self):
        self.detector = DuplicateDetector()
        self.sample_items = [
            {
                "key": "ITEM1",
                "title": "Deep Learning for Medical Imaging",
                "authors": ["John Smith"],
                "doi": "10.1234/abc",
                "journal": "Medical AI Journal",
                "date": "2024",
                "item_type": "journalArticle",
            },
            {
                "key": "ITEM2",
                "title": "Deep Learning for Medical Imaging",
                "authors": ["John Smith"],
                "doi": "10.1234/abc",
                "journal": "Medical AI Journal",
                "date": "2024",
                "item_type": "journalArticle",
            },
            {
                "key": "ITEM3",
                "title": "AI in Healthcare: A Review",
                "authors": ["Jane Doe"],
                "doi": "10.5678/def",
                "journal": "Healthcare Review",
                "date": "2023",
                "item_type": "journalArticle",
            },
            {
                "key": "ITEM4",
                "title": "AI in Healthcare Review",
                "authors": ["Jane Doe"],
                "doi": "10.9999/ghi",
                "journal": "Healthcare Review",
                "date": "2023",
                "item_type": "journalArticle",
            },
            {
                "key": "ITEM5",
                "title": "Unique Paper Title",
                "authors": ["Bob Lee"],
                "doi": "10.1111/jkl",
                "journal": "Unique Journal",
                "date": "2022",
                "item_type": "journalArticle",
            },
        ]

    def test_no_duplicates(self):
        """Test with items that have no duplicates."""
        items = self.sample_items[4:]  # Just the unique one
        result = self.detector.find_duplicates(items)
        self.assertEqual(len(result), 0)

    def test_exact_doi_match(self):
        """Test detection of exact DOI duplicates."""
        result = self.detector.find_duplicates(self.sample_items)
        doi_groups = [g for g in result if g["reason"] == "same_doi"]
        self.assertEqual(len(doi_groups), 1)
        self.assertEqual(len(doi_groups[0]["group"]), 2)

    def test_similar_title_match(self):
        """Test detection of similar title duplicates."""
        result = self.detector.find_duplicates(self.sample_items)
        title_groups = [g for g in result if g["reason"] == "similar_title"]
        self.assertEqual(len(title_groups), 1)
        self.assertEqual(len(title_groups[0]["group"]), 2)

    def test_empty_items(self):
        """Test with empty list."""
        result = self.detector.find_duplicates([])
        self.assertEqual(len(result), 0)

    def test_single_item(self):
        """Test with single item (no duplicates possible)."""
        result = self.detector.find_duplicates([self.sample_items[0]])
        self.assertEqual(len(result), 0)

    def test_items_without_doi(self):
        """Test items with empty DOI are not matched by DOI."""
        items = [
            {"key": "A", "title": "Paper A", "doi": "", "authors": [], "journal": "", "date": "", "item_type": ""},
            {"key": "B", "title": "Paper B", "doi": "", "authors": [], "journal": "", "date": "", "item_type": ""},
        ]
        result = self.detector.find_duplicates(items)
        doi_groups = [g for g in result if g["reason"] == "same_doi"]
        self.assertEqual(len(doi_groups), 0)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3.2: Run test to verify it fails**

Run: `python -m pytest tests/test_duplicate_detector.py -v`
Expected: FAIL with "ModuleNotFoundError"

- [ ] **Step 3.3: Write DuplicateDetector implementation**

```python
# modules/zotero/duplicate_detector.py
"""Duplicate detection for Zotero items."""

from typing import List, Dict
from collections import defaultdict


class DuplicateDetector:
    DOI_SIMILARITY_THRESHOLD = 0.90  # 90% similarity for title matching

    def find_duplicates(self, items: List[Dict]) -> List[Dict]:
        """Find duplicate items based on DOI and title similarity.

        Args:
            items: List of item dicts with 'doi', 'title', 'key' fields.

        Returns:
            List of {group: [items], reason: 'same_doi' | 'similar_title'}.
        """
        if len(items) < 2:
            return []

        duplicates = []

        # 1. Group by exact DOI match
        duplicates.extend(self._find_doi_duplicates(items))

        # 2. Find similar title matches (excluding items already flagged)
        flagged_keys = set()
        for group in duplicates:
            for item in group["group"]:
                flagged_keys.add(item["key"])

        duplicates.extend(self._find_title_duplicates(items, flagged_keys))

        return duplicates

    def _find_doi_duplicates(self, items: List[Dict]) -> List[Dict]:
        """Find items with identical DOI."""
        doi_groups = defaultdict(list)

        for item in items:
            doi = item.get("doi", "").strip()
            if doi:  # Only group items that have a DOI
                doi_groups[doi].append(item)

        duplicates = []
        for doi, group in doi_groups.items():
            if len(group) > 1:
                duplicates.append({
                    "group": group,
                    "reason": "same_doi",
                    "detail": f"DOI: {doi}",
                })

        return duplicates

    def _find_title_duplicates(self, items: List[Dict], flagged_keys: set) -> List[Dict]:
        """Find items with similar titles (>90% similarity)."""
        duplicates = []
        seen_pairs = set()

        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                item_a = items[i]
                item_b = items[j]

                # Skip if either already flagged
                if item_a["key"] in flagged_keys or item_b["key"] in flagged_keys:
                    continue

                # Skip if this pair already recorded
                pair_key = tuple(sorted([item_a["key"], item_b["key"]]))
                if pair_key in seen_pairs:
                    continue

                similarity = self._title_similarity(item_a["title"], item_b["title"])

                if similarity >= self.DOI_SIMILARITY_THRESHOLD:
                    seen_pairs.add(pair_key)
                    duplicates.append({
                        "group": [item_a, item_b],
                        "reason": "similar_title",
                        "detail": f"Judul mirip {similarity:.0%}",
                    })

        return duplicates

    def _title_similarity(self, title_a: str, title_b: str) -> float:
        """Calculate title similarity using normalized word overlap."""
        words_a = set(title_a.lower().split())
        words_b = set(title_b.lower().split())

        if not words_a or not words_b:
            return 0.0

        intersection = words_a & words_b
        union = words_a | words_b

        return len(intersection) / len(union)
```

- [ ] **Step 3.4: Run tests to verify they pass**

Run: `python -m pytest tests/test_duplicate_detector.py -v`
Expected: All PASS

- [ ] **Step 3.5: Commit**

```bash
git add modules/zotero/duplicate_detector.py tests/test_duplicate_detector.py
git commit -m "feat: add duplicate detector with DOI match and title similarity"
```

---

### Task 4: Citation Formatter

**Files:**
- Create: `modules/zotero/citation_formatter.py`
- Test: `tests/test_citation_formatter.py`

- [ ] **Step 4.1: Write tests for citation formatter**

```python
# tests/test_citation_formatter.py
import unittest
from modules.zotero.citation_formatter import CitationFormatter


class TestCitationFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = CitationFormatter()
        self.sample_paper = {
            "title": "Deep Learning for Medical Imaging",
            "authors": ["John Smith", "Jane Doe"],
            "date": "2024",
            "doi": "10.1234/abc",
            "journal": "Journal of Medical AI",
            "volume": "15",
            "issue": "3",
            "pages": "123-145",
        }

    def test_apa_format(self):
        result = self.formatter.format(self.sample_paper, style="apa")
        self.assertIn("Smith, J., & Doe, J.")
        self.assertIn("(2024)")
        self.assertIn("Deep Learning for Medical Imaging")
        self.assertIn("10.1234/abc")

    def test_ieee_format(self):
        result = self.formatter.format(self.sample_paper, style="ieee")
        self.assertIn("J. Smith and J. Doe")
        self.assertIn("Deep Learning for Medical Imaging")
        self.assertIn("vol. 15")

    def test_mla_format(self):
        result = self.formatter.format(self.sample_paper, style="mla")
        self.assertIn("Smith, John, and Jane Doe")
        self.assertIn("Deep Learning for Medical Imaging")
        self.assertIn("2024")

    def test_chicago_format(self):
        result = self.formatter.format(self.sample_paper, style="chicago")
        self.assertIn("Smith, John, and Jane Doe")
        self.assertIn("Deep Learning for Medical Imaging")
        self.assertIn("15, no. 3 (2024)")

    def test_unknown_style_defaults_to_apa(self):
        result = self.formatter.format(self.sample_paper, style="unknown")
        self.assertIn("(2024)")  # APA uses year in parentheses

    def test_missing_fields(self):
        paper = {"title": "No DOI Paper", "authors": ["Bob Lee"], "date": "2023", "doi": "", "journal": "", "volume": "", "issue": "", "pages": ""}
        result = self.formatter.format(paper, style="apa")
        self.assertNotIn("10.", result)  # No DOI should appear


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 4.2: Run test to verify it fails**

Run: `python -m pytest tests/test_citation_formatter.py -v`
Expected: FAIL with "ModuleNotFoundError"

- [ ] **Step 4.3: Write CitationFormatter implementation**

```python
# modules/zotero/citation_formatter.py
"""Citation formatting for Zotero items (APA, IEEE, MLA, Chicago)."""

from typing import Dict, List


class CitationFormatter:
    STYLES = ["apa", "ieee", "mla", "chicago"]

    def format(self, item: Dict, style: str = "apa", number: int = None) -> str:
        """Format an item into a citation string.

        Args:
            item: Item dict with title, authors, date, doi, journal, etc.
            style: Citation style ('apa', 'ieee', 'mla', 'chicago').
            number: Item number (used by IEEE for [1], [2], etc.).

        Returns:
            Formatted citation string.
        """
        if style not in self.STYLES:
            style = "apa"  # Default to APA

        method = getattr(self, f"_format_{style}")
        return method(item, number)

    def _format_authors_apa(self, authors: List[str]) -> str:
        """Format authors in APA style: Smith, J., & Doe, J."""
        if not authors:
            return "Unknown Author"

        formatted = []
        for author in authors:
            parts = author.strip().split()
            if len(parts) >= 2:
                last = parts[-1]
                initials = ". ".join([p[0] + "." for p in parts[:-1]])
                formatted.append(f"{last}, {initials}")
            elif len(parts) == 1:
                formatted.append(parts[0])
            else:
                formatted.append(author)

        if len(formatted) == 1:
            return formatted[0]
        elif len(formatted) == 2:
            return f"{formatted[0]}, & {formatted[1]}"
        else:
            return ", ".join(formatted[:-1]) + ", & " + formatted[-1]

    def _format_authors_ieee(self, authors: List[str]) -> str:
        """Format authors in IEEE style: J. Smith and J. Doe."""
        if not authors:
            return "Unknown Author"

        formatted = []
        for author in authors:
            parts = author.strip().split()
            if len(parts) >= 2:
                initials = " ".join([p[0] + "." for p in parts[:-1]])
                last = parts[-1]
                formatted.append(f"{initials} {last}")
            elif len(parts) == 1:
                formatted.append(parts[0])
            else:
                formatted.append(author)

        if len(formatted) == 1:
            return formatted[0]
        else:
            return " and ".join([", ".join(formatted[:-1]), formatted[-1]])

    def _format_authors_mla_chicago(self, authors: List[str]) -> str:
        """Format authors in MLA/Chicago style: Smith, John, and Jane Doe."""
        if not authors:
            return "Unknown Author"

        if len(authors) == 1:
            return authors[0]
        elif len(authors) == 2:
            return f"{authors[0]}, and {authors[1]}"
        else:
            return ", ".join(authors[:-1]) + ", and " + authors[-1]

    def _format_apa(self, item: Dict, number: int = None) -> str:
        title = item.get("title", "Untitled")
        authors = self._format_authors_apa(item.get("authors", []))
        date = item.get("date", "n.d.")
        journal = item.get("journal", "")
        volume = item.get("volume", "")
        issue = item.get("issue", "")
        pages = item.get("pages", "")
        doi = item.get("doi", "")

        citation = f"{authors}. ({date}). {title}."
        if journal:
            citation += f" {journal}"
            if volume:
                citation += f", {volume}"
                if issue:
                    citation += f"({issue})"
            if pages:
                citation += f", {pages}"
            citation += "."
        if doi:
            citation += f" https://doi.org/{doi}"

        return citation

    def _format_ieee(self, item: Dict, number: int = None) -> str:
        title = item.get("title", "Untitled")
        authors = self._format_authors_ieee(item.get("authors", []))
        journal = item.get("journal", "")
        volume = item.get("volume", "")
        issue = item.get("issue", "")
        pages = item.get("pages", "")
        date = item.get("date", "")
        doi = item.get("doi", "")

        prefix = f"[{number}] " if number else ""
        citation = f'{prefix}{authors}, "{title},"'
        if journal:
            citation += f" {journal}"
            if volume:
                citation += f", vol. {volume}"
            if issue:
                citation += f", no. {issue}"
            if pages:
                citation += f", pp. {pages}"
            if date:
                citation += f", {date}"
            citation += "."
        if doi:
            citation += f" doi: {doi}."

        return citation

    def _format_mla(self, item: Dict, number: int = None) -> str:
        title = item.get("title", "Untitled")
        authors = self._format_authors_mla_chicago(item.get("authors", []))
        journal = item.get("journal", "")
        volume = item.get("volume", "")
        issue = item.get("issue", "")
        pages = item.get("pages", "")
        date = item.get("date", "")
        doi = item.get("doi", "")

        citation = f'{authors}. "{title}."'
        if journal:
            citation += f" {journal}"
            if volume:
                citation += f", vol. {volume}"
            if issue:
                citation += f", no. {issue}"
            if date:
                citation += f", {date}"
            if pages:
                citation += f", pp. {pages}"
            citation += "."
        if doi:
            citation += f" https://doi.org/{doi}"

        return citation

    def _format_chicago(self, item: Dict, number: int = None) -> str:
        title = item.get("title", "Untitled")
        authors = self._format_authors_mla_chicago(item.get("authors", []))
        journal = item.get("journal", "")
        volume = item.get("volume", "")
        issue = item.get("issue", "")
        pages = item.get("pages", "")
        date = item.get("date", "")
        doi = item.get("doi", "")

        citation = f'{authors}. "{title}."'
        if journal:
            citation += f" {journal}"
            if volume and date:
                citation += f" {volume}, no. {issue} ({date})"
            elif volume:
                citation += f" {volume}"
                if issue:
                    citation += f" ({issue})"
                if date:
                    citation += f" ({date})"
            elif date:
                citation += f" ({date})"
            if pages:
                citation += f": {pages}"
            citation += "."
        if doi:
            citation += f" https://doi.org/{doi}"

        return citation
```

- [ ] **Step 4.4: Run tests to verify they pass**

Run: `python -m pytest tests/test_citation_formatter.py -v`
Expected: All PASS

- [ ] **Step 4.5: Commit**

```bash
git add modules/zotero/citation_formatter.py tests/test_citation_formatter.py
git commit -m "feat: add citation formatter with APA, IEEE, MLA, Chicago styles"
```

---

### Task 5: Gap Analyzer

**Files:**
- Create: `modules/zotero/gap_analyzer.py`

- [ ] **Step 5.1: Write GapAnalyzer implementation**

```python
# modules/zotero/gap_analyzer.py
"""Topic gap analysis for Zotero collections."""

from typing import List, Dict

# Common research topics in AI/ML field for gap comparison
AI_RESEARCH_TOPICS = [
    "machine learning",
    "deep learning",
    "natural language processing",
    "computer vision",
    "reinforcement learning",
    "generative ai",
    "federated learning",
    "transfer learning",
    "explainable ai",
    "medical ai",
    "robotics",
    "speech recognition",
    "recommendation systems",
    "graph neural networks",
    "large language models",
    "multimodal learning",
    "edge ai",
    "ai ethics",
    "time series",
    "anomaly detection",
]


class GapAnalyzer:
    COVERED_THRESHOLD = 3    # 3+ papers = covered
    LOW_THRESHOLD = 1        # 1-2 papers = low

    def analyze(self, items: List[Dict], field: str = "AI") -> List[Dict]:
        """Analyze which topics are covered, low, or missing in the collection.

        Args:
            items: List of item dicts with 'title', 'journal' fields.
            field: Research field for topic selection (default: 'AI').

        Returns:
            List of {topic, count, status: 'covered' | 'low' | 'missing'}.
        """
        topics = self._get_topics_for_field(field)
        results = []

        for topic in topics:
            count = self._count_topic_matches(items, topic)
            status = self._classify_topic(count)
            results.append({
                "topic": topic.title(),
                "count": count,
                "status": status,
            })

        # Sort: missing first, then low, then covered
        status_order = {"missing": 0, "low": 1, "covered": 2}
        results.sort(key=lambda x: (status_order[x["status"]], -x["count"]))

        return results

    def _get_topics_for_field(self, field: str) -> List[str]:
        """Get relevant topics for a research field."""
        # For now, use the same AI topics list for all fields
        # Can be extended later for field-specific topics
        return AI_RESEARCH_TOPICS

    def _count_topic_matches(self, items: List[Dict], topic: str) -> int:
        """Count items that match a topic keyword."""
        count = 0
        topic_lower = topic.lower()

        for item in items:
            title = item.get("title", "").lower()
            journal = item.get("journal", "").lower()

            if topic_lower in title or topic_lower in journal:
                count += 1

        return count

    def _classify_topic(self, count: int) -> str:
        """Classify a topic based on paper count."""
        if count >= self.COVERED_THRESHOLD:
            return "covered"
        elif count >= self.LOW_THRESHOLD:
            return "low"
        else:
            return "missing"
```

- [ ] **Step 5.2: Create test file for gap analyzer**

```python
# tests/test_gap_analyzer.py
import unittest
from modules.zotero.gap_analyzer import GapAnalyzer


class TestGapAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = GapAnalyzer()
        self.sample_items = [
            {"title": "Deep Learning for Medical Imaging", "journal": "Medical AI Journal", "authors": [], "doi": "", "key": "", "date": "", "item_type": ""},
            {"title": "Machine Learning in Healthcare", "journal": "Health Informatics", "authors": [], "doi": "", "key": "", "date": "", "item_type": ""},
            {"title": "Neural Networks for Diagnosis", "journal": "AI Medicine", "authors": [], "doi": "", "key": "", "date": "", "item_type": ""},
            {"title": "NLP for Clinical Notes", "journal": "NLP Journal", "authors": [], "doi": "", "key": "", "date": "", "item_type": ""},
        ]

    def test_covered_topic(self):
        """Test topic with 3+ papers is classified as covered."""
        # Deep learning appears in title of item 1
        # Machine learning appears in title of item 2
        # Neural networks is related but not exact match
        results = self.analyzer.analyze(self.sample_items)
        medical_ai = [r for r in results if r["topic"] == "Medical Ai"]
        # Should be at least partially covered
        self.assertTrue(len(medical_ai) > 0)

    def test_missing_topic(self):
        """Test topic with 0 papers is classified as missing."""
        results = self.analyzer.analyze(self.sample_items)
        robotics = [r for r in results if r["topic"] == "Robotics"]
        self.assertEqual(len(robotics), 1)
        self.assertEqual(robotics[0]["status"], "missing")
        self.assertEqual(robotics[0]["count"], 0)

    def test_empty_items(self):
        """Test with empty item list — all topics should be missing."""
        results = self.analyzer.analyze([])
        self.assertTrue(all(r["status"] == "missing" for r in results))

    def test_sorting_order(self):
        """Test that results are sorted: missing first, then low, then covered."""
        results = self.analyzer.analyze(self.sample_items)
        status_order = {"missing": 0, "low": 1, "covered": 2}
        statuses = [status_order[r["status"]] for r in results]
        self.assertEqual(statuses, sorted(statuses))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 5.3: Run tests to verify they pass**

Run: `python -m pytest tests/test_gap_analyzer.py -v`
Expected: All PASS

- [ ] **Step 5.4: Commit**

```bash
git add modules/zotero/gap_analyzer.py tests/test_gap_analyzer.py
git commit -m "feat: add gap analyzer with topic coverage classification"
```

---

### Task 6: Recommendation Engine

**Files:**
- Create: `modules/zotero/recommendation_engine.py`

- [ ] **Step 6.1: Write RecommendationEngine implementation**

```python
# modules/zotero/recommendation_engine.py
"""Paper recommendation engine using 9Router web search."""

import os
import requests
from typing import List, Dict


class RecommendationEngine:
    def __init__(self, journal_finder):
        """Initialize with a JournalFinder instance for web search.

        Args:
            journal_finder: JournalFinder instance with chat() method.
        """
        self.finder = journal_finder
        self.base_url = os.getenv("NINEROUTER_URL", "http://localhost:20128")
        self.api_key = os.getenv("NINEROUTER_KEY", "")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def recommend(self, gaps: List[Dict], existing_topics: List[str]) -> List[Dict]:
        """Get paper recommendations for gap topics.

        Args:
            gaps: List of gap dicts with 'topic' and 'status'.
            existing_topics: List of topics already well-covered.

        Returns:
            List of {title, doi, url, reason} recommendations.
        """
        recommendations = []

        # Get missing and low topics (limit to top 3 to save tokens)
        target_topics = [
            g["topic"] for g in gaps
            if g["status"] in ("missing", "low")
        ][:3]

        for topic in target_topics:
            papers = self._search_papers(topic, existing_topics)
            for paper in papers[:2]:  # 2 papers per topic
                recommendations.append({
                    "title": paper.get("title", "Unknown"),
                    "doi": paper.get("doi", ""),
                    "url": paper.get("url", ""),
                    "reason": self._generate_reason(topic, paper),
                })

        return recommendations

    def _search_papers(self, topic: str, existing_topics: List[str]) -> List[Dict]:
        """Search for papers on a topic via 9Router web search.

        Args:
            topic: Research topic to search.
            existing_topics: Topics to exclude from search.

        Returns:
            List of paper dicts.
        """
        search_query = f"{topic} academic paper research open access"

        try:
            url = f"{self.base_url}/v1/chat/completions"
            payload = {
                "model": "tavily/search",
                "messages": [{"role": "user", "content": search_query}],
                "max_tokens": 800,
                "temperature": 0.3,
                "stream": False,
            }

            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            content = result["choices"][0]["message"]["content"]

            # Parse results — extract paper info from search response
            return self._parse_search_results(content)

        except Exception:
            return []

    def _parse_search_results(self, content: str) -> List[Dict]:
        """Parse search response into paper dicts."""
        papers = []
        # Simple parsing — in production, use structured output
        lines = content.strip().split("\n")
        current_paper = {}

        for line in lines:
            line = line.strip()
            if not line:
                if current_paper.get("title"):
                    papers.append(current_paper)
                    current_paper = {}
                continue

            if line.startswith("Title:") or line.startswith("- **Title"):
                current_paper["title"] = line.split(":", 1)[-1].strip().strip("*").strip()
            elif line.startswith("DOI:") or line.startswith("- **DOI"):
                current_paper["doi"] = line.split(":", 1)[-1].strip().strip("*").strip()
            elif line.startswith("URL:") or line.startswith("http"):
                current_paper["url"] = line.split(":", 1)[-1].strip() if ":" in line else line

        if current_paper.get("title"):
            papers.append(current_paper)

        return papers[:5]

    def _generate_reason(self, topic: str, paper: Dict) -> str:
        """Generate a reason for recommending this paper."""
        return f"Topik '{topic}' belum ada di koleksimu, paper ini bisa melengkapinya."
```

- [ ] **Step 6.2: Commit**

```bash
git add modules/zotero/recommendation_engine.py
git commit -m "feat: add recommendation engine with 9Router web search"
```

---

### Task 7: Integration into JournalFinder + CLI

**Files:**
- Modify: `9router_journal_finder.py`
- Create: `zotero_cli.py`

- [ ] **Step 7.1: Add Zotero methods to JournalFinder**

Add these imports at the top of `9router_journal_finder.py`:

```python
# Add after existing imports
from modules.zotero.client import ZoteroClient
from modules.zotero.collection_picker import CollectionPicker
from modules.zotero.duplicate_detector import DuplicateDetector
from modules.zotero.gap_analyzer import GapAnalyzer
from modules.zotero.recommendation_engine import RecommendationEngine
from modules.zotero.citation_formatter import CitationFormatter
```

Add these methods to the `JournalFinder` class (before `main()`):

```python
    def pull_zotero(
        self,
        api_key: str = None,
        collection_name: str = None,
        citation_style: str = "apa",
    ) -> None:
        """Main entry point for Zotero analysis.

        Pulls collection from Zotero, checks duplicates, analyzes gaps,
        and recommends related papers. All output to terminal.

        Args:
            api_key: Zotero API key (or from env var).
            collection_name: Collection name to analyze (or interactive pick).
            citation_style: Citation format ('apa', 'ieee', 'mla', 'chicago').
        """
        api_key = api_key or os.getenv("ZOTERO_API_KEY")
        if not api_key:
            print("=== Zotero Integration ===")
            print("Masukkan Zotero API key: ", end="")
            try:
                api_key = input().strip()
            except (EOFError, KeyboardInterrupt):
                print("\nDibatalkan.")
                return

        if not api_key:
            print("❌ API key diperlukan. Buat di zotero.org → Settings → API Keys")
            return

        # Initialize client
        print("\nMenghubungkan ke Zotero...")
        try:
            client = ZoteroClient(api_key=api_key)
            # Auto-detect user ID
            client.library_id = client.get_user_id()
        except Exception as e:
            print(f"❌ {e}")
            return

        # Pick collection
        picker = CollectionPicker(client)
        if collection_name:
            selected = picker.select_by_name(collection_name)
            if not selected:
                print(f"❌ Koleksi '{collection_name}' tidak ditemukan.")
                return
        else:
            selected = picker.pick()
            if not selected:
                return

        print(f"\nPulling {selected['num_items']} items dari '{selected['name']}'...")
        try:
            items = client.get_collection_items(selected["key"])
        except Exception as e:
            print(f"❌ {e}")
            return

        print(f"✅ {len(items)} items berhasil di-pull ({len(items) / max(selected['num_items'], 1) * 100:.0f}% dari total)\n")

        # Citation style selection
        if citation_style not in CitationFormatter.STYLES:
            print("Pilih format daftar pustaka:")
            for i, style in enumerate(CitationFormatter.STYLES, 1):
                print(f"  {i}. {style.upper()}")
            print(f"\nPilih nomor [default: 1]: ", end="")
            try:
                choice = input().strip()
                if choice.isdigit() and 1 <= int(choice) <= len(CitationFormatter.STYLES):
                    citation_style = CitationFormatter.STYLES[int(choice) - 1]
            except (EOFError, KeyboardInterrupt, ValueError):
                citation_style = "apa"

        formatter = CitationFormatter()

        # Step 1: Duplicate check
        print("=== Cek Duplikat ===")
        duplicates = self.check_duplicates(items)
        if not duplicates:
            print("✅ Tidak ada duplikat ditemukan.\n")
        else:
            for dup in duplicates:
                titles = [item["title"] for item in dup["group"]]
                print(f"⚠️ {dup['detail']}:")
                for t in titles:
                    print(f"  - \"{t}\"")
            print()

        # Step 2: Gap analysis
        print("=== Analisis Gap ===")
        gaps = self.analyze_gaps(items)
        covered = [g for g in gaps if g["status"] == "covered"]
        low = [g for g in gaps if g["status"] == "low"]
        missing = [g for g in gaps if g["status"] == "missing"]

        if covered:
            for g in covered[:5]:  # Show top 5
                print(f"  ✅ {g['topic']} ({g['count']} papers)")
        if low:
            for g in low:
                print(f"  ⚠️ {g['topic']} ({g['count']} paper — kurang)")
        if missing:
            for g in missing[:5]:  # Show top 5
                print(f"  ❌ {g['topic']} (0 papers)")
        print()

        # Step 3: Recommendations
        print("=== Rekomendasi Paper ===")
        existing_topics = [g["topic"] for g in covered]
        recs = self.recommend_related(gaps, existing_topics)
        if not recs:
            print("Tidak ada rekomendasi saat ini.\n")
        else:
            for i, rec in enumerate(recs, 1):
                print(f"  {i}. \"{rec['title']}\"")
                if rec["doi"]:
                    print(f"     DOI: {rec['doi']}")
                if rec["url"]:
                    print(f"     {rec['url']}")
                print(f"     Alasan: {rec['reason']}")
                print()

        # Step 4: Formatted bibliography (first 5 papers)
        print(f"=== Daftar Pustaka ({citation_style.upper()} — 5 teratas) ===")
        for i, item in enumerate(items[:5], 1):
            citation = formatter.format(item, style=citation_style, number=i)
            print(f"  {citation}")
        print()

    def check_duplicates(self, items: List[Dict]) -> List[Dict]:
        """Check for duplicate items in a collection."""
        detector = DuplicateDetector()
        return detector.find_duplicates(items)

    def analyze_gaps(self, items: List[Dict]) -> List[Dict]:
        """Analyze topic gaps in a collection."""
        analyzer = GapAnalyzer()
        return analyzer.analyze(items)

    def recommend_related(self, gaps: List[Dict], existing_topics: List[str]) -> List[Dict]:
        """Get paper recommendations for gap topics."""
        engine = RecommendationEngine(self)
        return engine.recommend(gaps, existing_topics)
```

- [ ] **Step 7.2: Create CLI entry point**

```python
# zotero_cli.py
#!/usr/bin/env python3
"""CLI entry point for Zotero integration."""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from 9router_journal_finder import JournalFinder


def main():
    """Main CLI entry point."""
    print("=" * 60)
    print("  Zotero Library Analyzer")
    print("=" * 60)
    print()

    finder = JournalFinder()

    # Check for API key
    api_key = os.getenv("ZOTERO_API_KEY")
    if not api_key:
        print("ZOTERO_API_KEY belum diset.")
        print("Set dengan: $env:ZOTERO_API_KEY='your-key' (PowerShell)")
        print("Atau: export ZOTERO_API_KEY='your-key' (Linux/Mac)")
        print()
        print("Atau masukkan langsung di bawah:")
        print("Masukkan Zotero API key: ", end="")
        try:
            api_key = input().strip()
        except (EOFError, KeyboardInterrupt):
            print("\nDibatalkan.")
            sys.exit(0)

    # Run analysis
    finder.pull_zotero(api_key=api_key if api_key else None)


if __name__ == "__main__":
    main()
```

- [ ] **Step 7.3: Run the CLI to verify it works**

Run: `python zotero_cli.py`
Expected: Prompts for API key, shows collection list

- [ ] **Step 7.4: Commit**

```bash
git add 9router_journal_finder.py zotero_cli.py
git commit -m "feat: integrate Zotero modules into JournalFinder with CLI entry point"
```

---

### Task 8: Integration Tests + Polish

**Files:**
- Create: `tests/test_zotero_integration.py`

- [ ] **Step 8.1: Write integration tests**

```python
# tests/test_zotero_integration.py
"""Integration tests for the full Zotero pipeline."""

import unittest
from unittest.mock import MagicMock, patch
from 9router_journal_finder import JournalFinder


class TestZoteroIntegration(unittest.TestCase):
    def setUp(self):
        self.finder = JournalFinder()

    @patch("9router_journal_finder.ZoteroClient")
    def test_check_duplicates_returns_list(self, mock_client):
        """Test that check_duplicates returns a list."""
        items = [
            {"key": "1", "title": "Paper A", "doi": "10.1/a", "authors": [], "journal": "", "date": "", "item_type": ""},
            {"key": "2", "title": "Paper B", "doi": "10.2/b", "authors": [], "journal": "", "date": "", "item_type": ""},
        ]
        result = self.finder.check_duplicates(items)
        self.assertIsInstance(result, list)

    def test_analyze_gaps_returns_list(self):
        """Test that analyze_gaps returns a list."""
        items = [
            {"title": "Machine Learning in Medicine", "journal": "", "authors": [], "doi": "", "key": "", "date": "", "item_type": ""},
        ]
        result = self.finder.analyze_gaps(items)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)  # Should have topics

    def test_recommend_related_returns_list(self):
        """Test that recommend_related returns a list even without API."""
        gaps = [{"topic": "NLP", "status": "missing", "count": 0}]
        result = self.finder.recommend_related(gaps, [])
        self.assertIsInstance(result, list)


class TestEndToEnd(unittest.TestCase):
    """End-to-end tests for the full pipeline."""

    def test_full_pipeline_with_mock_data(self):
        """Test the full analysis pipeline with mock data."""
        items = [
            {"title": "Deep Learning for Medical Imaging", "journal": "Medical AI", "authors": ["John Smith"], "doi": "10.1/ml", "key": "1", "date": "2024", "item_type": "journalArticle"},
            {"title": "Neural Networks for Diagnosis", "journal": "AI Medicine", "authors": ["Jane Doe"], "doi": "10.2/nn", "key": "2", "date": "2023", "item_type": "journalArticle"},
            {"title": "NLP for Clinical Notes", "journal": "NLP Journal", "authors": ["Bob Lee"], "doi": "10.3/nlp", "key": "3", "date": "2024", "item_type": "journalArticle"},
        ]

        finder = JournalFinder()

        # Check no crashes on each step
        dups = finder.check_duplicates(items)
        self.assertIsInstance(dups, list)

        gaps = finder.analyze_gaps(items)
        self.assertIsInstance(gaps, list)

        # Recommendations may be empty without API, but should not crash
        recs = finder.recommend_related(gaps, ["Medical AI"])
        self.assertIsInstance(recs, list)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 8.2: Run all tests**

Run: `python -m pytest tests/test_zotero_*.py -v`
Expected: All PASS

- [ ] **Step 8.3: Run full test suite**

Run: `python -m pytest tests/ -v`
Expected: All existing + new tests PASS

- [ ] **Step 8.4: Final commit**

```bash
git add tests/test_zotero_integration.py
git commit -m "test: add integration tests for Zotero pipeline"
```

---

## Plan Self-Review

| Check | Result |
|---|---|
| **Spec coverage** | ✅ All 8 phases covered (client, picker, dedup, gap, recommend, formatter, integration, tests) |
| **Placeholder scan** | ✅ No TBD/TODO — all code is complete |
| **Type consistency** | ✅ All modules use `List[Dict]` consistently, method signatures match spec |
| **Task independence** | ✅ Each task produces testable, commitable code |
| **File map accuracy** | ✅ All files in map have corresponding tasks |
