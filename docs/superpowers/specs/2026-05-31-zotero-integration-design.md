# Zotero Integration Design

**Date:** 2026-05-31  
**Status:** Approved  
**Scope:** Pull Zotero collection metadata, detect duplicates, analyze gaps, recommend related papers — CLI only

---

## Overview

Add Zotero Web API integration to the existing Journal Finder system. Users can pull their Zotero collection metadata (bibliography only, no PDFs), detect duplicate entries, identify gaps in their collection, and receive paper recommendations — all through a terminal CLI interface with minimal token usage.

---

## Requirements

### Functional Requirements

1. Connect to Zotero Web API using user-provided API key
2. List available collections and allow user to select one (by number or name)
3. Pull metadata (title, authors, DOI, URL, date, journal) from selected collection
4. Detect duplicate papers (exact DOI match + fuzzy title similarity >90%)
5. Analyze collection gaps (topics with 0 or few papers)
6. Recommend related papers via 9Router web search based on gaps and existing topics
7. Format bibliography output in user-selected citation style (APA, IEEE, MLA, Chicago)
8. Display all output in terminal (no file generation)

### Non-Functional Requirements

- Token efficiency: ~200-350 tokens per session (only web search uses LLM tokens)
- Direct HTTP calls to Zotero API (0 tokens for pull/dedupe/gap analysis)
- Graceful error handling with clear user messages
- Support for rate limit auto-retry (100 req/5s limit)
- Modular architecture for future extensibility (e.g., Mendeley integration)

---

## System Architecture

### File Structure

```
Mencari_Jurnal_Ilmiah/
├── 9router_journal_finder.py          (existing — enhanced with 4 new methods)
│   └── class JournalFinder:
│       ├── find_journals()             (existing)
│       ├── analyze_paper()             (existing)
│       ├── chat()                      (existing)
│       │
│       └── [NEW]
│           ├── pull_zotero()           → main entry point
│           ├── check_duplicates()      → delegate to duplicate_detector
│           ├── analyze_gaps()          → delegate to gap_analyzer
│           └── recommend_related()     → delegate to recommendation_engine
│
└── modules/zotero/
    ├── client.py            → Zotero API wrapper (auth, request, rate limit)
    ├── collection_picker.py → list collections + accept user input
    ├── duplicate_detector.py → duplicate detection logic (DOI, title similarity)
    ├── gap_analyzer.py      → topic extraction + gap identification
    ├── recommendation_engine.py → 9Router web search for related papers
    └── citation_formatter.py → convert metadata to APA/IEEE/MLA/Chicago
```

### Data Flow

```
User runs CLI
  │
  ├→ Enter Zotero API key (or use env var)
  ├→ Select collection (list + manual input)
  │
  ↓
modules/zotero/client.py
  ├→ GET /users/{userID}/collections → list collections
  ├→ GET /users/{userID}/collections/{key}/items → pull metadata
  └→ Return: List[{title, authors, date, DOI, url, journal, itemType}]
  │
  ↓
modules/zotero/duplicate_detector.py
  ├→ Group by exact DOI match
  ├→ Fuzzy match titles (>90% similarity via string comparison)
  └→ Return: List[duplicate groups]
  │
  ↓
modules/zotero/gap_analyzer.py
  ├→ Extract keywords/topics from existing papers
  ├→ Compare against common research areas in the field
  └→ Return: List[{topic, count, status: covered|low|missing}]
  │
  ↓
modules/zotero/recommendation_engine.py
  ├→ For each gap topic → 9Router web search
  ├→ Return top 3-5 relevant papers
  └→ Return: List[{title, doi, url, reason}]
  │
  ↓
modules/zotero/citation_formatter.py
  ├→ Format all papers in user-selected citation style
  └→ Return: Formatted strings
  │
  ↓
Terminal Output (all results displayed)
```

---

## Module Specifications

### 1. ZoteroClient (`modules/zotero/client.py`)

**Purpose:** Wrapper for Zotero Web API

