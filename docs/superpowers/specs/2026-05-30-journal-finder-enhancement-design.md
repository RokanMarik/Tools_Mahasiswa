# Journal Finder Enhancement Design
**Date:** 2026-05-30  
**Status:** Approved  
**Scope:** Token-efficient modular enhancement with web search and batch processing

## Overview

Enhance the existing 9Router Journal Finder with live web search, content fetching, and batch processing capabilities. The system prioritizes token efficiency while maintaining effectiveness in finding and analyzing academic papers.

## Requirements

### Functional Requirements
1. Search for academic papers via 9router-web-search
2. Fetch and extract paper content via 9router-web-fetch
3. Analyze papers using existing chat capabilities
4. Process multiple research questions in batch mode
5. Generate markdown reports with all findings
6. Implement retry logic with graceful degradation

### Non-Functional Requirements
- Token efficiency: ~500-800 tokens per research question
- Support batch processing of 5+ questions
- Cache search results to reduce duplicate API calls
- Error handling with fallback strategies

## System Architecture

### Core Modules

```
Research Questions (batch input)
    ↓
BatchProcessor (orchestrates)
    ├→ WebSearchOptimizer (1 search per question)
    │   ↓
    │   Top 5 results
    │   ↓
    ├→ ContentFetcher (fetch top 3-5)
    │   ↓
    │   Paper content + metadata
    │   ↓
    ├→ JournalFinder.analyze_paper (chat analysis)
    │   ↓
    │   Analysis results
    │   ↓
    └→ MarkdownReporter
        ↓
    Markdown Report (output)
```

### Module Specifications

#### 1. WebSearchOptimizer
**Purpose:** Generate optimized search queries and execute web searches

**Responsibilities:**
- Accept research question as input
- Use chat to generate ONE powerful search query (token-efficient)
- Execute search via 9router-web-search
- Extract top 5 results with URLs, titles, snippets
- Return structured result list

**Token Cost:** ~200 tokens per question

**Interface:**
```python
class WebSearchOptimizer:
    def optimize_and_search(self, research_question: str) -> List[Dict]:
        """Returns list of papers with {url, title, snippet, source}"""
```

#### 2. ContentFetcher
**Purpose:** Retrieve and extract content from papers

**Responsibilities:**
- Accept list of paper URLs
- Fetch content via 9router-web-fetch
- Extract title, abstract, key sections
- Implement caching to avoid duplicate fetches
- Handle fetch failures gracefully

**Token Cost:** ~300-500 tokens per paper (top 3-5 papers)

**Interface:**
```python
class ContentFetcher:
    def fetch_papers(self, urls: List[str], max_papers: int = 5) -> List[Dict]:
        """Returns list of papers with {url, title, abstract, content, metadata}"""
```

#### 3. BatchProcessor
**Purpose:** Orchestrate processing of multiple research questions

**Responsibilities:**
- Accept list of research questions
- Coordinate WebSearchOptimizer → ContentFetcher → JournalFinder.analyze_paper
- Implement retry logic: attempt primary search, fallback to alternative if needed
- Implement graceful degradation: include partial results with notes
- Aggregate all results for reporting
- Track errors and successes

**Error Handling Strategy:**
1. **Primary attempt:** Standard web search
2. **Retry with fallback:** Try alternative search terms or providers
3. **Graceful degradation:** If all retries fail, include partial results with error notes

**Interface:**
```python
class BatchProcessor:
    def process_batch(self, research_questions: List[str]) -> Dict:
        """Returns aggregated results with {question, papers, analysis, errors}"""
```

#### 4. MarkdownReporter
**Purpose:** Generate human-readable markdown reports

**Responsibilities:**
- Accept aggregated results from BatchProcessor
- Format each research question as a section
- Include: search query, papers found, links, summaries, analysis
- Add metadata (timestamp, total tokens used, processing time)
- Write to markdown file

**Output Format:**
```markdown
# Journal Research Report
Generated: [timestamp]

## Research Question 1: [question]
### Search Query: [optimized query]
### Papers Found: [count]

#### Paper 1: [title]
- **URL:** [link]
- **Source:** [source]
- **Summary:** [summary]
- **Analysis:** [chat analysis]

...

## Metadata
- Total Questions: [count]
- Total Papers Found: [count]
- Estimated Tokens Used: [count]
- Processing Time: [duration]
```

