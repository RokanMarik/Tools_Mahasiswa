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