**Responsibilities:**
- Store API key and user ID
- Handle authentication (Authorization header)
- Execute HTTP GET requests with rate limit handling
- Auto-retry on 503 (rate limited) with 5-second backoff
- Parse JSON responses into structured data

**Interface:**
```python
class ZoteroClient:
    def __init__(self, api_key: str, library_type: str = "users", library_id: str = None):
        ...

    def get_collections(self) -> List[Dict]:
        """Returns list of {key, name, num_items}"""

    def get_collection_items(self, collection_key: str, limit: int = 100) -> List[Dict]:
        """Returns list of {title, authors, date, doi, url, journal, item_type}"""
```

**Error Handling:**
- 401 → "API key tidak valid"
- 404 → "Library atau koleksi tidak ditemukan"
- 503 → Auto retry after 5 seconds (max 3 retries)
- Connection error → "Tidak bisa terhubung ke Zotero API"

### 2. CollectionPicker (`modules/zotero/collection_picker.py`)

**Purpose:** Display available collections and accept user selection

**Responsibilities:**
- Fetch collections from ZoteroClient
- Display numbered list with item counts
- Accept selection by number or by name
- Handle invalid input gracefully

**Interface:**
```python
class CollectionPicker:
    def __init__(self, client: ZoteroClient):
        ...

    def pick_collection(self) -> Optional[Dict]:
        """Returns selected collection {key, name, num_items} or None if cancelled"""
```

### 3. DuplicateDetector (`modules/zotero/duplicate_detector.py`)

**Purpose:** Detect duplicate papers in a collection

**Responsibilities:**
- Group papers by exact DOI match
- Fuzzy match titles using string similarity (>90% threshold)
- Return grouped duplicates with reason

**Interface:**
```python
class DuplicateDetector:
    def find_duplicates(self, items: List[Dict]) -> List[Dict]:
        """Returns list of {group: [items], reason: "same_doi" | "similar_title"}"""
```

### 4. GapAnalyzer (`modules/zotero/gap_analyzer.py`)

**Purpose:** Identify topics not covered or under-represented in collection

**Responsibilities:**
- Extract keywords from paper titles and metadata
- Compare against known research areas in the field
- Categorize topics as: covered (3+ papers), low (1-2 papers), missing (0 papers)

**Interface:**
```python
class GapAnalyzer:
    def analyze(self, items: List[Dict], field: str = "AI") -> List[Dict]:
        """Returns list of {topic, count, status: "covered" | "low" | "missing"}"""
```

### 5. RecommendationEngine (`modules/zotero/recommendation_engine.py`)

**Purpose:** Find related papers via 9Router web search

**Responsibilities:**
- Accept gap topics as input
- Execute web search via 9Router for each topic
- Return top 3-5 relevant papers with metadata
- Format with reason why recommended

**Interface:**
```python
class RecommendationEngine:
    def __init__(self, journal_finder):
        ...

    def recommend(self, gaps: List[Dict], existing_topics: List[str]) -> List[Dict]:
        """Returns list of {title, doi, url, reason}"""
```

### 6. CitationFormatter (`modules/zotero/citation_formatter.py`)

**Purpose:** Format paper metadata into citation styles

**Responsibilities:**
- Support APA, IEEE, MLA, Chicago formats
- Handle missing fields gracefully (e.g., no DOI → omit)
- Return formatted string

**Interface:**
```python
class CitationFormatter:
    STYLES = ["apa", "ieee", "mla", "chicago"]

    def format(self, item: Dict, style: str = "apa") -> str:
        """Returns formatted citation string"""
```

### 7. JournalFinder Enhancements (`9router_journal_finder.py`)

**New Methods:**
```python
class JournalFinder:
    def pull_zotero(self, api_key: str = None, collection: str = None, citation_style: str = "apa"):
        """Main entry point: pull, dedupe, gap analyze, recommend, display"""

    def check_duplicates(self, items: List[Dict]) -> List[Dict]:
        """Wrapper around DuplicateDetector"""

    def analyze_gaps(self, items: List[Dict]) -> List[Dict]:
        """Wrapper around GapAnalyzer"""

    def recommend_related(self, gaps: List[Dict]) -> List[Dict]:
        """Wrapper around RecommendationEngine"""
```

