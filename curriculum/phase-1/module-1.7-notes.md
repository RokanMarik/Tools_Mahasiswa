# Lembar Catatan — Modul 1.7: Peluang Dasar

> **Fase:** 1 | **Minggu:** 13-14 | **Hari:** 1-14

---

## 1. RINGKASAN KONSEP

Peluang = ukuran kemungkinan kejadian. Nilai 0 (mustahil) sampai 1 (pasti).

Rumus: P(A) = hasil menguntungkan ÷ semua hasil mungkin.

Komplemen: P(tidak A) = 1 − P(A).
AND (independen): P(A DAN B) = P(A) × P(B).
OR (saling lepas): P(A ATAU B) = P(A) + P(B).
OR (overlap): P(A ATAU B) = P(A) + P(B) − P(A DAN B).

---

## 2. RUMUS PENTING

- **Peluang dasar:** `P(A) = n(A) ÷ n(S)`
- **Komplemen:** `P(tidak A) = 1 − P(A)`
- **AND (independen):** `P(A DAN B) = P(A) × P(B)`
- **OR (saling lepas):** `P(A ATAU B) = P(A) + P(B)`
- **OR (umum):** `P(A ATAU B) = P(A) + P(B) − P(A DAN B)`
- **Tanpa pengembalian:** total berkurang setelah pengambilan pertama

---

## 3. ANALOGI KUNCI

"Peluang itu seperti ramalan cuaca. 70% hujan = dari 10 hari dengan kondisi sama, 7 hari hujan."

"Komplemen itu seperti koin: kalau bukan gambar, pasti angka. P(gambar) + P(angka) = 1."

---

## 4. CONTOH KERJA

**Soal:** Lempar 2 dadu. P(jumlah = 7)?

**Jawaban:**
1. Total hasil = 6 × 6 = 36
2. Hasil jumlah 7: (1,6),(2,5),(3,4),(4,3),(5,2),(6,1) = 6
3. P = 6/36 = 1/6 ≈ 16,7%

---

## 5. KESALAHAN UMUM

⚠️ P(A ATAU B) = P(A)+P(B) selalu (salah jika overlap) → kurangi P(A DAN B)
⚠️ Tanpa pengembalian: lupa kurangi total → total berkurang setelah ambil
⚠️ P(genap ATAU prima) = 3/6+3/6 (salah, 2 overlap) → kurangi 1/6

---

## 6. KONEKSI KE TOPIK LAIN

→ Dipakai lagi di: Fase 4 (Naive Bayes), Fase 5 (NLP)
→ Berdasarkan dari: Modul 1.1 (pecahan), Modul 1.5 (statistika)

---

## 7. CHECKLIST PEMAHAMAN

- [ ] Saya bisa hitung peluang sederhana
- [ ] Saya bisa hitung komplemen
- [ ] Saya bisa hitung P(A DAN B) dan P(A ATAU B)
- [ ] Saya paham beda dengan dan tanpa pengembalian
- [ ] Saya tahu kenapa peluang penting untuk AI
- [ ] Saya tahu apa yang belum saya pahami
