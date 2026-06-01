"""CSV export."""
import csv
import io
from typing import List, Dict

class CsvExporter:
    FIELDS = ["title", "authors", "year", "citations", "doi", "url", "journal", "source"]
    def export(self, papers: List[Dict]) -> str:
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=self.FIELDS, extrasaction="ignore")
        writer.writeheader()
        for paper in papers:
            writer.writerow({"title": paper.get("title", ""), "authors": "; ".join(paper.get("authors", [])), "year": paper.get("year", ""), "citations": paper.get("citations", 0), "doi": paper.get("doi", ""), "url": paper.get("url", ""), "journal": paper.get("journal", ""), "source": paper.get("source", "")})
        return output.getvalue()
    def export_to_file(self, papers, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.export(papers))
        return filepath
