# AI Engineer Path: Zero to Professional — Design Spec

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Merancang program pembelajaran teks-based yang membawa siswa dari nol (tidak paham matematika, tidak bisa coding) hingga menjadi AI Engineer profesional siap kerja.

**Arsitektur:** 6 fase sequential (22 bulan, 1-2 jam/hari) dengan metode adaptif: sequential/mastery untuk pemula, spiral untuk intermediate, project-based untuk advanced. Berdasarkan Cognitive Load Theory.

**Format:** Teks saja — materi, soal harian, ulangan, kunci jawaban, feedback guide, catatan terstruktur.

**Bahasa:** Campuran — penjelasan dalam Bahasa Indonesia, istilah teknis dan kode dalam Bahasa Inggris.

---

## 1. Prinsip Pedagogis

### 1.1 Cognitive Load Theory (Sweller, 1988+)
- **Novice learners** butuh explicit instruction, worked examples, sequential building
- Working memory terbatas — jangan overload
- **Expertise Reversal Effect:** Setelah fondasi terbangun, spiral dan project-based menjadi lebih efektif

### 1.2 Metode Adaptif Per Fase
| Fase | Metode | Alasan |
|------|--------|--------|
| 1-2 (bulan 1-6) | Sequential/Mastery | Pemula butuh instruksi eksplisit & berurutan |
| 3-4 (bulan 6-14) | Spiral + Mini Proyek | Konsep diulang dalam konteks baru |
| 5-6 (bulan 14-22) | Project-Based | Expertise cukup tinggi → proyek = optimal |

---

## 2. Struktur Keseluruhan

### 2.1 Enam Fase Utama

| Fase | Bulan | Topik | Output |
|------|-------|-------|--------|
| 1. Math Foundation | 1-4 | Aritmetika, Aljabar, Statistika | Skor ulangan ≥ 80% |
| 2. Programming Basics | 3-6 | Python, Logika, Struktur Data | Script sederhana |
| 3. Data Science | 6-9 | NumPy, Pandas, Visualisasi, EDA | Analisis dataset lengkap |
| 4. Machine Learning | 9-14 | Regresi, Klasifikasi, Clustering, Evaluation | Model ML berfungsi |
| 5. Deep Learning | 14-18 | Neural Network, CNN, RNN, NLP | Model DL untuk klasifikasi |
| 6. AI Engineering | 18-22 | MLOps, Deployment, RAG, LLM, Best Practices | Sistem AI production-ready |

**Overlap Fase 1 & 2 (bulan 3-4):** Matematika dan coding dipelajari bersamaan untuk meningkatkan motivasi dan konteks.

### 2.2 Struktur Setiap Modul (~2 Minggu)

```
Hari 1-2:  Teori + Contoh (materi baru)
Hari 3-5:  Latihan Harian (soal per topik)
Hari 6-8:  Latihan Lanjutan (soal campuran)
Hari 9-10: Review + Persiapan Ulangan
Hari 11:   Ulangan Akhir Modul
Hari 12:   Self-Correction (cek jawaban, baca penjelasan)
Hari 13-14: Buffer / remedial jika diperlukan
```

---

## 3. Model Pembelajaran: Socratic Sequential Instruction

### 3.1 Lima Langkah Setiap Sesi

1. **HOOK (5 menit):** Pertanyaan/cerita pembuka yang relate dengan kehidupan sehari-hari
2. **CONCEPT (15-20 menit):** Penjelasan teori dengan analogi, bukan definisi kaku
3. **WORKED EXAMPLE (10 menit):** Contoh soal diselesaikan langkah demi langkah, setiap langkah dijelaskan "kenapa"
4. **GUIDED PRACTICE (15 menit):** Soal latihan dengan hint/clue bertahap
5. **REFLECTION (5 menit):** "Apa yang dipelajari? Apa yang masih bingung?" — dengan self-reflection guide

### 3.2 Persona Guru: "Pak Guru Sabar"

