# Modul 1.7: Peluang Dasar

> **Fase:** 1 — Math Foundation
> **Durasi:** 2 minggu (Hari 1-14)
> **Prerequisite:** Modul 1.1 (Angka & Operasi), Modul 1.5 (Statistika Deskriptif)
> **Preview:** Ulangan Besar Fase 1

---

## 📋 Target Pembelajaran

Setelah menyelesaikan modul ini, kamu bisa:
1. Memahami konsep peluang (probability)
2. Menghitung peluang kejadian sederhana
3. Memahami peluang komplemen
4. Menghitung peluang gabungan (AND, OR)
5. Memahami peluang bersyarat dasar

---

## Hari 1-2: Teori + Contoh

### HOOK

Tidak perlu sempurna hari ini. Mari kita pelan-pelan.

Pernah lempar koin? "Kemungkinan muncul gambar" — itu peluang! Setiap hari kamu pakai konsep peluang: "kemungkinan hujan", "peluang menang lotre", "berapa persen kemungkinan..."

### CONCEPT

**Apa itu Peluang?**

Peluang = ukuran seberapa mungkin suatu kejadian terjadi.

Nilai peluang: antara 0 dan 1 (atau 0% sampai 100%).

- **0** = mustahil (tidak pernah terjadi)
- **1** = pasti (selalu terjadi)
- **0,5** = 50% (sama kemungkinan terjadi atau tidak)

**Rumus Dasar:**

`P(A) = jumlah hasil yang menguntungkan ÷ jumlah semua hasil yang mungkin`

**Contoh 1:** Lempar koin. Peluang muncul GAMBAR?

```
Hasil yang mungkin: {Angka, Gambar} = 2 hasil
Hasil menguntungkan: {Gambar} = 1 hasil

P(Gambar) = 1 ÷ 2 = 0,5 = 50%
```

**Contoh 2:** Lempar dadu. Peluang muncul angka GENAP?

```
Hasil yang mungkin: {1, 2, 3, 4, 5, 6} = 6 hasil
Hasil menguntungkan (genap): {2, 4, 6} = 3 hasil

P(Genap) = 3 ÷ 6 = 0,5 = 50%
```

**Contoh 3:** Ambil kartu dari deck (52 kartu). Peluang dapat AS?

```
Hasil yang mungkin: 52 kartu
Hasil menguntungkan (AS): 4 kartu (AS♠, AS♥, AS♦, AS♣)

P(AS) = 4 ÷ 52 = 1/13 ≈ 0,077 = 7,7%
```

**Peluang Komplemen:**

Komplemen = "KEBALIKAN" dari kejadian.

`P(tidak A) = 1 − P(A)`

Contoh: P(muncul 6 pada dadu) = 1/6
P(tidak muncul 6) = 1 − 1/6 = 5/6

**Peluang Gabungan (OR):**

"P(A ATAU B)" = P(A) + P(B) − P(A DAN B)

Jika A dan B SALING LEPAS (tidak bisa terjadi bersamaan):
`P(A ATAU B) = P(A) + P(B)`

Contoh: P(genap ATAU 3) pada dadu:
- P(genap) = 3/6
- P(3) = 1/6
- Tidak overlap → P = 3/6 + 1/6 = 4/6 = 2/3

**Peluang Gabungan (AND):**

"P(A DAN B)" = P(A) × P(B) (jika kejadian INDEPENDEN)

Contoh: Lempar 2 koin. P(kedua-duanya gambar)?
- P(koin 1 gambar) = 1/2
- P(koin 2 gambar) = 1/2
- P(keduanya gambar) = 1/2 × 1/2 = 1/4 = 25%

**Peluang Bersyarat:**

`P(A | B)` = peluang A terjadi, DIKETAHUI B sudah terjadi.

`P(A | B) = P(A DAN B) ÷ P(B)`

Contoh: Dadu. Peluang muncul 6, DIKETAHUI hasilnya genap?
- P(6 DAN genap) = P(6) = 1/6
- P(genap) = 3/6 = 1/2
- P(6 | genap) = (1/6) ÷ (1/2) = 1/3

💡 **Kenapa ini penting untuk AI?**
- Naive Bayes classifier = berdasarkan teorema Bayes
- Model evaluation = accuracy, precision, recall = konsep peluang
- A/B testing = berdasarkan peluang statistik
- LLM = output = distribusi peluang atas kata-kata

### WORKED EXAMPLE

**Soal 1:** Sebuah tas berisi 3 bola merah, 2 bola biru, 5 bola hijau. Ambil 1 bola acak.
a) P(merah)? b) P(bukan hijau)? c) P(merah ATAU biru)?

**Penyelesaian:**

```
Total bola = 3 + 2 + 5 = 10

a) P(merah) = 3/10 = 0,3 = 30%

b) P(bukan hijau) = 1 − P(hijau) = 1 − 5/10 = 5/10 = 0,5 = 50%
   ATAU: P(bukan hijau) = (3+2)/10 = 5/10 = 0,5

c) P(merah ATAU biru) = P(merah) + P(biru) = 3/10 + 2/10 = 5/10 = 0,5
```

---

**Soal 2:** Lempar 2 dadu. Peluang JUMLAH = 7?

**Penyelesaian:**

```
Total hasil: 6 × 6 = 36

Hasil yang jumlahnya 7:
(1,6), (2,5), (3,4), (4,3), (5,2), (6,1) = 6 hasil

P(jumlah = 7) = 6/36 = 1/6 ≈ 16,7%
```

---

## Hari 3-5: Latihan Harian

### 🟢 Pemanasan (3 soal)

**Soal 1:** Lempar dadu. P(muncul 3)?

**Soal 2:** Lempar koin. P(Angka)?

**Soal 3:** Dari 52 kartu, P(kartu merah)?

### 🟡 Inti (2 soal)

**Soal 1:** Tas: 4 bola kuning, 6 bola putih. Ambil 1 bola. P(kuning), P(bukan putih), P(kuning ATAU putih).

**Soal 2:** Lempar 2 koin. P(paling sedikit 1 gambar)?

### 🔴 Tantangan (1 soal, opsional)

**Soal:** Dadu dilempar 2 kali. Peluang:
a) Kedua kali muncul angka yang sama?
b) Jumlah keduanya > 9?
c) Pertama genap DAN kedua ganjil?

> 💡 **Hint 1:** Total hasil = 6 × 6 = 36
> 💡 **Hint 2:** a) (1,1), (2,2), ..., (6,6) = 6 hasil
> 💡 **Hint 3:** b) Jumlah > 9: (4,6),(5,5),(5,6),(6,4),(6,5),(6,6) = 6 hasil

---

## Hari 6-8: Latihan Lanjutan

[Soal-soal campuran — lihat file exercises]

---

## Hari 9-10: Review

**Coba jawab tanpa melihat catatan:**
1. Apa rumus dasar peluang?
2. P(muncul 4 pada dadu)?
3. P(tidak muncul 5 pada dadu)?
4. Lempar 2 koin. P(kedua-duanya angka)?

---

## Hari 11: Ulangan

Buka file: `module-1.7-exam.md`

---

## Hari 12: Self-Correction

Buka file: `module-1.7-answer-key.md`

---

## Hari 13-14: Buffer

Pilih sesuai kebutuhan.

---

## 🔗 Koneksi ke Topik Lain

- **Dipakai lagi di:** Fase 4 (Naive Bayes, Model Evaluation), Fase 5 (NLP — distribusi kata)
- **Berdasarkan dari:** Modul 1.1 (pecahan, pembagian), Modul 1.5 (statistika)
