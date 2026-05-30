#!/usr/bin/env python3
"""CLI entry point for Zotero integration."""

import os
import sys
import importlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

JournalFinder = importlib.import_module("9router_journal_finder").JournalFinder
ZoteroClient = importlib.import_module("modules.zotero.client").ZoteroClient
CollectionPicker = importlib.import_module("modules.zotero.collection_picker").CollectionPicker


def get_api_key() -> str:
    """Get API key from env or prompt."""
    api_key = os.getenv("ZOTERO_API_KEY")
    if not api_key:
        print("Masukkan Zotero API key: ", end="")
        try:
            api_key = input().strip()
        except (EOFError, KeyboardInterrupt):
            print("\nDibatalkan.")
            sys.exit(0)
    return api_key


def menu_analyze(finder: JournalFinder, api_key: str):
    """Analyze a collection (existing feature)."""
    finder.pull_zotero(api_key=api_key)


def menu_create_collection(finder: JournalFinder, api_key: str):
    """Create a new collection."""
    print("\n=== Buat Koleksi Baru ===")
    print("Nama koleksi: ", end="")
    try:
        name = input().strip()
    except (EOFError, KeyboardInterrupt):
        print("\nDibatalkan.")
        return

    if not name:
        print("Nama tidak boleh kosong.")
        return

    # Optional: show existing collections for parent selection
    client = ZoteroClient(api_key=api_key)
    client.library_id = client.get_user_id()
    picker = CollectionPicker(client)
    print(picker.display_collections())
    print("\nParent collection (ketik nama atau Enter untuk top-level): ", end="")
    try:
        parent_input = input().strip()
    except (EOFError, KeyboardInterrupt):
        parent_input = ""

    parent_key = None
    if parent_input:
        selected = picker.select_by_name(parent_input)
        if selected:
            parent_key = selected["key"]
            print(f"Parent: {selected['name']}")
        else:
            print(f"Koleksi '{parent_input}' tidak ditemukan. Buat sebagai top-level.")

    try:
        result = finder.create_zotero_collection(api_key, name, parent_key)
        print(f"\nOK: Koleksi '{name}' berhasil dibuat!")
        print(f"  Key: {result['key']}")
    except Exception as e:
        print(f"\nError: {e}")


def menu_add_item(finder: JournalFinder, api_key: str):
    """Add an item to a collection."""
    print("\n=== Tambah Paper ke Koleksi ===")

    # Select collection
    client = ZoteroClient(api_key=api_key)
    client.library_id = client.get_user_id()
    picker = CollectionPicker(client)
    selected = picker.pick()
    if not selected:
        return

    print(f"\nKoleksi: {selected['name']}")
    print("\nJudul paper: ", end="")
    try:
        title = input().strip()
    except (EOFError, KeyboardInterrupt):
        print("\nDibatalkan.")
        return

    print("Penulis (pisah koma, misal: John Smith, Jane Doe): ", end="")
    try:
        authors_raw = input().strip()
    except (EOFError, KeyboardInterrupt):
        authors_raw = ""
    authors = [a.strip() for a in authors_raw.split(",") if a.strip()]

    print("Tahun: ", end="")
    try:
        date = input().strip()
    except (EOFError, KeyboardInterrupt):
        date = ""

    print("DOI (opsional): ", end="")
    try:
        doi = input().strip()
    except (EOFError, KeyboardInterrupt):
        doi = ""

    print("URL (opsional): ", end="")
    try:
        url = input().strip()
    except (EOFError, KeyboardInterrupt):
        url = ""

    print("Jurnal (opsional): ", end="")
    try:
        journal = input().strip()
    except (EOFError, KeyboardInterrupt):
        journal = ""

    item_data = {
        "title": title,
        "authors": authors,
        "date": date,
        "doi": doi,
        "url": url,
        "journal": journal,
        "itemType": "journalArticle",
    }

    try:
        result = finder.add_item_to_zotero_collection(api_key, selected["key"], item_data)
        print(f"\nOK: Paper '{title}' berhasil ditambahkan!")
        print(f"  Key: {result['key']}")
    except Exception as e:
        print(f"\nError: {e}")


def main():
    """Main CLI entry point."""
    print("=" * 60)
    print("  Zotero Library Tool")
    print("=" * 60)
    print()

    api_key = get_api_key()
    finder = JournalFinder()

    while True:
        print("\nPilih menu:")
        print("  1. Analisis koleksi")
        print("  2. Buat koleksi baru")
        print("  3. Tambah paper ke koleksi")
        print("  4. Keluar")
        print("\nPilih nomor [1-4]: ", end="")

        try:
            choice = input().strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if choice == "1":
            menu_analyze(finder, api_key)
        elif choice == "2":
            menu_create_collection(finder, api_key)
        elif choice == "3":
            menu_add_item(finder, api_key)
        elif choice == "4":
            print("Bye!")
            break
        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()
