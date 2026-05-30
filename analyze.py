#!/usr/bin/env python3
"""Journal Analysis System — Entry point wrapper.

Usage:
    python analyze.py jurnal.pdf --mode read
    python analyze.py jurnal.pdf --mode review
    python analyze.py jurnal.pdf --mode full
    python analyze.py jurnal.pdf --mode gap
    python analyze.py --input-text "teks..." --mode review
    python analyze.py --research-question "Pertanyaan riset" --dataset data.csv --mode data-analysis
"""

from journal_analyzer.analyze import main

if __name__ == "__main__":
    main()
