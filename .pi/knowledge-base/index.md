# Tools Mahasiswa - Project Index

## Overview
Repo: RokanMarik/Tools_Mahasiswa
Branch: feature/zotero-integration
Latest commit: 0ed0778
Tests: 73 passed, 0 failed
Rating: 5/5

## Purpose
Alat bantu cari jurnal ilmiah. Mahasiswa bisa cari artikel, liat jumlah sitasi, tahun terbit, simpan ke Zotero, dan export ke berbagai format.

## Cara Pakai
- python main.py search "query" -> cari jurnal
- python main.py search "query" --sort citations -> urutkan paling banyak disitasi
- python main.py search "query" --sort year -> urutkan terbaru
- python main.py search "query" --balanced -> campuran jurnal terkenal + terbaru
- python main.py search "query" --year-from 2024 -> filter tahun
- python main.py citation --papers JSON --style apa -> buat sitasi
- python main.py export --papers JSON --format bibtex -> export

## Sumber Data
- Crossref: API gratis, DOI-based, ada jumlah sitasi (working)
- Semantic Scholar: API gratis, ada jumlah sitasi (rate-limited)
- Garuda: Jurnal Indonesia (placeholder)

## Struktur File
main.py -> entry point CLI
modules/search/engine.py -> mesin pencarian utama
modules/search/crossref.py -> client Crossref API
modules/search/semantic_scholar.py -> client Semantic Scholar API
modules/export/csv_export.py -> export CSV
modules/export/bibtex_export.py -> export BibTeX
modules/export/ris_export.py -> export RIS
modules/ui/display.py -> tampilan terminal
modules/zotero/ -> integrasi Zotero (client, citation formatter, collection picker)

## Plugin yang Setup
- pi-subagents: sub-AI paralel
- pi-web-access: akses internet
- pi-lens: auto-index file
- context-mode: memory permanen
- pi-hermes-memory: auto-save keputusan
- pi-permission-system: kontrol akses
- rpiv-todo: tracking tugas
- Semua config ada di .pi/config/

## Hasil Pencarian Contoh
Query: "flipped classroom" -> 7 artikel ditemukan dari Crossref
- Top sitasi: "Introduction to the Flipped Classroom" (17x, 2017)
- Terbaru: "Flipped Classroom Based Learning Management at PAUD" (2024, jurnal Indonesia)
