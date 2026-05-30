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
