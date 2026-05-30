import os
import re
from models.article_data import StructuredArticleData


class PDFParser:
    """Extract text and structure from PDF files.

    Uses pymupdf (fitz) for text extraction.
    """

    def __init__(self):
        self._fitz = None

    def _get_fitz(self):
        """Lazy import fitz to avoid import error if pymupdf not installed."""
        if self._fitz is None:
            try:
                import fitz
                self._fitz = fitz
            except ImportError:
                raise ImportError(
                    "pymupdf is required for PDF parsing. Install: pip install pymupdf"
                )
        return self._fitz

    def parse(self, file_path: str) -> StructuredArticleData:
        """Parse a PDF file into StructuredArticleData."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        fitz = self._get_fitz()
        doc = fitz.open(file_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()

        article = StructuredArticleData(
            metadata={"source_file": file_path, "source_type": "pdf"},
            raw_text=full_text,
        )

        # Basic section detection from headings
        article.sections = self._detect_sections(full_text)
        return article

    def _detect_sections(self, text: str) -> dict[str, str]:
        """Detect sections from common academic paper headings."""
        section_patterns = [
            r"(?i)^abstract\s*$",
            r"(?i)^introduction\s*$",
            r"(?i)^(literature\s*review|related\s*work)\s*$",
            r"(?i)^(methodology|methods|materials?\s*and\s*methods)\s*$",
            r"(?i)^(results?|findings)\s*$",
            r"(?i)^discussion\s*$",
            r"(?i)^conclusion\s*$",
            r"(?i)^(references|bibliography)\s*$",
        ]
        section_names = [
            "abstract", "introduction", "literature_review",
            "methodology", "results", "discussion", "conclusion", "references",
        ]

        sections = {}
        lines = text.split("\n")
        current_section = None
        current_text = []

        for line in lines:
            matched = False
            for i, pattern in enumerate(section_patterns):
                if re.match(pattern, line.strip()):
                    if current_section is not None:
                        sections[current_section] = "\n".join(current_text).strip()
                    current_section = section_names[i]
                    current_text = []
                    matched = True
                    break
            if not matched:
                current_text.append(line)

        if current_section is not None:
            sections[current_section] = "\n".join(current_text).strip()

        # If no sections detected, put everything in raw_text fallback
        if not sections:
            sections["full_text"] = text.strip()

        return sections
