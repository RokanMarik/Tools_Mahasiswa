# AI Engineer Zero to Pro Curriculum — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Membuat struktur kurikulum lengkap + 1 modul contoh (Modul 1.1) sebagai golden sample, plus semua template, style guide, dan tooling pendukung.

**Arsitektur:** Direktori `curriculum/` dengan folder per fase, setiap modul punya 5 file (materi, latihan, ulangan, kunci jawaban, lembar catatan). Template konsisten menggunakan Markdown.

**Tech Stack:** Markdown (.md files), Git untuk versioning.

**Scope Note:** Plan ini membuat STRUKTUR LENGKAP + 1 modul contoh (Modul 1.1: Angka & Operasi Dasar). Modul lainnya mengikuti pola yang sama dan bisa dibuat di plan terpisah. Ini memastikan kualitas konsisten sebelum scale-up.

---

### Task 1: Buat Struktur Direktori Kurikulum

**Files:**
- Create: `curriculum/` (root directory)
- Create: `curriculum/phase-1/` s/d `curriculum/phase-6/`
- Create: `curriculum/phase-4/phase-4a/` dan `curriculum/phase-4/phase-4b/`
- Create: `curriculum/validation-exams/`

- [ ] **Step 1: Buat direktori utama**

```bash
mkdir -p curriculum/phase-1
mkdir -p curriculum/phase-2
mkdir -p curriculum/phase-3
mkdir -p curriculum/phase-4/phase-4a
mkdir -p curriculum/phase-4/phase-4b
mkdir -p curriculum/phase-5
mkdir -p curriculum/phase-6
mkdir -p curriculum/validation-exams
```

- [ ] **Step 2: Verifikasi struktur**

```bash
tree curriculum/
```

Expected output:
```
curriculum/
├── phase-1/
├── phase-2/
├── phase-3/
├── phase-4/
│   ├── phase-4a/
│   └── phase-4b/
├── phase-5/
├── phase-6/
└── validation-exams/
```

- [ ] **Step 3: Commit**

```bash
git add curriculum/
git commit -m "feat: create curriculum directory structure"
```

---

### Task 2: Buat `curriculum/overview.md` — Peta Perjalanan & Panduan

**Files:**
- Create: `curriculum/overview.md`

- [ ] **Step 1: Tulis overview.md**

```markdown
# AI Engineer Path: Zero to Professional

> **Status:** In Progress
> **Version:** v1.0.0
> **Started:** Mei 2026
> **Estimasi selesai:** ~22 bulan

---

## Peta Perjalanan

```
Fase 1: Math Foundation     [░░░░░░░░░░] 0% — Bulan 1-4
Fase 2: Programming Basics  [░░░░░░░░░░] 0% — Bulan 3-6
Fase 3: Data Science        [░░░░░░░░░░] 0% — Bulan 6-9
Fase 4A: Supervised ML      [░░░░░░░░░░] 0% — Bulan 9-11
Fase 4B: Advanced ML        [░░░░░░░░░░] 0% — Bulan 12-14
Fase 5: Deep Learning       [░░░░░░░░░░] 0% — Bulan 14-18
Fase 6: AI Engineering      [░░░░░░░░░░] 0% — Bulan 18-22
```

---

## Cara Menggunakan Kurikulum Ini

### Untuk Siswa

1. **Mulai dari Fase 1** — jangan skip kecuali kamu yakin sudah paham (pakai Ujian Validasi)
2. **Ikuti jadwal 14 hari per modul** — teori → latihan → ulangan → self-correction
3. **Tulis di buku fisik** — gunakan Lembar Catatan di setiap modul
4. **Isi Jurnal Belajar** setiap hari
5. **Jangan buru-buru** — maksimal 2 jam/hari, 1 hari libur/minggu

### Struktur Setiap Modul

```
module-X.Y.md              ← Materi lengkap (baca Hari 1-2)
module-X.Y-exercises.md    ← Soal latihan (kerjakan Hari 3-8)
module-X.Y-exam.md         ← Ulangan akhir (Hari 11)
module-X.Y-answer-key.md   ← Kunci jawaban (cek Hari 12)
module-X.Y-notes.md        ← Lembar catatan (tulis di buku fisik)
```

### Sistem Level Soal

| Level | Kuota/Hari | Kapan Dikerjakan |
|-------|-----------|------------------|
| 🟢 Pemanasan | 3 soal | Hari 3-5 |
| 🟡 Inti | 2 soal | Hari 3-5 |
| 🔴 Tantangan | 1 soal (opsional) | Hari 6-8 |

### Kriteria Kelulusan

| Skor Ulangan | Status |
|-------------|--------|
| ≥ 80% | Lulus → lanjut modul berikutnya |
| 60-79% | Remedial → review + 2 soal tambahan |
| < 60% | Ulang modul → mulai dari ringkasan |

### Skip / Fast-Track

Jika kamu sudah paham topik tertentu:
1. Buka `validation-exams/module-X.Y.md`
2. Kerjakan ujian validasi (30 menit, pass mark 85%)
3. Jika lulus → langsung ke modul berikutnya
4. Jika gagal → belajar modul dari awal

### Aturan Anti-Burnout

1. Maksimal 2 jam/hari
2. Stuck > 30 menit → STOP, lanjut besok
3. 1 hari libur/minggu WAJIB
4. Absen 1 hari → tidak apa-apa
5. Absen 1 minggu → mulai dari review, bukan dari awal

---

## Kompetensi Akhir (Siap Kerja)

Setelah menyelesaikan semua fase, kamu harus bisa:
- ✅ Bangun & deploy ML model ke production
- ✅ Jelaskan trade-off 5+ algoritma ML
- ✅ Baca paper AI dan implementasi dasar
- ✅ Punya portfolio 3+ proyek
- ✅ Paham MLOps basics

---

## Support

- **Jurnal Belajar:** `journal-template.md`
- **Style Guide:** `style-guide.md` (untuk konsistensi materi)
- **Progress Map:** `progress-map.md` (update manual)
- **Changelog:** `CHANGELOG.md` (log perubahan kurikulum)
```

- [ ] **Step 2: Commit**

```bash
git add curriculum/overview.md
git commit -m "feat: add curriculum overview with roadmap and usage guide"
```

---

### Task 3: Buat `curriculum/style-guide.md` — Panduan Tone & Persona

**Files:**
- Create: `curriculum/style-guide.md`

- [ ] **Step 1: Tulis style-guide.md**