---

## Terminal Output Format

### Collection Selection
```
Koleksi Zotero kamu:
  1. Machine Learning (23 items)
  2. Medical AI (15 items)
  3. Natural Language Processing (9 items)

Pilih nomor (atau ketik nama koleksi): 2
```

### Citation Style Selection
```
Pilih format daftar pustaka:
  1. APA (Social Sciences, umum)
  2. IEEE (Engineering, Komputer)
  3. MLA (Humaniora)
  4. Chicago (Sejarah, Sains Sosial)

Pilih nomor [default: 1]:
```

### Duplicate Check
```
=== Cek Duplikat ===
⚠ 2 duplikat ditemukan:
  1. "Deep Learning for Medical Imaging" (DOI sama persis)
  2. "AI in Healthcare Review" vs "AI in Healthcare: A Review" (judul mirip 95%)
```

### Gap Analysis
```
=== Analisis Gap ===
Topik yang sudah ada di koleksimu:
  ✅ Medical Imaging (6 papers)
  ✅ Diagnosis (4 papers)
  ✅ Drug Discovery (3 papers)
  ⚠️ Federated Learning (1 paper — kurang)
  ❌ Natural Language Processing (0 papers)
  ❌ Reinforcement Learning (0 papers)
```

### Recommendations
```
=== Rekomendasi Paper ===
Berdasarkan koleksimu, paper berikut mungkin relevan:

  1. "NLP for Clinical Notes Extraction"
     DOI: 10.xxxx/xxxx | https://journal.example.com/nlp-clinical
     Alasan: Koleksimu banyak di Medical Imaging, tapi belum ada NLP

  2. "Federated Learning for Privacy-Preserving Healthcare"
     DOI: 10.xxxx/xxxx | https://journal.example.com/federated-health
     Alasan: Kamu punya 1 paper federated learning, ini topik yang sedang tren
```

---

## Token Budget

| Stage | Token Usage | Notes |
|---|---|---|
| Pull Zotero | 0 | Direct HTTP API |
| Duplicate detection | 0 | String comparison |
| Gap analysis | 0-50 | Keyword extraction (Python) or LLM |
| Recommendations | 200-300 | 9Router web search |
| **Total per session** | **~200-350** | |

---

## Error Handling

| Error | Cause | Response |
|---|---|---|
| `Invalid API key` | Wrong or expired key | ❌ Clear message with instructions |
| `No collections found` | Empty library or insufficient permission | ⚠️ Suggest checking permissions |
| `Rate limited` | Too many requests in short time | ⏳ Auto-retry after 5s (max 3 retries) |
| `No internet` | Connection lost | ❌ "Cek koneksi internet" |
| `Collection not found` | User typed wrong name | ⚠️ Suggest using 'list' command |

---

## Implementation Phases

| Phase | Deliverable | Dependencies |
|---|---|---|
| 1 | `client.py` — API wrapper | None |
| 2 | `collection_picker.py` — user selection | Phase 1 |
| 3 | `duplicate_detector.py` — dedup logic | Phase 1 (items) |
| 4 | `gap_analyzer.py` — topic analysis | Phase 1 (items) |
| 5 | `recommendation_engine.py` — web search | Phase 4, existing JournalFinder |
| 6 | `citation_formatter.py` — APA/IEEE/MLA/Chicago | Phase 1 (items) |
| 7 | Integration to `JournalFinder` + CLI entry | Phases 1-6 |
| 8 | Testing + polish | All phases |

---

## Success Criteria

1. ✅ Zotero API connection working with valid key
2. ✅ Collection list + selection working
3. ✅ Metadata pull returning structured data
4. ✅ Duplicate detection finding DOI matches + similar titles
5. ✅ Gap analysis identifying missing/low topics
6. ✅ Recommendations returning relevant papers via web search
7. ✅ Citation formatting in all 4 styles
8. ✅ Token usage under 350 per session
9. ✅ All error scenarios handled gracefully
10. ✅ CLI output clean and readable
