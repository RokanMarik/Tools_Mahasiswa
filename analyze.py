#!/usr/bin/env python3
"""Journal Analysis System — Entry point wrapper.

Usage:
    python analyze.py jurnal.pdf --mode read
    python analyze.py jurnal.pdf --mode review
    python analyze.py jurnal.pdf --mode full
    python analyze.py --input-text "teks..." --mode review
"""

from journal_analyzer.analyze import main

if __name__ == "__main__":
    main()
