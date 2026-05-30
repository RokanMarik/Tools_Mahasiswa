---
name: journal-help
description: Show cheat sheet for journal finder commands. Use when user types ?, /help, or asks for help.
---

# Journal Help — Cheat Sheet

Show this when user types `?`, `/help`, "bantuan", or asks what commands are available.

## Cheat Sheet

```
📚 Journal Finder — Perintah Tersedia

Cari Jurnal:
  "cari jurnal [topik]"          → Cari 3-5 paper (mode cepat)
  "cari jurnal lengkap [topik]"  → Cari + analisis + report

Simpan ke Zotero:
  "simpan [nomor/judul]"         → Simpan paper ke Zotero
  "simpan semua"                 → Simpan semua hasil pencarian

Citation:
  "citation [nomor/judul]"       → Generate APA citation
  "citation semua"               → Citation semua paper yang dipilih

Lainnya:
  "analisis paper [judul/link]"  → AI analisis paper
  "cari lagi [topik]"            → Pencarian baru
  "?" atau "/help"               → Tampilkan contekannya ini

Tips:
  - Gak perlu hafal, tinggal ngomong aja
  - AI bakal tanya kalau butuh klarifikasi
```

## When to Show

- User explicitly types `?`, `/help`, "bantuan", "help"
- User seems confused or asks "bisa apa aja?"
- First time user interacts with journal-related commands (optional welcome hint)

## How to Show

Display the cheat sheet as a code block. Keep it concise — don't add extra explanation unless user asks.
