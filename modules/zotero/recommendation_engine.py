"""Paper recommendation engine using 9Router web search."""

import os
import requests
from typing import List, Dict


class RecommendationEngine:
    def __init__(self, journal_finder):
        """Initialize with a JournalFinder instance for web search.

        Args:
            journal_finder: JournalFinder instance with chat() method.
        """
        self.finder = journal_finder
        self.base_url = os.getenv("NINEROUTER_URL", "http://localhost:20128")
        self.api_key = os.getenv("NINEROUTER_KEY", "")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def recommend(self, gaps: List[Dict], existing_topics: List[str]) -> List[Dict]:
        """Get paper recommendations for gap topics.

        Args:
            gaps: List of gap dicts with 'topic' and 'status'.
            existing_topics: List of topics already well-covered.

        Returns:
            List of {title, doi, url, reason} recommendations.
        """
        recommendations = []

        # Get missing and low topics (limit to top 3 to save tokens)
        target_topics = [
            g["topic"] for g in gaps
            if g["status"] in ("missing", "low")
        ][:3]

        for topic in target_topics:
            papers = self._search_papers(topic)
            for paper in papers[:2]:  # 2 papers per topic
                recommendations.append({
                    "title": paper.get("title", "Unknown"),
                    "doi": paper.get("doi", ""),
                    "url": paper.get("url", ""),
                    "reason": self._generate_reason(topic),
                })

        return recommendations

    def _search_papers(self, topic: str) -> List[Dict]:
        """Search for papers on a topic via 9Router web search.

        Args:
            topic: Research topic to search.

        Returns:
            List of paper dicts.
        """
        search_query = f"{topic} academic paper research open access site:scholar.google.com OR site:arxiv.org"

        try:
            url = f"{self.base_url}/v1/chat/completions"
            payload = {
                "model": "tavily/search",
                "messages": [{"role": "user", "content": search_query}],
                "max_tokens": 800,
                "temperature": 0.3,
                "stream": False,
            }

            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            content = result["choices"][0]["message"]["content"]

            # Parse results -- extract paper info from search response
            return self._parse_search_results(content)

        except Exception:
            return []

    def _parse_search_results(self, content: str) -> List[Dict]:
        """Parse search response into paper dicts."""
        papers = []
        lines = content.strip().split("\n")
        current_paper = {}

        for line in lines:
            line = line.strip()
            if not line:
                if current_paper.get("title"):
                    papers.append(current_paper)
                    current_paper = {}
                continue

            lower_line = line.lower()
            if "title" in lower_line:
                current_paper["title"] = line.split(":", 1)[-1].strip().strip("*").strip('"')
            elif "doi" in lower_line:
                current_paper["doi"] = line.split(":", 1)[-1].strip().strip("*").strip()
            elif line.startswith("http"):
                current_paper["url"] = line

        if current_paper.get("title"):
            papers.append(current_paper)

        return papers[:5]

    def _generate_reason(self, topic: str) -> str:
        """Generate a reason for recommending this paper."""
        return f"Topik '{topic}' belum ada di koleksimu, paper ini bisa melengkapinya."