```markdown
# Style Guide — Persona "Pak Guru Sabar"

> **Versi:** v1.0.0
> ** Berlaku untuk:** Semua modul di kurikulum ini

---

## Prinsip Utama

1. **Sabar** — Tidak pernah tergesa-gesa, tidak pernah frustrasi dengan siswa
2. **Analogi** — Selalu gunakan analogi kehidupan sehari-hari
3. **Validasi** — Akui bahwa bingung itu normal
4. **Progressif** — Tunjukkan kemajuan yang sudah dicapai
5. **Jujur** — Akui kalau topik memang sulit

---

## Frase yang SELALU Dipakai

| Situasi | Frase |
|---------|-------|
| Pembuka sesi | "Saatnya belajar. Tidak perlu sempurna hari ini." |
| Siswa stuck | "Tidak apa-apa. Mari kita pelan-pelan." |
| Setelah contoh | "Coba kamu kerjakan sendiri dulu. Hint ada di bawah kalau perlu." |
| Siswa salah | "Hampir! Ini kesalahan yang wajar. Coba perhatikan bagian [X]." |
| Siswa benar | "Bagus! Kamu sudah paham. Ini langkah yang tepat." |
| Penutup sesi | "Hari ini kamu sudah [pencapaian]. Istirahat. Besok kita lanjut." |

---

## Frase yang DILARANG

| Frase | Alasan | Ganti Dengan |
|-------|--------|-------------|
| "Ini kan gampang" | Merendahkan | "Ini konsep penting, mari kita pelajari bersama" |
| "Harusnya kamu sudah tahu" | Menghakimi | "Mari kita review sebentar konsep sebelumnya" |
| "Perhatian!" | Terlalu kaku | "Ini bagian yang penting ya" |
| "Kamu harus" | Otoriter | "Coba lakukan ini" |
| "Jelas bahwa..." | Asumsikan paham | "Seperti yang sudah kita bahas..." |

---

## Format Penulisan

### Panjang Kalimat
- Kalimat penjelasan: maksimal 25 kata
- Worked example: setiap langkah max 15 kata + rumus
- Analogi: max 3 kalimat

### Struktur Materi (5 Langkah)
1. **HOOK** — Pertanyaan/cerita pembuka (1-2 paragraf)
2. **CONCEPT** — Penjelasan teori dengan analogi (2-4 paragraf)
3. **WORKED EXAMPLE** — Contoh diselesaikan langkah demi langkah
4. **GUIDED PRACTICE** — Soal latihan dengan hint bertahap
5. **REFLECTION** — Pertanyaan refleksi + self-reflection guide

### Struktur Kunci Jawaban
```
✅ JAWABAN: [jawaban langsung]

📝 PENJELASAN:
   [Langkah demi langkah dengan alasan]

💡 KONSEP KUNCI: [konsep inti]

⚠️ KESALAHAN UMUM:
   - [Kesalahan 1] → [Koreksi]

🔗 TERKAIT: [kapan dipakai lagi]
```

---

## Checklist Sebelum Publish Modul

- [ ] Tone konsisten "Pak Guru Sabar"
- [ ] Tidak ada frase terlarang
- [ ] Minimal 2 analogi per modul
- [ ] Kalimat tidak lebih dari 25 kata
- [ ] Setiap soal punya kunci jawaban lengkap
```

- [ ] **Step 2: Commit**

```bash
git add curriculum/style-guide.md
git commit -m "feat: add style guide for Pak Guru Sabar persona"
```

---

### Task 4: Buat `curriculum/journal-template.md` & `curriculum/progress-map.md`

**Files:**
- Create: `curriculum/journal-template.md`
- Create: `curriculum/progress-map.md`

- [ ] **Step 1: Tulis journal-template.md**

```markdown
# Jurnal Belajar — Template

> Salin template ini setiap hari belajar. Isi di buku fisik atau file terpisah.

---

## Template Harian

```
📖 JURNAL BELAJAR — Hari [N], Modul [X.Y]: [Nama Modul]
Tanggal: [YYYY-MM-DD]

✅ Yang sudah paham:
   - [topik 1]
   - [topik 2]

❓ Yang masih bingung:
   - [topik yang belum masuk]

📝 Catatan tambahan:
   - [apa yang butuh penjelasan lebih]

⏰ Waktu belajar hari ini: [X jam Y menit]
😐 Mood: 😊 / 😐 / 😞 — [bagaimana perasaan hari ini]
```

---

## Tips Mengisi Jurnal

1. **Jujur** — Tulis apa adanya, jangan di-"bikin bagus"
2. **Spesifik** — Jangan cuma "masih bingung", tapi "bingung bedanya list dan dictionary"
3. **Konsisten** — Isi setiap hari, bahkan kalau cuma 1 baris
4. **Review** — Baca jurnal minggu lalu sebelum mulai modul baru
```

- [ ] **Step 2: Tulis progress-map.md**

```markdown
# Progress Map — AI Engineer Path

> Update manual setiap selesai modul. Ganti `🔲` dengan `✅`.

---

```
PETA PERJALANAN AI ENGINEER
═══════════════════════════════════════════════

🏁 Tujuan: AI Engineer Professional
📅 Estimasi selesai: ~22 bulan dari mulai

Fase 1: Math Foundation        [░░░░░░░░░░] 0%
  🔲 Modul 1.1: Angka & Operasi Dasar
  🔲 Modul 1.2: Persamaan Linear
  🔲 Modul 1.3: Fungsi & Grafik
  🔲 Modul 1.4: Eksponen & Logaritma
  🔲 Modul 1.5: Statistika Deskriptif
  🔲 Modul 1.6: Varians & Distribusi Normal
  🔲 Modul 1.7: Peluang Dasar
  🔲 Ulangan Besar Fase 1

Fase 2: Programming Basics     [░░░░░░░░░░] 0%
  🔲 Modul 2.1: Python Basics
  🔲 Modul 2.2: If-Else & Boolean
  🔲 Modul 2.3: Loop
  🔲 Modul 2.4: Fungsi
  🔲 Modul 2.5: Struktur Data
  🔲 Modul 2.6: String & File I/O
  🔲 Modul 2.7: Error Handling
  🔲 Mini Project + Ulangan Fase 2

Fase 3: Data Science           [░░░░░░░░░░] 0%
  🔲 Modul 3.1: NumPy
  🔲 Modul 3.2: Pandas
  🔲 Modul 3.3: Visualisasi
  🔲 Modul 3.4: EDA
  🔲 Modul 3.5: Statistika Inferensial
  🔲 Modul 3.6: Regresi Linear
  🔲 Modul 3.7: Data Cleaning
  🔲 Proyek Analisis Dataset + Ulangan

Fase 4A: Supervised ML         [░░░░░░░░░░] 0%
  🔲 Modul 4.1: Konsep ML
  🔲 Modul 4.2: Linear Regression
  🔲 Modul 4.3: Logistic Regression
  🔲 Modul 4.4: Decision Trees
  🔲 Modul 4.5: Model Evaluation
  🔲 Mini Project + Ulangan Fase 4A

Fase 4B: Advanced ML           [░░░░░░░░░░] 0%
  🔲 Modul 4.7: Clustering & PCA
  🔲 Modul 4.8: Feature Engineering
  🔲 Modul 4.9: Cross-validation
  🔲 Modul 4.10: SVM & Ensemble
  🔲 Proyek ML End-to-End + Ulangan

Fase 5: Deep Learning          [░░░░░░░░░░] 0%
  🔲 Modul 5.1: Perceptron & Backprop
  🔲 Modul 5.2: Neural Network
  🔲 Modul 5.3: CNN
  🔲 Modul 5.4: RNN & LSTM
  🔲 Modul 5.5: NLP Basics
  🔲 Modul 5.6: Transfer Learning
  🔲 Modul 5.7: Hyperparameter Tuning
  🔲 Modul 5.8: Proyek DL
  🔲 Modul 5.9: AI Ethics

Fase 6: AI Engineering         [░░░░░░░░░░] 0%
  🔲 Modul 6.1: MLOps
  🔲 Modul 6.2: API Development
  🔲 Modul 6.3: Deployment
  🔲 Modul 6.4: LLM & Prompt Engineering
  🔲 Modul 6.5: RAG
  🔲 Modul 6.6: Monitoring
  🔲 Modul 6.7: Best Practices
  🔲 Modul 6.8: Capstone Project
  🔲 Modul 6.9: Interview Prep

═══════════════════════════════════════════════
🎖️ Gelar yang didapat:
  [ ] 🧮 Math Apprentice
  [ ] 💻 Code Beginner
  [ ] 📊 Data Explorer
  [ ] 🤖 ML Practitioner
  [ ] 🧠 Deep Learner
  [ ] ⚡ AI Engineer
