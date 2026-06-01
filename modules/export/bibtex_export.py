"""BibTeX export."""
from typing import List, Dict

class BibtexExporter:
    def export(self, papers: List[Dict]) -> str:
        entries = []
        for i, paper in enumerate(papers, 1):
            entries.append(self._to_bibtex(paper, f"paper{i}"))
        return chr(10).join(entries)
    def _to_bibtex(self, paper: Dict, key: str) -> str:
        authors = " and ".join(paper.get("authors", []) or ["Unknown"])
        fields = []
        fields.append("  title = {" + paper.get("title", "Untitled") + "}")
        fields.append("  author = {" + authors + "}")
        if paper.get("year"):
            fields.append("  year = {" + str(paper["year"]) + "}")
        if paper.get("journal"):
            fields.append("  journal = {" + paper["journal"] + "}")
        if paper.get("doi"):
            fields.append("  doi = {" + paper["doi"] + "}")
        if paper.get("url"):
            fields.append("  url = {" + paper["url"] + "}")
        return "@article{" + key + "," + chr(10) + ("," + chr(10)).join(fields) + chr(10) + "}"
