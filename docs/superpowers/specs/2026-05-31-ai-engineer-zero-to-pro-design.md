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
| 3-4A (bulan 6-11) | Spiral + Mini Proyek | Konsep diulang dalam konteks baru |
| 4B-5 (bulan 12-18) | Spiral → Project-Based | Transisi ke pembelajaran berbasis proyek |
| 6 (bulan 18-22) | Project-Based | Expertise cukup tinggi → proyek = optimal |

---

## 2. Struktur Keseluruhan

### 2.1 Enam Fase Utama

| Fase | Bulan | Topik | Output |
|------|-------|-------|--------|
| 1. Math Foundation | 1-4 | Aritmetika, Aljabar, Statistika | Skor ulangan ≥ 80% |
| 2. Programming Basics | 3-6 | Python, Logika, Struktur Data | Script sederhana |
| 3. Data Science | 6-9 | NumPy, Pandas, Visualisasi, EDA | Analisis dataset lengkap |
| 4A. Supervised ML | 9-11 | Regresi, Klasifikasi, Model Evaluation | Model supervised berfungsi |
| 4B. Advanced ML | 12-14 | Clustering, Feature Engineering, Ensemble | Model unsupervised + pipeline |
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

| Level | Nama | Contoh | Kuota/Hari | Tujuan |
|-------|------|--------|-----------|--------|
| 🟢 | Pemanasan | "Hitung: 3x + 5 = 14, berapa x?" | 3 soal | Cek pemahaman dasar |
| 🟡 | Inti | "Buat fungsi Python yang hitung rata-rata dari list" | 2 soal | Terapkan konsep |
| 🔴 | Tantangan | "Dari data penjualan ini, prediksi bulan depan." | 1 soal (opsional) | Berpikir kritis |

**Total: ~5-6 soal/hari**, realistis untuk sesi 1-2 jam.

**Aturan:** Harus selesaikan 🟢 → 🟡 → 🔴 secara berurutan. Jika 🔴 tidak bisa, kembali ke 🟡 dan review. Jika 🟢 salah > 2 dari 3, ulangi materi sebelum lanjut ke 🟡.

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

### 5.4 Spaced Repetition — Review Berkala

Setiap **4 minggu** (setelah 2 modul selesai), ada **1 hari Review**:

```
REVIEW DAY (setiap 4 minggu):
────────────────────────────
1. Soal campuran dari modul-modul sebelumnya (🟢 🟡 dari 2-4 modul lalu)
2. Koneksi antar topik: "Ingat aljabar linear di Modul 1.2? Ini dipakai di neural network."
3. Self-assessment: "Topik mana dari fase sebelumnya yang sudah lupa?"
4. Refresh singkat: Baca ulang lembar catatan dari topik yang lupa
```

**Tujuan:** Mencegah "forgetting curve" — siswa tidak lupa fondasi saat masuk ke topik lanjut.

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

### 10.4 Fase 4A: Supervised Machine Learning (Bulan 9-11)

| Modul | Minggu | Topik | Lembar Catatan |
|-------|--------|-------|----------------|
| 4.1 | 1-2 | Konsep ML: supervised vs unsupervised, train/test split | Fondasi ML |
| 4.2 | 3-4 | Linear Regression | 🔄 Ulang aljabar linear + statistika |
| 4.3 | 5-6 | Logistic Regression | 🔄 Ulang probability |
| 4.4 | 7-8 | Decision Trees & Random Forest | Algoritma non-linear |
| 4.5 | 9-10 | Model Evaluation: accuracy, precision, recall, F1, ROC | Cara ukur kualitas model |
| 4.6 | 11-12 | **Mini Project Supervised ML + Ulangan Fase 4A** | 🎉 Milestone: "ML Apprentice" |

### 10.5 Fase 4B: Advanced Machine Learning (Bulan 12-14)

