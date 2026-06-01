"""RIS export."""
from typing import List, Dict

class RisExporter:
    def export(self, papers: List[Dict]) -> str:
        entries = []
        for paper in papers:
            lines = ["TY  - JOUR"]
            if paper.get("title"): lines.append(f"TI  - {paper['title']}")
            for a in (paper.get("authors") or []): lines.append(f"AU  - {a}")
            if paper.get("year"): lines.append(f"PY  - {paper['year']}")
            if paper.get("journal"): lines.append(f"T2  - {paper['journal']}")
            if paper.get("doi"): lines.append(f"DO  - {paper['doi']}")
            if paper.get("url"): lines.append(f"UR  - {paper['url']}")
            if paper.get("citations"): lines.append(f"N1  - Cited by: {paper['citations']}")
            if paper.get("source"): lines.append(f"DB  - {paper['source']}")
            lines.append("ER  - ")
            entries.append(chr(10).join(lines))
        return chr(10).join(entries)
