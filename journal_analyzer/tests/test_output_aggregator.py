from core.output_aggregator import OutputAggregator


def test_aggregate_single_worker():
    agg = OutputAggregator()
    result = agg.aggregate({
        "reader": {"status": "success", "data": {"summary": "Paper about X."}},
    })
    assert "Paper about X." in result


def test_aggregate_multiple_workers():
    agg = OutputAggregator()
    result = agg.aggregate({
        "reader": {"status": "success", "data": {"summary": "Summary here."}},
        "reviewer": {"status": "success", "data": {"assessment": "Major Revision", "comments": "Fix methods."}},
    })
    assert "Summary here." in result
    assert "Major Revision" in result


def test_aggregate_partial_failure():
    agg = OutputAggregator()
    result = agg.aggregate({
        "reader": {"status": "success", "data": {"summary": "Summary."}},
        "reviewer": {"status": "failed", "error": "Model unavailable"},
    })
    assert "Summary." in result
    assert "[reviewer] Gagal: Model unavailable" in result


def test_format_markdown():
    agg = OutputAggregator()
    result = agg.aggregate({
        "reader": {"status": "success", "data": {"summary": "Test summary"}},
    })
    assert "# Ringkasan Jurnal" in result
    assert "Test summary" in result


def test_aggregate_with_gap_analysis():
    agg = OutputAggregator()
    result = agg.aggregate({
        "reader": {"status": "success", "data": {"summary": "Summary."}},
        "gap_analyzer": {"status": "success", "data": {"gap_text": "Gap: longitudinal study needed."}},
    })
    assert "Ringkasan Jurnal" in result
    assert "Research Gap" in result
    assert "longitudinal study" in result


def test_aggregate_with_data_analysis():
    agg = OutputAggregator()
    result = agg.aggregate({
        "data_analysis": {"status": "success", "data": {"interpretation": "H0 ditolak, p<0.05"}},
    })
    assert "Analisis Data" in result
    assert "H0 ditolak" in result


def test_aggregate_all_workers():
    agg = OutputAggregator()
    result = agg.aggregate({
        "reader": {"status": "success", "data": {"summary": "Summary."}},
        "reviewer": {"status": "success", "data": {"assessment": "Minor Revision", "review_text": "Good paper."}},
        "gap_analyzer": {"status": "success", "data": {"gap_text": "Gap identified."}},
    })
    assert "Ringkasan Jurnal" in result
    assert "Review Peer" in result
    assert "Research Gap" in result


def test_aggregate_with_generation():
    agg = OutputAggregator()
    result = agg.aggregate({
        "generator": {"status": "success", "data": {"draft": "# DRAFT ARTIKEL\n\nTest content."}},
    })
    assert "Draft Artikel" in result
    assert "Test content" in result


def test_aggregate_with_generation_and_self_review():
    agg = OutputAggregator()
    result = agg.aggregate({
        "generator": {"status": "success", "data": {"draft": "# DRAFT\nContent."}},
        "self_review": {"status": "success", "data": {"review": "QUALITY SCORE: 8/10"}},
    })
    assert "Draft Artikel" in result
    assert "Self-Review" in result
    assert "8/10" in result


def test_aggregate_with_comparison():
    agg = OutputAggregator()
    result = agg.aggregate({
        "comparison": {"status": "success", "data": {"comparison": "Paper 1 vs Paper 2: ..."}},
    })
    assert "Perbandingan" in result
    assert "Paper 1 vs Paper 2" in result
