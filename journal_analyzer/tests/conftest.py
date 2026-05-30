import sys
import os

# Add journal_analyzer/ to Python path so tests can import
# `from models.article_data import ...` instead of `from journal_analyzer.models...`
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
