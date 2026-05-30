import os
import tempfile
from parsers.pdf_parser import PDFParser


def _create_test_pdf(text: str, path: str) -> str:
    """Create a minimal PDF with the given text using pymupdf."""
    import fitz
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    doc.save(path)
    doc.close()
    return path


def test_parse_simple_pdf(tmp_path):
    pdf_path = str(tmp_path / "test.pdf")
    _create_test_pdf("Abstract: This is a test.\n\nIntroduction: Hello world.", pdf_path)
    parser = PDFParser()
    article = parser.parse(pdf_path)
    assert "test" in article.raw_text.lower()
    assert article.metadata.get("source_file") == pdf_path


def test_parse_nonexistent_file():
    parser = PDFParser()
    try:
        parser.parse("/nonexistent/file.pdf")
        assert False, "Should raise FileNotFoundError"
    except FileNotFoundError:
        pass


from parsers.text_parser import TextParser


def test_parse_text_with_sections():
    text = """## ABSTRACT
This is the abstract.

## INTRODUCTION
This is the introduction.

## METHODOLOGY
We used a survey method.
"""
    parser = TextParser()
    article = parser.parse(text)
    assert article.sections["abstract"] == "This is the abstract."
    assert article.sections["introduction"] == "This is the introduction."
    assert article.sections["methodology"] == "We used a survey method."


def test_parse_text_without_sections():
    text = "This is just plain text with no headings."
    parser = TextParser()
    article = parser.parse(text)
    assert article.sections["full_text"] == text
    assert article.raw_text == text


def test_parse_short_text_warning():
    text = "Short text."
    parser = TextParser()
    article = parser.parse(text)
    assert article.metadata.get("warning") is not None


from unittest.mock import patch, MagicMock
from parsers.url_fetcher import URLFetcher


def test_fetch_url_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "## ABSTRACT\nTest abstract.\n\n## INTRODUCTION\nTest intro."}}]
    }
    with patch("parsers.url_fetcher.requests.post", return_value=mock_response):
        fetcher = URLFetcher(ninerouter_url="http://localhost:20128", ninerouter_key="test-key")
        article = fetcher.fetch("https://doi.org/10.1234/test")
        assert article.metadata["source_type"] == "url"
        assert article.sections["abstract"] == "Test abstract."


def test_fetch_invalid_url():
    with patch("parsers.url_fetcher.requests.post") as mock_post:
        mock_post.side_effect = Exception("Connection refused")
        fetcher = URLFetcher(ninerouter_url="http://localhost:20128", ninerouter_key="test-key")
        try:
            fetcher.fetch("https://invalid-url-xyz.com")
            assert False, "Should raise"
        except Exception as e:
            assert "Connection refused" in str(e)
