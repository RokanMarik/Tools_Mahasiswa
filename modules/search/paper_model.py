"""Paper data model for multi-source journal search."""

from dataclasses import dataclass, field


@dataclass
class Paper:
    title: str
    authors: list[str]
    year: int | None
    journal: str
    doi: str
    url: str
    source: str
    abstract: str = ""
    relevance_score: float = 0.0
