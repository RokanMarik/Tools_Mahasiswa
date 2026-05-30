# Modul 1.5: Statistika Deskriptif

> **Fase:** 1 — Math Foundation
> **Durasi:** 2 minggu (Hari 1-14)
> **Prerequisite:** Modul 1.1 (Angka & Operasi Dasar)
> **Preview:** Modul 1.6: Varians & Distribusi Normal

---

## 📋 Target Pembelajaran

Setelah menyelesaikan modul ini, kamu bisa:
1. Menghitung mean (rata-rata) dari sekumpulan data
2. Menentukan median (nilai tengah)
3. Menentukan modus (nilai paling sering muncul)
4. Menghitung range (jangkauan)
5. Memilih ukuran pemusatan yang tepat untuk data tertentu

---

## Hari 1-2: Teori + Contoh

### HOOK

Tidak perlu sempurna hari ini. Mari kita pelan-pelan.

Pernah lihat nilai rata-rata di rapor? Itu statistika! Setiap hari kamu pakai statistika tanpa sadar — rata-rata harga, rata-rata waktu tempuh, rata-rata nilai.

### CONCEPT

**Apa itu Statistika Deskriptif?**

Statistika deskriptif = cara menggambarkan data dengan angka ringkasan.

Dari sekumpulan angka, kita cari:
- **Mean** = rata-rata
- **Median** = nilai tengah
- **Modus** = yang paling sering muncul
- **Range** = selisih terbesar dan terkecil

**Mean (Rata-rata):**

Mean = jumlah semua data ÷ banyak data

Contoh: Data nilai = {7, 8, 6, 9, 5}

```
Mean = (7 + 8 + 6 + 9 + 5) ÷ 5
     = 35 ÷ 5
     = 7
```

💡 Mean = "nilai yang seimbang" — kalau semua nilai diganti mean, jumlahnya tetap sama.

**Median (Nilai Tengah):**

Median = nilai yang ada di TENGAH setelah data diurutkan.

Contoh: Data = {7, 8, 6, 9, 5}

```
Langkah 1: Urutkan → {5, 6, 7, 8, 9}
Langkah 2: Cari tengah → 7 (ada di posisi ke-3 dari 5)

Median = 7
```

Jika data GENAP (contoh: {5, 6, 7, 8, 9, 10}):

```
Urutkan: {5, 6, 7, 8, 9, 10}
Tengah: ada 2 nilai → 7 dan 8
Median = (7 + 8) ÷ 2 = 7,5
```

**Modus (Nilai Paling Sering):**

Modus = nilai yang PALING SERING muncul.

Contoh:
- {3, 5, 5, 7, 8} → Modus = 5 (muncul 2 kali)
- {2, 3, 4, 5} → Tidak ada modus (semua muncul 1 kali)
- {1, 2, 2, 3, 3} → Dua modus: 2 dan 3 (bimodal)

**Range (Jangkauan):**

Range = nilai terbesar − nilai terkecil

Contoh: {5, 6, 7, 8, 9}

```
Range = 9 − 5 = 4
```

💡 Range memberi tahu seberapa "melebar" data.

**Kapan Pakai yang Mana?**

| Ukuran | Kapan Dipakai |
|--------|--------------|
| Mean | Data normal, tidak ada outlier |
| Median | Ada outlier (nilai ekstrem) |
| Modus | Data kategorikal (misal: warna favorit) |
| Range | Lihat sebaran data secara cepat |

💡 **Kenapa ini penting untuk AI?**
- Data preprocessing: pahami data sebelum train model
- Outlier detection: nilai ekstrem bisa merusak model
- Feature analysis: pilih fitur yang informatif

### WORKED EXAMPLE

**Soal 1:** Data tinggi badan (cm): {150, 155, 160, 155, 170, 155, 165}

Hitung mean, median, modus, range.

**Penyelesaian:**

```
Mean: (150+155+160+155+170+155+165) ÷ 7
    = 1110 ÷ 7
    = 158,57 cm

Median: Urutkan → {150, 155, 155, 155, 160, 165, 170}
        Tengah (posisi ke-4) = 155

Modus: 155 (muncul 3 kali, paling sering)

Range: 170 − 150 = 20 cm
```

---

**Soal 2:** Gaji karyawan (juta): {5, 6, 5, 50, 6, 5, 7}

Hitung mean dan median. Mana yang lebih mewakili?

**Penyelesaian:**

```
Mean: (5+6+5+50+6+5+7) ÷ 7 = 84 ÷ 7 = 12 juta

Median: Urutkan → {5, 5, 5, 6, 6, 7, 50}
        Tengah = 6 juta

Analisis: Mean (12 juta) jauh lebih tinggi karena ada outlier (50 juta).
Median (6 juta) lebih mewakili gaji "typical" karyawan.
→ Median LEBIH BAIK untuk data ini.
```

---

## Hari 3-5: Latihan Harian

### 🟢 Pemanasan (3 soal)

**Soal 1:** Data: {4, 6, 8, 10, 12}. Hitung mean.

**Soal 2:** Data: {3, 7, 1, 9, 5}. Cari median.

**Soal 3:** Data: {2, 5, 5, 8, 5, 3}. Cari modus.

### 🟡 Inti (2 soal)

**Soal 1:** Data ujian: {75, 80, 65, 90, 85, 70, 80, 75}. Hitung mean, median, modus, range.

**Soal 2:** Data: {12, 15, 12, 18, 12, 20, 15}. Hitung semua ukuran pemusatan.

### 🔴 Tantangan (1 soal, opsional)

**Soal:** Toko sepatu punya data ukuran terjual: {38, 39, 40, 39, 41, 39, 40, 42, 39, 40}
a) Hitung mean, median, modus.
b) Ukuran sepatu mana yang paling banyak terjual?
c) Jika toko mau restock, ukuran mana yang harus diperbanyak? Kenapa?

> 💡 **Hint 1:** Urutkan data dulu
> 💡 **Hint 2:** Modus = ukuran paling sering
> 💡 **Hint 3:** Modus lebih berguna dari mean untuk data kategorikal

---

## Hari 6-8: Latihan Lanjutan

[Soal-soal campuran — lihat file exercises]

---

## Hari 9-10: Review

**Coba jawab tanpa melihat catatan:**
1. Apa beda mean dan median?
2. Data: {10, 20, 30, 40, 50}. Hitung mean dan median.
3. Kapan median lebih baik dari mean?
4. Apa itu modus?

---

## Hari 11: Ulangan

Buka file: `module-1.5-exam.md`

---

## Hari 12: Self-Correction

Buka file: `module-1.5-answer-key.md`

---

## Hari 13-14: Buffer

Pilih sesuai kebutuhan.

---

## 🔗 Koneksi ke Topik Lain

- **Dipakai lagi di:** Modul 1.6 (Varians & Distribusi Normal), Fase 3 (Data Science — EDA)
- **Berdasarkan dari:** Modul 1.1 (operasi dasar: tambah, bagi)