```
```

- [ ] **Step 3: Commit**

```bash
git add curriculum/journal-template.md curriculum/progress-map.md
git commit -m "feat: add journal template and progress map"
```

---

### Task 5: Buat `curriculum/CHANGELOG.md`

**Files:**
- Create: `curriculum/CHANGELOG.md`

- [ ] **Step 1: Tulis CHANGELOG.md**

```markdown
# Changelog — AI Engineer Curriculum

## v1.0.0 — 2026-05-31

### Added
- Initial curriculum structure (6 phases, 55+ modules)
- Style guide for "Pak Guru Sabar" persona
- Journal template and progress map
- Modul 1.1 (golden sample)
- Module templates (materi, exercises, exam, answer key, notes)
- Validation exam templates
- QA checklist for module creation

### Design Decisions
- Based on Cognitive Load Theory (Sweller, 1988+)
- Adaptive method: sequential → spiral → project-based
- Text-only format (Markdown)
- Bahasa Indonesia explanation, English terms & code
- 22-month timeline, 1-2 hours/day
```

- [ ] **Step 2: Commit**

```bash
git add curriculum/CHANGELOG.md
git commit -m "feat: add curriculum changelog"
```

---

### Task 6: Buat Template Modul (5 File Template)

**Files:**
- Create: `curriculum/_templates/module-template.md`
- Create: `curriculum/_templates/exercises-template.md`
- Create: `curriculum/_templates/exam-template.md`
- Create: `curriculum/_templates/answer-key-template.md`
- Create: `curriculum/_templates/notes-template.md`

- [ ] **Step 1: Buat folder template**

```bash
mkdir -p curriculum/_templates
```

- [ ] **Step 2: Tulis module-template.md**

```markdown
# Modul [X.Y]: [Nama Modul]

> **Fase:** [N] — [Nama Fase]
> **Durasi:** 2 minggu (Hari 1-14)
> **Prerequisite:** [Modul sebelumnya]
> **Preview:** [Modul berikutnya]

---

## 📋 Target Pembelajaran

Setelah menyelesaikan modul ini, kamu bisa:
1. [Kemampuan 1]
2. [Kemampuan 2]
3. [Kemampuan 3]

---

## Hari 1-2: Teori + Contoh

### HOOK

[1-2 paragraf cerita/pertanyaan pembuka yang relate dengan kehidupan sehari-hari]

### CONCEPT

[2-4 paragraf penjelasan teori dengan analogi]

**Istilah penting:**
- **[Istilah 1]:** [Penjelasan sederhana]
- **[Istilah 2]:** [Penjelasan sederhana]

### WORKED EXAMPLE

**Soal:** [Soal contoh]

**Penyelesaian:**

```
Langkah 1: [penjelasan]
  [rumus/operasi]

Langkah 2: [penjelasan]
  [rumus/operasi]

Langkah 3: [penjelasan]
  [hasil akhir]
```

💡 **Kenapa langkah ini?** [Alasan setiap langkah]

---

## Hari 3-5: Latihan Harian

### 🟢 Pemanasan (3 soal)

**Soal 1:** [Soal level dasar]

**Soal 2:** [Soal level dasar]

**Soal 3:** [Soal level dasar]

### 🟡 Inti (2 soal)

**Soal 1:** [Soal level penerapan]

**Soal 2:** [Soal level penerapan]

### 🔴 Tantangan (1 soal, opsional)

**Soal:** [Soal level analisis]

> 💡 **Hint 1:** [Clue pertama]
> 💡 **Hint 2:** [Clue kedua]
> 💡 **Hint 3:** [Clue ketiga — hampir jawaban]

---

## Hari 6-8: Latihan Lanjutan

[3-5 soal campuran dari konsep yang sudah dipelajari]

---

## Hari 9-10: Review

[Ringkasan konsep + self-assessment questions]

---

## Hari 11: Ulangan

Buka file: `module-X.Y-exam.md`

---

## Hari 12: Self-Correction

Buka file: `module-X.Y-answer-key.md`

---

## Hari 13-14: Buffer

Pilih sesuai kebutuhan:
- **Opsi A** (remedial): Baca ulang lembar catatan, kerjakan ulang soal yang salah
- **Opsi B** (pengayaan): Coba soal 🔴 lagi, baca preview modul berikutnya
- **Opsi C** (catch-up): Kerjakan latihan yang terlewat, isi jurnal
- **Opsi D** (istirahat): Tidak ada tugas. Istirahat.

---

## 🔗 Koneksi ke Topik Lain

- **Dipakai lagi di:** [Fase/Modul berikutnya]
- **Berdasarkan dari:** [Fase/Modul sebelumnya]
```

- [ ] **Step 3: Tulis exercises-template.md**

```markdown
# Latihan — Modul [X.Y]: [Nama Modul]

> **Hari:** 3-8
> **Total soal:** ~30 (5 soal/hari × 6 hari)

---

## Hari 3

### 🟢 Pemanasan

**Soal 1:** [Soal]

**Soal 2:** [Soal]

**Soal 3:** [Soal]

### 🟡 Inti

**Soal 1:** [Soal]

**Soal 2:** [Soal]

### 🔴 Tantangan

**Soal:** [Soal]

---

## Hari 4

[Format sama seperti Hari 3]

---

## Hari 5

[Format sama]

---

## Hari 6-8: Latihan Campuran

[Soal yang menggabungkan beberapa konsep]
```

- [ ] **Step 4: Tulis exam-template.md**

```markdown
# Ulangan — Modul [X.Y]: [Nama Modul]

> **Durasi:** 45-60 menit
> **Open-book:** Ya
> **Total poin:** 100

---

## Bagian A: Konsep Dasar (30 poin)

### Pilihan Ganda (10 soal × 2 poin = 20 poin)

**A1.** [Soal pilihan ganda]
  a) [Opsi]
  b) [Opsi]
  c) [Opsi]
  d) [Opsi]

[A2-A10: format sama]

### Benar/Salah + Alasan (5 soal × 2 poin = 10 poin)

**A11.** [Pernyataan] — Benar atau Salah? Jelaskan.

[A12-A15: format sama]

---

## Bagian B: Penerapan (40 poin)

**B1.** [Soal hitungan/coding] (10 poin)

**B2.** [Soal hitungan/coding] (10 poin)

**B3.** [Soal hitungan/coding] (10 poin)

**B4.** [Analisis kasus] (10 poin)

---

## Bagian C: Tantangan (30 poin)

**C1.** [Soal esai terbuka]

**Rubrik:**
| Kriteria | 0 poin | 5 poin | 10 poin |
|----------|--------|--------|---------|
| [Kriteria 1] | ... | ... | ... |
| [Kriteria 2] | ... | ... | ... |
| [Kriteria 3] | ... | ... | ... |

---

**Kriteria kelulusan:** ≥ 80 poin
```

- [ ] **Step 5: Tulis answer-key-template.md**

