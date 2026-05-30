# Lembar Catatan — Modul 1.4: Eksponen & Logaritma

> **Fase:** 1 | **Minggu:** 7-8 | **Hari:** 1-14

---

## 1. RINGKASAN KONSEP

Eksponen = perkalian berulang. `aⁿ` artinya a dikalikan n kali.

Logaritma = kebalikan eksponen. `logₐ(c) = b` artinya aᵇ = c.

Keduanya saling terkait dan sangat penting di AI: loss functions, probability, scaling data.

---

## 2. RUMUS PENTING

- **Eksponen:** `aⁿ = a × a × ... × a` (n kali)
- **Aturan kali:** `aᵐ × aⁿ = aᵐ⁺ⁿ`
- **Aturan bagi:** `aᵐ ÷ aⁿ = aᵐ⁻ⁿ`
- **Aturan pangkat:** `(aᵐ)ⁿ = aᵐˣⁿ`
- **Pangkat 0:** `a⁰ = 1`
- **Pangkat negatif:** `a⁻ⁿ = 1/aⁿ`
- **Logaritma:** `logₐ(c) = b` ↔ `aᵇ = c`

---

## 3. ANALOGI KUNCI

"Eksponen itu seperti mesin fotokopi: 1 dokumen jadi 2, 2 jadi 4, 4 jadi 8... berkembang cepat!"

"Logaritma itu seperti pertanyaan: 'perlu berapa kali lipat supaya dapat angka ini?'"

---

## 4. CONTOH KERJA

**Soal:** Hitung `log₂(64)` dan sederhanakan `2⁴ × 2³`

**Jawaban:**
1. log₂(64): 2⁶ = 64 → log₂(64) = 6
2. 2⁴ × 2³ = 2⁷ = 128

---

## 5. KESALAHAN UMUM

⚠️ `2³ × 2² = 4⁵` (salah, basis harus sama) → Koreksi: 2⁵ = 32
⚠️ `log₂(8) = 2` (salah) → Koreksi: 2³ = 8, jadi log₂(8) = 3
⚠️ `2⁻² = −4` (salah) → Koreksi: 2⁻² = 1/4

---

## 6. KONEKSI KE TOPIK LAIN

→ Dipakai lagi di: Fase 4 (ML loss functions), Fase 5 (DL activation functions)
→ Berdasarkan dari: Modul 1.1 (perkalian)

---

## 7. CHECKLIST PEMAHAMAN

- [ ] Saya bisa hitung eksponen sederhana
- [ ] Saya tahu aturan eksponen
- [ ] Saya bisa hitung logaritma sederhana
- [ ] Saya paham hubungan eksponen ↔ logaritma
- [ ] Saya tahu kenapa ini penting untuk AI
- [ ] Saya tahu apa yang belum saya pahami
