# 9Router Journal Finder - Panduan Penggunaan

## Setup

1. **Set environment variables:**
   ```powershell
   # Windows PowerShell
   $env:NINEROUTER_URL = "http://localhost:20128"
   $env:NINEROUTER_KEY = "sk-2ce0b3116b58ede3-4v2kkj-033fc842"
   ```

   ```bash
   # Linux/Mac
   export NINEROUTER_URL="http://localhost:20128"
   export NINEROUTER_KEY="sk-2ce0b3116b58ede3-4v2kkj-033fc842"
   ```

2. **Install dependencies:**
   ```bash
   pip install requests
   ```

## Penggunaan

### 1. Mencari Jurnal Berdasarkan Topik

```python
from 9router_journal_finder import JournalFinder

finder = JournalFinder()
result = finder.find_journals("deep learning for cancer detection")
print(result)
```

### 2. Generate Keywords untuk Penelitian

```python
finder = JournalFinder()
keywords = finder.generate_search_keywords(
    "How does AI improve early detection of Alzheimer's disease?"
)
print(keywords)
```

### 3. Analisis Paper

```python
finder = JournalFinder()
analysis = finder.analyze_paper(
    paper_title="Deep Learning for Medical Image Analysis",
    paper_abstract="This paper presents a novel approach..."
)
print(analysis)
```

### 4. Custom Chat dengan Model Tertentu

```python
finder = JournalFinder()
response = finder.chat(
    prompt="Jelaskan perbedaan CNN dan Transformer untuk medical imaging",
    model="kr/claude-sonnet-4.5",
    temperature=0.7
)
print(response)
```

## Model yang Tersedia

- **Mencari_Jurnal_Ilmiah** - Untuk mencari dan merekomendasikan jurnal
- **Merangkum_Memperjelas_Catatan** - Untuk merangkum dan menganalisis paper
- **Vibecoding** - Untuk generate kode
- **MemperbaikiCoding** - Untuk debug dan fix kode
- **kr/claude-sonnet-4.5** - Model general purpose berkualitas tinggi

## Contoh Workflow Lengkap

```python
# 1. Tentukan topik penelitian
topic = "machine learning for diabetes prediction"

# 2. Cari jurnal yang relevan
journals = finder.find_journals(topic)
print("=== JURNAL YANG RELEVAN ===")
print(journals)

# 3. Generate keywords untuk pencarian
keywords = finder.generate_search_keywords(
    "What are the best ML algorithms for predicting diabetes onset?"
)
print("\n=== KEYWORDS PENCARIAN ===")
print(keywords)

# 4. Setelah menemukan paper, analisis
analysis = finder.analyze_paper(
    paper_title="Random Forest for Diabetes Prediction",
    paper_abstract="We propose a random forest model..."
)
print("\n=== ANALISIS PAPER ===")
print(analysis)
```

## Tips

1. **Gunakan model yang tepat:**
   - `Mencari_Jurnal_Ilmiah` untuk rekomendasi jurnal/database
   - `Merangkum_Memperjelas_Catatan` untuk analisis paper
   - `kr/claude-sonnet-4.5` untuk pertanyaan umum

2. **Atur temperature:**
   - 0.0-0.3: Lebih konsisten, faktual
   - 0.7-1.0: Lebih kreatif, variatif

3. **Atur max_tokens:**
   - 500-800: Response singkat
   - 1000-1500: Response detail
   - 2000+: Response sangat lengkap

## Troubleshooting

**Error: Connection refused**
- Pastikan 9Router berjalan di `http://localhost:20128`
- Cek dengan: `curl http://localhost:20128/api/health`

**Error: 401 Unauthorized**
- Pastikan `NINEROUTER_KEY` sudah diset dengan benar
- Cek key di 9Router Dashboard → Keys

**Response terpotong**
- Tingkatkan `max_tokens` parameter
- Atau buat prompt lebih spesifik
