#!/usr/bin/env python3
"""
Indonesian Academic APIs Module
Supports: Garuda Portal, SINTA, Neliti (all FREE, no API key needed)
"""

import requests
from typing import List, Dict
from urllib.parse import quote


class IndonesianAPIs:
    """Search Indonesian academic databases"""
    
    def __init__(self):
        self.garuda_base = "https://garuda.kemdikbud.go.id/api"
        self.sinta_base = "https://sinta.kemdikbud.go.id/api"
        self.neliti_base = "https://www.neliti.com/api"
    
    def search_all(self, query: str, max_results: int = 3) -> List[Dict]:
        """
        Search across Indonesian academic APIs
        
        Args:
            query: Search query
            max_results: Max papers to return
        
        Returns:
            List of papers with title and URL
        """
        papers = []
        
        # Search Garuda
        try:
            garuda_papers = self.search_garuda(query, max_results=2)
            papers.extend(garuda_papers)
        except Exception as e:
            print(f"[Garuda ERROR] {e}")
        
        # Search SINTA (if not enough)
        if len(papers) < max_results:
            try:
                sinta_papers = self.search_sinta(query, max_results=2)
                papers.extend(sinta_papers)
            except Exception as e:
                print(f"[SINTA ERROR] {e}")
        
        # Search Neliti (if still not enough)
        if len(papers) < max_results:
            try:
                neliti_papers = self.search_neliti(query, max_results=2)
                papers.extend(neliti_papers)
            except Exception as e:
                print(f"[Neliti ERROR] {e}")
        
        return papers[:max_results]
    
    def search_garuda(self, query: str, max_results: int = 3) -> List[Dict]:
        """
        Search Garuda Portal (Indonesian journal portal)
        Coverage: Indonesian journals
        """
        url = f"{self.garuda_base}/search"
        params = {
            'q': query,
            'limit': max_results
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            papers = []
            for item in data.get('data', []):
                papers.append({
                    'title': item.get('title', 'Untitled'),
                    'url': item.get('url', f"https://garuda.kemdikbud.go.id/documents/{item.get('id', '')}"),
                    'source': 'Garuda'
                })
            
            return papers
        except Exception as e:
            print(f"[Garuda] Fallback: {e}")
            return []
    
    def search_sinta(self, query: str, max_results: int = 3) -> List[Dict]:
        """
        Search SINTA (Indonesian research database)
        Coverage: Indonesian research, journals, articles
        """
        url = f"{self.sinta_base}/search"
        params = {
            'q': query,
            'limit': max_results,
            'type': 'article'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            papers = []
            for item in data.get('data', []):
                papers.append({
                    'title': item.get('title', 'Untitled'),
                    'url': item.get('url', f"https://sinta.kemdikbud.go.id/articles/{item.get('id', '')}"),
                    'source': 'SINTA'
                })
            
            return papers
        except Exception as e:
            print(f"[SINTA] Fallback: {e}")
            return []
    
    def search_neliti(self, query: str, max_results: int = 3) -> List[Dict]:
        """
        Search Neliti (Indonesian research platform)
        Coverage: Indonesian research papers, articles
        """
        url = f"{self.neliti_base}/search"
        params = {
            'q': query,
            'limit': max_results
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            papers = []
            for item in data.get('results', []):
                papers.append({
                    'title': item.get('title', 'Untitled'),
                    'url': item.get('url', f"https://www.neliti.com/publications/{item.get('id', '')}"),
                    'source': 'Neliti'
                })
            
            return papers
        except Exception as e:
            print(f"[Neliti] Fallback: {e}")
            return []


def search_indonesian_papers(query: str, max_results: int = 3) -> List[Dict]:
    """
    Convenience function to search Indonesian papers
    
    Args:
        query: Search query
        max_results: Max papers to return
    
    Returns:
        List of papers with title, URL, source
    """
    api = IndonesianAPIs()
    return api.search_all(query, max_results)


# Example usage
if __name__ == "__main__":
    print("Testing Indonesian APIs (FREE, no API key needed)\n")
    print("=" * 60)
    
    api = IndonesianAPIs()
    
    # Test search
    print("\n[TEST] Searching: 'machine learning indonesia'")
    print("-" * 60)
    papers = search_indonesian_papers("machine learning indonesia", max_results=3)
    
    for i, paper in enumerate(papers, 1):
        print(f"{i}. [{paper['source']}] {paper['title'][:60]}...")
        print(f"   {paper['url']}\n")
    
    print("=" * 60)
    print("Test complete!")
