# Modul 1.4: Eksponen & Logaritma

> **Fase:** 1 — Math Foundation
> **Durasi:** 2 minggu (Hari 1-14)
> **Prerequisite:** Modul 1.1 (Angka & Operasi), Modul 1.2 (Persamaan Linear)
> **Preview:** Modul 1.5: Statistika Deskriptif

---

## 📋 Target Pembelajaran

Setelah menyelesaikan modul ini, kamu bisa:
1. Memahami konsep eksponen (perpangkatan)
2. Menghitung nilai eksponen sederhana
3. Memahami aturan-aturan eksponen
4. Memahami apa itu logaritma dan hubungannya dengan eksponen
5. Menghitung logaritma sederhana

---

## Hari 1-2: Teori + Contoh

### HOOK

Tidak apa-apa kalau topik ini terdengar menakutkan. Mari kita pelan-pelan.

Pernah dengar "bakteri berkembang biak tiap jam"? Kalau 1 bakteri jadi 2, lalu 2 jadi 4, lalu 4 jadi 8... itu eksponen!

Dan logaritma? Itu cuma cara bertanya: "perpangkatan berapa supaya dapat angka ini?"

### CONCEPT

**Apa itu Eksponen?**

Eksponen = perkalian berulang dengan angka yang sama.

`2³ = 2 × 2 × 2 = 8`

Dibaca: "dua pangkat tiga" atau "dua kubik"

- **2** = basis (angka yang dikalikan)
- **3** = eksponen/pangkat (berapa kali dikalikan)

Contoh lain:
- `5² = 5 × 5 = 25` (lima kuadrat)
- `10³ = 10 × 10 × 10 = 1.000`
- `2⁰ = 1` (apapun pangkat 0 = 1)

**Aturan Eksponen:**

| Aturan | Contoh |
|--------|--------|
| `aᵐ × aⁿ = aᵐ⁺ⁿ` | `2³ × 2² = 2⁵ = 32` |
| `aᵐ ÷ aⁿ = aᵐ⁻ⁿ` | `2⁵ ÷ 2² = 2³ = 8` |
| `(aᵐ)ⁿ = aᵐˣⁿ` | `(2³)² = 2⁶ = 64` |
| `a⁰ = 1` | `5⁰ = 1` |
| `a⁻ⁿ = 1/aⁿ` | `2⁻³ = 1/8` |

**Apa itu Logaritma?**

Logaritma adalah KEBALIKAN dari eksponen.

Pertanyaan logaritma: "Basis pangkat BERAPA supaya dapat hasil ini?"

`log₂(8) = ?` → "2 pangkat berapa = 8?" → Jawab: 3 (karena 2³ = 8)

Contoh lain:
- `log₁₀(100) = 2` (karena 10² = 100)
- `log₂(16) = 4` (karena 2⁴ = 16)
- `log₃(27) = 3` (karena 3³ = 27)

**Hubungan Eksponen ↔ Logaritma:**

```
Eksponen:  2³ = 8
Logaritma: log₂(8) = 3
```

Mereka saling membalikkan!

💡 **Kenapa ini penting untuk AI?**
- Loss function di neural network pakai logaritma
- Probability sering ditulis dalam log (log-likelihood)
- Skala data (normalisasi) pakai log transform

### WORKED EXAMPLE

**Soal 1:** Hitung `3⁴`

**Penyelesaian:**

```
3⁴ = 3 × 3 × 3 × 3
   = 9 × 9
   = 81
```

---

**Soal 2:** Hitung `log₅(125)`

**Penyelesaian:**

```
Pertanyaan: 5 pangkat berapa = 125?

5¹ = 5
5² = 25
5³ = 125 ← ini!

Jadi: log₅(125) = 3
```

---

**Soal 3:** Sederhanakan `2⁴ × 2³`

**Penyelesaian:**

```
Aturan: aᵐ × aⁿ = aᵐ⁺ⁿ

2⁴ × 2³ = 2⁴⁺³ = 2⁷ = 128

Cek: 2⁴ = 16, 2³ = 8, 16 × 8 = 128 ✅
```

---

## Hari 3-5: Latihan Harian

### 🟢 Pemanasan (3 soal)

**Soal 1:** Hitung `2⁵`

**Soal 2:** Hitung `log₂(32)`

**Soal 3:** Hitung `10²`

### 🟡 Inti (2 soal)

**Soal 1:** Sederhanakan `3² × 3⁴`

**Soal 2:** Hitung `log₃(81)`

### 🔴 Tantangan (1 soal, opsional)

**Soal:** Sebuah bakteri membelah diri setiap 30 menit. Mulai dari 1 bakteri, berapa banyak setelah 5 jam?

> 💡 **Hint 1:** 5 jam = 10 × 30 menit
> 💡 **Hint 2:** Setiap pembelahan = kali 2
> 💡 **Hint 3:** 2¹⁰ = ?

---

## Hari 6-8: Latihan Lanjutan

[Soal-soal campuran — lihat file exercises]

---

## Hari 9-10: Review

**Coba jawab tanpa melihat catatan:**
1. Apa arti `5³`?
2. Hitung `log₂(64)`
3. Sederhanakan `2⁵ ÷ 2²`
4. Kenapa `a⁰ = 1`?

---

## Hari 11: Ulangan

Buka file: `module-1.4-exam.md`

---

## Hari 12: Self-Correction

Buka file: `module-1.4-answer-key.md`

---

## Hari 13-14: Buffer

Pilih sesuai kebutuhan:
- **Opsi A** (remedial): Baca ulang lembar catatan, kerjakan ulang soal yang salah
- **Opsi B** (pengayaan): Coba soal 🔴 lagi, lihat preview Modul 1.5
- **Opsi C** (catch-up): Kerjakan latihan yang terlewat, isi jurnal
- **Opsi D** (istirahat): Tidak ada tugas. Istirahat.

---

## 🔗 Koneksi ke Topik Lain

- **Dipakai lagi di:** Fase 4 (ML — loss functions), Fase 5 (DL — activation functions)
- **Berdasarkan dari:** Modul 1.1 (perkalian)