| Modul | Minggu | Topik | Lembar Catatan |
|-------|--------|-------|----------------|
| 4.7 | 1-2 | K-Means Clustering, PCA | 🔄 Ulang statistik deskriptif |
| 4.8 | 3-4 | Feature Engineering & Selection | Seni menyiapkan data |
| 4.9 | 5-6 | Cross-validation, overfitting, regularization | 🔄 Ulang konsep generalisasi |
| 4.10 | 7-8 | SVM, Naive Bayes, Gradient Boosting | Algoritma lanjutan |
| 4.11 | 9-10 | **Proyek ML End-to-End + Ulangan Fase 4B** | Portfolio piece #2 |

### 10.6 Fase 5: Deep Learning (Bulan 14-18)

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
| 5.9 | 17-18 | AI Ethics: bias, fairness, interpretability | Tanggung jawab engineer |

### 10.7 Fase 6: AI Engineering & Production (Bulan 18-22)

| Modul | Minggu | Topik | Lembar Catatan |
|-------|--------|-------|----------------|
| 6.1 | 1-2 | MLOps: versioning data, model, experiment tracking | Produksi, bukan notebook |
| 6.2 | 3-4 | API Development: Flask/FastAPI untuk model | Serve model ke user |
| 6.3 | 5-6 | Deployment: Docker, cloud basics | Containerize & deploy |
| 6.4 | 7-8 | LLM & Prompt Engineering | AI modern |
| 6.5 | 9-10 | RAG (Retrieval-Augmented Generation) | Sistem AI + knowledge base |
| 6.6 | 11-12 | Monitoring & Maintaining ML in Production | Model drift, retraining |
| 6.7 | 13-14 | Best Practices: code review, testing ML, documentation | Profesional |
| 6.8 | 15-16 | Capstone Project: Sistem AI Production-Ready | Portfolio final |
| 6.9 | 17-18 | Interview Prep & Portfolio Presentation | Siap kerja |

### 10.8 Competency Checklist — Definisi "Siap Kerja"

Setelah menyelesaikan Fase 6, siswa harus bisa menjawab **YA** pada semua item berikut:

```
COMPETENCY CHECKLIST — AI ENGINEER READY
═══════════════════════════════════════════

TEKNIS:
[ ] Bisa bangun & deploy ML model ke production (API + container)
[ ] Bisa menjelaskan trade-off antara 5+ algoritma ML dan kapan pakai masing-masing
[ ] Bisa baca paper AI dan implementasi dasar dari paper tersebut
[ ] Bisa melakukan EDA lengkap pada dataset baru (dari loading sampai insight)
[ ] Paham MLOps basics: versioning data/model, monitoring, retraining trigger
[ ] Bisa membuat pipeline ML end-to-end (data → train → evaluate → deploy)

PORTFOLIO:
[ ] Punya 3+ proyek yang bisa ditunjukkan:
    - Proyek 1: Analisis dataset lengkap (Fase 3)
    - Proyek 2: Model ML dengan evaluasi (Fase 4)
    - Proyek 3: Model DL atau sistem AI production-ready (Fase 5/6)

KOMUNIKASI:
[ ] Bisa jelaskan konsep ML ke non-technical stakeholder
[ ] Bisa dokumentasikan proyek dengan README yang jelas
[ ] Bisa presentasi hasil analisis/model dalam 10 menit

MINDSET:
[ ] Tahu cara cari jawaban sendiri (dokumentasi, Stack Overflow, paper)
[ ] Paham bahwa "model sempurna" tidak ada — yang ada "model cukup baik untuk konteks ini"
[ ] Siap terus belajar — AI berkembang cepat, tidak ada yang "selesai belajar"
═══════════════════════════════════════════
```

**Kriteria kelulusan akhir:** Semua item ✅ = "AI Engineer Ready"

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
     - Catatan: Fase 4 punya sub-folder `phase-4a/` dan `phase-4b/`
     - `curriculum/phase-N/module-X.Y.md` — Materi lengkap per modul
     - `curriculum/phase-N/module-X.Y-exercises.md` — Soal latihan harian
     - `curriculum/phase-N/module-X.Y-exam.md` — Ulangan akhir modul
     - `curriculum/phase-N/module-X.Y-answer-key.md` — Kunci jawaban + penjelasan
     - `curriculum/phase-N/module-X.Y-notes.md` — Lembar catatan terstruktur
   - `curriculum/validation-exams/` — Ujian validasi untuk skip
     - `curriculum/validation-exams/module-X.Y.md` — Ujian validasi per modul
     - `curriculum/validation-exams/module-X.Y-answer-key.md` — Kunci validasi
   - `curriculum/journal-template.md` — Template jurnal belajar
   - `curriculum/progress-map.md` — Progress tracker (update manual)
   - `curriculum/CHANGELOG.md` — Log perubahan kurikulum
   - `curriculum/style-guide.md` — Panduan tone & persona (extract dari Section 13)