| Sifat | Implementasi |
|-------|-------------|
| Sabar | "Tidak apa-apa kalau belum paham. Ulangi pelan-pelan." |
| Banyak analogi | "Array itu seperti loker di gym." |
| Tidak merendahkan | ✅ "Ini konsep penting, wajar kalau butuh waktu" ❌ "Ini kan dasar banget" |
| Validasi emosi | "Bingung itu tanda kamu lagi belajar, bukan tanda kamu bodoh." |
| Progressif | "Dulu kamu tidak tahu x. Sekarang sudah bisa selesaikan persamaan." |
| Jujur | "Topik ini memang sulit. Bahkan engineer senior masih cek dokumentasi." |

---

## 4. Sistem Soal & Latihan

### 4.1 Tiga Level Soal Harian

| Level | Nama | Contoh | Tujuan |
|-------|------|--------|--------|
| 🟢 | Pemanasan | "Hitung: 3x + 5 = 14, berapa x?" | Cek pemahaman dasar |
| 🟡 | Inti | "Buat fungsi Python yang hitung rata-rata dari list" | Terapkan konsep |
| 🔴 | Tantangan | "Dari data penjualan ini, prediksi bulan depan." | Berpikir kritis |

**Aturan:** Harus selesaikan 🟢 → 🟡 → 🔴 secara berurutan. Jika 🔴 tidak bisa, kembali ke 🟡 dan review.

---

## 5. Sistem Ulangan & Evaluasi

### 5.1 Ulangan Akhir Modul

```
STRUKTUR:
┌─────────────────────────────────────────┐
│ Bagian A: Konsep Dasar (30 poin)        │
│   - 10 soal pilihan ganda               │
│   - 5 soal benar/salah + alasan         │
│ Bagian B: Penerapan (40 poin)           │
│   - 3 soal hitungan / coding pendek     │
│   - 1 soal analisis kasus               │
│ Bagian C: Tantangan (30 poin)           │
│   - 1 soal terbuka (esai)               │
│   - Dinilai dengan rubrik               │
└─────────────────────────────────────────┘
Total: 100 poin
```

### 5.2 Kriteria Kelulusan

| Skor | Status | Tindakan |
|------|--------|----------|
| ≥ 80% | Lulus | Lanjut modul berikutnya |
| 60-79% | Remedial | Review bagian salah, ulangi 2 soal tambahan |
| < 60% | Ulang modul | Mulai dari ringkasan (bukan baca ulang semua) |

### 5.3 Frekuensi Ulangan
- Setiap akhir modul (~2 minggu sekali)
- Ringan, fokus pemahaman konsep (bukan menghafal)

---

## 6. Kunci Jawaban & Self-Check

### 6.1 Format Kunci Jawaban Berlapis

```
✅ JAWABAN: [jawaban langsung]

📝 PENJELASAN:
   [Langkah demi langkah dengan alasan setiap langkah]

💡 KONSEP KUNCI: [konsep inti yang diuji]

⚠️ KESALAHAN UMUM:
   - [Kesalahan yang sering dibuat siswa]

🔗 TERKAIT: [kapan konsep ini akan dipakai lagi]
```

### 6.2 Checklist Self-Correction

```
[ ] 1. Buka kunci jawaban
[ ] 2. Cek jawaban 🟢 — semua benar? Jika salah, baca penjelasan
[ ] 3. Cek jawaban 🟡 — semua benar? Jika salah, ulang worked example
[ ] 4. Coba jawab 🔴 lagi — apakah lebih bisa setelah cek kunci?
[ ] 5. Catat di "Jurnal Belajar" — topik mana yang masih bingung
[ ] 6. Jika ada yang bingung, ulang materi Hari 1-2 sebelum lanjut
```

---

## 7. Jurnal Belajar (Logbook)

Template harian yang diisi siswa:

```
📖 JURNAL BELAJAR — Hari [N], Modul [X]
Tanggal: [YYYY-MM-DD]

✅ Yang sudah paham:
   - [topik 1]
   - [topik 2]

❓ Yang masih bingung:
   - [topik yang belum masuk]

📝 Catatan tambahan:
   - [apa yang butuh penjelasan lebih]

⏰ Waktu belajar hari ini: [X jam Y menit]
😐 Mood: [bagaimana perasaan hari ini]
```

---

