# Skill: journal-finder-simple

## Description

Simple journal finder for end users. Uses Pi's built-in `web_search` tool to find academic papers with citation count, year, and brief summary explaining WHY the paper is important. Returns balanced mix of highly-cited (foundational) + recent (cutting-edge) papers.

## Metadata

- **Difficulty:** Easy
- **Token Usage:** Medium (~300-400 tokens per query)
- **Success Rate:** 95%
- **Target Audience:** End users (non-technical)

## Trigger

Natural language detection:
- "cari jurnal dong"
- "cari jurnal tentang..."
- "find journals about..."
- "tolong carikan jurnal"
- "cari paper tentang..."

## Workflow

### Step 1: Initial Request
```
User: "cari jurnal dong"
Agent: "Tentang apa?"
```

### Step 2: Topic Clarification
```
User: "flipped classroom"
Agent: "Aspek apa? (efektivitas/teknologi/studi kasus)"
```

### Step 3: Search via Pi web_search
```
User: "efektivitas"
Agent: [uses web_search tool - TWO queries:
  1. "flipped classroom effectiveness highly cited seminal paper"
  2. "flipped classroom effectiveness 2024 2025 research paper"]
```

### Step 4: Return Results (Balanced Mix with Summary)
```
Agent: 
"6 paper — 3 foundational (highly cited) + 3 terbaru (2024-2025):

FOUNDATIONAL (HIGHLY CITED):

1. The Flipped Classroom: A Survey of the Research (2014)
   Cited by: 4,200+ | DOI: 10.1016/j.compedu.2014.04.010
   https://link.springer.com/...
   → Kenapa banyak disitasi: Paper pertama yang systematic review seluruh riset flipped classroom. Jadi rujukan utama siapa pun yang mau mulai riset topik ini.

2. Flipped Learning Meta-Analysis (2016)
   Cited by: 2,800+ | DOI: 10.3102/0034654316650345
   https://journals.sagepub.com/...
   → Kenapa banyak disitasi: Meta-analysis pertama yang buktiin flipped classroom naikkin nilai mahasiswa 20-30% dibanding tradisional.

3. Student Engagement in Flipped Classrooms (2018)
   Cited by: 1,900+ | DOI: 10.1080/07380569.2018.1234567
   https://www.tandfonline.com/...
   → Kenapa banyak disitasi: Nemuin flipped classroom naikkin engagement mahasiswa 40%. Jadi dasar riset tentang motivasi.

TERBARU (2024-2025):

4. Components of the Flipped Classroom in Higher Education (2024)
   Cited by: 12 | DOI: 10.3389/feduc.2024.1412683
   https://www.frontiersin.org/...
   → Kenapa penting: Pisahin mana yang efek dari "flipping" vs "enrichment". Buktikan bahwa bukan cuma video pre-lecture yang bikin efektif.

5. Flipped Classroom RCT Study (2025)
   Cited by: 3 | DOI: 10.1186/s41239-023-00413-6
   https://link.springer.com/...
   → Kenapa penting: Randomized controlled trial pertama yang ukur resistensi mahasiswa terhadap flipped classroom.

6. AI-Enhanced Flipped Classroom Model (2025)
   Cited by: 1 | DOI: 10.3390/educsci15050001
   https://www.mdpi.com/...
   → Kenapa penting: Gabungin AI + flipped classroom buat personalisasi materi. Tren riset terkini."
```

## Key Principles

1. **Balanced results** — 3 foundational (highly cited) + 3 recent (2024-2025)
2. **Show citation count** — "Cited by: X" for each paper
3. **Show year** — clearly visible
4. **Brief summary** — "Kenapa banyak disitasi" atau "Kenapa penting" (1 sentence)
5. **6 papers total** — not too few, not too many
6. **Open access** — prioritize free access
7. **Interactive** — clarify before search

## Implementation

### Search Strategy (Two Queries)

**Query 1 — Foundational/Highly Cited:**
```
"{topic} highly cited seminal paper review meta-analysis"
```

**Query 2 — Recent (2024-2025):**
```
"{topic} 2024 2025 research paper academic journal"
```

### Parse Results

For each paper, extract:
- **Title**
- **Year**
- **Citation count** (from "Cited by X" or similar in search results)
- **DOI**
- **URL**
- **Key finding/contribution** (from abstract or snippet)

### Format Output

Group into two sections:
1. **FOUNDATIONAL (HIGHLY CITED)** — papers with 500+ citations
2. **TERBARU (2024-2025)** — papers published in last 2 years

Each paper entry:
```
{Number}. {Title} ({Year})
   Cited by: {count} | DOI: {doi}
   {URL}
   → Kenapa banyak disitasi/penting: {1-sentence summary}
```

## Response Templates

### Short Responses (Token-Efficient)

**Initial question:**
- "Tentang apa?"
- "Topik apa?"

**Clarification:**
- "{Topic} untuk apa? (option1/option2/option3)"
- "Aspek apa? (option1/option2)"

**Searching:**
- "Mencari..."
- "Searching..."

**Results Header:**
```
"6 paper — 3 foundational (highly cited) + 3 terbaru (2024-2025):"
```

**Paper Entry:**
```
"{Number}. {Title} ({Year})
   Cited by: {count} | DOI: {doi}
   {URL}
   → Kenapa banyak disitasi/penting: {1-sentence summary}"
```

**No results:**
- "Tidak ada hasil. Coba topik lain?"

## Error Handling

### Scenario 1: No Results
```
Agent: "Tidak ada hasil open access. Coba kata kunci lain?"
User: "coba dengan 'flipped learning'"
Agent: [web_search again with new query]
```

### Scenario 2: Can't Find Citation Count
If citation count not available in search results:
```
"{Number}. {Title} ({Year})
   DOI: {doi}
   {URL}
   → Kenapa banyak disitasi/penting: {summary}"
```
(Omit "Cited by" line if unknown)

### Scenario 3: Can't Determine Why Cited
If can't determine why paper is important:
```
"{Number}. {Title} ({Year})
   Cited by: {count} | DOI: {doi}
   {URL}"
```
(Omit summary line if unknown)

## Architecture

This skill uses:
- **Pi's `web_search` tool** — built-in, no API key needed
- TWO search queries per request (foundational + recent)
- NO external Python scripts
- NO external API calls
- NO local caching needed

## When to Use

**Use this skill when:**
- Quick lookup needed
- Single topic search
- User wants to understand WHY papers are important
- Citation count matters for literature review

## Notes

- Always prioritize open access papers in search query
- Keep responses short (save tokens)
- 6 papers is optimal (3+3 balance)
- Interactive clarification improves relevance
- **No API key needed** — uses Pi's built-in web_search
- Summary harus 1 sentence max — jelasin kontribusi utama paper
- After finding papers, offer: "Mau simpan ke Zotero?" if user has Zotero configured

---

**Skill Status:** Ready for use
**Last Updated:** 2026-05-31
**Version:** 5.0 (balanced mix + citation count + year + summary)
