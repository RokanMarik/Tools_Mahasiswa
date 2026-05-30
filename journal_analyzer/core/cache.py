import os
import json
import glob
import time
from typing import Optional

SECONDS_PER_DAY = 86400


class AnalysisCache:
    """Content-hash based cache for parsed articles and analysis results.

    Parse cache is permanent. Analysis cache has configurable TTL.
    """

    def __init__(self, cache_dir: str = "cache", ttl_days: int = 7):
        self.cache_dir = cache_dir
        self.ttl_days = ttl_days
        self._parsed_dir = os.path.join(cache_dir, "parsed")
        self._analysis_dir = os.path.join(cache_dir, "analysis")
        os.makedirs(self._parsed_dir, exist_ok=True)
        os.makedirs(self._analysis_dir, exist_ok=True)

    def _parsed_path(self, content_hash: str) -> str:
        return os.path.join(self._parsed_dir, f"{content_hash}.json")

    def _analysis_path(self, content_hash: str, worker: str) -> str:
        return os.path.join(self._analysis_dir, f"{content_hash}_{worker}.json")

    # --- Parsed article cache (permanent) ---

    def set_parsed(self, content_hash: str, data: dict) -> None:
        path = self._parsed_path(content_hash)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def get_parsed(self, content_hash: str) -> Optional[dict]:
        path = self._parsed_path(content_hash)
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return None

    # --- Analysis result cache (TTL-based) ---

    def set_analysis(self, content_hash: str, worker: str, data: dict) -> None:
        path = self._analysis_path(content_hash, worker)
        with open(path, "w") as f:
            json.dump({"data": data, "timestamp": time.time()}, f, indent=2)

    def get_analysis(self, content_hash: str, worker: str) -> Optional[dict]:
        path = self._analysis_path(content_hash, worker)
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            try:
                entry = json.load(f)
            except json.JSONDecodeError:
                return None
        age_seconds = time.time() - entry["timestamp"]
        if age_seconds > self.ttl_days * SECONDS_PER_DAY:
            os.remove(path)
            return None
        return entry["data"]

    def clear_analysis(self, content_hash: str) -> None:
        """Clear all analysis cache for a content hash."""
        pattern = os.path.join(self._analysis_dir, f"{content_hash}_*.json")
        for path in glob.glob(pattern):
            os.remove(path)