## 8. Suasana & Atmosfer

### 8.1 Ritual Harian

**Pembuka:** "Saatnya belajar. Tidak perlu sempurna hari ini. Cukup 1% lebih baik dari kemarin. Mari kita mulai."

**Penutup:** "Hari ini kamu sudah [pencapaian kecil]. Istirahat. Besok kita lanjut."

### 8.2 Progress Map (Text-Based)

```
PETA PERJALANAN AI ENGINEER
═══════════════════════════════════════════
Fase 1: Math Foundation  [████████░░] 80%
  ✅ Aritmetika
  ✅ Aljabar Dasar
  🔲 Statistika Dasar ← kamu di sini
Fase 2: Programming      [██░░░░░░░░] 20%
  ...
```

### 8.3 Milestone Gelar

| Selesai | Gelar |
|---------|-------|
| Fase 1 | 🧮 "Math Apprentice" |
| Fase 2 | 💻 "Code Beginner" |
| Fase 3 | 📊 "Data Explorer" |
| Fase 4 | 🤖 "ML Practitioner" |
| Fase 5 | 🧠 "Deep Learner" |
| Fase 6 | ⚡ "AI Engineer" |

### 8.4 Aturan Anti-Burnout

1. Maksimal 2 jam/hari
2. Stuck > 30 menit → STOP, lanjut besok
3. 1 hari libur/minggu WAJIB
4. Absen 1 hari → tidak apa-apa, hanya jeda
5. Absen 1 minggu → mulai dari review, bukan dari awal

---

## 9. Mekanisme Skip / Fast-Track

### 9.1 Kapan Boleh Skip
- Siswa merasa sudah paham topik
- Sudah punya pengalaman kerja di area tersebut
- Pernah belajar topik ini sebelumnya

### 9.2 Syarat Skip
- Harus melewati **Ujian Validasi** terlebih dahulu
- Skor minimal **85%** (lebih tinggi dari lulus biasa 80%)
- Jika gagal → harus belajar modul dari awal

### 9.3 Format Ujian Validasi

```
BAGIAN A: Konsep Cepat (20 poin)
  - 5 soal pilihan ganda TINGKAT MENENGAH
  - Bukan definisi dasar, tapi penerapan

BAGIAN B: Coding / Hitungan (40 poin)
  - 2 soal yang harus diselesaikan dari nol
  - Tanpa hint, tanpa contoh

BAGIAN C: Analisis (40 poin)
  - 1 soal kasus nyata
  - Harus bisa jelaskan "kenapa" bukan cuma "bagaimana"

Total: 100 poin | Pass mark: 85% | Waktu: 30 menit
```

### 9.4 Aturan Ulang Ujian Validasi
- Lulus (≥85%) → langsung ke modul berikutnya
- Gagal (<85%) → dapat feedback soal yang salah → belajar dari materi → ulangi
- Maksimal 2x attempt; jika gagal lagi → harus belajar full modul

---

## 10. Curriculum Outline Detail

### 10.1 Fase 1: Math Foundation (Bulan 1-4)

| Modul | Minggu | Topik | Lembar Catatan |
|-------|--------|-------|----------------|
| 1.1 | 1-2 | Angka, operasi dasar, pecahan, desimal, persen | Aritmetika fundamental |
| 1.2 | 3-4 | Persamaan linear, variabel, substitusi | Dasar aljabar |
| 1.3 | 5-6 | Fungsi, grafik, slope | Visualisasi relasi |
| 1.4 | 7-8 | Eksponen, logaritma | Penting untuk loss function & probability |
| 1.5 | 9-10 | Statistika deskriptif: mean, median, modus, range | Ringkasan data |
| 1.6 | 11-12 | Varians, standar deviasi, distribusi normal | Fondasi statistik ML |
| 1.7 | 13-14 | Peluang dasar, conditional probability | Bayes theorem nanti dipakai |
| 1.8 | 15-16 | **Ulangan Besar Fase 1** | Assessment komprehensif |

### 10.2 Fase 2: Programming Basics (Bulan 3-6)

