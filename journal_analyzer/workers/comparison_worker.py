import os
import requests
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class ComparisonWorker:
    """Multi-paper comparison worker. Analyzes multiple papers side-by-side."""

    def __init__(
        self,
        ninerouter_url: str | None = None,
        ninerouter_key: str | None = None,
        prompts_dir: str = "journal_analyzer/prompts",
    ):
        self.ninerouter_url = ninerouter_url or os.getenv("NINEROUTER_URL", "http://localhost:20128")
        self.ninerouter_key = ninerouter_key or os.getenv("NINEROUTER_KEY", "")
        self._headers = {"Content-Type": "application/json"}
        if self.ninerouter_key:
            self._headers["Authorization"] = f"Bearer {self.ninerouter_key}"

        self._prompts_dir = Path(prompts_dir)
        self._env = Environment(loader=FileSystemLoader(str(self._prompts_dir / "templates")))

    def run(
        self,
        papers: list[dict],
        model: str = "anthropic/claude-opus-4-20250514",
    ) -> dict | None:
        """Run comparison analysis on multiple papers.

        Args:
            papers: List of dicts with keys: title, summary, methodology, key_findings.

        Returns:
            {"comparison": str} or None on failure.
        """
        if len(papers) < 2:
            return {"comparison": "Perbandingan membutuhkan minimal 2 paper."}

        system_prompt = self._load_system_prompt("comparison.md")
        user_prompt = self._build_user_prompt(papers)

        try:
            response = self._chat(system_prompt, user_prompt, model)
            if response is None:
                return None
            return {"comparison": response}
        except Exception:
            return None

    def _chat(self, system_prompt: str, user_prompt: str, model: str) -> str | None:
        endpoint = f"{self.ninerouter_url}/v1/chat/completions"
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "max_tokens": 8000,
            "temperature": 0.3,
            "stream": False,
        }
        try:
            response = requests.post(endpoint, headers=self._headers, json=payload, timeout=180)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception:
            return None

    def _load_system_prompt(self, filename: str) -> str:
        path = self._prompts_dir / "system" / filename
        if path.exists():
            return path.read_text(encoding="utf-8")
        return ""

    def _build_user_prompt(self, papers: list[dict]) -> str:
        template = self._env.get_template("comparison_user.j2")
        return template.render(papers=papers)
