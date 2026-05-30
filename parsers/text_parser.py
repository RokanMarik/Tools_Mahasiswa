import re
from models.article_data import StructuredArticleData


class TextParser:
    """Parse plain text or markdown input into StructuredArticleData.

    Detects sections from markdown-style headings (## HEADING).
    """

    SECTION_PATTERNS = {
        r"(?i)##\s*abstract\s*$": "abstract",
        r"(?i)##\s*introduction\s*$": "introduction",
        r"(?i)##\s*(literature\s*review|related\s*work)\s*$": "literature_review",
        r"(?i)##\s*(methodology|methods)\s*$": "methodology",
        r"(?i)##\s*(results?|findings)\s*$": "results",
        r"(?i)##\s*discussion\s*$": "discussion",
        r"(?i)##\s*conclusion\s*$": "conclusion",
        r"(?i)##\s*(references|bibliography)\s*$": "references",
    }

    def parse(self, text: str) -> StructuredArticleData:
        """Parse text into StructuredArticleData."""
        article = StructuredArticleData(
            metadata={"source_type": "text"},
            raw_text=text,
        )

        article.sections = self._detect_sections(text)

        if len(text.split()) < 500:
            article.metadata["warning"] = "Teks terlalu pendek untuk analisis meaningful"

        return article

    def _detect_sections(self, text: str) -> dict[str, str]:
        """Detect sections from markdown headings."""
        lines = text.split("\n")
        sections = {}
        current_section = None
        current_text = []

        for line in lines:
            matched = False
            for pattern, name in self.SECTION_PATTERNS.items():
                if re.match(pattern, line.strip()):
                    if current_section is not None:
                        sections[current_section] = "\n".join(current_text).strip()
                    current_section = name
                    current_text = []
                    matched = True
                    break
            if not matched:
                current_text.append(line)

        if current_section is not None:
            sections[current_section] = "\n".join(current_text).strip()

        if not sections:
            sections["full_text"] = text.strip()

        return sections