| Modul | Minggu | Topik | Lembar Catatan |
|-------|--------|-------|----------------|
| 2.1 | 1-2 | Install Python, print, variabel, tipe data | Mulai coding |
| 2.2 | 3-4 | If-else, perbandingan, boolean | Logika percabangan |
| 2.3 | 5-6 | Loop (for, while), range | Otomatisasi repetisi |
| 2.4 | 7-8 | Fungsi, parameter, return | Modularisasi kode |
| 2.5 | 9-10 | List, tuple, dictionary, set | Struktur data utama |
| 2.6 | 11-12 | String manipulation, file I/O | Baca/tulis data |
| 2.7 | 13-14 | Error handling, debugging dasar | Cara baca error |
| 2.8 | 15-16 | **Mini Project + Ulangan Fase 2** | Script analisis sederhana |

### 10.3 Fase 3: Data Science Basics (Bulan 6-9)

| Modul | Minggu | Topik | Lembar Catatan |
|-------|--------|-------|----------------|
| 3.1 | 1-2 | NumPy: array, operasi matrix | 🔄 Ulang aljabar linear dalam kode |
| 3.2 | 3-4 | Pandas: DataFrame, filtering, grouping | 🔄 Ulang statistika deskriptif |
| 3.3 | 5-6 | Matplotlib/Seaborn: visualisasi | 🔄 Ulang grafik fungsi |
| 3.4 | 7-8 | Exploratory Data Analysis (EDA) | 🔄 Terapkan semua |
| 3.5 | 9-10 | Statistika inferensial: hipotesis, p-value | 🔄 Ulang probability |
| 3.6 | 11-12 | Correlation, simple linear regression | 🔄 Ulang persamaan linear |
| 3.7 | 13-14 | Data cleaning, handling missing values | Praktik nyata |
| 3.8 | 15-16 | **Proyek: Analisis Dataset Lengkap + Ulangan** | Portfolio piece #1 |

### 10.4 Fase 4: Machine Learning (Bulan 9-14)

| Modul | Minggu | Topik | Lembar Catatan |
|-------|--------|-------|----------------|
| 4.1 | 1-2 | Konsep ML: supervised vs unsupervised, train/test split | Fondasi ML |
| 4.2 | 3-4 | Linear Regression | 🔄 Ulang aljabar linear + statistika |
| 4.3 | 5-6 | Logistic Regression | 🔄 Ulang probability |
| 4.4 | 7-8 | Decision Trees & Random Forest | Algoritma non-linear |
| 4.5 | 9-10 | K-Means Clustering | 🔄 Ulang statistik deskriptif |
| 4.6 | 11-12 | Model Evaluation: accuracy, precision, recall, F1, ROC | Cara ukur kualitas model |
| 4.7 | 13-14 | Feature Engineering & Selection | Seni menyiapkan data |
| 4.8 | 15-16 | Cross-validation, overfitting, regularization | 🔄 Ulang konsep generalisasi |
| 4.9 | 17-20 | SVM, Naive Bayes, Gradient Boosting | Algoritma lanjutan |
| 4.10 | 21-24 | **Proyek ML End-to-End + Ulangan Fase 4** | Portfolio piece #2 |

### 10.5 Fase 5: Deep Learning (Bulan 14-18)

| Modul | Minggu | Topik | Lembar Catatan |
|-------|--------|-------|----------------|
| 5.1 | 1-2 | Perceptron, activation function, backpropagation | 🔄 Ulang aljabar + kalkulus konsep |
| 5.2 | 3-4 | Multi-layer Neural Network (PyTorch/TensorFlow) | Framework DL |
| 5.3 | 5-6 | Convolutional Neural Network (CNN) | Computer vision |
| 5.4 | 7-8 | Recurrent Neural Network (RNN) & LSTM | Sequential data |
| 5.5 | 9-10 | Natural Language Processing basics | Text processing |
| 5.6 | 11-12 | Transfer Learning | Pakai model pre-trained |
| 5.7 | 13-14 | Hyperparameter Tuning | Optimasi model |
| 5.8 | 15-16 | **Proyek DL: Image/Text Classifier + Ulangan** | Portfolio piece #3 |

