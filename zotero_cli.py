#!/usr/bin/env python3
"""CLI entry point for Zotero integration."""

import os
import sys
import importlib

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import using importlib since module name starts with digit
JournalFinder = importlib.import_module("9router_journal_finder").JournalFinder


def main():
    """Main CLI entry point."""
    print("=" * 60)
    print("  Zotero Library Analyzer")
    print("=" * 60)
    print()

    finder = JournalFinder()

    # Check for API key
    api_key = os.getenv("ZOTERO_API_KEY")
    if not api_key:
        print("ZOTERO_API_KEY belum diset.")
        print("Set dengan: $env:ZOTERO_API_KEY='your-key' (PowerShell)")
        print("Atau: export ZOTERO_API_KEY='your-key' (Linux/Mac)")
        print()
        print("Atau masukkan langsung di bawah:")
        print("Masukkan Zotero API key: ", end="")
        try:
            api_key = input().strip()
        except (EOFError, KeyboardInterrupt):
            print("\nDibatalkan.")
            sys.exit(0)

    # Run analysis
    finder.pull_zotero(api_key=api_key if api_key else None)


if __name__ == "__main__":
    main()
