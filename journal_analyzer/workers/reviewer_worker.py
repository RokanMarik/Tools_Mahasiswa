import os
import re
import requests
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from models.article_data import StructuredArticleData


class ReviewerWorker:
    """Peer reviewer worker. Produces international journal-level reviews."""

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
        article: StructuredArticleData,
        reader_summary: str | None = None,
        model: str = "anthropic/claude-opus-4-20250514",
    ) -> dict | None:
        """Run the reviewer worker on an article.

        Args:
            article: The article to review.
            reader_summary: Optional summary from Reader Worker for context.
            model: 9Router model name.

        Returns:
            {"assessment": str, "review_text": str} or None on failure.
        """
        system_prompt = self._load_system_prompt("reviewer.md")
        user_prompt = self._build_user_prompt(article, reader_summary)

        try:
            response = self._chat(system_prompt, user_prompt, model)
        except Exception:
            return None
        if response is None:
            return None

        assessment = self._extract_assessment(response)
        return {"assessment": assessment, "review_text": response}

    def _chat(self, system_prompt: str, user_prompt: str, model: str) -> str | None:
        """Call 9Router chat completion."""
        endpoint = f"{self.ninerouter_url}/v1/chat/completions"
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "max_tokens": 8000,
            "temperature": 0.2,
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

    def _build_user_prompt(
        self, article: StructuredArticleData, reader_summary: str | None = None
    ) -> str:
        template = self._env.get_template("reviewer_user.j2")
        return template.render(
            metadata=article.metadata,
            sections=article.sections,
            methodology_type=article.methodology_type,
            reader_summary=reader_summary or "",
        )

    def _extract_assessment(self, review_text: str) -> str:
        """Extract overall assessment from review text."""
        patterns = [
            r"(?i)OVERALL ASSESSMENT[:\s]*(Accept|Minor Revision|Major Revision|Reject)",
            r"(?i)overall[:\s]*(Accept|Minor Revision|Major Revision|Reject)",
            r"(?i)penilaian[:\s]*(Accept|Minor Revision|Major Revision|Reject)",
        ]
        for pattern in patterns:
            match = re.search(pattern, review_text)
            if match:
                return match.group(1).strip()
        return "N/A"
