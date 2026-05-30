from models.article_data import StructuredArticleData


class TextParser:
    """Parse plain text files into StructuredArticleData."""

    def parse(self, file_path: str) -> StructuredArticleData:
        """Parse a text file into StructuredArticleData."""
        raise NotImplementedError("TextParser not yet implemented")
