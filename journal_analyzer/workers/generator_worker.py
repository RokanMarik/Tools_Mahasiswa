import os
import requests
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class GeneratorWorker:
    """Article generation worker. Creates new article drafts from reference journals."""

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
        research_topic: str,
        reader_summaries: list[str] | None = None,
        gap_analysis: str = "",
        methodology: str = "",
        citation_style: str = "APA7",
        model: str = "anthropic/claude-opus-4-20250514",
    ) -> dict | None:
        """Generate an article draft.

        Returns:
            {"draft": str} or None on failure.
        """
        system_prompt = self._load_system_prompt("generator.md")
        user_prompt = self._build_user_prompt(research_topic, reader_summaries, gap_analysis, methodology, citation_style)

        try:
            response = self._chat(system_prompt, user_prompt, model)
            if response is None:
                return None
            return {"draft": response}
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
            "max_tokens": 16000,
            "temperature": 0.4,
            "stream": False,
        }
        try:
            response = requests.post(endpoint, headers=self._headers, json=payload, timeout=300)
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
        self,
        research_topic: str,
        reader_summaries: list[str] | None,
        gap_analysis: str,
        methodology: str,
        citation_style: str,
    ) -> str:
        template = self._env.get_template("generator_user.j2")
        return template.render(
            research_topic=research_topic,
            reader_summaries=reader_summaries or [],
            gap_analysis=gap_analysis,
            methodology=methodology,
            citation_style=citation_style,
        )
