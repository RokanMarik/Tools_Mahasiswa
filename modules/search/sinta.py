"""SINTA client for Indonesian journals."""

from typing import List, Dict, Optional


class SintaClient:
    """Client for SINTA Indonesian journal database."""

    def search(self, query: str, limit: int = 10, year_from: Optional[int] = None, year_to: Optional[int] = None) -> List[Dict]:
        """SINTA focuses on journal-level metadata, not papers."""
        return []