```markdown
# Kunci Jawaban — Modul [X.Y]: [Nama Modul]

---

## Latihan Harian

### Hari 3

#### 🟢 Pemanasan

**Soal 1:**
✅ **JAWABAN:** [jawaban]

📝 **PENJELASAN:**
   [Langkah demi langkah]

💡 **KONSEP KUNCI:** [konsep]

⚠️ **KESALAHAN UMUM:**
   - [Kesalahan] → [Koreksi]

🔗 **TERKAIT:** [dipakai lagi di modul X.Y]

[Soal 2-3: format sama]

#### 🟡 Inti

[Format sama]

#### 🔴 Tantangan

[Format sama + hint explanation]

---

## Ulangan

### Bagian A

**A1.** ✅ [Jawaban] + 📝 [Penjelasan]
**A2.** ✅ [Jawaban] + 📝 [Penjelasan]
[A3-A15: format sama]

### Bagian B

**B1.** ✅ [Jawaban] + 📝 [Penjelasan langkah demi langkah]
[B2-B4: format sama]

### Bagian C

**C1.** 📝 **Rubrik Jawaban:**
- Poin 1: [Apa yang harus ada di jawaban]
- Poin 2: [Apa yang harus ada]
- Contoh jawaban lengkap: [Contoh]

---

## Checklist Self-Correction

- [ ] Cek jawaban 🟢 — semua benar?
- [ ] Cek jawaban 🟡 — semua benar?
- [ ] Coba jawab 🔴 lagi
- [ ] Catat di Jurnal Belajar
- [ ] Jika bingung, ulang materi Hari 1-2
```

- [ ] **Step 6: Tulis notes-template.md**

```markdown
# Lembar Catatan — Modul [X.Y]: [Nama Modul]

> **Fase:** [N] | **Minggu:** [N-N] | **Hari:** [N-N]

---

## 1. RINGKASAN KONSEP

[2-4 paragraf ringkasan materi utama — ini yang siswa tulis di buku]

---

## 2. RUMUS / SINTAKS PENTING

- **[Rumus/Sintaks 1]:** [Penjelasan singkat + contoh]
- **[Rumus/Sintaks 2]:** [Penjelasan singkat + contoh]

---

## 3. ANALOGI KUNCI

"[Analogi yang dipakai di materi]"

---

## 4. CONTOH KERJA (Worked Example)

**Soal:** [Soal]

**Jawaban:**
[Langkah 1]
[Langkah 2]
[Hasil]

---

## 5. KESALAHAN UMUM

⚠️ [Kesalahan 1] → [Koreksi]
⚠️ [Kesalahan 2] → [Koreksi]

---

## 6. KONEKSI KE TOPIK LAIN

→ Dipakai lagi di: [Fase/Modul]
→ Berdasarkan dari: [Fase/Modul]

---

## 7. CHECKLIST PEMAHAMAN

- [ ] Saya bisa jelaskan konsep ini dengan kata sendiri
- [ ] Saya bisa selesaikan soal level 🟢 tanpa bantuan
- [ ] Saya paham kapan menggunakan konsep ini
- [ ] Saya tahu apa yang belum saya pahami
```

- [ ] **Step 7: Commit**

```bash
git add curriculum/_templates/
git commit -m "feat: add module templates (materi, exercises, exam, answer key, notes)"
```

---

### Task 7: Buat Modul 1.1 Lengkap (Golden Sample)

**Files:**
- Create: `curriculum/phase-1/module-1.1.md`
- Create: `curriculum/phase-1/module-1.1-exercises.md`
- Create: `curriculum/phase-1/module-1.1-exam.md`
- Create: `curriculum/phase-1/module-1.1-answer-key.md`
- Create: `curriculum/phase-1/module-1.1-notes.md`

**Topic:** Angka, Operasi Dasar, Pecahan, Desimal, Persen

- [ ] **Step 1: Buat module-1.1.md — Materi Lengkap**

```markdown
# Modul 1.1: Angka, Operasi Dasar, Pecahan, Desimal, Persen

> **Fase:** 1 — Math Foundation
> **Durasi:** 2 minggu (Hari 1-14)
> **Prerequisite:** Tidak ada — ini awal perjalanan
> **Preview:** Modul 1.2: Persamaan Linear

---

## 📋 Target Pembelajaran

Setelah menyelesaikan modul ini, kamu bisa:
1. Melakukan operasi hitung (tambah, kurang, kali, bagi) dengan benar
2. Mengubah pecahan ke desimal dan sebaliknya
3. Menghitung persentase dalam konteks sehari-hari
4. Memahami urutan operasi (PEMDAS/BODMAS)

---

## Hari 1-2: Teori + Contoh

### HOOK

Saatnya belajar. Tidak perlu sempurna hari ini. Cukup 1% lebih baik dari kemarin.

Bayangkan kamu pergi ke pasar. Kamu beli 3 apel seharga Rp 5.000 per apel.
Kamu bayar dengan Rp 20.000. Berapa kembalianmu?

Kalau kamu bisa jawab itu, kamu sudah pakai matematika.
Sekarang kita pelajari dasarnya supaya lebih yakin.

### CONCEPT

**Apa itu angka?**
Angka adalah cara kita menghitung dan mengukur. Sudah kamu pakai setiap hari — umur, harga, jam, tanggal. Itu semua angka.

**Operasi Dasar — Ada 4:**

1. **Penjumlahan (+)** — Menambahkan. `3 + 2 = 5`
   - Seperti menambah barang ke keranjang.

2. **Pengurangan (−)** — Mengurangi. `5 − 2 = 3`
   - Seperti mengambil barang dari keranjang.

3. **Perkalian (×)** — Penjumlahan berulang. `3 × 4 = 12`
   - `3 × 4` artinya `3 + 3 + 3 + 3` atau `4 + 4 + 4`
   - Seperti beli 3 apel seharga Rp 4.000 — total Rp 12.000.

4. **Pembagian (÷)** — Membagi rata. `12 ÷ 3 = 4`
   - Seperti membagi 12 permen ke 3 teman — masing-masing dapat 4.

**Pecahan — Bagian dari Keseluruhan:**

Pecahan ditulis `a/b` dimana:
- **a** (atas) = **numerator** = berapa bagian yang kamu punya
- **b** (bawah) = **denominator** = total berapa bagian

Contoh: `3/4` artinya "dari 4 bagian, kamu punya 3 bagian."
- Seperti pizza dipotong 4. Kamu makan 3 potong. → `3/4` pizza.

**Desimal — Pecahan dalam Bentuk Lain:**

`3/4` = `0,75` — artinya sama, cuma beda cara tulis.
- `1/2` = `0,5` (setengah)
- `1/4` = `0,25` (seperempat)
- `3/4` = `0,75` (tiga perempat)

**Persen — Per Seratus:**

Persen (%) artinya "per 100". `50%` = `50/100` = `0,5` = `1/2`

Contoh sehari-hari:
- Diskon 20% di toko — artinya kamu bayar 80% dari harga asli
- Nilai ujian 85% — artinya dari 100 soal, kamu benar 85

**Urutan Operasi (Penting!):**

Kalau ada banyak operasi dalam satu soal, urutannya:
1. **Kurung** dulu → `(3 + 2) × 4`
2. **Kali/Bagi** → `3 + 2 × 4`
3. **Tambah/Kurang** terakhir

Contoh: `3 + 2 × 4 = 3 + 8 = 11` (bukan `5 × 4 = 20`!)

💡 **Mudah diingat:** Ingat kata **"Kurung-Kali-Tambah"** — urutan prioritas.

### WORKED EXAMPLE

**Soal 1:** Hitung `3/4 + 1/4`

**Penyelesaian:**

```
Langkah 1: Penyebut sudah sama (4) → bisa langsung jumlahkan pembilang
  3/4 + 1/4 = (3+1)/4

Langkah 2: Jumlahkan pembilang
  = 4/4

Langkah 3: Sederhanakan
  = 1 (karena 4/4 = 1 keseluruhan)
```

💡 **Kenapa penyebut harus sama?** Karena kita cuma bisa menambahkan "potongan pizza" yang ukurannya sama.

---

**Soal 2:** Hitung 25% dari Rp 80.000

**Penyelesaian:**

```
Langkah 1: Ubah persen ke desimal
  25% = 25/100 = 0,25