### 10.6 Fase 6: AI Engineering & Production (Bulan 18-22)

| Modul | Minggu | Topik | Lembar Catatan |
|-------|--------|-------|----------------|
| 6.1 | 1-2 | MLOps: versioning data, model, experiment tracking | Produksi, bukan notebook |
| 6.2 | 3-4 | API Development: Flask/FastAPI untuk model | Serve model ke user |
| 6.3 | 5-6 | Deployment: Docker, cloud basics | Containerize & deploy |
| 6.4 | 7-8 | LLM & Prompt Engineering | AI modern |
| 6.5 | 9-10 | RAG (Retrieval-Augmented Generation) | Sistem AI + knowledge base |
| 6.6 | 11-12 | Monitoring & Maintaining ML in Production | Model drift, retraining |
| 6.7 | 13-14 | Best Practices: code review, testing ML, documentation | Profesional |
| 6.8 | 15-18 | **Capstone Project: Sistem AI Production-Ready** | Portfolio final + job-ready |

---

## 11. Lembar Catatan Terstruktur (Template Per Bab)

Setiap bab menghasilkan **Lembar Catatan** yang siap ditulis siswa di buku fisik:

```
═══════════════════════════════════════════════
📘 LEMBAR CATATAN — Modul [X.Y]: [Nama Modul]
Fase: [Fase N] | Minggu: [N-N] | Hari: [N-N]
═══════════════════════════════════════════════

1. RINGKASAN KONSEP
   [2-4 paragraf ringkasan materi utama]

2. RUMUS / SINTAKS PENTING
   - [Rumus 1]: [penjelasan singkat]
   - [Sintaks 2]: [penjelasan singkat]

3. ANALOGI KUNCI
   "[Analogi yang dipakai di materi]"

4. CONTOH KERJA (Worked Example)
   [Soal contoh + langkah penyelesaian]

5. KESALAHAN UMUM
   ⚠️ [Kesalahan 1] → [Koreksi]
   ⚠️ [Kesalahan 2] → [Koreksi]

6. KONEKSI KE TOPIK LAIN
   → Dipakai lagi di: [Fase/Modul berikutnya]

7. CHECKLIST PEMAHAMAN
   [ ] Saya bisa jelaskan konsep ini dengan kata sendiri
   [ ] Saya bisa selesaikan soal level 🟢 tanpa bantuan
   [ ] Saya paham kapan menggunakan konsep ini
   [ ] Saya tahu apa yang belum saya pahami
═══════════════════════════════════════════════
```

---

## 12. Deliverables (Apa yang Dibuat)

Program ini menghasilkan **file-file teks** berikut:

1. **`curriculum/`** — Direktori utama
   - `curriculum/overview.md` — Peta perjalanan + panduan penggunaan
   - `curriculum/phase-1/` s/d `curriculum/phase-6/` — Folder per fase
     - `curriculum/phase-N/module-X.Y.md` — Materi lengkap per modul
     - `curriculum/phase-N/module-X.y-exercises.md` — Soal latihan harian
     - `curriculum/phase-N/module-X.y-exam.md` — Ulangan akhir modul
     - `curriculum/phase-N/module-X.y-answer-key.md` — Kunci jawaban + penjelasan
     - `curriculum/phase-N/module-X.y-notes.md` — Lembar catatan terstruktur
   - `curriculum/validation-exams/` — Ujian validasi untuk skip
     - `curriculum/validation-exams/module-X.y.md` — Ujian validasi per modul
     - `curriculum/validation-exams/module-X.y-answer-key.md` — Kunci validasi
   - `curriculum/journal-template.md` — Template jurnal belajar
   - `curriculum/progress-map.md` — Progress tracker (update manual)

---

## 13. Non-Goals

- Tidak ada video, audio, atau multimedia — **teks only**
- Tidak ada platform digital khusus — file Markdown bisa dibaca di mana saja
- Tidak ada auto-grading — semua self-check dengan kunci jawaban
- Tidak ada AI tutor interaktif dalam kurikulum ini (opsional di luar)
- Tidak membahas matematika tingkat tinggi yang tidak dipakai di AI (misal: topologi, abstract algebra)
