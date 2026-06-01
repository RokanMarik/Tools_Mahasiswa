"""Paper quality scoring."""
from typing import Dict
import math
from datetime import datetime


class PaperScorer:
    """Score paper quality 0-100."""

    def __init__(self):
        self.current_year = datetime.now().year

    def score(self, paper: Dict) -> float:
        score = 0.0
        citations = paper.get('citations', 0) or 0
        score += min(50, math.log10(citations + 1) * 15)

        year = paper.get('year', 0) or 0
        if year:
            age = self.current_year - year
            if age <= 1: score += 30
            elif age <= 3: score += 25
            elif age <= 5: score += 20
            elif age <= 10: score += 10
            else: score += 5

        if paper.get('abstract'): score += 8
        if paper.get('doi'): score += 6
        if paper.get('authors'): score += 4
        if paper.get('journal'): score += 2
        return round(score, 1)

    def score_all(self, papers):
        for paper in papers:
            paper['quality_score'] = self.score(paper)
        return sorted(papers, key=lambda p: p.get('quality_score', 0), reverse=True)
