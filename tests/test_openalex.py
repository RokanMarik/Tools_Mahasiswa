from modules.search.openalex import search


def test_openalex_search_returns_papers():
    papers = search("artificial intelligence education", limit=2)
    assert len(papers) > 0
    assert papers[0].title != ""


def test_openalex_paper_has_citation_count():
    papers = search("machine learning", limit=3)
    assert any(p.citation_count >= 0 for p in papers)


def test_openalex_paper_fields():
    papers = search("deep learning", limit=1)
    paper = papers[0]
    assert paper.title
    assert paper.source == "openalex"
    assert isinstance(paper.citation_count, int)
