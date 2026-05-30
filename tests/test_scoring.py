from modules.search.paper_model import Paper
from modules.search.scoring import compute_composite_score, sort_papers


def _make_paper(title, year=2023, citations=0):
    return Paper(
        title=title, authors=["Test"], year=year,
        journal="Test", doi="10.x/x", url="http://x",
        source="test", citation_count=citations,
    )


def test_composite_score_high_citation_old_paper():
    papers = [
        _make_paper("New Low Cit", year=2025, citations=1),
        _make_paper("Old High Cit", year=2020, citations=100),
    ]
    compute_composite_score(papers)
    assert papers[0].relevance_score < papers[1].relevance_score


def test_composite_score_new_high_citation_wins():
    papers = [
        _make_paper("Old Low Cit", year=2020, citations=5),
        _make_paper("New High Cit", year=2025, citations=100),
    ]
    compute_composite_score(papers)
    assert papers[0].relevance_score < papers[1].relevance_score


def test_composite_score_all_zero_citations():
    papers = [
        _make_paper("A", year=2023, citations=0),
        _make_paper("B", year=2025, citations=0),
    ]
    compute_composite_score(papers)
    assert papers[0].relevance_score < papers[1].relevance_score


def test_sort_by_citations():
    papers = [
        _make_paper("Low", citations=5),
        _make_paper("High", citations=100),
        _make_paper("Med", citations=50),
    ]
    result = sort_papers(papers, sort_by="citations")
    assert result[0].citation_count == 100
    assert result[1].citation_count == 50
    assert result[2].citation_count == 5


def test_sort_by_year():
    papers = [
        _make_paper("Old", year=2020),
        _make_paper("New", year=2025),
        _make_paper("Mid", year=2023),
    ]
    result = sort_papers(papers, sort_by="year")
    assert result[0].year == 2025
    assert result[1].year == 2023
    assert result[2].year == 2020


def test_sort_by_composite():
    papers = [
        _make_paper("A", year=2020, citations=100),
        _make_paper("B", year=2025, citations=100),
    ]
    result = sort_papers(papers, sort_by="composite")
    assert result[0].title == "B"
