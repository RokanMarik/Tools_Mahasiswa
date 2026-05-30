import os
import json
from typing import Optional, List, Dict


class SearchCache:
    def __init__(self, cache_file: str = "cache/search_results.json"):
        """Initialize cache with file path"""
        self.cache_file = cache_file
        self.cache = {}
        self._load_cache()
    
    def _load_cache(self):
        """Load cache from file if it exists"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    self.cache = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.cache = {}
        else:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
    
    def _save_cache(self):
        """Save cache to file"""
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def get(self, query: str) -> Optional[List[Dict]]:
        """Get cached results for a query"""
        return self.cache.get(query)
    
    def set(self, query: str, results: List[Dict]) -> None:
        """Cache results for a query"""
        self.cache[query] = results
        self._save_cache()
    
    def clear(self) -> None:
        """Clear all cache"""
        self.cache = {}
        self._save_cache()
