"""Abstract summarizer."""
import re


class AbstractSummarizer:
    """Summarize paper abstracts."""

    def summarize(self, abstract, max_length=200):
        if not abstract or len(abstract) <= max_length:
            return abstract
        sentences = re.split(r"(?<=[.!?])\s+", abstract)
        scored = []
        for i, sent in enumerate(sentences):
            score = self._score(sent, i, len(sentences))
            scored.append((score, sent))
        scored.sort(key=lambda x: x[0], reverse=True)
        result = []
        total = 0
        for score, sent in scored:
            if total + len(sent) + 3 <= max_length:
                result.append(sent)
                total += len(sent) + 3
            else:
                break
        if not result:
            return abstract[:max_length-3] + "..."
        summary = " ".join(result)
        if len(summary) < len(abstract):
            summary += "..."
        return summary

    def _score(self, sentence, index, total):
        score = 0.0
        lower = sentence.lower()
        if index == 0: score += 3
        if index == total - 1: score += 2
        for word in ["propose", "method", "result", "achieve", "novel", "show", "demonstrate"]:
            if word in lower: score += 1
        if re.search(r"\d+%", lower) or re.search(r"\d+\.\d+", lower): score += 2
        if len(sentence) < 50: score += 1
        return score

    def summarize_papers(self, papers, max_length=200):
        for paper in papers:
            abstract = paper.get('abstract', '')
            if abstract:
                paper['summary'] = self.summarize(abstract, max_length)
        return papers
