class OutputAggregator:
    """Combines worker outputs into a single Bahasa Indonesia markdown report."""

    def aggregate(self, worker_results: dict[str, dict]) -> str:
        """Aggregate worker results into markdown.

        Args:
            worker_results: {worker_name: {"status": "success"|"failed", "data": {...}|None, "error": str|None}}

        Returns:
            Markdown string in Bahasa Indonesia.
        """
        parts = []

        if "reader" in worker_results and worker_results["reader"]["status"] == "success":
            data = worker_results["reader"]["data"]
            parts.append("# Ringkasan Jurnal\n")
            parts.append(data.get("summary", "Tidak ada ringkasan."))
            parts.append("")

        if "reviewer" in worker_results:
            wr = worker_results["reviewer"]
            if wr["status"] == "success":
                data = wr["data"]
                parts.append("## Review Peer\n")
                parts.append(f"**Penilaian:** {data.get('assessment', 'N/A')}\n")
                parts.append(data.get("review_text", "Tidak ada review."))
            else:
                parts.append("## Review Peer\n")
                parts.append(f"[reviewer] Gagal: {wr.get('error', 'Unknown error')}. Coba lagi nanti.\n")
            parts.append("")

        if "gap_analyzer" in worker_results:
            ga = worker_results["gap_analyzer"]
            if ga["status"] == "success":
                parts.append("## Research Gap\n")
                parts.append(ga["data"].get("gap_text", "Tidak ada gap teridentifikasi."))
            else:
                parts.append("## Research Gap\n")
                parts.append(f"[gap_analyzer] Gagal: {ga.get('error', 'Unknown error')}. Coba lagi nanti.\n")
            parts.append("")

        if "data_analysis" in worker_results:
            da = worker_results["data_analysis"]
            if da["status"] == "success":
                parts.append("## Analisis Data\n")
                parts.append(da["data"].get("interpretation", "Tidak ada interpretasi."))
            else:
                parts.append("## Analisis Data\n")
                parts.append(f"[data_analysis] Gagal: {da.get('error', 'Unknown error')}. Coba lagi nanti.\n")
            parts.append("")

        if "generator" in worker_results:
            gen = worker_results["generator"]
            if gen["status"] == "success":
                parts.append("## Draft Artikel\n")
                parts.append(gen["data"].get("draft", "Tidak ada draft."))
            else:
                parts.append("## Draft Artikel\n")
                parts.append(f"[generator] Gagal: {gen.get('error', 'Unknown error')}. Coba lagi nanti.\n")
            parts.append("")

        if "self_review" in worker_results:
            sr = worker_results["self_review"]
            if sr["status"] == "success":
                parts.append("## Self-Review\n")
                parts.append(sr["data"].get("review", "Tidak ada review."))
            else:
                parts.append("## Self-Review\n")
                parts.append(f"[self_review] Gagal: {sr.get('error', 'Unknown error')}. Coba lagi nanti.\n")
            parts.append("")

        return "\n".join(parts)