**Interface:**
```python
class MarkdownReporter:
    def generate_report(self, results: Dict, output_file: str) -> str:
        """Generates markdown report and returns file path"""
```

#### 5. Caching Layer
**Purpose:** Reduce duplicate API calls

**Responsibilities:**
- Store search results locally (JSON format)
- Check cache before making new searches
- Implement cache invalidation (optional TTL)
- Support cache clearing

**Storage:** `cache/search_results.json`

**Interface:**
```python
class SearchCache:
    def get(self, query: str) -> Optional[List[Dict]]:
    def set(self, query: str, results: List[Dict]) -> None:
    def clear(self) -> None:
```

## Data Flow

### Single Research Question Flow
1. User provides research question
2. WebSearchOptimizer generates optimized search query
3. Execute web search, get top 5 results
4. ContentFetcher retrieves top 3-5 papers
5. JournalFinder.analyze_paper analyzes each paper
6. Results aggregated and formatted

### Batch Processing Flow
1. User provides list of research questions (file or list)
2. BatchProcessor iterates through each question
3. For each question: execute single question flow
4. Aggregate all results
5. MarkdownReporter generates final report
6. Output: Single markdown file with all findings

## Token Efficiency Strategy

### Optimizations
1. **Single search per question:** One optimized query instead of multiple attempts
2. **Selective fetching:** Only fetch top 3-5 papers instead of all results
3. **Caching:** Reuse results for similar queries
4. **Efficient prompts:** Shorter, focused chat prompts
5. **Batch aggregation:** Process multiple questions in one session

### Token Budget
- Per research question: ~500-800 tokens
- Batch of 5 questions: ~2500-4000 tokens
- With caching: 30-50% reduction on repeated searches

## Error Handling

### Retry Strategy (B → D)
1. **Primary attempt:** Standard search with optimized query
2. **Retry with fallback:** 
   - Try alternative search terms
   - Try different search provider if available
   - Adjust search parameters
3. **Graceful degradation:**
   - Include partial results with error notes
   - Document what couldn't be found
   - Continue processing other questions

### Error Scenarios
- Search returns no results → Try fallback search
- Content fetch fails → Note in report, continue
- Chat analysis fails → Use basic metadata only
- Batch processing fails → Report which questions succeeded/failed

## Implementation Phases

### Phase 1: Core Modules
- Implement WebSearchOptimizer
- Implement ContentFetcher
- Implement SearchCache
- Test individual modules

### Phase 2: Integration
- Implement BatchProcessor
- Integrate with existing JournalFinder
- Test end-to-end flow

### Phase 3: Reporting
- Implement MarkdownReporter
- Test report generation
- Optimize token usage

### Phase 4: Polish
- Error handling refinement
- Performance optimization
- Documentation and examples

## Success Criteria

1. ✓ Web search integration working
2. ✓ Content fetching working
3. ✓ Batch processing 5+ questions
4. ✓ Markdown reports generated correctly
5. ✓ Token usage ~500-800 per question
6. ✓ Retry/fallback logic working
7. ✓ Caching reducing duplicate calls

## File Structure

```
Mencari_Jurnal_Ilmiah/
├── 9router_journal_finder.py (existing, enhanced)
├── modules/
│   ├── web_search_optimizer.py (new)
│   ├── content_fetcher.py (new)
│   ├── batch_processor.py (new)
│   ├── markdown_reporter.py (new)
│   └── search_cache.py (new)
├── cache/
│   └── search_results.json (new)
├── reports/
│   └── [generated markdown reports]
└── docs/
    └── superpowers/
        └── specs/
            └── 2026-05-30-journal-finder-enhancement-design.md
```

## Dependencies

- `requests` (existing)
- `json` (standard library)
- `typing` (standard library)
- 9Router with web-search and web-fetch capabilities

## Next Steps

1. Review and approve this design
2. Create implementation plan with writing-plans skill
3. Implement modules in phases
4. Test and verify
5. Generate example reports
