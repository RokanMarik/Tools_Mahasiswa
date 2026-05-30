class WorkerError(Exception):
    """Raised when a worker fails."""
    def __init__(self, worker_name: str, message: str):
        self.worker_name = worker_name
        self.message = message
        super().__init__(f"[{worker_name}] Failed: {message}")


class ErrorHandler:
    """Tracks per-worker success/failure across the pipeline."""

    def __init__(self):
        self._results: dict[str, dict] = {}
        self._errors: dict[str, str] = {}

    def record_success(self, worker_name: str, result: dict) -> None:
        self._results[worker_name] = result
        self._errors.pop(worker_name, None)

    def record_failure(self, worker_name: str, error: str) -> None:
        self._errors[worker_name] = error
        self._results.pop(worker_name, None)

    def get_results(self, worker_name: str) -> dict | None:
        return self._results.get(worker_name)

    def get_error(self, worker_name: str) -> str | None:
        return self._errors.get(worker_name)

    def get_status(self, worker_name: str) -> str:
        if worker_name in self._results:
            return "success"
        if worker_name in self._errors:
            return "failed"
        return "not_run"

    def all_workers_succeeded(self, worker_names: list[str]) -> bool:
        return all(self.get_status(name) == "success" for name in worker_names)

    def has_partial_failure(self, worker_names: list[str]) -> bool:
        statuses = [self.get_status(name) for name in worker_names]
        return "failed" in statuses and "success" in statuses

    def get_summary(self, worker_names: list[str]) -> dict:
        summary = {}
        for name in worker_names:
            status = self.get_status(name)
            entry = {"status": status}
            if status == "success":
                entry["data"] = self._results.get(name)
            elif status == "failed":
                entry["error"] = self._errors.get(name)
            summary[name] = entry
        return summary
