import os
import requests
from typing import List, Dict, Optional
from modules.search_cache import SearchCache


class WebSearchOptimizer:
    def __init__(self, ninerouter_url: str = None, ninerouter_key: str = None, cache: SearchCache = None):
        """Initialize web search optimizer"""
        self.ninerouter_url = ninerouter_url or os.getenv("NINEROUTER_URL", "http://localhost:20128")
        self.ninerouter_key = ninerouter_key or os.getenv("NINEROUTER_KEY", "")
        self.cache = cache or SearchCache()
        self.headers = {
            "Authorization": f"Bearer {self.ninerouter_key}",
            "Content-Type": "application/json"
        }
    
    def _generate_search_query(self, research_question: str) -> str:
        """Generate optimized search query from research question using chat"""
        prompt = f"""Buat satu search query yang optimal dan powerful untuk mencari paper ilmiah tentang:
"{research_question}"

Berikan HANYA query-nya saja, tanpa penjelasan. Query harus:
- Singkat (3-5 kata kunci)
- Spesifik dan relevan
- Menggunakan istilah akademik yang tepat

Contoh format: "deep learning cancer detection medical imaging"
"""
        
        url = f"{self.ninerouter_url}/v1/chat/completions"
        payload = {
            "model": "Mencari_Jurnal_Ilmiah",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100,
            "temperature": 0.3,
            "stream": False
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()
            query = result["choices"][0]["message"]["content"].strip()
            return query
        except Exception as e:
            print(f"Error generating search query: {e}")
            # Fallback: use research question as-is
            return research_question
    
    def optimize_and_search(self, research_question: str, model: str = "tavily/search") -> List[Dict]:
        """Generate optimized query and execute web search"""
        
        # Check cache first
        cached = self.cache.get(research_question)
        if cached:
            print(f"[CACHE HIT] Using cached results for: {research_question}")
            return cached
        
        print(f"[CACHE MISS] Searching for: {research_question}")
        
        # Generate optimized query
        search_query = self._generate_search_query(research_question)
        print(f"[OPTIMIZED QUERY] {search_query}")
        
        # Execute web search
        url = f"{self.ninerouter_url}/v1/search"
        payload = {
            "model": model,
            "query": search_query,
            "limit": 5
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=15)
            response.raise_for_status()
            result = response.json()
            
            # Extract and format results
            papers = []
            for item in result.get("results", []):
                papers.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("snippet", ""),
                    "source": item.get("source", "")
                })
            
            # Cache results
            self.cache.set(research_question, papers)
            print(f"[SEARCH SUCCESS] Found {len(papers)} papers")
            return papers
        
        except Exception as e:
            print(f"[SEARCH ERROR] Error during web search: {e}")
            return []