Langkah 2: Kalikan dengan angka
  0,25 × 80.000 = 20.000
```

💡 **Cara cepat:** 25% = 1/4, jadi `80.000 ÷ 4 = 20.000`

---

**Soal 3:** Hitung `2 + 3 × 4 − 1`

**Penyelesaian:**

```
Langkah 1: Kerjakan perkalian dulu (sebelum tambah/kurang)
  3 × 4 = 12
  Jadi: 2 + 12 − 1

Langkah 2: Kerjakan dari kiri ke kanan
  2 + 12 = 14
  14 − 1 = 13
```

💡 **Hasil: 13** (bukan 19, karena perkalian didahulukan)

---

## Hari 3-5: Latihan Harian

### 🟢 Pemanasan (3 soal)

**Soal 1:** Hitung `7 + 8 = ?`

**Soal 2:** Hitung `15 − 6 = ?`

**Soal 3:** Hitung `4 × 3 = ?`

### 🟡 Inti (2 soal)

**Soal 1:** Hitung `2/5 + 1/5 = ?` (tuliskan dalam bentuk pecahan paling sederhana)

**Soal 2:** Toko memberi diskon 30% dari harga Rp 50.000. Berapa yang harus dibayar?

### 🔴 Tantangan (1 soal, opsional)

**Soal:** Hitung `(3 + 2) × 4 − 10 ÷ 2 = ?`

> 💡 **Hint 1:** Kerjakan yang di kurung dulu
> 💡 **Hint 2:** Lalu perkalian dan pembagian
> 💡 **Hint 3:** Terakhir penjumlahan dan pengurangan

---

## Hari 6-8: Latihan Lanjutan

[Soal-soal campuran — lihat file exercises]

---

## Hari 9-10: Review

**Coba jawab tanpa melihat catatan:**
1. Apa 4 operasi dasar matematika?
2. Ubah `3/5` ke desimal
3. Berapa 15% dari 200?
4. Hitung: `5 + 2 × 3`

---

## Hari 11: Ulangan

Buka file: `module-1.1-exam.md`

---

## Hari 12: Self-Correction

Buka file: `module-1.1-answer-key.md`

---

## Hari 13-14: Buffer

Pilih sesuai kebutuhan:
- **Opsi A** (remedial): Baca ulang lembar catatan, kerjakan ulang soal yang salah
- **Opsi B** (pengayaan): Coba soal 🔴 lagi, lihat preview Modul 1.2
- **Opsi C** (catch-up): Kerjakan latihan yang terlewat, isi jurnal
- **Opsi D** (istirahat): Tidak ada tugas. Istirahat.

---

## 🔗 Koneksi ke Topik Lain

- **Dipakai lagi di:** Modul 1.2 (Persamaan Linear), Modul 2.1 (Python — operasi aritmetika di kode)
- **Berdasarkan dari:** Tidak ada — ini fondasi paling dasar
```

- [ ] **Step 2: Buat module-1.1-exercises.md**

```markdown
# Latihan — Modul 1.1: Angka & Operasi Dasar

> **Hari:** 3-8
> **Total soal:** ~30

---

## Hari 3

### 🟢 Pemanasan

**Soal 1:** Hitung `7 + 8 = ?`

**Soal 2:** Hitung `15 − 6 = ?`

**Soal 3:** Hitung `4 × 3 = ?`

### 🟡 Inti

**Soal 1:** Hitung `2/5 + 1/5 = ?` (pecahan paling sederhana)

**Soal 2:** Toko memberi diskon 30% dari Rp 50.000. Berapa yang harus dibayar?

### 🔴 Tantangan

**Soal:** Hitung `(3 + 2) × 4 − 10 ÷ 2 = ?`

---

## Hari 4

### 🟢 Pemanasan

**Soal 1:** Hitung `9 + 6 = ?`

**Soal 2:** Hitung `20 − 13 = ?`

**Soal 3:** Hitung `7 × 2 = ?`

### 🟡 Inti

**Soal 1:** Ubah `3/4` ke desimal

**Soal 2:** Kamu dapat nilai 45/60 di ujian. Berapa persen?

### 🔴 Tantangan

**Soal:** Sebuah baju harga Rp 120.000, diskon 25%. Setelah diskon, kena pajak 10%. Berapa harga final?

---

## Hari 5

### 🟢 Pemanasan

**Soal 1:** Hitung `11 + 9 = ?`

**Soal 2:** Hitung `100 − 37 = ?`

**Soal 3:** Hitung `6 × 5 = ?`

### 🟡 Inti

**Soal 1:** Hitung `1/3 + 1/6 = ?` (hint: samakan penyebut dulu)

**Soal 2:** Hitung `0,75 × 200 = ?`

### 🔴 Tantangan

**Soal:** Ibu punya 3/4 kg gula. Pakai 1/3 kg untuk kue. Berapa sisa gula dalam desimal?

---

## Hari 6-8: Latihan Campuran

**Soal 1:** Hitung `8 ÷ 2 + 3 × 4 − 1`

**Soal 2:** Ubah `0,6` ke pecahan paling sederhana

**Soal 3:** Sebuah toko jual 3 barang: A (Rp 25.000), B (Rp 35.000), C (Rp 40.000). Diskon 15% untuk total belanja > Rp 80.000. Berapa yang dibayar jika beli ketiganya?

**Soal 4:** Hitung `(1/2 + 1/3) × 6`

**Soal 5:** Jelaskan dengan kata sendiri: kenapa `2 + 3 × 4` hasilnya 14, bukan 20?
```

- [ ] **Step 3: Buat module-1.1-exam.md**

