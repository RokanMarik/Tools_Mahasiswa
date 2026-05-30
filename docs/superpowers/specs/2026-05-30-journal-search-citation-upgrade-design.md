# Journal Search Citation + Sorting Upgrade

## Overview
Upgrade journal search system untuk menampilkan paper berdasarkan **citation count terbanyak** dan **tahun terbaru**, dengan opsi sorting yang bisa dipilih user via CLI.

## Architecture Changes

### 1. Paper Model (`paper_model.py`)
- Tambah field `citation_count: int = 0`
- Field ini diisi oleh source modules dari API response

### 2. Source: OpenAlex (`openalex.py`) — NEW
- Endpoint: `https://api.openalex.org/works`
- Query params: `search=<topic>`, `per_page=<limit>`, `sort=cited_by_count`
- Extract: `title`, `authorships`, `publication_year`, `primary_location.source.display_name`, `doi`, `cited_by_count`, `abstract_inverted_index`
- Citation count: `cited_by_count` (integer, langsung dari API)
- Abstract: reconstruct dari `abstract_inverted_index`

### 3. Source: Garuda (`garuda.py`) — UNCHANGED
- Tetap sebagai source untuk jurnal Indonesia
- Citation count: 0 (API tidak menyediakan)

### 4. Drop Sources: CrossRef + Semantic Scholar
- Di-remove dari `SOURCES` list di `aggregator.py`
- File `crossref.py` dan `semantic_scholar.py` bisa di-arsipkan atau dihapus

### 5. Scoring Module (`scoring.py`) — NEW
- `compute_composite_score(papers)`:
  - Normalisasi sitasi: `citations / max(citations)` (min-max 0-1)
  - Normalisasi tahun: `(year - min_year) / (max_year - min_year)` (0-1)
  - Formula: `score = (norm_citations × 0.6) + (norm_recency × 0.4)`
  - Paper dengan citation_count=0 dan tahun=none mendapat score 0
- `sort_papers(papers, sort_by)`:
  - `composite` (default): pakai composite score
  - `citations`: sort descending by citation_count
  - `year`: sort descending by year
  - `relevance`: sort by existing relevance_score

### 6. Aggregator (`aggregator.py`)
- Update `SOURCES` list: `[openalex, garuda]`
- Setelah fetch + dedup, panggil `scoring.sort_papers(papers, sort_by)`
- Default `sort_by="composite"`, bisa override via CLI

### 7. CLI (`journal_search.py`)
- Tambah argument `--sort` dengan choices: `composite`, `citations`, `year`, `relevance`
- Default: `composite`
- Pass `sort_by` value ke aggregator

## File Changes
| File | Action | Description |
|------|--------|-------------|
| `paper_model.py` | Modify | Tambah `citation_count` field |
| `openalex.py` | Create | New OpenAlex API source |
| `scoring.py` | Create | Composite scoring + sorting logic |
| `aggregator.py` | Modify | Update SOURCES, integrate scoring |
| `journal_search.py` | Modify | Tambah `--sort` CLI arg |
| `crossref.py` | Remove/Delete | Redundan dengan OpenAlex |
| `semantic_scholar.py` | Remove/Delete | Redundan dengan OpenAlex |

## Error Handling
- OpenAlex API error → fallback ke Garuda (jika ada)
- Semua source error → raise RuntimeError seperti sebelumnya
- Invalid `--sort` value → argparse error (built-in validation)
- Division by zero di scoring (semua paper citation=0) → score = recency only

## Testing
- Test OpenAlex search returns papers dengan citation_count
- Test composite score calculation (normalisasi benar, weight 0.6/0.4)
- Test sort by citations, year, composite
- Test edge case: semua paper citation=0
- Test edge case: paper tanpa tahun
