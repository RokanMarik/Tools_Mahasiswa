from models.article_data import StructuredArticleData


class URLFetcher:
    """Fetch and parse content from URLs into StructuredArticleData."""

    def parse(self, url: str) -> StructuredArticleData:
        """Fetch a URL and parse it into StructuredArticleData."""
        raise NotImplementedError("URLFetcher not yet implemented")
