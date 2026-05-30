"""Duplicate detection for Zotero items."""

from typing import List, Dict
from collections import defaultdict


class DuplicateDetector:
    DOI_SIMILARITY_THRESHOLD = 0.80  # 80% similarity for title matching

    def find_duplicates(self, items: List[Dict]) -> List[Dict]:
        """Find duplicate items based on DOI and title similarity.

        Args:
            items: List of item dicts with 'doi', 'title', 'key' fields.

        Returns:
            List of {group: [items], reason: 'same_doi' | 'similar_title'}.
        """
        if len(items) < 2:
            return []

        duplicates = []

        # 1. Group by exact DOI match
        duplicates.extend(self._find_doi_duplicates(items))

        # 2. Find similar title matches (excluding items already flagged)
        flagged_keys = set()
        for group in duplicates:
            for item in group["group"]:
                flagged_keys.add(item["key"])

        duplicates.extend(self._find_title_duplicates(items, flagged_keys))

        return duplicates

    def _find_doi_duplicates(self, items: List[Dict]) -> List[Dict]:
        """Find items with identical DOI."""
        doi_groups = defaultdict(list)

        for item in items:
            doi = item.get("doi", "").strip()
            if doi:  # Only group items that have a DOI
                doi_groups[doi].append(item)

        duplicates = []
        for doi, group in doi_groups.items():
            if len(group) > 1:
                duplicates.append({
                    "group": group,
                    "reason": "same_doi",
                    "detail": f"DOI: {doi}",
                })

        return duplicates

    def _find_title_duplicates(self, items: List[Dict], flagged_keys: set) -> List[Dict]:
        """Find items with similar titles (>90% similarity)."""
        duplicates = []
        seen_pairs = set()

        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                item_a = items[i]
                item_b = items[j]

                # Skip if either already flagged
                if item_a["key"] in flagged_keys or item_b["key"] in flagged_keys:
                    continue

                # Skip if this pair already recorded
                pair_key = tuple(sorted([item_a["key"], item_b["key"]]))
                if pair_key in seen_pairs:
                    continue

                similarity = self._title_similarity(item_a["title"], item_b["title"])

                if similarity >= self.DOI_SIMILARITY_THRESHOLD:
                    seen_pairs.add(pair_key)
                    duplicates.append({
                        "group": [item_a, item_b],
                        "reason": "similar_title",
                        "detail": f"Judul mirip {similarity:.0%}",
                    })

        return duplicates

    def _title_similarity(self, title_a: str, title_b: str) -> float:
        """Calculate title similarity using normalized word overlap (Jaccard)."""
        import re
        # Remove punctuation and normalize
        words_a = set(re.sub(r'[^\w\s]', '', title_a.lower()).split())
        words_b = set(re.sub(r'[^\w\s]', '', title_b.lower()).split())

        if not words_a or not words_b:
            return 0.0

        intersection = words_a & words_b
        union = words_a | words_b

        return len(intersection) / len(union)
