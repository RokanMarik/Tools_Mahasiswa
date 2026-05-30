from core.chunker import Chunker
from models.article_data import StructuredArticleData


def _make_article(sections: dict) -> StructuredArticleData:
    return StructuredArticleData(
        metadata={"title": "Test"},
        sections=sections,
    )


def test_no_chunking_small_article():
    article = _make_article({"abstract": "one two three"})
    chunker = Chunker(threshold_small=5000, threshold_large=20000, max_chunk_size=5000)
    result = chunker.chunk(article)
    assert result.chunks == []
    assert result == article


def test_chunk_by_section_medium_article():
    sections = {
        "abstract": "word " * 1000,
        "introduction": "word " * 3000,
        "methodology": "word " * 3000,
        "results": "word " * 3000,
    }
    article = _make_article(sections)
    chunker = Chunker()
    result = chunker.chunk(article)
    assert len(result.chunks) == 4
    assert result.chunks[0].section == "abstract"
    assert result.chunks[0].index == 0


def test_sub_chunk_large_section():
    sections = {
        "abstract": "word " * 1000,
        "introduction": "word " * 8000,
    }
    article = _make_article(sections)
    chunker = Chunker(max_chunk_size=5000)
    result = chunker.chunk(article)
    # introduction > 5000 words, should be split
    intro_chunks = [c for c in result.chunks if c.section == "introduction"]
    assert len(intro_chunks) >= 2


def test_chunk_preserves_raw_text():
    article = _make_article({"abstract": "test content"})
    article.raw_text = "full raw text"
    chunker = Chunker()
    result = chunker.chunk(article)
    assert result.raw_text == "full raw text"
