# Modul 1.6: Varians & Distribusi Normal

> **Fase:** 1 — Math Foundation
> **Durasi:** 2 minggu (Hari 1-14)
> **Prerequisite:** Modul 1.5 (Statistika Deskriptif)
> **Preview:** Modul 1.7: Peluang Dasar

---

## 📋 Target Pembelajaran

Setelah menyelesaikan modul ini, kamu bisa:
1. Memahami apa itu varians dan standar deviasi
2. Menghitung varians dan standar deviasi sederhana
3. Memahami bentuk distribusi normal (bell curve)
4. Mengetahui aturan 68-95-99,7
5. Menerapkan konsep ini dalam konteks data nyata

---

## Hari 1-2: Teori + Contoh

### HOOK

Tidak apa-apa kalau topik ini terdengar kompleks. Mari kita pelan-pelan.

Dua kelas punya rata-rata nilai sama: 75. Tapi di kelas A, semua dapat 74-76. Di kelas B, ada yang dapat 40 dan ada yang dapat 100.

Rata-rata sama, tapi SANGAT berbeda. Bagaimana mengukur perbedaannya? Jawabannya: standar deviasi.

### CONCEPT

**Mengapa Range Tidak Cukup?**

Range = terbesar − terkecil. Tapi range hanya lihat 2 nilai, abaikan sisanya.

Kita perlu ukuran yang lihat SEMUA data.

**Varians (Variance):**

Varians = rata-rata dari KUADRAT selisih setiap data dari mean.

Rumus: `σ² = Σ(xᵢ − x̄)² ÷ n`

Langkah hitung:
1. Hitung mean
2. Kurangi mean dari setiap data → selisih
3. Kuadratkan setiap selisih
4. Rata-ratakan semua kuadrat selisih

Contoh: Data = {2, 4, 4, 4, 6}

```
Langkah 1: Mean = (2+4+4+4+6) ÷ 5 = 20 ÷ 5 = 4

Langkah 2: Selisih dari mean:
  2 − 4 = −2
  4 − 4 = 0
  4 − 4 = 0
  4 − 4 = 0
  6 − 4 = 2

Langkah 3: Kuadratkan:
  (−2)² = 4
  0² = 0
  0² = 0
  0² = 0
  2² = 4

Langkah 4: Rata-rata kuadrat:
  (4+0+0+0+4) ÷ 5 = 8 ÷ 5 = 1,6

Varians = 1,6
```

**Standar Deviasi (Standard Deviation):**

Standar deviasi = akar kuadrat dari varians.

`σ = √(varians)`

Dari contoh di atas:
`σ = √1,6 ≈ 1,26`

💡 **Kenapa pakai standar deviasi?** Karena varians pakai kuadrat → satuannya berubah. Standar deviasi balik ke satuan asli.

**Apa Artinya?**
- Standar deviasi KECIL = data rapat di sekitar mean
- Standar deviasi BESAR = data tersebar jauh dari mean

**Distribusi Normal (Bell Curve):**

Distribusi normal = bentuk "lonceng" yang simetris.

Ciri-ciri:
- Mean = Median = Modus (di tengah)
- Simetris kiri-kanan
- Ekornya mendekati sumbu X tapi tidak pernah menyentuh

Contoh data yang mendekati normal:
- Tinggi badan orang dewasa
- IQ
- Kesalahan pengukuran

**Aturan 68-95-99,7:**

Untuk data normal:
- **68%** data dalam ±1 standar deviasi dari mean
- **95%** data dalam ±2 standar deviasi dari mean
- **99,7%** data dalam ±3 standar deviasi dari mean

Contoh: Tinggi badan pria Indonesia: mean = 168 cm, σ = 7 cm.

```
68% pria: antara 161 cm dan 175 cm (168 ± 7)
95% pria: antara 154 cm dan 182 cm (168 ± 14)
99,7% pria: antara 147 cm dan 189 cm (168 ± 21)
```

💡 **Kenapa ini PENTING untuk AI?**
- Banyak model ML asumsikan data berdistribusi normal
- Outlier detection: data di luar ±3σ = outlier
- Normalisasi data: transform ke distribusi normal
- Confidence intervals: "95% yakin nilai ada di rentang ini"

### WORKED EXAMPLE

**Soal 1:** Data = {3, 5, 5, 7}. Hitung varians dan standar deviasi.

**Penyelesaian:**

```
Mean = (3+5+5+7) ÷ 4 = 20 ÷ 4 = 5

Selisih:
  3 − 5 = −2
  5 − 5 = 0
  5 − 5 = 0
  7 − 5 = 2

Kuadrat selisih:
  4, 0, 0, 4

Varians = (4+0+0+4) ÷ 4 = 8 ÷ 4 = 2

Standar deviasi = √2 ≈ 1,41
```

---

**Soal 2:** IQ: mean = 100, σ = 15. Berapa persen orang dengan IQ 70-130?

**Penyelesaian:**

```
70 = 100 − 30 = 100 − 2(15) = mean − 2σ
130 = 100 + 30 = 100 + 2(15) = mean + 2σ

Jadi: 70-130 = mean ± 2σ

Aturan 68-95-99,7: ±2σ = 95%

Jawaban: 95% orang punya IQ 70-130.
```

---

## Hari 3-5: Latihan Harian

### 🟢 Pemanasan (3 soal)

**Soal 1:** Data = {1, 3, 5}. Hitung mean.

**Soal 2:** Apa arti standar deviasi = 0?

**Soal 3:** Jika mean = 50 dan σ = 5, berapa range ±1σ?

### 🟡 Inti (2 soal)

**Soal 1:** Data = {2, 4, 6, 8}. Hitung varians dan standar deviasi.

**Soal 2:** Nilai ujian: mean = 70, σ = 10. Berapa persen siswa dengan nilai 60-80?

### 🔴 Tantangan (1 soal, opsional)

**Soal:** Berat badan bayi: mean = 3,5 kg, σ = 0,5 kg.
a) Berapa range ±2σ?
b) Seorang bayi berat 2,2 kg. Apakah ini outlier? (Petunjuk: apakah di luar ±3σ?)
c) Berapa persen bayi yang beratnya antara 3-4 kg?

> 💡 **Hint 1:** ±2σ = mean ± 2(0,5)
> 💡 **Hint 2:** Outlier = di luar ±3σ = di luar 2,0-5,0 kg
> 💡 **Hint 3:** 3-4 kg = mean ± 1σ → pakai aturan 68-95-99,7

---

## Hari 6-8: Latihan Lanjutan

[Soal-soal campuran — lihat file exercises]

---

## Hari 9-10: Review

**Coba jawab tanpa melihat catatan:**
1. Apa beda varians dan standar deviasi?
2. Hitung varians dari {1, 2, 3, 4, 5}.
3. Apa aturan 68-95-99,7?
4. Kenapa distribusi normal penting di AI?

---

## Hari 11: Ulangan

Buka file: `module-1.6-exam.md`

---

## Hari 12: Self-Correction

Buka file: `module-1.6-answer-key.md`

---

## Hari 13-14: Buffer

Pilih sesuai kebutuhan.

---

## 🔗 Koneksi ke Topik Lain

- **Dipakai lagi di:** Modul 1.7 (Peluang), Fase 3 (Statistika Inferensial), Fase 4 (Model Evaluation)
- **Berdasarkan dari:** Modul 1.5 (mean)