```markdown
# Ulangan — Modul 1.1: Angka & Operasi Dasar

> **Durasi:** 45-60 menit
> **Open-book:** Ya
> **Total poin:** 100

---

## Bagian A: Konsep Dasar (30 poin)

### Pilihan Ganda (10 soal × 2 poin = 20 poin)

**A1.** Hasil dari `6 × 7` adalah:
  a) 36
  b) 42
  c) 48
  d) 54

**A2.** `3/4` dalam desimal adalah:
  a) 0,34
  b) 0,75
  c) 0,43
  d) 1,33

**A3.** 20% dari 150 adalah:
  a) 20
  b) 25
  c) 30
  d) 35

**A4.** Hasil dari `2 + 3 × 5` adalah:
  a) 25
  b) 17
  c) 15
  d) 10

**A5.** Pecahan paling sederhana dari `4/8` adalah:
  a) `2/4`
  b) `1/2`
  c) `1/4`
  d) `8/16`

**A6.** `0,5` dalam persen adalah:
  a) 5%
  b) 50%
  c) 500%
  d) 0,5%

**A7.** Hasil dari `(4 + 3) × 2` adalah:
  a) 10
  b) 11
  c) 14
  d) 17

**A8.** `1/3 + 1/3 = ?`
  a) `1/6`
  b) `2/3`
  c) `2/6`
  d) `1/3`

**A9.** Harga Rp 80.000 diskon 25%. Harga setelah diskon:
  a) Rp 20.000
  b) Rp 55.000
  c) Rp 60.000
  d) Rp 75.000

**A10.** Urutan operasi yang benar:
  a) Tambah → Kali → Kurung
  b) Kurung → Kali → Tambah
  c) Kali → Kurung → Tambah
  d) Kurung → Tambah → Kali

### Benar/Salah + Alasan (5 soal × 2 poin = 10 poin)

**A11.** `5 + 3 × 2 = 16` — Benar atau Salah? Jelaskan.

**A12.** `1/2 = 0,5` — Benar atau Salah? Jelaskan.

**A13.** 100% dari angka apapun = angka itu sendiri — Benar atau Salah? Jelaskan.

**A14.** `3/4` lebih besar dari `2/3` — Benar atau Salah? Jelaskan.

**A15.** `10 ÷ 2 + 3 = 8` — Benar atau Salah? Jelaskan.

---

## Bagian B: Penerapan (40 poin)

**B1.** (10 poin) Hitung: `(5 + 3) × 2 − 10 ÷ 5`

**B2.** (10 poin) Sebuah laptop harga Rp 7.500.000. Toko memberi diskon 15%. Berapa harga setelah diskon?

**B3.** (10 poin) Ibu membuat kue. Pakai `2/3` kg tepung, lalu tambah `1/4` kg lagi. Berapa total tepung dalam desimal?

**B4.** (10 poin) Jelaskan: kenapa `2 + 3 × 4` hasilnya berbeda dengan `(2 + 3) × 4`? Beri contoh dengan kata-kata.

---

## Bagian C: Tantangan (30 poin)

**C1.** (30 poin) Kamu mau beli 3 barang:
- Sepatu: Rp 250.000
- Tas: Rp 180.000
- Topi: Rp 70.000

Toko memberi diskon 20% jika total belanja > Rp 400.000.
Setelah diskon, ada pajak 10%.

Hitung: Berapa total yang harus dibayar?
Jelaskan setiap langkah perhitunganmu.

**Rubrik C1:**

| Kriteria | 0 poin | 5 poin | 10 poin |
|----------|--------|--------|---------|
| Hitung total belanja | Salah | Benar tapi tidak lengkap | Benar + jelaskan |
| Cek syarat diskon | Tidak cek | Cek tapi salah | Cek + benar |
| Hitung diskon | Salah | Benar tapi salah persen | Benar semua |
| Hitung pajak | Tidak hitung | Salah perhitungan | Benar semua |
| Total final | Salah | Benar tapi tidak lengkap | Benar + jelas |

---

**Kriteria kelulusan:** ≥ 80 poin
```

- [ ] **Step 4: Buat module-1.1-answer-key.md**

```markdown
# Kunci Jawaban — Modul 1.1: Angka & Operasi Dasar

---

## Latihan Harian

### Hari 3

#### 🟢 Pemanasan

**Soal 1:**
✅ **JAWABAN:** 15

📝 **PENJELASAN:** 7 + 8 = 15 (penjumlahan langsung)

💡 **KONSEP KUNCI:** Penjumlahan dasar

**Soal 2:**
✅ **JAWABAN:** 9

📝 **PENJELASAN:** 15 − 6 = 9

💡 **KONSEP KUNCI:** Pengurangan dasar

**Soal 3:**
✅ **JAWABAN:** 12

📝 **PENJELASAN:** 4 × 3 = 12 (atau 4 + 4 + 4 = 12)

💡 **KONSEP KUNCI:** Perkalian = penjumlahan berulang

#### 🟡 Inti

**Soal 1:**
✅ **JAWABAN:** `3/5`

📝 **PENJELASAN:**
   2/5 + 1/5 = (2+1)/5 = 3/5
   Penyebut sama → langsung jumlahkan pembilang.

💡 **KONSEP KUNCI:** Penjumlahan pecahan dengan penyebut sama

**Soal 2:**
✅ **JAWABAN:** Rp 35.000

📝 **PENJELASAN:**
   30% dari 50.000 = 0,30 × 50.000 = 15.000 (diskon)
   50.000 − 15.000 = 35.000 (yang dibayar)

💡 **KONSEP KUNCI:** Menghitung persen → kurangi dari harga asli

⚠️ **KESALAHAN UMUM:**
   - Langsung jawab 15.000 (itu diskon, bukan harga bayar)
   - 30% = 0,30 bukan 0,03

🔗 **TERKAIT:** Dipakai di Modul 1.5 (statistika) dan Fase 3 (analisis data)

#### 🔴 Tantangan

**Soal:**
✅ **JAWABAN:** 15

📝 **PENJELASAN:**
   (3 + 2) × 4 − 10 ÷ 2
   = 5 × 4 − 10 ÷ 2      ← kurung dulu
   = 20 − 10 ÷ 2          ← perkalian
   = 20 − 5               ← pembagian
   = 15                   ← pengurangan

💡 **KONSEP KUNCI:** Urutan operasi (Kurung → Kali/Bagi → Tambah/Kurang)

🔗 **TERKAIT:** Sangat penting untuk Fase 2 (coding) — urutan operasi sama di Python

---

### Hari 4

#### 🟢 Pemanasan
**Soal 1:** ✅ 15 | **Soal 2:** ✅ 7 | **Soal 3:** ✅ 14

#### 🟡 Inti
**Soal 1:** ✅ 0,75 (3 ÷ 4 = 0,75)
**Soal 2:** ✅ 75% (45 ÷ 60 = 0,75 = 75%)

#### 🔴 Tantangan
✅ **JAWABAN:** Rp 92.400

📝 **PENJELASAN:**
   Harga awal: 120.000
   Diskon 25%: 0,25 × 120.000 = 30.000
   Setelah diskon: 120.000 − 30.000 = 90.000
   Pajak 10%: 0,10 × 90.000 = 9.000
   Final: 90.000 + 9.000 = 99.000

⚠️ **KESALAHAN UMUM:**
   - Pajak dihitung dari harga awal (salah — harus dari harga setelah diskon)
   - Diskon dan pajak langsung dijumlahkan (25% + 10% = 35%, salah)

---

### Hari 5

#### 🟢 Pemanasan
**Soal 1:** ✅ 20 | **Soal 2:** ✅ 63 | **Soal 3:** ✅ 30

#### 🟡 Inti
**Soal 1:** ✅ `1/2` (1/3 = 2/6, jadi 2/6 + 1/6 = 3/6 = 1/2)
**Soal 2:** ✅ 150

#### 🔴 Tantangan
✅ **JAWABAN:** ≈ 0,417 kg

📝 **PENJELASAN:**
   3/4 − 1/3
   = 9/12 − 4/12    ← samakan penyebut (12)
   = 5/12
   = 0,4166... ≈ 0,417

---

### Hari 6-8: Latihan Campuran

**Soal 1:** ✅ 17 (8÷2=4, 3×4=12, 4+12=16, 16−1=15) — koreksi: 8÷2+3×4−1 = 4+12−1 = 15

**Soal 2:** ✅ `3/5` (0,6 = 6/10 = 3/5)

**Soal 3:** ✅ Rp 85.000 (total = 100.000, diskon 15% = 15.000, final = 85.000)

**Soal 4:** ✅ 5 ((1/2+1/3) = 3/6+2/6 = 5/6, 5/6×6 = 5)

**Soal 5:** ✅ Karena perkalian didahulukan: 2+(3×4) = 2+12 = 14. Kalau (2+3)×4 = 5×4 = 20. Kurung mengubah urutan.

---

## Ulangan

### Bagian A

**A1.** ✅ b) 42
**A2.** ✅ b) 0,75
**A3.** ✅ c) 30 (0,20 × 150 = 30)
**A4.** ✅ b) 17 (2 + (3×5) = 2 + 15 = 17)
**A5.** ✅ b) 1/2
**A6.** ✅ b) 50%
**A7.** ✅ c) 14 ((4+3)×2 = 7×2 = 14)
**A8.** ✅ b) 2/3
**A9.** ✅ c) Rp 60.000 (25% dari 80.000 = 20.000, 80.000−20.000 = 60.000)
**A10.** ✅ b) Kurung → Kali → Tambah

**A11.** ✅ Salah. 5 + 3×2 = 5 + 6 = 11 (bukan 8×2 = 16). Perkalian didahulukan.
**A12.** ✅ Benar. 1 ÷ 2 = 0,5
**A13.** ✅ Benar. 100% = 100/100 = 1, jadi 1 × angka = angka itu
**A14.** ✅ Benar. 3/4 = 0,75; 2/3 ≈ 0,667; 0,75 > 0,667
**A15.** ✅ Benar. 10÷2 = 5, 5+3 = 8

### Bagian B

**B1.** ✅ 14
   (5+3)×2 − 10÷5 = 8×2 − 2 = 16 − 2 = 14

**B2.** ✅ Rp 6.375.000
   15% dari 7.500.000 = 1.125.000
   7.500.000 − 1.125.000 = 6.375.000

**B3.** ✅ ≈ 0,917 kg
   2/3 + 1/4 = 8/12 + 3/12 = 11/12 = 0,9166...

**B4.** ✅ `2+3×4` = 2+12 = 14 (perkalian dulu). `(2+3)×4` = 5×4 = 20 (kurung dulu). Contoh: beli 2 permen lalu tambah 3 bungkus (masing-masing 4 permen) = 2+12 = 14. VS beli 5 permen lalu kalikan 4 = 20.

### Bagian C

**C1.** ✅ Rp 420.000

📝 **Langkah lengkap:**
   Total belanja: 250.000 + 180.000 + 70.000 = 500.000
   Cek syarat: 500.000 > 400.000 → YA, dapat diskon 20%
   Diskon: 20% dari 500.000 = 100.000
   Setelah diskon: 500.000 − 100.000 = 400.000
   Pajak: 10% dari 400.000 = 40.000
   Final: 400.000 + 40.000 = 440.000

⚠️ **Perhatian:** Koreksi perhitungan — 400.000 + 40.000 = **440.000** (bukan 420.000)

**Rubrik:**
- Hitung total: ✅ 500.000 (10 poin)
- Cek syarat diskon: ✅ > 400.000 (10 poin)
- Hitung diskon: ✅ 100.000 (5 poin)
- Hitung pajak: ✅ 40.000 (5 poin)
- Total final: ✅ 440.000 (10 poin)
Total: 40/40 (jika semua langkah benar)

---

## Checklist Self-Correction

- [ ] Cek jawaban 🟢 — semua benar?
- [ ] Cek jawaban 🟡 — semua benar?
- [ ] Coba jawab 🔴 lagi
- [ ] Catat di Jurnal Belajar
- [ ] Jika bingung, ulang materi Hari 1-2
```