---

## 13. Style Guide — Konsistensi Persona "Pak Guru Sabar"

Agar tone tidak "drift" di 50+ modul, ikuti aturan ini:

### 13.1 Kata & Frase yang SELALU Dipakai
| Situasi | Frase |
|---------|-------|
| Pembuka sesi | "Saatnya belajar. Tidak perlu sempurna hari ini." |
| Siswa stuck | "Tidak apa-apa. Mari kita pelan-pelan." |
| Setelah contoh | "Coba kamu kerjakan sendiri dulu. Hint ada di bawah kalau perlu." |
| Siswa salah | "Hampir! Ini kesalahan yang wajar. Coba perhatikan bagian [X]." |
| Siswa benar | "Bagus! Kamu sudah paham. Ini langkah yang tepat." |
| Penutup sesi | "Hari ini kamu sudah [pencapaian]. Istirahat. Besok kita lanjut." |

### 13.2 Kata & Frase yang DILARANG
| Frase | Alasan | Ganti Dengan |
|-------|--------|-------------|
| "Ini kan gampang" | Merendahkan | "Ini konsep penting, mari kita pelajari bersama" |
| "Harusnya kamu sudah tahu" | Menghakimi | "Mari kita review sebentar konsep sebelumnya" |
| "Perhatian!" | Terlalu kaku | "Ini bagian yang penting ya" |
| "Kamu harus" | Otoriter | "Coba lakukan ini" |
| "Jelas bahwa..." | Asumsikan paham | "Seperti yang sudah kita bahas..." |

### 13.3 Panjang Kalimat
- Kalimat penjelasan: maksimal 25 kata
- Worked example: setiap langkah max 15 kata + rumus
- Analogi: max 3 kalimat

---

## 14. Rollback Mechanism — "Kembali ke Modul Sebelumnya"

Jika siswa yang sudah skip modul (via validasi) ternyata kesulitan di modul berikutnya:

```
ROLLBACK PROTOCOL:
──────────────────
1. Identifikasi: "Di soal mana kamu stuck? Konsep apa yang belum jelas?"
2. Traceback: Cek di lembar catatan modul sebelumnya — "🔗 TERKAIT" section akan tunjuk ke modul yang perlu diulang
3. Remedial Path: Siswa tidak perlu ulang SEMUA modul sebelumnya — hanya modul spesifik yang jadi fondasi topik yang stuck
4. Contoh: Stuck di Linear Regression → trace ke Aljabar Linear (Modul 1.2) → ulang hanya Modul 1.2 + lembar catatannya
```

**Aturan:** Max 2 modul rollback per fase. Jika lebih dari 2, berarti siswa harus review fase tersebut secara menyeluruh.

---

## 15. Quality Assurance — Kriteria Modul "Siap Dipakai"

Setiap modul harus memenuhi checklist ini sebelum ditandai ✅:

```
MODUL QA CHECKLIST:
──────────────────
STRUKTUR:
[ ] Materi punya 5 langkah: Hook → Concept → Worked Example → Guided Practice → Reflection
[ ] Ada 14 hari aktivitas terdefinisi (Hari 1-14)
[ ] Ada lembar catatan terstruktur (template Section 11)

SOAL:
[ ] 🟢 Pemanasan: tepat 3 soal, level dasar
[ ] 🟡 Inti: tepat 2 soal, level penerapan
[ ] 🔴 Tantangan: tepat 1 soal, level analisis
[ ] Total soal harian = 5-6 per hari latihan
[ ] Soal ulangan: Bagian A (15 soal), Bagian B (4 soal), Bagian C (1 soal)

KUNCI JAWABAN:
[ ] Setiap soal punya: jawaban + penjelasan langkah + konsep kunci + kesalahan umum + koneksi topik
[ ] Tidak ada soal tanpa kunci jawaban

PERSONA:
[ ] Tone konsisten "Pak Guru Sabar" (cek Section 13)
[ ] Tidak ada frase terlarang
[ ] Ada minimal 2 analogi per modul

KONEKSI:
[ ] Minimal 1 referensi ke modul sebelumnya (🔄 spiral)
[ ] Minimal 1 preview ke modul berikutnya (🔗 terkait)
──────────────────
Semua ✅ = Modul siap dipakai
```

---

## 16. Buffer Day Guidance (Hari 13-14)

Hari 13-14 BUKAN hari libur. Ini panduan aktivitas:

```
BUFFER DAY MENU (pilih sesuai kebutuhan):

OPSI A — Remedial (jika nilai ulangan < 80%):
  → Baca ulang lembar catatan modul ini
  → Kerjakan ulang soal 🟡 yang kemarin salah
  → Minta hint ke "kunci jawaban" untuk soal yang masih stuck

OPSI B — Pengayaan (jika nilai ulangan > 90%):
  → Coba soal 🔴 lagi (yang kemarin dilewati)
  → Baca "🔗 TERKAIT" di kunci jawaban — pelajari topik yang akan datang
  → Eksplorasi dataset nyata dari Kaggle (opsional)

OPSI C — Catch-up (jika ada hari yang terlewat):
  → Kerjakan latihan harian yang terlewat
  → Tulis jurnal belajar yang belum diisi
  → Review progress map

OPSI D — Istirahat total (jika burnout):
  → Tidak ada tugas. Istirahat.
  → Tidak perlu merasa bersalah.
```

---

## 17. Difficulty Scaling — Progression Level 🔴

Tantangan (🔴) meningkat secara bertahap:

| Fase | Level 🔴 | Contoh |
|------|----------|--------|
| 1 (Math) | Recall + Apply sederhana | "Selesaikan persamaan, lalu jelaskan langkahmu" |
| 2 (Coding) | Implement dari spesifikasi | "Buat fungsi yang melakukan X, handle edge case Y" |
| 3 (Data Science) | Analisis + Insight | "Dari dataset ini, temukan 2 pola dan jelaskan artinya" |
| 4A (Supervised ML) | Model selection + Justifikasi | "Pilih algoritma untuk masalah ini, jelaskan kenapa" |
| 4B (Advanced ML) | Full pipeline | "Dari data mentah sampai model, buat pipeline lengkap" |
| 5 (Deep Learning) | Arsitektur + Tuning | "Desain arsitektur neural network untuk masalah X" |
| 6 (Engineering) | Production-ready system | "Bangun sistem AI end-to-end dengan monitoring" |

---

## 18. Maintenance Strategy — Update Kurikulum

Karena field AI berkembang cepat, kurikulum perlu update berkala:

```
UPDATE CYCLE:
─────────────
- Setiap 6 bulan: Review modul Fase 5-6 (DL & Engineering) untuk update tool/library terbaru
- Setiap 12 bulan: Review keseluruhan kurikulum — apakah ada topik baru yang harus masuk?
- Versioning: File spec ini menggunakan semantic versioning di header
  v1.0.0 = versi initial (Mei 2026)
  v1.1.0 = update minor (tambah modul, ganti contoh)
  v2.0.0 = update mayor (struktur fase berubah)

CHANGE LOG (di file terpisah): `curriculum/CHANGELOG.md`
```

---

## 19. Non-Goals

- Tidak ada video, audio, atau multimedia — **teks only**
- Tidak ada platform digital khusus — file Markdown bisa dibaca di mana saja
- Tidak ada auto-grading — semua self-check dengan kunci jawaban
- Tidak ada AI tutor interaktif dalam kurikulum ini (opsional di luar)
- Tidak membahas matematika tingkat tinggi yang tidak dipakai di AI (misal: topologi, abstract algebra)
