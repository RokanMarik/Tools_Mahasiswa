# Smart Cleanup Tool — Design Spec

**Date:** 2026-01-28
**Status:** Draft — awaiting review

---

## 1. Overview

Smart Cleanup Tool adalah aplikasi TUI (Terminal UI) berbasis Python + Textual yang memindai laptop untuk file sampah (cache, downloads lama, duplikat, file besar tidak terpakai), menampilkan pro/kons per sub-kategori sebelum penghapusan, dan memberikan kontrol penuh kepada user untuk memilih mana yang dihapus.

### Prinsip Desain
- **Safety first** — tidak pernah hapus file penting tanpa konfirmasi ganda
- **Transparan** — user tahu persis apa yang akan dihapus dan konsekuensinya
- **Interaktif** — user bisa pilah-pilih, bukan "hapus semua" buta
- **Ringan** — TUI, bukan GUI berat, launch dari satu klik

---

## 2. Architecture

```
┌─────────────────────────────────────────────────┐
│                  TUI Layer (Textual)             │
│  ┌───────────┬──────────────────┬─────────────┐  │
│  │  Sidebar  │   Main Panel     │  Status Bar │  │
│  │ Kategori  │   Sub-kategori   │  Progress   │  │
│  │ + Checkbox│   + Pros/Cons    │  + Total GB │  │
│  └───────────┴──────────────────┴─────────────┘
└─────────────────────┬───────────────────────────┘
                      │ events (toggle, confirm)
┌─────────────────────▼───────────────────────────┐
│              Orchestrator Layer                  │
│  ┌────────────┐ ┌──────────┐ ┌───────────────┐  │
│  │ Scanner    │ │ Analyzer │ │ Deletion      │  │
│  │ Workers    │ │ Engine   │ │ Engine        │  │
│  │ (parallel) │ │ (size,   │ │ (recycle bin  │  │
│  │            │ │  dupes,  │ │  + force)     │  │
│  │            │ │  safety) │ │               │  │
│  └────────────┘ └──────────┘ └───────────────┘  │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────┐
│              Safety Layer                        │
│  • Whitelist (skip: Windows/, Program Files/)   │
│  • Blacklist (protect: .exe, .docx, .git/)      │
│  • Confirmation for anomalous files             │
└─────────────────────────────────────────────────┘
```

---

## 3. Components

### 3.1 Scanner Workers (Parallel)

| Worker | Target Paths | Output |
|---|---|---|
| `CacheScanner` | `AppData/Local/*/Cache`, `AppData/Local/Temp/`, `AppData/Local/Microsoft/Windows/Explorer/thumbcache_*.db` | `ScannedFile` list: path, size, app_name, type |
| `DownloadScanner` | `Downloads/`, custom user folders | `ScannedFile` list: path, size, last_accessed, age_days |
| `DuplicateScanner` | All scanned paths (post-scan) | `DuplicateGroup` list: hash, [files], total_wasted |
| `LargeFileScanner` | All scanned paths | `ScannedFile` list: path, size, last_accessed |

**Execution:** Workers berjalan paralel via `asyncio.gather()` atau `concurrent.futures.ThreadPoolExecutor`.

### 3.2 Analyzer Engine

Meng-enrich setiap `ScannedFile` dengan metadata:

```python
@dataclass
class AnalyzedFile:
    path: Path
    size: int
    size_human: str          # "1.2 GB"
    age_days: int
    age_human: str           # "3 months old"
    risk_level: str          # "safe" | "caution" | "danger"
    pros: list[str]          # ["Free up 500MB", "No functional impact"]
    cons: list[str]          # ["Browser login lost", "App startup slower"]
    safety_flag: str         # "allowed" | "blocked" | "confirm"
    is_duplicate: bool
    duplicate_group_id: str | None
```

**Rules:**
- `risk_level = "safe"` jika: temp files, cache, confirmed duplicates
- `risk_level = "caution"` jika: file di Downloads > 30 hari, file > 1GB
- `risk_level = "danger"` jika: sistem-adjacent, recently accessed (< 7 hari)
- `safety_flag = "blocked"` jika: di whitelist folder atau blacklist ekstensi

### 3.3 Safety Layer

**Whitelist (selalu skip, tidak pernah ditampilkan):**
- `C:\Windows\`
- `C:\Program Files\`, `C:\Program Files (x86)\`
- `AppData\Roaming\` (settings, bukan cache)
- `.git\` di manapun
- `node_modules\` di manapun
- File dengan ekstensi: `.exe`, `.dll`, `.sys`, `.msi`, `.lnk`

**Blacklist (ditampilkan tapi blocked by default):**
- File di `Desktop\` (user mungkin taruh file penting)
- File di `Documents\` yang `.docx`, `.xlsx`, `.pdf`
- File yang sedang di-lock oleh process lain

**Extra Confirmation:**
- File di folder "aman" tapi ukurannya > 500MB → flag "unusually large for this category, review carefully"
- File dengan `last_accessed < 7 days` → flag "recently used, possibly still needed"

### 3.4 Deletion Engine

```python
def delete_files(files: list[AnalyzedFile], mode: str):
    """
    mode = "recycle" → move to Recycle Bin (default)
    mode = "force"   → permanent delete (os.remove)
    """
