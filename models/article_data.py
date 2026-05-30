from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Chunk:
    """A chunk of a long document for section-by-section analysis."""
    section: str
    text: str
    index: int
    analysis_result: str | None = None


@dataclass
class StructuredArticleData:
    """Shared data model that all parsers produce and all workers consume."""
    metadata: dict[str, Any] = field(default_factory=dict)
    sections: dict[str, str] = field(default_factory=dict)
    methodology_type: str = "unknown"
    research_gap: str = ""
    key_findings: list[str] = field(default_factory=list)
    statistical_methods: list[str] = field(default_factory=list)
    chunks: list[Chunk] = field(default_factory=list)
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

    def add_chunks(self, chunks: list[Chunk]) -> None:
        """Add chunks for long document processing."""
        self.chunks = chunks
