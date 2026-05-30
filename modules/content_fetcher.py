import os
import requests
from typing import List, Dict, Optional
from modules.search_cache import SearchCache


class ContentFetcher:
    def __init__(self, ninerouter_url: str = None, ninerouter_key: str = None, cache: SearchCache = None):
        """Initialize content fetcher"""
        self.ninerouter_url = ninerouter_url or os.getenv("NINEROUTER_URL", "http://localhost:20128")
        self.ninerouter_key = ninerouter_key or os.getenv("NINEROUTER_KEY", "")
        self.cache = cache or SearchCache()
        self.headers = {
            "Authorization": f"Bearer {self.ninerouter_key}",
            "Content-Type": "application/json"
        }
    
    def fetch_papers(self, urls: List[str], max_papers: int = 5) -> List[Dict]:
        """Fetch content from papers, limit to max_papers"""
        papers = []
        
        for i, url in enumerate(urls[:max_papers]):
            try:
                paper_content = self._fetch_single_paper(url)
                if paper_content:
                    papers.append(paper_content)
            except Exception as e:
                print(f"[FETCH ERROR] Error fetching {url}: {e}")
                continue
        
        return papers
    
    def _fetch_single_paper(self, url: str) -> Optional[Dict]:
        """Fetch content from a single paper URL"""
        
        # Check cache first
        cache_key = f"content:{url}"
        cached = self.cache.get(cache_key)
        if cached:
            print(f"[CACHE HIT] Using cached content for: {url}")
            return cached
        
        print(f"[FETCHING] Retrieving content from: {url}")
        
        # Fetch via 9router web-fetch
        fetch_url = f"{self.ninerouter_url}/v1/web/fetch"
        payload = {
            "url": url,
            "format": "markdown"
        }
        
        try:
            response = requests.post(fetch_url, headers=self.headers, json=payload, timeout=20)
            response.raise_for_status()
            result = response.json()
            
            paper_data = {
                "url": url,
                "title": result.get("title", ""),
                "content": result.get("content", "")[:2000],  # Limit content to 2000 chars
                "metadata": {
                    "source": result.get("source", ""),
                    "fetch_time": result.get("fetch_time", "")
                }
            }
            
            # Cache the content
            self.cache.set(cache_key, paper_data)
            print(f"[FETCH SUCCESS] Retrieved content from: {url}")
            return paper_data
        
        except Exception as e:
            print(f"[FETCH ERROR] Error fetching content from {url}: {e}")
            return None