```

**Default behavior:** Pindah ke Recycle Bin via `send2trash` library.
**Force option:** Untuk kategori yang user yakin (Temp Files, Thumbnails), user bisa pilih "Force Delete" untuk skip Recycle Bin.
**Fallback:** Jika Recycle Bin penuh → prompt user: "Recycle Bin penuh. Force delete atau batalkan?"

---

## 4. TUI Screens (Textual)

### Screen 1: CONFIG
- Pilih scope: default user folders (`Downloads`, `Desktop`, `AppData\Local`) + tombol "Add Folder"
- Pilih kategori yang di-scan: toggle checkbox per kategori
- Tombol "Start Scan"

### Screen 2: SCANNING
- Progress bar per worker (4 bars)
- Live counter: "Found 2,340 files (4.7 GB)"
- Animasi spinner
- Tombol "Cancel" (graceful stop)

### Screen 3: REVIEW (main screen)

```
┌─ Kategori ───────┬─ Sub-kategori ──────────┬─ Pros/Cons ─────────────────────┐
│ ☑ Cache  (2.3GB) │  ☑ Browser Cache 1.2GB  │ ✓ Free up 1.2GB                 │
│ ☐ Downloads      │  ☑ Temp Files    800MB  │ ✗ Websites reload, login lost   │
│ ☑ Duplicates     │  ☑ Thumbnails    300MB  │                                 │
│                  │                         │                                 │
│                  │                         │                                 │
└──────────────────┴─────────────────────────┴─────────────────────────────────┘

Total selected: 1.5 GB  |  [Space] toggle  [Enter] drill-down  [F2] Execute
```

**Interaksi:**
- `Space` / `Click` → toggle checkbox
- `Enter` → drill-down ke sub-kategori (expand/collapse)
- `Tab` → navigate antar panel
- `F2` → execute deletion
- `Esc` → back / cancel

### Screen 4: EXECUTION
- Progress bar: "Deleting 234 files (1.5 GB)..."
- Per-file status: ✓ / ⚠ / ✗
- Tombol "Cancel" (stop, yang sudah terhapus tetap terhapus)

### Screen 5: RESULT
- Summary: "Deleted 1.5 GB to Recycle Bin. Skipped 23 files (protected)."
- Breakdown per kategori
- Tombol "View Log" (buka log file) / "Exit"

---

## 5. Error Handling

| Scenario | Behavior |
|---|---|
| Permission denied | Skip, catat log, tampilkan di summary |
| File locked | Skip, catat, tampilkan di summary |
| Scanner crash | Isolasi error, lanjut folder lain, log warning |
| Recycle Bin penuh | Fallback ke force delete dengan konfirmasi |
| User interrupt (Ctrl+C) | Graceful stop, tampilkan partial results |
| No files found | Pesan: "Tidak ada junk files ditemukan." |
| Whitelisted file forced | Konfirmasi ganda: "⚠️ File di folder protected. Yakin?" |
| Duplicate di folder penting | Hanya tampilkan duplicate di folder aman |
| File besar masih aktif | Flag "possibly active, review carefully" |

---

## 6. Data Structures

```python
@dataclass
class ScannedFile:
    path: Path
    size: int
    last_modified: datetime
    last_accessed: datetime | None
    category: str          # "cache" | "download" | "duplicate" | "large"
    subcategory: str       # "browser_cache" | "temp" | "thumbnails" | ...

@dataclass
class DuplicateGroup:
    file_hash: str
    files: list[ScannedFile]
    keep_index: int        # which file to keep (first by default)
    wasted_bytes: int

@dataclass
class ScanResult:
    files: list[AnalyzedFile]
    duplicate_groups: list[DuplicateGroup]
    total_size: int
    total_files: int
    scan_duration: float
    errors: list[str]

@dataclass
class CategoryInfo:
    name: str
    icon: str
    subcategories: list[str]
    default_pros: list[str]
    default_cons: list[str]
```

---

## 7. File Structure

```
smart_cleanup/
├── cleanup.bat                    # One-click launcher
├── cleanup.py                     # Entry point (textual app, run: python cleanup.py)
├── pyproject.toml                 # Dependencies: textual, send2trash
│
├── core/
│   ├── __init__.py
│   ├── models.py                  # Data structures
│   ├── scanner.py                 # Scanner orchestrator
│   ├── analyzer.py                # Pros/cons engine
│   ├── safety.py                  # Whitelist/blacklist
│   └── deletion.py                # Recycle bin + force delete
│
├── scanners/
│   ├── __init__.py
│   ├── cache_scanner.py
│   ├── download_scanner.py
│   ├── duplicate_scanner.py
│   └── large_file_scanner.py
│
├── ui/
│   ├── __init__.py
│   ├── app.py                     # Main Textual App
│   ├── config_screen.py           # Screen 1
│   ├── scanning_screen.py         # Screen 2
│   ├── review_screen.py           # Screen 3 (main)
│   ├── execution_screen.py        # Screen 4
│   └── result_screen.py           # Screen 5
│
└── tests/
    ├── test_scanners.py
    ├── test_analyzer.py
    ├── test_safety.py
    └── test_deletion.py
```

---

## 8. Dependencies

```
textual>=2.0.0          # TUI framework
send2trash>=1.8.0       # Recycle Bin integration
rich>=13.0.0            # Already pulled by textual, for console helpers
```

---

## 9. One-Click Launcher (`cleanup.bat`)

```bat
@echo off
cd /d "%~dp0"
python cleanup.py
pause
```

User double-click → terminal buka → TUI langsung muncul.

---

## 10. Testing Strategy

- **Unit tests:** Setiap scanner worker dengan mock filesystem
- **Integration tests:** Scanner → Analyzer → Safety pipeline
- **Safety tests:** Verifikasi whitelist/blacklist tidak bisa di-bypass
- **UI tests:** Manual testing (Textual punya `textual run --dev` untuk debug mode)
