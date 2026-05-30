from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Chunk:
    """A chunk of a long document for section-by-section analysis."""
    section: str
    text: str
    index: int
    analysis_result: Optional[str] = None


@dataclass
class StructuredArticleData:
    """Shared data model that all parsers produce and all workers consume."""
    metadata: dict = field(default_factory=dict)
    sections: dict = field(default_factory=dict)
    methodology_type: str = "unknown"
    research_gap: str = ""
    key_findings: list = field(default_factory=list)
    statistical_methods: list = field(default_factory=list)
    chunks: list = field(default_factory=list)
    raw_text: str = ""

    def get_section(self, name: str) -> str:
        """Get a section by name. Returns empty string if not found."""
        return self.sections.get(name, "")

    def get_full_text(self) -> str:
        """Concatenate all sections with headers."""
        parts = []
        for section_name, content in self.sections.items():
            parts.append(f"## {section_name.upper()}\n\n{content}")
        return "\n\n".join(parts)

    @property
    def word_count(self) -> int:
        """Count total words across all sections."""
        return sum(len(text.split()) for text in self.sections.values())

    def add_chunks(self, chunks: list) -> None:
        """Add chunks for long document processing."""
        self.chunks = chunks