- [ ] **Step 5: Buat module-1.1-notes.md**

```markdown
# Lembar Catatan — Modul 1.1: Angka & Operasi Dasar

> **Fase:** 1 | **Minggu:** 1-2 | **Hari:** 1-14

---

## 1. RINGKASAN KONSEP

Matematika dimulai dari 4 operasi dasar: tambah (+), kurang (−), kali (×), bagi (÷). Semua matematika lanjutan dibangun dari sini.

Pecahan (`a/b`) adalah bagian dari keseluruhan. Desimal (0,5) dan persen (50%) adalah cara lain menulis pecahan yang sama.

Urutan operasi sangat penting: Kurung dulu, lalu Kali/Bagi, terakhir Tambah/Kurang. Tanpa urutan ini, hasil bisa salah.

---

## 2. RUMUS PENTING

- **Pecahan + Pecahan (penyebut sama):** `a/c + b/c = (a+b)/c`
- **Pecahan + Pecahan (penyebut beda):** Samakan penyebut dulu (cari KPK)
- **Persen ke Desimal:** Bagi 100 → `25% = 25/100 = 0,25`
- **Desimal ke Pecahan:** Tulis sebagai x/10, x/100, dst → sederhanakan
- **Urutan Operasi:** Kurung → Kali/Bagi → Tambah/Kurang

---

## 3. ANALOGI KUNCI

"Pecahan itu seperti pizza. `3/4` artinya pizza dipotong 4 potong, kamu punya 3 potong."

"Urutan operasi itu seperti resep masak. Kalau salah urutan — misal masukkan garam sebelum air — hasilnya beda."

---

## 4. CONTOH KERJA

**Soal:** Hitung `(3 + 2) × 4 − 10 ÷ 2`

**Jawaban:**
1. Kurung: 3 + 2 = 5
2. Kali: 5 × 4 = 20
3. Bagi: 10 ÷ 2 = 5
4. Kurang: 20 − 5 = 15
Hasil = 15

---

## 5. KESALAHAN UMUM

⚠️ `2 + 3 × 4` = 20 (salah) → Koreksi: perkalian dulu → 2 + 12 = 14
⚠️ `1/2 + 1/3` = `2/5` (salah) → Koreksi: samakan penyebut → 3/6 + 2/6 = 5/6
⚠️ 20% dari 100 = 2 (salah) → Koreksi: 20/100 × 100 = 20

---

## 6. KONEKSI KE TOPIK LAIN

→ Dipakai lagi di: Modul 1.2 (Persamaan Linear), Modul 2.1 (Python aritmetika)

---

## 7. CHECKLIST PEMAHAMAN

- [ ] Saya bisa jelaskan 4 operasi dasar dengan kata sendiri
- [ ] Saya bisa selesaikan soal 🟢 tanpa bantuan
- [ ] Saya paham urutan operasi
- [ ] Saya bisa ubah pecahan ↔ desimal ↔ persen
- [ ] Saya tahu apa yang belum saya pahami
```

- [ ] **Step 6: Verifikasi QA Checklist**

```bash
echo "=== QA Checklist for Module 1.1 ==="
echo "✅ 5 langkah (Hook, Concept, Worked Example, Guided Practice, Reflection) — ada"
echo "✅ 14 hari aktivitas — ada"
echo "✅ Lembar catatan — ada"
echo "✅ 🟢 3 soal, 🟡 2 soal, 🔴 1 soal per hari latihan — ada"
echo "✅ Ulangan: Bagian A (15 soal), Bagian B (4 soal), Bagian C (1 soal) — ada"
echo "✅ Kunci jawaban lengkap (jawaban + penjelasan + konsep + kesalahan + terkait) — ada"
echo "✅ Persona Pak Guru Sabar — konsisten (cek frase, tidak ada terlarang) — OK"
echo "✅ Minimal 2 analogi — ada (pizza, resep masak, keranjang)"
echo "✅ Referensi ke modul sebelumnya — ada (tidak ada, ini awal)"
echo "✅ Preview ke modul berikutnya — ada (Modul 1.2)"
echo "=== ALL CHECKS PASSED ==="
```

- [ ] **Step 7: Commit**

```bash
git add curriculum/phase-1/
git commit -m "feat: add Module 1.1 (golden sample) — Angka & Operasi Dasar with full exercises, exam, answer key, and notes"
```

---

### Task 8: Buat Template Ujian Validasi

**Files:**
- Create: `curriculum/validation-exams/module-1.1.md`
- Create: `curriculum/validation-exams/module-1.1-answer-key.md`
- Create: `curriculum/validation-exams/README.md`

- [ ] **Step 1: Tulis README.md untuk validation-exams**

