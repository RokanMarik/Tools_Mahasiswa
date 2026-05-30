import os
import requests
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from models.article_data import StructuredArticleData


class ReaderWorker:
    """Smart summarizer worker. Produces richer summaries than original abstracts."""

    def __init__(
        self,
        ninerouter_url: str | None = None,
        ninerouter_key: str | None = None,
        prompts_dir: str = "prompts",
    ):
        self.ninerouter_url = ninerouter_url or os.getenv("NINEROUTER_URL", "http://localhost:20128")
        self.ninerouter_key = ninerouter_key or os.getenv("NINEROUTER_KEY", "")
        self._headers = {"Content-Type": "application/json"}
        if self.ninerouter_key:
            self._headers["Authorization"] = f"Bearer {self.ninerouter_key}"

        self._prompts_dir = Path(prompts_dir)
        self._env = Environment(loader=FileSystemLoader(str(self._prompts_dir / "templates")))

    def run(self, article: StructuredArticleData, model: str = "anthropic/claude-sonnet-4-20250514") -> dict | None:
        """Run the reader worker on an article.

        Returns:
            {"summary": str} or None on failure.
        """
        system_prompt = self._load_system_prompt("reader.md")
        user_prompt = self._build_user_prompt(article)

        try:
            response = self._chat(system_prompt, user_prompt, model)
            if response is None:
                return None
            return {"summary": response}
        except Exception:
            return None

    def _chat(self, system_prompt: str, user_prompt: str, model: str) -> str | None:
        """Call 9Router chat completion."""
        endpoint = f"{self.ninerouter_url}/v1/chat/completions"
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "max_tokens": 4000,
            "temperature": 0.3,
            "stream": False,
        }
        try:
            response = requests.post(endpoint, headers=self._headers, json=payload, timeout=120)
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

    def _build_user_prompt(self, article: StructuredArticleData) -> str:
        template = self._env.get_template("reader_user.j2")
        return template.render(
            metadata=article.metadata,
            sections=article.sections,
        )
