import os
import requests
from models.article_data import StructuredArticleData
from parsers.text_parser import TextParser


class URLFetcher:
    """Fetch content from DOI or URL via 9router-web-fetch, then parse."""

    def __init__(self, ninerouter_url: str | None = None, ninerouter_key: str | None = None):
        self.ninerouter_url = ninerouter_url or os.getenv("NINEROUTER_URL", "http://localhost:20128")
        self.ninerouter_key = ninerouter_key or os.getenv("NINEROUTER_KEY", "")
        self._headers = {"Content-Type": "application/json"}
        if self.ninerouter_key:
            self._headers["Authorization"] = f"Bearer {self.ninerouter_key}"

    def fetch(self, url: str) -> StructuredArticleData:
        """Fetch URL content and parse into StructuredArticleData."""
        text = self._fetch_via_9router(url)
        parser = TextParser()
        article = parser.parse(text)
        article.metadata["source_type"] = "url"
        article.metadata["source_url"] = url
        return article

    def _fetch_via_9router(self, url: str) -> str:
        """Fetch URL content using 9router-web-fetch."""
        endpoint = f"{self.ninerouter_url}/v1/chat/completions"
        payload = {
            "model": "jina/reader",
            "messages": [
                {
                    "role": "user",
                    "content": f"Fetch and extract the full text content from this URL: {url}. Return only the article text in markdown format."
                }
            ],
            "max_tokens": 16000,
            "temperature": 0,
            "stream": False,
        }
        response = requests.post(endpoint, headers=self._headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
