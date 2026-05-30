from core.error_handler import ErrorHandler, WorkerError


def test_record_success():
    handler = ErrorHandler()
    handler.record_success("reader", {"summary": "done"})
    assert handler.get_results("reader") == {"summary": "done"}
    assert handler.get_status("reader") == "success"


def test_record_failure():
    handler = ErrorHandler()
    handler.record_failure("reviewer", "Model unavailable")
    assert handler.get_status("reviewer") == "failed"
    assert "Model unavailable" in handler.get_error("reviewer")


def test_all_success():
    handler = ErrorHandler()
    handler.record_success("reader", {})
    assert handler.all_workers_succeeded(["reader", "reviewer"]) == False


def test_partial_failure():
    handler = ErrorHandler()
    handler.record_success("reader", {"summary": "ok"})
    handler.record_failure("reviewer", "timeout")
    assert handler.has_partial_failure(["reader", "reviewer"]) == True


def test_get_summary():
    handler = ErrorHandler()
    handler.record_success("reader", {"summary": "ok"})
    handler.record_failure("reviewer", "model down")
    summary = handler.get_summary(["reader", "reviewer"])
    assert summary["reader"]["status"] == "success"
    assert summary["reviewer"]["status"] == "failed"
