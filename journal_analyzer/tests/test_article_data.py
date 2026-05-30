from models.article_data import StructuredArticleData, Chunk


def test_create_article_data():
    article = StructuredArticleData(
        metadata={"title": "Test Paper", "authors": ["John Doe"], "publication_year": 2024},
        sections={"abstract": "This is a test abstract.", "introduction": "Intro text."},
        methodology_type="kuantitatif",
        raw_text="Full text here."
    )
    assert article.metadata["title"] == "Test Paper"
    assert article.sections["abstract"] == "This is a test abstract."
    assert article.methodology_type == "kuantitatif"


def test_get_section():
    article = StructuredArticleData(
        metadata={"title": "Test"},
        sections={"abstract": "Abstract text", "methods": "Methods text"}
    )
    assert article.get_section("abstract") == "Abstract text"
    assert article.get_section("nonexistent") == ""


def test_get_full_text():
    article = StructuredArticleData(
        metadata={"title": "Test"},
        sections={"abstract": "A", "introduction": "B", "conclusion": "C"}
    )
    text = article.get_full_text()
    assert "A" in text
    assert "B" in text
    assert "C" in text


def test_word_count():
    article = StructuredArticleData(
        metadata={"title": "Test"},
        sections={"abstract": "one two three four five"}
    )
    assert article.word_count == 5


def test_add_chunks():
    article = StructuredArticleData(
        metadata={"title": "Test"},
        sections={"abstract": "text"},
        raw_text="long text"
    )
    article.add_chunks([
        Chunk(section="abstract", text="chunk 1", index=0),
        Chunk(section="intro", text="chunk 2", index=1),
    ])
    assert len(article.chunks) == 2
    assert article.chunks[0].text == "chunk 1"


def test_default_values():
    article = StructuredArticleData(metadata={"title": "Test"})
    assert article.methodology_type == "unknown"
    assert article.key_findings == []
    assert article.statistical_methods == []
    assert article.chunks == []