```markdown
# Ujian Validasi — Skip Mechanism

> Gunakan ujian ini jika kamu merasa sudah paham modul tertentu dan ingin skip.

---

## Aturan

1. Kerjakan tanpa bantuan materi/modul
2. Waktu: 30 menit
3. Pass mark: 85% (85 dari 100 poin)
4. Maksimal 2x attempt
5. Jika gagal → belajar modul dari awal

## Struktur

| Bagian | Poin | Deskripsi |
|--------|------|-----------|
| A: Konsep Cepat | 20 | 5 soal pilihan ganda tingkat menengah |
| B: Coding/Hitungan | 40 | 2 soal dari nol, tanpa hint |
| C: Analisis | 40 | 1 soal kasus nyata, jelaskan "kenapa" |

## Index

| Modul | File |
|-------|------|
| 1.1 | `module-1.1.md` |
| ... | ... |
```

- [ ] **Step 2: Buat module-1.1.md (validation exam)**

```markdown
# Ujian Validasi — Modul 1.1: Angka & Operasi Dasar

> **Waktu:** 30 menit
> **Pass mark:** 85/100
> **Tanpa bantuan materi**

---

## Bagian A: Konsep Cepat (20 poin)

**A1.** (4 poin) Hasil dari `7 − 3 × 2 + 4` adalah:
  a) 12
  b) 5
  c) 16
  d) 2

**A2.** (4 poin) Manakah yang sama dengan 60%?
  a) `3/5`
  b) `6/100`
  c) `0,06`
  d) `1/6`

**A3.** (4 poin) `2/3 + 1/6 = ?`
  a) `3/9`
  b) `5/6`
  c) `3/6`
  d) `1/2`

**A4.** (4 poin) Harga Rp 200.000 diskon 35%, lalu pajak 10%. Harga final:
  a) Rp 130.000
  b) Rp 143.000
  c) Rp 133.000
  d) Rp 140.000

**A5.** (4 poin) Manakah yang hasilnya PALING BESAR?
  a) `(2 + 3) × 4`
  b) `2 + 3 × 4`
  c) `2 × 3 + 4`
  d) `2 × (3 + 4)`

---

## Bagian B: Hitungan (40 poin)

**B1.** (20 poin) Hitung tanpa kalkulator: `(1/4 + 2/3) × 12 − 5`

**B2.** (20 poin) Sebuah produk harga Rp 350.000. Toko A memberi diskon 20%. Toko B memberi diskon 15% tapi gratis ongkir Rp 25.000. Di mana lebih murah? Jelaskan perhitunganmu.

---

## Bagian C: Analisis (40 poin)

**C1.** (40 poin) Budi menghitung `3 + 4 × 5` dan hasilnya 35. Dia bilang: "Saya hitung dari kiri ke kanan, jadi 3+4=7, lalu 7×5=35."

Jelaskan:
a) Kenapa cara Budi salah? (10 poin)
b) Apa yang seharusnya dilakukan? (10 poin)
c) Berapa hasil yang benar? (10 poin)
d) Beri contoh situasi nyata dimana kesalahan urutan ini bisa berakibat fatal (misal: resep obat, konstruksi bangunan). (10 poin)
```

- [ ] **Step 3: Buat module-1.1-answer-key.md (validation answer key)**

```markdown
# Kunci Jawaban — Validasi Modul 1.1

---

## Bagian A

**A1.** ✅ b) 5 (7−6+4 = 1+4 = 5)
**A2.** ✅ a) 3/5 (60/100 = 3/5)
**A3.** ✅ b) 5/6 (4/6+1/6 = 5/6)
**A4.** ✅ b) Rp 143.000 (350K×0,80=280K... koreksi: 200K×0,65=130K, 130K×1,10=143K)
**A5.** ✅ a) 20 (a=20, b=14, c=10, d=14)

## Bagian B

**B1.** ✅ 15
   1/4+2/3 = 3/12+8/12 = 11/12
   11/12 × 12 = 11
   11 − 5 = 6

⚠️ **Koreksi:** 11/12 × 12 = 11, 11−5 = **6** (bukan 15)

**B2.** ✅ Toko A lebih murah
   Toko A: 350.000 × 0,80 = 280.000
   Toko B: 350.000 × 0,85 + 0 (ongkir gratis) = 297.500
   Toko A lebih murah 17.500

## Bagian C

**C1.**
a) ❌ Salah karena mengabaikan urutan operasi — perkalian harus sebelum penjumlahan (10 poin)
b) Seharusnya: 3 + (4×5) = 3 + 20 (10 poin)
c) Hasil benar: 23 (10 poin)
d) Contoh: Resep obat "3 tablet + 4× dosis harian" — kalau salah urutan bisa overdosis. (10 poin)

---

**Total: 100 poin | Pass mark: 85**
```

- [ ] **Step 4: Commit**

```bash
git add curriculum/validation-exams/
git commit -m "feat: add validation exam templates with Module 1.1 example"
```

---

## Plan Summary

| Task | Output | Estimasi |
|------|--------|----------|
| 1 | Struktur direktori | 2 menit |
| 2 | overview.md | 5 menit |
| 3 | style-guide.md | 5 menit |
| 4 | journal-template.md + progress-map.md | 5 menit |
| 5 | CHANGELOG.md | 2 menit |
| 6 | 5 file template modul | 10 menit |
| 7 | Modul 1.1 lengkap (5 file) | 15 menit |
| 8 | Validation exam + answer key | 10 menit |
| **Total** | **19 file baru** | **~54 menit** |

---

## Self-Review

### 1. Spec Coverage Check

| Spec Section | Covered By Task | Status |
|-------------|-----------------|--------|
| 6 Fase struktur | Task 1 (direktori) | ✅ |
| Socratic Sequential (5 langkah) | Task 6 (template), Task 7 (modul 1.1) | ✅ |
| Persona Pak Guru Sabar | Task 3 (style guide), Task 7 (modul 1.1) | ✅ |
| Soal 🟢🟡🔴 + kuota | Task 6 (template), Task 7 (modul 1.1) | ✅ |
| Ulangan akhir modul | Task 6 (template), Task 7 (modul 1.1-exam) | ✅ |
| Kunci jawaban berlapis | Task 6 (template), Task 7 (modul 1.1-answer-key) | ✅ |
| Jurnal belajar | Task 4 (journal-template) | ✅ |
| Progress map | Task 4 (progress-map) | ✅ |
| Anti-burnout | Task 2 (overview) | ✅ |
| Skip/Fast-Track | Task 8 (validation exams) | ✅ |
| Spaced repetition | Task 2 (overview) | ✅ |
| Competency checklist | Task 2 (overview) | ✅ |
| Lembar catatan | Task 6 (template), Task 7 (modul 1.1-notes) | ✅ |
| Rollback mechanism | Task 2 (overview) | ✅ |
| QA checklist | Task 7 (step 6 verification) | ✅ |
| Buffer day guidance | Task 6 (template), Task 7 (modul 1.1) | ✅ |
| Difficulty scaling | Task 6 (template) | ✅ |
| Maintenance strategy | Task 5 (CHANGELOG) | ✅ |
| Fase 4A/4B split | Task 1 (sub-direktori) | ✅ |
| Module 5.9 Ethics | Progress map (Task 4) | ✅ |
| Module 6.9 Interview Prep | Progress map (Task 4) | ✅ |

**No gaps found.**

### 2. Placeholder Scan

Scanning plan for: TBD, TODO, implement later, fill in details, similar to Task N...

**Result:** No placeholders found. All steps contain actual content.

### 3. Type/Filename Consistency

All module files follow pattern: `module-X.Y[-suffix].md`
All directories follow pattern: `curriculum/phase-N/`
Validation exams: `curriculum/validation-exams/module-X.Y.md`

**Consistent throughout.**

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-05-31-ai-engineer-curriculum.md`. Two execution options:

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** — Execute tasks in this session, batch execution with checkpoints

Which approach?
