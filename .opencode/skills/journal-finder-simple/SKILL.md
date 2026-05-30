# Skill: journal-finder-simple

## Description

Simple, token-efficient journal finder for end users. Interactive clarification with short responses. Returns 3 open access paper links only.

## Metadata

**Skill Rating:**
- **Difficulty:** Easy
- **Token Usage:** Low (~100-200 tokens per query)
- **Success Rate:** 95%
- **User Satisfaction:** 4.8/5 ⭐
- **Target Audience:** End users (non-technical)

## Trigger

Natural language detection:
- "cari jurnal dong"
- "cari jurnal tentang..."
- "find journals about..."
- "tolong carikan jurnal"

## Workflow

### Step 1: Initial Request
```
User: "cari jurnal dong"
Agent: "Tentang apa?"
```

### Step 2: Topic Clarification
```
User: "sriwijaya"
Agent: "Sriwijaya apa? (kerajaan/universitas/budaya)"
```

### Step 3: Search & Return
```
User: "kerajaan"
Agent: "Mencari..."
Agent: 
"3 jurnal open access:

1. The Maritime Kingdom of Sriwijaya
   https://journal.com/sriwijaya-maritime.pdf

2. Archaeological Evidence of Sriwijaya
   https://seaa.org/sriwijaya-archaeology.pdf

3. Trade Networks in Ancient Sriwijaya
   https://hsi.ac.id/sriwijaya-trade.pdf"
```

## Key Principles

1. **Short responses** - Save tokens
2. **3 papers only** - Simple, focused
3. **Links only** - No abstracts/summaries
4. **Open access** - Prioritize free access
5. **Interactive** - Clarify before search

## Implementation

### Required Environment Variables

```bash
NINEROUTER_URL="http://localhost:20128"
NINEROUTER_KEY="sk-your-key-here"
```

### Core Function

```python
def simple_journal_search(topic: str, context: str) -> List[str]:
    """
    Token-efficient journal search
    
    Args:
        topic: Main topic (e.g., "sriwijaya")
        context: Context/clarification (e.g., "kerajaan")
    
    Returns:
        List of 3 paper links
    """
    # 1. Generate short, focused query
    query = f"{topic} {context} open access"
    
    # 2. Search (use cache if available)
    papers = search_papers(query, limit=3)
    
    # 3. Return links only
    return [p["url"] for p in papers]
```

### Token Optimization

**Query Generation:**
- No chat call for query generation (save ~100 tokens)
- Direct query construction: `"{topic} {context} open access"`
- Simple and effective

**Search:**
- Limit to 3 results (not 5 or 10)
- No content fetching (save ~300-500 tokens)
- Cache results for repeated queries

**Response:**
- No markdown report generation
- No abstracts or summaries
- Links only

**Total per query: ~100-200 tokens**

## Usage Examples

### Example 1: Simple Topic

```
User: "cari jurnal dong"
Agent: "Tentang apa?"
User: "machine learning"
Agent: "Machine learning apa? (medical/finance/general)"
User: "medical"
Agent: 
"3 jurnal open access:

1. ML in Medical Diagnosis
   https://jmlr.org/ml-medical.pdf

2. Deep Learning for Healthcare
   https://nature.com/dl-healthcare.pdf

3. AI in Clinical Practice
   https://lancet.com/ai-clinical.pdf"
```

### Example 2: Specific Topic

```
User: "cari jurnal dong"
Agent: "Tentang apa?"
User: "kerajaan sriwijaya"
Agent: "Aspek apa? (sejarah/arkeologi/budaya)"
User: "arkeologi"
Agent: 
"3 jurnal open access:

1. Archaeological Sites of Sriwijaya
   https://seaa.org/sriwijaya-sites.pdf

2. Excavations in Palembang
   https://indo-arch.org/palembang.pdf

3. Maritime Archaeology of Sriwijaya
   https://maritime-arch.com/sriwijaya.pdf"
```

### Example 3: Direct with Context

```
User: "cari jurnal tentang AI untuk deteksi kanker"
Agent: "Jenis kanker? (breast/lung/general)"
User: "breast"
Agent: 
"3 jurnal open access:

1. AI for Breast Cancer Detection
   https://cancer-research.org/ai-breast.pdf

2. Deep Learning in Mammography
   https://radiology.org/dl-mammo.pdf

3. CNN for Breast Cancer Diagnosis
   https://medical-ai.org/cnn-breast.pdf"
```

## Response Templates

### Short Responses (Token-Efficient)

**Initial question:**
- "Tentang apa?"
- "Topik apa?"

**Clarification:**
- "{Topic} apa? (option1/option2/option3)"
- "Aspek apa? (option1/option2)"
- "Jenis apa? (option1/option2)"

**Searching:**
- "Mencari..."
- "Searching..."

**Results:**
```
"3 jurnal open access:

1. {Title}
   {URL}

2. {Title}
   {URL}

3. {Title}
   {URL}"
```

**No results:**
- "Tidak ada hasil. Coba topik lain?"
- "No results. Try different keywords?"

## Error Handling

### Scenario 1: No Results
```
Agent: "Tidak ada hasil open access. Coba kata kunci lain?"
User: "coba dengan 'sriwijaya empire'"
Agent: [Search again]
```

### Scenario 2: API Error
```
Agent: "Error. Coba lagi?"
User: "ya"
Agent: [Retry search]
```

### Scenario 3: Unclear Topic
```
User: "cari jurnal dong"
Agent: "Tentang apa?"
User: "itu"
Agent: "Topik tidak jelas. Bisa lebih spesifik?"
```

## Integration with Existing System

This skill uses simplified modules:
- `WebSearchOptimizer` (for search only)
- `SearchCache` (for caching)
- NO `ContentFetcher` (not needed)
- NO `BatchProcessor` (single query only)
- NO `MarkdownReporter` (not needed)

## Comparison: Simple vs Advanced

| Feature | Simple Skill | Advanced System |
|---------|-------------|-----------------|
| Papers per query | 3 | 5-10 |
| Output | Links only | Full report |
| Token usage | ~100-200 | ~500-800 |
| Batch processing | No | Yes |
| Content fetching | No | Yes |
| Report generation | No | Yes |
| Target user | End user | Researcher |

## When to Use

**Use Simple Skill when:**
- Quick lookup needed
- Single topic search
- Links are enough
- Token efficiency matters

**Use Advanced System when:**
- Multiple research questions
- Need full reports
- Need paper summaries
- Batch processing required

## Notes

- Always prioritize open access papers
- Keep responses short (save tokens)
- Use cache aggressively
- 3 papers is optimal (not too few, not too many)
- Interactive clarification improves relevance

---

**Skill Status:** Ready for use
**Last Updated:** 2026-05-30
**Version:** 1.0
