"""Topic gap analysis for Zotero collections."""

from typing import List, Dict

# Common research topics in AI/ML field for gap comparison
AI_RESEARCH_TOPICS = [
    "machine learning",
    "deep learning",
    "natural language processing",
    "computer vision",
    "reinforcement learning",
    "generative ai",
    "federated learning",
    "transfer learning",
    "explainable ai",
    "medical ai",
    "robotics",
    "speech recognition",
    "recommendation systems",
    "graph neural networks",
    "large language models",
    "multimodal learning",
    "edge ai",
    "ai ethics",
    "time series",
    "anomaly detection",
]


class GapAnalyzer:
    COVERED_THRESHOLD = 3    # 3+ papers = covered
    LOW_THRESHOLD = 1        # 1-2 papers = low

    def analyze(self, items: List[Dict], field: str = "AI") -> List[Dict]:
        """Analyze which topics are covered, low, or missing in the collection.

        Args:
            items: List of item dicts with 'title', 'journal' fields.
            field: Research field for topic selection (default: 'AI').

        Returns:
            List of {topic, count, status: 'covered' | 'low' | 'missing'}.
        """
        topics = self._get_topics_for_field(field)
        results = []

        for topic in topics:
            count = self._count_topic_matches(items, topic)
            status = self._classify_topic(count)
            results.append({
                "topic": topic.title(),
                "count": count,
                "status": status,
            })

        # Sort: missing first, then low, then covered
        status_order = {"missing": 0, "low": 1, "covered": 2}
        results.sort(key=lambda x: (status_order[x["status"]], -x["count"]))

        return results

    def _get_topics_for_field(self, field: str) -> List[str]:
        """Get relevant topics for a research field."""
        # For now, use the same AI topics list for all fields
        # Can be extended later for field-specific topics
        return AI_RESEARCH_TOPICS

    def _count_topic_matches(self, items: List[Dict], topic: str) -> int:
        """Count items that match a topic keyword."""
        count = 0
        topic_lower = topic.lower()

        for item in items:
            title = item.get("title", "").lower()
            journal = item.get("journal", "").lower()

            if topic_lower in title or topic_lower in journal:
                count += 1

        return count

    def _classify_topic(self, count: int) -> str:
        """Classify a topic based on paper count."""
        if count >= self.COVERED_THRESHOLD:
            return "covered"
        elif count >= self.LOW_THRESHOLD:
            return "low"
        else:
            return "missing"
